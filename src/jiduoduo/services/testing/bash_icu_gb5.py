from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class BashIcuGB5TestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class BashIcuGB5TestingResult(TestingResult):
    pass


class BashIcuGB5TestingService(TestingService):
    testing_type: TestingType = TestingType.BASH_ICU_GB5
    testing_params_cls: type[BashIcuGB5TestingParams] = BashIcuGB5TestingParams
    testing_result_cls: type[BashIcuGB5TestingResult] = BashIcuGB5TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: BashIcuGB5TestingParams,
            flush_callback: Callable[[str], None],
    ) -> BashIcuGB5TestingResult:
        # https://github.com/i-abc/gb5

        command = 'bash <(curl -sL bash.icu/gb5)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return BashIcuGB5TestingResult(result=str(run_result))
