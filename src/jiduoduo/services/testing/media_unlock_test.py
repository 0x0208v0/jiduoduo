import time
from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class MediaUnlockTestTestingParams(TestingParams):
    timeout: int = Field(60 * 10)  # seconds


class MediaUnlockTestTestingResult(TestingResult):
    pass


class MediaUnlockTestTestingService(TestingService):
    testing_type: TestingType = TestingType.MEDIA_UNLOCK_TEST
    testing_params_cls: type[MediaUnlockTestTestingParams] = MediaUnlockTestTestingParams
    testing_result_cls: type[MediaUnlockTestTestingResult] = MediaUnlockTestTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: MediaUnlockTestTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> MediaUnlockTestTestingResult:
        # https://github.com/HsukqiLee/MediaUnlockTest

        command = 'bash <(curl -Ls unlock.icmp.ing/test.sh)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            hide=True,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'回车确认', response='\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )
        time.sleep(1)
        return MediaUnlockTestTestingResult(result=str(run_result))
