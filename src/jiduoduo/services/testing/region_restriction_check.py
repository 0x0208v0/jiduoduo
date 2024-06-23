import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


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

        run_result = vps.run(
            command,
            timeout=params.timeout,
            hide=True,
            warn=True,
            pty=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )
        time.sleep(1)
        return RegionRestrictionCheckTestingResult(result=str(run_result))
