import io
import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class RegionRestrictionCheckTestingParams(TestingParams):
    timeout: int = Field(60 * 5)  # seconds


class RegionRestrictionCheckTestingResult(TestingResult):
    pass


class RegionRestrictionCheckTestingService(TestingService):
    testing_type: TestingType = TestingType.REGION_RESTRICTION_CHECK
    testing_params_cls: type[RegionRestrictionCheckTestingParams] = RegionRestrictionCheckTestingParams
    testing_result_cls: type[RegionRestrictionCheckTestingResult] = RegionRestrictionCheckTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: RegionRestrictionCheckTestingParams,
            flush_callback: Callable[[str], None],
    ) -> RegionRestrictionCheckTestingResult:
        command = 'bash <(curl -L -s https://github.com/1-stream/RegionRestrictionCheck/raw/main/check.sh)'

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
        return RegionRestrictionCheckTestingResult(result=str(run_result))
