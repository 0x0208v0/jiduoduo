from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class LoginTestingParams(TestingParams):
    timeout: int = Field(5)  # seconds


class LoginTestingResult(TestingResult):
    pass


class LoginTestingService(TestingService):
    testing_type: TestingType = TestingType.LOGIN
    testing_params_cls: type[LoginTestingParams] = LoginTestingParams
    testing_result_cls: type[LoginTestingResult] = LoginTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: LoginTestingParams,
            flush_callback: Callable[[str], None],
    ) -> LoginTestingResult:
        run_result = vps.run(
            'echo login ok!',
            timeout=params.timeout,
            warn=True,
        )

        return LoginTestingResult(result=str(run_result))
