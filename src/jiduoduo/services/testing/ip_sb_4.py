from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class IPSB4TestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class IPSB4TestingResult(TestingResult):
    pass


class IPSB4TestingService(TestingService):
    testing_type: TestingType = TestingType.IP_SB_4
    testing_params_cls: type[IPSB4TestingParams] = IPSB4TestingParams
    testing_result_cls: type[IPSB4TestingResult] = IPSB4TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: IPSB4TestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> IPSB4TestingResult:
        run_result = vps.run(
            'curl -4 ip.sb',
            timeout=params.timeout,
            warn=True,
        )

        return IPSB4TestingResult(result=str(run_result))
