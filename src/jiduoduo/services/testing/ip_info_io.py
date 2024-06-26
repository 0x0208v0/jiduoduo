from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class IPInfoIOTestingParams(TestingParams):
    timeout: int = Field(10)  # seconds


class IPInfoIOTestingResult(TestingResult):
    pass


class IPInfoIOTestingService(TestingService):
    testing_type: TestingType = TestingType.IP_INFO_IO
    testing_params_cls: type[IPInfoIOTestingParams] = IPInfoIOTestingParams
    testing_result_cls: type[IPInfoIOTestingResult] = IPInfoIOTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: IPInfoIOTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> IPInfoIOTestingResult:
        run_result = vps.run(
            'curl https://ipinfo.io/',
            timeout=params.timeout,
            warn=True,
        )

        return IPInfoIOTestingResult(result=str(run_result))
