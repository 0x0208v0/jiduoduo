from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class SpiritLHLSECSTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class SpiritLHLSECSTestingResult(TestingResult):
    pass


class SpiritLHLSECSTestingService(TestingService):
    testing_type: TestingType = TestingType.SPIRITLHLS_ECS
    testing_params_cls: type[SpiritLHLSECSTestingParams] = SpiritLHLSECSTestingParams
    testing_result_cls: type[SpiritLHLSECSTestingResult] = SpiritLHLSECSTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: SpiritLHLSECSTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> SpiritLHLSECSTestingResult:
        # https://github.com/spiritLHLS/ecs

        command = 'curl -L https://gitlab.com/spiritysdx/za/-/raw/main/ecs.sh -o ecs.sh && chmod +x ecs.sh && bash ecs.sh -m 1'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'[y]/n', response='y\n'),
                Responder(pattern=r'Y/n', response='Y\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return SpiritLHLSECSTestingResult(result=str(run_result))
