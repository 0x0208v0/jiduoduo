import time
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


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
            flush_callback: Callable[[str], None] | None = None,
    ) -> CheckUnlockMediaTestingResult:
        # https://github.com/lmc999/RegionRestrictionCheck

        command = "bash <(curl -L -s check.unlock.media) <<< '4'"

        run_result = vps.run(
            command,
            timeout=params.timeout,
            hide=True,
            warn=True,
            pty=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )
        time.sleep(1)
        return CheckUnlockMediaTestingResult(result=str(run_result))
