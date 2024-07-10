from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class SpiritLHLSECSBasicSysInfoTestingParams(TestingParams):
    timeout: int = Field(60 * 10)  # seconds


class SpiritLHLSECSBasicSysInfoTestingResult(TestingResult):
    pass


class SpiritLHLSECSBasicSysInfoTestingService(TestingService):
    testing_type: TestingType = TestingType.SPIRITLHLS_ECS_BASIC_SYS_INFO
    testing_params_cls: type[SpiritLHLSECSBasicSysInfoTestingParams] = SpiritLHLSECSBasicSysInfoTestingParams
    testing_result_cls: type[SpiritLHLSECSBasicSysInfoTestingResult] = SpiritLHLSECSBasicSysInfoTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: SpiritLHLSECSBasicSysInfoTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> SpiritLHLSECSBasicSysInfoTestingResult:
        # https://github.com/spiritLHLS/ecs

        command = 'curl -L https://gitlab.com/spiritysdx/za/-/raw/main/ecs.sh -o ecs.sh && chmod +x ecs.sh && bash ecs.sh -base'

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

        return SpiritLHLSECSBasicSysInfoTestingResult(result=str(run_result))
