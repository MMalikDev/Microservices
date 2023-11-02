import json
from typing import Annotated, Dict

import httpx
from configs.core import settings
from fastapi import Body, FastAPI, File, Header, HTTPException, status
from fastapi.responses import Response, StreamingResponse
from lib import database, queue
from lib.utilities import logger
from models.users import UserBase
from uvicorn import run


def validate(authorization: str, level: str) -> Dict[str, str]:
    headers = {"authorization": authorization}
    response = httpx.post(settings.VALIDATE_API, headers=headers)
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    access = dict(json.loads(response.text))
    if not access.get(level):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
        )

    return access


channel = queue.get_channel(settings.QUEUE_URI, settings.VIDEO_QUEUE)
db_video = database.get_db("video")
db_audio = database.get_db("audio")
app = FastAPI()


@app.post("/login", response_description="Login User")
def login(authorization: UserBase = Body(...)) -> Response:
    response = httpx.post(settings.LOGIN_API, json=authorization.__dict__)
    return Response(response.text, response.status_code)


@app.get("/download", response_description="Download Audio File")
def download(id: str, authorization: Annotated[str, Header()]) -> StreamingResponse:
    _ = validate(authorization, "admin")
    return StreamingResponse(database.streams(db_audio, id))


@app.post("/upload", response_description="Upload Video File")
def upload(
    file: Annotated[bytes, File()], authorization: Annotated[str, Header()]
) -> Response:
    access = validate(authorization, "admin")
    id = db_video.put(file)
    message = {
        "username": access.get("username"),
        "video_id": str(id),
        "audio_id": None,
    }

    if not queue.published(channel, settings.VIDEO_QUEUE, message):
        db_video.delete(id)
        logger.info("Deleted Incomplete Video with ID: %s", id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return Response("Video Uploaded Successfully", status.HTTP_200_OK)


@app.get("/test/download", response_description="Download Audio File without Auth Token")
def download(id: str) -> StreamingResponse:
    return StreamingResponse(database.streams(db_audio, id))


@app.post("/test/upload", response_description="Upload Video File without Auth Token")
def upload(file: Annotated[bytes, File()]) -> Response:
    id = db_video.put(file)
    message = {
        "username": "test_user",
        "video_id": str(id),
        "audio_id": None,
    }

    if not queue.published(channel, settings.VIDEO_QUEUE, message):
        db_video.delete(id)
        logger.info("Deleted Incomplete Video with ID: %s", id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return Response("Video Uploaded Successfully", status.HTTP_200_OK)


if __name__ == "__main__":
    run(app, host=settings.API_HOST, port=settings.API_PORT)
