import logging
import uuid
from io import StringIO
from typing import Self

from fabric2 import Connection
from fabric2.runners import Result
from paramiko import DSSKey
from paramiko import ECDSAKey
from paramiko import Ed25519Key
from paramiko import RSAKey
from paramiko import SSHException
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from jiduoduo.models.base import BaseModel
from jiduoduo.models.base import UUID
from jiduoduo.models.base import UserMixin

logger = logging.getLogger(__name__)

PKEY_CLS_LIST = [RSAKey, Ed25519Key, DSSKey, ECDSAKey]


class VPS(BaseModel, UserMixin):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
    )
    host: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    port: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=22,
    )
    user: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        default='root',
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        default='',
        server_default='',
    )
    identify_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
    )

    @classmethod
    def get_by_name(cls, name: str) -> Self | None:
        return cls.get_one(cls.name == name)

    def make_new_connection(self) -> Connection:
        connect_kwargs = {}
        if self.password:
            connect_kwargs['password'] = self.password

        elif self.identify_key:
            pkey = None
            for pk_cls in PKEY_CLS_LIST:
                try:
                    pkey = pk_cls.from_private_key(StringIO(self.identify_key))
                    break
                except SSHException as e:
                    logger.error(f'{e}')
                    continue

            if pkey is None:
                raise ValueError(f'identify_key无效')

            connect_kwargs['pkey'] = pkey

        return Connection(
            host=self.host,
            port=self.port,
            user=self.user,
            connect_kwargs=connect_kwargs,
        )

    @property
    def connection(self) -> Connection:
        attr = '_connection'
        if getattr(self, attr, None) is None:
            setattr(self, attr, self.make_new_connection())
        return getattr(self, attr)

    def close_connection(self):
        self.connection.close()
        setattr(self, '_connection', None)

    def run(
            self,
            command: str,
            hide: bool | str | None = None,
            timeout: float | None = None,
            warn: bool = False,
            **kwargs,
    ) -> Result | None:
        result = self.connection.run(
            command=command,
            hide=hide,
            timeout=timeout,
            warn=warn,
            **kwargs,
        )
        self.close_connection()
        return result
