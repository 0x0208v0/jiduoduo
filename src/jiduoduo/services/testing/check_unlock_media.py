import io
import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class CheckUnlockMediaTestingParams(TestingParams):
    timeout: int = Field(60 * 5)  # seconds


class CheckUnlockMediaTestingResult(TestingResult):
    pass


class CheckUnlockMediaTestingService(TestingService):
    testing_type: TestingType = TestingType.CHECK_UNLOCK_MEDIA
    testing_params_cls: type[CheckUnlockMediaTestingParams] = CheckUnlockMediaTestingParams
    testing_result_cls: type[CheckUnlockMediaTestingResult] = CheckUnlockMediaTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: CheckUnlockMediaTestingParams,
            flush_callback: Callable[[str], None],
    ) -> CheckUnlockMediaTestingResult:
        command = "bash <(curl -L -s check.unlock.media) <<< '4'"

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
            hide=True,
            warn=True,
            pty=True,
            out_stream=StreamLogger(),
        )
        time.sleep(1)
        return CheckUnlockMediaTestingResult(result=str(run_result))
