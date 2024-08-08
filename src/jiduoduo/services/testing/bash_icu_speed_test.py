from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class BashIcuSpeedTestTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class BashIcuSpeedTestTestingResult(TestingResult):
    pass


class BashIcuSpeedTestTestingService(TestingService):
    testing_type: TestingType = TestingType.BASH_ICU_SPEED_TEST
    testing_params_cls: type[BashIcuSpeedTestTestingParams] = BashIcuSpeedTestTestingParams
    testing_result_cls: type[BashIcuSpeedTestTestingResult] = BashIcuSpeedTestTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: BashIcuSpeedTestTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> BashIcuSpeedTestTestingResult:
        # https://github.com/i-abc/speedtest

        command = 'bash <(curl -sL bash.icu/speedtest)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'请输入', response='1\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return BashIcuSpeedTestTestingResult(result=str(run_result))
