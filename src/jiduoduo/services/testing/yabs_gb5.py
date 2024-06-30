from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class YABSGB5TestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class YABSGB5TestingResult(TestingResult):
    pass


class YABSGB5TestingService(TestingService):
    testing_type: TestingType = TestingType.YABS_GB5
    testing_params_cls: type[YABSGB5TestingParams] = YABSGB5TestingParams
    testing_result_cls: type[YABSGB5TestingResult] = YABSGB5TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: YABSGB5TestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> YABSGB5TestingResult:
        # https://github.com/masonr/yet-another-bench-script

        command = 'curl -sL yabs.sh | bash -s -- -i -5'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            hide=True,
            warn=True,
            pty=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return YABSGB5TestingResult(result=str(run_result))
