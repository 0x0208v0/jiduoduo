from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class FreeHTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class FreeHTestingResult(TestingResult):
    pass


class FreeHTestingService(TestingService):
    testing_type: TestingType = TestingType.FREE_H
    testing_params_cls: type[FreeHTestingParams] = FreeHTestingParams
    testing_result_cls: type[FreeHTestingResult] = FreeHTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: FreeHTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> FreeHTestingResult:
        run_result = vps.run(
            'free -h',
            timeout=params.timeout,
            warn=True,
        )

        return FreeHTestingResult(result=str(run_result))
