from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class FREEHTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class FREEHTestingResult(TestingResult):
    pass


class FREEHTestingService(TestingService):
    testing_type: TestingType = TestingType.FREE_H
    testing_params_cls: type[FREEHTestingParams] = FREEHTestingParams
    testing_result_cls: type[FREEHTestingResult] = FREEHTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: FREEHTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> FREEHTestingResult:
        run_result = vps.run(
            'free -h',
            timeout=params.timeout,
            warn=True,
        )

        return FREEHTestingResult(result=str(run_result))
