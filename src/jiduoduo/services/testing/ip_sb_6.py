from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class IPSB6TestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class IPSB6TestingResult(TestingResult):
    pass


class IPSB6TestingService(TestingService):
    testing_type: TestingType = TestingType.IP_SB_6
    testing_params_cls: type[IPSB6TestingParams] = IPSB6TestingParams
    testing_result_cls: type[IPSB6TestingResult] = IPSB6TestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: IPSB6TestingParams,
            flush_callback: Callable[[str], None],
    ) -> IPSB6TestingResult:
        run_result = vps.run(
            'curl -6 ip.sb',
            timeout=params.timeout,
            warn=True,
        )

        return IPSB6TestingResult(result=str(run_result))
