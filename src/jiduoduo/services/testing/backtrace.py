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
            flush_callback: Callable[[str], None] | None = None,
    ) -> BacktraceTestingResult:
        # https://github.com/zhanghanyun/backtrace # 更新滞后，暂时去掉
        # https://github.com/oneclickvirt/backtrace

        # command = 'curl https://raw.githubusercontent.com/zhanghanyun/backtrace/main/install.sh -sSf | sh'
        command = 'curl https://cdn.spiritlhl.net/https://raw.githubusercontent.com/oneclickvirt/backtrace/main/backtrace_install.sh -sSf | bash && backtrace'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
        )

        return BacktraceTestingResult(result=str(run_result))
