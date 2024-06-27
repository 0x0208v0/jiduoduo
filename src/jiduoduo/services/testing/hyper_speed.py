from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class HyperSpeedTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class HyperSpeedTestingResult(TestingResult):
    pass


class HyperSpeedTestingService(TestingService):
    testing_type: TestingType = TestingType.HYPER_SPEED
    testing_params_cls: type[HyperSpeedTestingParams] = HyperSpeedTestingParams
    testing_result_cls: type[HyperSpeedTestingResult] = HyperSpeedTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: HyperSpeedTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> HyperSpeedTestingResult:
        # https://hostloc.com/thread-1076585-1-1.html

        command = 'bash <(wget -qO- https://bench.im/hyperspeed)'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'请选择测速类型', response='1\n'),
                Responder(pattern=r'启用八线程测速', response='N\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return HyperSpeedTestingResult(result=str(run_result))
