from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class YABSDefaultTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class YABSDefaultTestingResult(TestingResult):
    pass


class YABSDefaultTestingService(TestingService):
    testing_type: TestingType = TestingType.YABS_DEFAULT
    testing_params_cls: type[YABSDefaultTestingParams] = YABSDefaultTestingParams
    testing_result_cls: type[YABSDefaultTestingResult] = YABSDefaultTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: YABSDefaultTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> YABSDefaultTestingResult:
        # https://github.com/masonr/yet-another-bench-script

        command = 'curl -sL yabs.sh | bash'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return YABSDefaultTestingResult(result=str(run_result))
