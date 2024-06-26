from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class MemoryCheckTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class MemoryCheckTestingResult(TestingResult):
    pass


class MemoryCheckTestingService(TestingService):
    testing_type: TestingType = TestingType.MEMORY_CHECK
    testing_params_cls: type[MemoryCheckTestingParams] = MemoryCheckTestingParams
    testing_result_cls: type[MemoryCheckTestingResult] = MemoryCheckTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: MemoryCheckTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> MemoryCheckTestingResult:
        # https://github.com/uselibrary/memoryCheck

        command = 'curl https://raw.githubusercontent.com/uselibrary/memoryCheck/main/memoryCheck.sh | bash'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
        )

        return MemoryCheckTestingResult(result=str(run_result))
