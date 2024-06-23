import datetime
import json
import uuid
from datetime import datetime
from typing import Self

import pendulum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import Select
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import FunctionElement
from sqlalchemy.types import CHAR
from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import TypeEngine

ZERO_UUID = uuid.UUID('00000000-0000-0000-0000-000000000000')


class GenerateUUID(FunctionElement):
    name = "uuid_default"


@compiles(GenerateUUID, "sqlite")
def _generate_uuid_sqlite(element, compiler, **kwargs):
    return """
    (
        lower(hex(randomblob(4)))
        || '-'
        || lower(hex(randomblob(2)))
        || '-4'
        || substr(lower(hex(randomblob(2))),2)
        || '-'
        || substr('89ab',abs(random()) % 4 + 1, 1)
        || substr(lower(hex(randomblob(2))),2)
        || '-'
        || lower(hex(randomblob(6)))
    )
    """


@compiles(GenerateUUID, "postgresql")
@compiles(GenerateUUID)
def _generate_uuid_postgresql(element, compiler, **kwargs):
    return "(GEN_RANDOM_UUID())"


class UUID(TypeDecorator):
    impl = TypeEngine
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgresql.UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        elif dialect.name == "postgresql":
            return str(value)
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class SqlalchemyBaseModel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        primary_key=True,
        server_default=GenerateUUID(),
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        server_default=func.current_timestamp(),
        onupdate=lambda: datetime.utcnow(),
        server_onupdate=func.current_timestamp(),
    )

    def format_created_at(self, fmt='%Y-%m-%d %H:%M:%S', tz='UTC') -> str:
        return pendulum.from_timestamp(self.created_at.timestamp(), tz).strftime(fmt)

    def format_updated_at(self, fmt='%Y-%m-%d %H:%M:%S', tz='UTC') -> str:
        return pendulum.from_timestamp(self.updated_at.timestamp(), tz).strftime(fmt)

    def save(self, commit: bool = True):
        db.session.add(self)
        db.session.flush([self])
        if commit:
            db.session.commit()

    def delete(self, commit: bool = True):
        db.session.delete(self)
        db.session.flush()
        if commit:
            db.session.commit()

    @classmethod
    def get_obj_id(cls, obj_or_id: Self | uuid.UUID) -> uuid.UUID:
        if isinstance(obj_or_id, uuid.UUID):
            return obj_or_id

        elif isinstance(obj_or_id, cls):
            return obj_or_id.id

        else:
            id = getattr(obj_or_id, 'id', None)
            if id is None:
                raise ValueError(f'obj {obj_or_id} 没有ID')
            return id

    @classmethod
    def get(cls, ident) -> Self | None:
        return db.session.get(cls, ident)

    @classmethod
    def get_one(cls, *where) -> Self | None:
        stmt = select(cls)
        if where:
            stmt = stmt.where(*where)
        result = db.session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    def build_stmt(
            cls,
            *where, order_by: list | None = None,
            offset: int | None = None, limit: int | None = None,
    ) -> Select:
        stmt = select(cls)

        if where:
            stmt = stmt.where(*where)
        if order_by:
            stmt = stmt.order_by(*order_by)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt

    @classmethod
    def count(cls, *where) -> int:
        subquery = cls.build_stmt(*where).subquery()
        stmt = select(func.count(subquery.c.id).label('count'))
        result = db.session.execute(stmt)
        for (count,) in result:
            return count

    @classmethod
    def get_list(
            cls,
            *where, order_by: list | None = None,
            offset: int | None = None, limit: int | None = None,

    ) -> list[Self]:
        stmt = cls.build_stmt(*where, order_by=order_by, offset=offset, limit=limit)
        result = db.session.execute(stmt).scalars()
        return list(result)

    @classmethod
    def get_list_by_page(
            cls,
            *where, order_by: list | None = None,
            page_num: int = 1, page_size: int = 20,
    ) -> list[Self]:
        if not order_by:
            order_by = [cls.created_at.desc(), cls.id.desc()]
        return cls.get_list(
            *where, order_by=order_by,
            offset=(page_num - 1) * page_size, limit=page_size,
        )

    @classmethod
    def get_id_name_list(cls, *where, order_by: list | None = None) -> list[uuid.UUID]:
        subquery = cls.build_stmt(*where, order_by=order_by).subquery()
        stmt = select(subquery.c.id, subquery.c.name)
        result = db.session.execute(stmt)
        id_list = [(id, name) for (id, name) in result]
        return id_list

    def to_dict(self) -> dict:
        return {'id': self.id}

    def to_json(self) -> str:

        class MyJsonEncoder(json.JSONEncoder):
            def default(self, field):
                if isinstance(field, uuid.UUID):
                    return str(field)
                else:
                    return super().default(field)

        return json.dumps(self.to_dict(), cls=MyJsonEncoder)


db = SQLAlchemy(
    model_class=SqlalchemyBaseModel,
    engine_options={
        'pool_size': 5,
        'pool_recycle': 100,
        'pool_pre_ping': True
    },
    session_options={
        'autocommit': False,
        'autoflush': False,
        'expire_on_commit': False,
    }
)

BaseModel: type[SqlalchemyBaseModel] = db.Model


class UserMixin:
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )
