from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class BacktraceTestingParams(TestingParams):
    timeout: int = Field(60)  # seconds


class BacktraceTestingResult(TestingResult):
    pass


class BacktraceTestingService(TestingService):
    testing_type: TestingType = TestingType.BACKTRACE
    testing_params_cls: type[BacktraceTestingParams] = BacktraceTestingParams
    testing_result_cls: type[BacktraceTestingResult] = BacktraceTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: BacktraceTestingParams,
            flush_callback: Callable[[str], None],
    ) -> BacktraceTestingResult:
        run_result = vps.run(
            'curl https://raw.githubusercontent.com/zhanghanyun/backtrace/main/install.sh -sSf | sh',
            timeout=params.timeout,
            warn=True,
        )

        return BacktraceTestingResult(result=str(run_result))
