import io
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class BashICUGB5TestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class BashICUGB5TestingResult(TestingResult):
    pass


class BashICUGB5TestingService(TestingService):
    testing_type: TestingType = TestingType.BASH_ICU_GB5
    testing_params_cls: type[BashICUGB5TestingParams] = BashICUGB5TestingParams
    testing_result_cls: type[BashICUGB5TestingResult] = BashICUGB5TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: BashICUGB5TestingParams,
            flush_callback: Callable[[str], None],
    ) -> BashICUGB5TestingResult:
        command = 'bash <(curl -sL bash.icu/gb5)'

        class StreamLogger:
            def __init__(self):
                self.buffer = io.StringIO()

            def write(self, message):
                self.buffer.write(message)

            def flush(self):
                flush_callback(self.buffer.getvalue())

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            out_stream=StreamLogger(),
        )

        return BashICUGB5TestingResult(result=str(run_result))
