from typing import Any, Dict, List, Optional, Type, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from configs.core import settings
from database import Base

ModelType = Base
CreateType = Dict[str, Any]
UpdateType = Dict[str, Any]


class DataAccessLayer:
    def __init__(self, *, model: Type[ModelType]):
        self.model = model
        self.engine = create_engine(settings.DATABASE_URI)
        self.db = Session(bind=self.engine)

        self.init_db()

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def read_all(self, *, page: int = 1, limit: int = 100) -> List[Optional[ModelType]]:
        skip = (page - 1) * limit
        with self.db as con:
            data = con.query(self.model).offset(skip).limit(limit).all()
        return data

    def create(self, data: CreateType) -> ModelType:
        item = self.model(**data)
        with self.db as con:
            con.add(item)
            con.commit()
            con.refresh(item)
        return item

    def read_1(self, id: Union[int, str]) -> Optional[ModelType]:
        with self.db as con:
            data = con.query(self.model).get(id)
        return data

    def update(self, id: Union[int, str], data: UpdateType) -> Optional[ModelType]:
        if not (item := self.read_1(id)):
            return None

        fields = item.__dict__.keys()
        for field in fields:
            if field in data:
                setattr(item, field, data[field])

        with self.db as con:
            con.add(item)
            con.commit()
            con.refresh(item)
        return item

    def delete(self, id: Union[int, str]) -> bool:
        if not (data := self.read_1(id)):
            return False
        with self.db as con:
            con.delete(data)
            con.commit()
        return True
