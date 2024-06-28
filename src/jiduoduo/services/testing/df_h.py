from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class DFHTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class DFHTestingResult(TestingResult):
    pass


class DFHTestingService(TestingService):
    testing_type: TestingType = TestingType.DF_H
    testing_params_cls: type[DFHTestingParams] = DFHTestingParams
    testing_result_cls: type[DFHTestingResult] = DFHTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: DFHTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> DFHTestingResult:
        run_result = vps.run(
            'df -h',
            timeout=params.timeout,
            warn=True,
        )

        return DFHTestingResult(result=str(run_result))
