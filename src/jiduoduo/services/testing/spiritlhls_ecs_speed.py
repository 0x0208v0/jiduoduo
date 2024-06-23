from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class SpiritLHLSECSSpeedTestingParams(TestingParams):
    timeout: int = Field(60 * 10)  # seconds


class SpiritLHLSECSSpeedTestingResult(TestingResult):
    pass


class SpiritLHLSECSSpeedTestingService(TestingService):
    testing_type: TestingType = TestingType.SPIRITLHLS_ECS_SPEED
    testing_params_cls: type[SpiritLHLSECSSpeedTestingParams] = SpiritLHLSECSSpeedTestingParams
    testing_result_cls: type[SpiritLHLSECSSpeedTestingResult] = SpiritLHLSECSSpeedTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: SpiritLHLSECSSpeedTestingParams,
            flush_callback: Callable[[str], None],
    ) -> SpiritLHLSECSSpeedTestingResult:
        # https://github.com/spiritLHLS/ecsspeed

        command = 'bash <(wget -qO- bash.spiritlhl.net/ecs-net)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'[y]/n', response='y\n'),
                Responder(pattern=r'Y/n', response='Y\n'),
                Responder(pattern=r'请输入数字', response='1\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return SpiritLHLSECSSpeedTestingResult(result=str(run_result))
