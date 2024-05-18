import io
from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class ECSTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class ECSTestingResult(TestingResult):
    pass


class ECSTestingService(TestingService):
    testing_type: TestingType = TestingType.ECS
    testing_params_cls: type[ECSTestingParams] = ECSTestingParams
    testing_result_cls: type[ECSTestingResult] = ECSTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: ECSTestingParams,
            flush_callback: Callable[[str], None],
    ) -> ECSTestingResult:
        command = 'curl -L https://gitlab.com/spiritysdx/za/-/raw/main/ecs.sh -o ecs.sh && chmod +x ecs.sh && bash ecs.sh -m 1'

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

        return ECSTestingResult(result=str(run_result))
