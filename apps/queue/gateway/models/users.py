import hashlib
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserBase:
    email: str
    password: str

    def get_id(self) -> int:
        id = "".join(filter(str.isalnum, self.email)).lower().encode("utf-8")
        return int(hashlib.sha1(id).hexdigest(), 16) % (10**8)

    def __post_init__(self) -> None:
        self.id: str = self.get_id()

    def __repr__(self) -> str:
        return "User(%i)" % self.email


@dataclass
class UserUpdate(UserBase):
    email: str
    password: str

    def __post_init__(self) -> None:
        self.updated_date: str = datetime.now().isoformat()

    def __repr__(self) -> str:
        return "User(%i)" % self.email


@dataclass
class UserCreate(UserBase):
    email: str
    password: str

    def __post_init__(self) -> None:
        self.id: str = self.get_id()
        self.updated_date: str = datetime.now().isoformat()
        self.creation_date: str = self.updated_date

    def __repr__(self) -> str:
        return "User(%i)" % self.email
