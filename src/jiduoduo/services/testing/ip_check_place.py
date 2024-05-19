import io
import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class IPCheckPlaceTestingParams(TestingParams):
    timeout: int = Field(60 * 5)  # seconds


class IPCheckPlaceTestingResult(TestingResult):
    pass


class IPCheckPlaceTestingService(TestingService):
    testing_type: TestingType = TestingType.IP_CHECK_PLACE
    testing_params_cls: type[IPCheckPlaceTestingParams] = IPCheckPlaceTestingParams
    testing_result_cls: type[IPCheckPlaceTestingResult] = IPCheckPlaceTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: IPCheckPlaceTestingParams,
            flush_callback: Callable[[str], None],
    ) -> IPCheckPlaceTestingResult:
        command = 'bash <(curl -sL IP.Check.Place)'

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
        return IPCheckPlaceTestingResult(result=str(run_result))
