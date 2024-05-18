import io
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class GB5TestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class GB5TestingResult(TestingResult):
    pass


class GB5TestingService(TestingService):
    testing_type: TestingType = TestingType.GB5
    testing_params_cls: type[GB5TestingParams] = GB5TestingParams
    testing_result_cls: type[GB5TestingResult] = GB5TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: GB5TestingParams,
            flush_callback: Callable[[str], None],
    ) -> GB5TestingResult:
        command = 'curl -sL yabs.sh | bash -s -- -i -5'

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

        return GB5TestingResult(result=str(run_result))
