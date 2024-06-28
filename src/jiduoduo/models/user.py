from typing import Self

from flask_login import UserMixin
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from jiduoduo.models.base import BaseModel


class User(BaseModel, UserMixin):
    email: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default='1',
    )

    @property
    def username(self) -> str:
        return self.email.split('@')[0]

    @property
    def password(self):
        raise ValueError('can not read password')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_email(cls, email: str) -> Self | None:
        email = email.strip()
        if not email:
            return
        return cls.get_one(cls.email == email)

    @classmethod
    def login(cls, email: str, password: str) -> Self:
        email = (email or '').strip()
        if not email:
            raise ValueError('邮箱不能为空')

        password = (password or '').strip()
        if not password:
            raise ValueError('密码不能为空')

        user = cls.get_by_email(email)
        if user is None or not user.is_active or not user.verify_password(password):
            raise ValueError('用户不存在或密码不对')

        return user

    @classmethod
    def register(cls, email: str, password: str, commit: bool = True) -> Self:
        email = (email or '').strip()
        if not email:
            raise ValueError('邮箱不能为空')

        password = (password or '').strip()
        if not password:
            raise ValueError('密码不能为空')

        user = cls.get_by_email(email)
        if user:
            raise ValueError('用户已存在')

        user = cls(email=email)
        user.password = password
        user.save(commit=commit)
        return user
