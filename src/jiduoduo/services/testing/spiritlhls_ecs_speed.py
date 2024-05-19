import io
from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


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
        command = 'bash <(wget -qO- bash.spiritlhl.net/ecs-net)'

        class StreamLogger:
            def __init__(self):
                self.buffer = io.StringIO()

            def write(self, message):
                self.buffer.write(message)

            def flush(self):
                flush_callback(self.buffer.getvalue())

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
            out_stream=StreamLogger(),
        )

        return SpiritLHLSECSSpeedTestingResult(result=str(run_result))
