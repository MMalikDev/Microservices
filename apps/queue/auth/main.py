import datetime
import json
from typing import Annotated

import jwt
from configs.core import settings
from database import DataAccessLayer
from fastapi import Body, FastAPI, Header, HTTPException, status
from fastapi.responses import Response
from lib.utilities import logger
from models.users import User, UserBase, UserCreate, UserUpdate
from uvicorn import run


def create_superuser() -> None:
    user = UserCreate(settings.SUPERUSER_EMAIL, settings.SUPERUSER_PASSWORD)
    update_data = UserUpdate(email=user.email, password=user.password)
    db = DataAccessLayer(model=User)

    if not db.update(user.id, update_data.__dict__):
        db.create(user.__dict__)


def createJWT(username: str, token: str, authz: bool) -> str:
    tz = datetime.timezone.utc
    now = datetime.datetime.now(tz)
    exp = now + datetime.timedelta(days=1)
    payload = {"username": username, "exp": exp, "iat": now, "admin": authz}
    return jwt.encode(payload, token, algorithm="HS256")


create_superuser()
app = FastAPI()


@app.post("/login", response_description="Login User")
def login(authorization: UserBase = Body(...)) -> Response:
    db = DataAccessLayer(model=User)
    if not (user := db.read_1(authorization.id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    if user.email != authorization.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    # Plain Password used for demonstration purposes.
    # Use hashed password with salt for production use.
    if user.password != authorization.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    token = settings.JWT_SECRET
    content = createJWT(authorization.email, token, True)
    return Response(content, status.HTTP_200_OK)


@app.post("/validate", response_description="Validate Credentials")
def validate(authorization: Annotated[str, Header()]) -> Response:
    token = settings.JWT_SECRET
    try:
        content = jwt.decode(authorization, token, algorithms=["HS256"])
    except jwt.InvalidSignatureError as error:
        logger.error("%s - %s", error.__class__.__name__, error)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Signature Error",
        )
    except jwt.ExpiredSignatureError as error:
        logger.error("%s - %s", error.__class__.__name__, error)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Expired Signature Error",
        )
    except Exception as error:
        logger.error("%s - %s", error.__class__.__name__, error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    return Response(json.dumps(content), status.HTTP_200_OK)


if __name__ == "__main__":
    run(app, host=settings.API_HOST, port=settings.API_PORT)
