from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class IPSBTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class IPSBTestingResult(TestingResult):
    pass


class IPSBTestingService(TestingService):
    testing_type: TestingType = TestingType.IP_SB
    testing_params_cls: type[IPSBTestingParams] = IPSBTestingParams
    testing_result_cls: type[IPSBTestingResult] = IPSBTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: IPSBTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> IPSBTestingResult:
        command = 'echo "IPv4"; curl -4 ip.sb; echo; echo "IPv6:"; curl -6 ip.sb'

        run_result = vps.run(
            command=command,
            timeout=params.timeout,
            warn=True,
        )

        return IPSBTestingResult(result=str(run_result))
