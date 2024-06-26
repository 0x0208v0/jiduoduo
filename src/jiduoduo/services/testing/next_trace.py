from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class NextTraceTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 2)  # seconds


class NextTraceTestingResult(TestingResult):
    pass


class NextTraceTestingService(TestingService):
    testing_type: TestingType = TestingType.NEXT_TRACE
    testing_params_cls: type[NextTraceTestingParams] = NextTraceTestingParams
    testing_result_cls: type[NextTraceTestingResult] = NextTraceTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: NextTraceTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> NextTraceTestingResult:
        # https://github.com/nxtrace/NTrace-core

        command = 'curl nxtrace.org/nt |bash && nexttrace 1.1.1.1'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return NextTraceTestingResult(result=str(run_result))
