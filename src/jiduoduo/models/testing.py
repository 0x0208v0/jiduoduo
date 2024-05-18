import json
import logging
import uuid
from datetime import datetime
from datetime import timedelta
from enum import StrEnum
from functools import cached_property
from typing import Self

from flask_login import current_user
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from jiduoduo.models.base import BaseModel
from jiduoduo.models.base import UUID
from jiduoduo.models.base import UserMixin
from jiduoduo.models.base import db
from jiduoduo.models.user import User
from jiduoduo.models.vps import VPS

logger = logging.getLogger(__name__)


class TestingState(StrEnum):
    CREATED = 'created'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'


UNKNOWN_TESTING_STATE_ZH = '未知状态'
TESTING_STATE_ZH = {
    TestingState.CREATED: '刚刚创建，还未运行',
    TestingState.RUNNING: '正在运行...',
    TestingState.SUCCESS: '测试成功',
    TestingState.FAILED: '测试失败',
}

UNKNOWN_TESTING_STATE_EMOJI = '❔'
TESTING_STATE_EMOJI = {
    TestingState.CREATED: '👀',
    TestingState.RUNNING: '⏳',
    TestingState.SUCCESS: '✅',
    TestingState.FAILED: '❌',
}


class TestingType(StrEnum):
    LOGIN = 'login'
    ECS = 'ecs'
    IP_CHECK = 'ip_check'
    GB5 = 'gb5'


UNKNOWN_TESTING_TYPE_ZH = '未知测试类型'
TESTING_TYPE_ZH = {
    TestingType.LOGIN: '登陆测试',
    TestingType.ECS: '融合怪',
    TestingType.IP_CHECK: 'IP质量体检报告',
    TestingType.GB5: 'GB5',
}


class Testing(BaseModel, UserMixin):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )
    _type: Mapped[str] = mapped_column(
        'type',
        String(32),
        nullable=False,
    )
    vps_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )

    vps: Mapped[VPS] = relationship(
        'VPS',
        uselist=False,
        primaryjoin='foreign(Testing.vps_id)==VPS.id',
        lazy='subquery',
    )

    _state: Mapped[str] = mapped_column(
        'state',
        String(32),
        nullable=False,
        default=TestingState.CREATED,
        server_default=TestingState.CREATED,
    )
    params: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    result: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default='',
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    ended_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )

    @cached_property
    def display_name(self) -> str:
        state = self.display_state_emoji
        if self.vps:
            vps_name = self.vps.name
        else:
            vps_name = '未知VPS'
        return f'{state}【{self.display_type_zh}】{vps_name}'

    @property
    def type(self) -> TestingType:
        return TestingType(self._type)

    @type.setter
    def type(self, type: TestingType):
        self._type = TestingType(type).value

    @cached_property
    def display_type_zh(self) -> str:
        return TESTING_TYPE_ZH.get(self.type, UNKNOWN_TESTING_STATE_ZH)

    @property
    def state(self) -> TestingState:
        return TestingState(self._state)

    @state.setter
    def state(self, state: TestingState):
        self._state = TestingState(state).value

    @cached_property
    def display_state_zh(self) -> str:
        return TESTING_STATE_ZH.get(self.state, UNKNOWN_TESTING_STATE_ZH)

    @cached_property
    def display_state_emoji(self) -> str:
        return TESTING_STATE_EMOJI.get(self.state, UNKNOWN_TESTING_STATE_EMOJI)

    @property
    def is_done(self) -> bool:
        return True if self.state in (TestingState.SUCCESS, TestingState.FAILED) else False

    @property
    def is_running(self) -> bool:
        return True if self.state == TestingState.RUNNING else False

    @property
    def duration(self) -> timedelta:
        return self.ended_at - self.started_at

    def set_result(self, result: str | None, commit: bool = True):
        if result is not None:
            self.result = result
        self.save(commit=commit)

    @classmethod
    def create(
            cls,
            type: TestingType,
            vps_or_id: VPS | uuid.UUID,
            params: str | dict | PydanticBaseModel | None = None,
            user_or_id: User | uuid.UUID = current_user,
            commit: bool = True,
    ) -> Self:
        if isinstance(vps_or_id, uuid.UUID):
            vps_id = vps_or_id
        else:
            vps_id = vps_or_id.id
        testing = cls(vps_id=vps_id, user_id=User.get_obj_id(user_or_id))
        testing.type = type
        testing.set_state_created(params=params, commit=commit)
        return testing

    def set_state_created(
            self,
            params: str | dict | PydanticBaseModel | None = None,
            result: str | None = '',
            commit: bool = True,
    ):
        self.state = TestingState.CREATED
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = json.dumps(params)
        if isinstance(params, PydanticBaseModel):
            params = params.model_dump_json()
        self.params = params
        self.set_result(result=result, commit=commit)

    def set_state_running(self, result: str | None = None, commit: bool = True):
        self.started_at = datetime.utcnow()
        self.state = TestingState.RUNNING
        self.set_result(result=result, commit=commit)

    def set_state_failed(self, result: str | None = None, commit: bool = True):
        self.ended_at = datetime.utcnow()
        self.state = TestingState.FAILED
        self.set_result(result=result, commit=commit)

    def set_state_success(self, result: str | None = None, commit: bool = True):
        self.ended_at = datetime.utcnow()
        self.state = TestingState.SUCCESS
        self.set_result(result=result, commit=commit)

    @classmethod
    def get_created_id_list(cls) -> list:
        stmt = (
            select(cls.id)
            .where(cls.state == TestingState.CREATED.value)
        )
        result = db.session.execute(stmt).scalars()
        return list(result)