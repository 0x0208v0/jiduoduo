from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


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
        # https://github.com/masonr/yet-another-bench-script

        command = 'curl -sL yabs.sh | bash -s -- -ign'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return YABSDiskTestingResult(result=str(run_result))
