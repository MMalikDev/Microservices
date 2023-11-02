import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime

from database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String)

    # salt: str = Column(String)
    password: str = Column(String)

    updated_date: str = Column(String)
    creation_date: str = Column(String)

    def __repr__(self) -> str:
        return "User(%i)" % self.email


@dataclass
class UserBase:
    email: str
    password: str

    def get_id(self) -> int:
        id = "".join(filter(str.isalnum, self.email)).lower().encode("utf-8")
        return int(hashlib.sha1(id).hexdigest(), 16) % (10**8)

    def get_hashed_password(self) -> int:
        # self.salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(self.password + self.salt).hexdigest()
        # Plain Password used for demonstration purposes.
        # Use hashed password with salt for production use.
        return self.password

    def __post_init__(self) -> None:
        self.id: str = self.get_id()
        self.password: str = self.get_hashed_password()

    def __repr__(self) -> str:
        return "User(%i)" % self.email


@dataclass
class UserUpdate(UserBase):
    email: str
    password: str

    def __post_init__(self) -> None:
        self.password: str = self.get_hashed_password()
        self.updated_date: str = datetime.now().isoformat()

    def __repr__(self) -> str:
        return "User(%i)" % self.email


@dataclass
class UserCreate(UserBase):
    email: str
    password: str

    def __post_init__(self) -> None:
        self.id: str = self.get_id()
        self.password: str = self.get_hashed_password()
        self.updated_date: str = datetime.now().isoformat()
        self.creation_date: str = self.updated_date

    def __repr__(self) -> str:
        return "User(%i)" % self.email
