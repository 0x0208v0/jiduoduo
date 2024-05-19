from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class YABSBasicSysInfoTestingParams(TestingParams):
    timeout: int = Field(15)  # seconds


class YABSBasicSysInfoTestingResult(TestingResult):
    pass


class YABSBasicSysInfoTestingService(TestingService):
    testing_type: TestingType = TestingType.YABS_BASIC_SYS_INFO
    testing_params_cls: type[YABSBasicSysInfoTestingParams] = YABSBasicSysInfoTestingParams
    testing_result_cls: type[YABSBasicSysInfoTestingResult] = YABSBasicSysInfoTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: YABSBasicSysInfoTestingParams,
            flush_callback: Callable[[str], None],
    ) -> YABSBasicSysInfoTestingResult:
        run_result = vps.run(
            'curl -sL yabs.sh | bash -s -- -dign',
            timeout=params.timeout,
            warn=True,
        )

        return YABSBasicSysInfoTestingResult(result=str(run_result))
