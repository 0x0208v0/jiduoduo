from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class NWSGlobalDefaultTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class NWSGlobalDefaultTestingResult(TestingResult):
    pass


class NWSGlobalDefaultTestingService(TestingService):
    testing_type: TestingType = TestingType.NWS_GLOBAL
    testing_params_cls: type[NWSGlobalDefaultTestingParams] = NWSGlobalDefaultTestingParams
    testing_result_cls: type[NWSGlobalDefaultTestingResult] = NWSGlobalDefaultTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: NWSGlobalDefaultTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> NWSGlobalDefaultTestingResult:
        command = 'curl -sL nws.sh | bash'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return NWSGlobalDefaultTestingResult(result=str(run_result))
