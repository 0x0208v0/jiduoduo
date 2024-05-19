import io
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class YABSDefaultTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class YABSDefaultTestingResult(TestingResult):
    pass


class YABSDefaultTestingService(TestingService):
    testing_type: TestingType = TestingType.YABS_DEFAULT
    testing_params_cls: type[YABSDefaultTestingParams] = YABSDefaultTestingParams
    testing_result_cls: type[YABSDefaultTestingResult] = YABSDefaultTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: YABSDefaultTestingParams,
            flush_callback: Callable[[str], None],
    ) -> YABSDefaultTestingResult:
        command = 'curl -sL yabs.sh | bash'

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
            out_stream=StreamLogger(),
        )

        return YABSDefaultTestingResult(result=str(run_result))
