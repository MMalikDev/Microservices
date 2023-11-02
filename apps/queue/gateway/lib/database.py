from typing import Any, Generator

from bson.objectid import ObjectId
from configs.core import settings
from gridfs import GridFS
from pymongo import MongoClient


def streams(db: GridFS, id: str) -> Generator[bytes, Any, None]:
    for bytes in db.get(ObjectId(id)):
        yield bytes


def get_db(name: str | None) -> GridFS | MongoClient:
    client = MongoClient(settings.MONGO_URI)
    if name:
        return GridFS(client[name])
    return client
