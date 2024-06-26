import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class IPCheckPlaceTestingParams(TestingParams):
    timeout: int = Field(60 * 10)  # seconds


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
            flush_callback: Callable[[str], None] | None = None,
    ) -> IPCheckPlaceTestingResult:
        # https://github.com/xykt/IPQuality

        command = 'bash <(curl -sL IP.Check.Place)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            hide=True,
            warn=True,
            pty=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )
        time.sleep(1)
        return IPCheckPlaceTestingResult(result=str(run_result))
