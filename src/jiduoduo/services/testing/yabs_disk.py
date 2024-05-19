import io
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class YABSDiskTestingParams(TestingParams):
    timeout: int = Field(60 * 10)  # seconds


class YABSDiskTestingResult(TestingResult):
    pass


class YABSDiskTestingService(TestingService):
    testing_type: TestingType = TestingType.YABS_DISK
    testing_params_cls: type[YABSDiskTestingParams] = YABSDiskTestingParams
    testing_result_cls: type[YABSDiskTestingResult] = YABSDiskTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: YABSDiskTestingParams,
            flush_callback: Callable[[str], None],
    ) -> YABSDiskTestingResult:
        command = 'curl -sL yabs.sh | bash -s -- -ign'

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

        return YABSDiskTestingResult(result=str(run_result))
