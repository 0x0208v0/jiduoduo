import json
import logging
from abc import ABC
from abc import abstractmethod
from typing import Callable

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from jiduoduo.models import Testing
from jiduoduo.models import TestingType
from jiduoduo.models import VPS

logger = logging.getLogger(__name__)


class TestingParams(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TestingResult(BaseModel):
    is_success: bool = Field(True)
    result: str = Field('success')


def remove_x00(obj):
    if isinstance(obj, list):
        return [remove_x00(item) for item in obj]
    if isinstance(obj, dict):
        return {k: remove_x00(v) for k, v in obj.items()}
    if isinstance(obj, str):
        return obj.replace('\x00', '')
    return obj


class TestingService(ABC):
    testing_type: TestingType
    testing_params_cls: type[TestingParams] = TestingParams
    testing_result_cls: type[TestingResult] = TestingResult

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def run(
            self,
            testing: Testing,
            params: TestingParams | dict | None = None,
    ) -> Testing:
        if not testing.vps:
            raise ValueError(f'not found vps, testing_id={testing.id}')

        if params is None:
            params = testing.params

        if params is None or isinstance(params, self.testing_params_cls):
            pass

        if isinstance(params, str):
            params = json.loads(params)

        if isinstance(params, dict):
            params = self.testing_params_cls(**params)

        else:
            params = self.testing_params_cls.from_orm(params)

        testing.set_state_running(commit=not self.dry_run)

        def flush_result(r):
            from jiduoduo.app import app
            from jiduoduo.models import db
            with app.app_context():
                session = db.session.object_session(testing)
                testing.result = remove_x00(r)
                session.add(testing)
                session.commit()

        try:
            result = self.run_on_vps(
                vps=testing.vps,
                params=params,
                flush_callback=flush_result,
            )

            if result.is_success:
                testing.set_state_success(result=remove_x00(result.result), commit=not self.dry_run)

            else:
                testing.set_state_failed(result=remove_x00(result.result), commit=not self.dry_run)

        except Exception as e:
            result = f'error: {e}'
            logger.error(result)
            testing.set_state_failed(result=result, commit=not self.dry_run)

        return testing

    @abstractmethod
    def run_on_vps(self, vps: VPS, params: TestingParams, flush_callback: Callable[[str], None]) -> TestingResult:
        pass
