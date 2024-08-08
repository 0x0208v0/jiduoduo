import logging
import uuid
from enum import StrEnum

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from jiduoduo.models.base import BaseModel
from jiduoduo.models.base import UUID
from jiduoduo.models.base import UserMixin

logger = logging.getLogger(__name__)


class ImageState(StrEnum):
    CREATED = 'created'
    UPLOADING = 'uploading'
    SUCCESS = 'success'
    FAILED = 'failed'


class Image(BaseModel, UserMixin):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )

    _type: Mapped[str] = mapped_column(
        'type',
        String(32),
        nullable=False,
    )

    _state: Mapped[str] = mapped_column(
        'state',
        String(32),
        nullable=False,
        default=ImageState.CREATED,
        server_default=ImageState.CREATED,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
    )
