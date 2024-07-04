from typing import Callable

from invoke import Responder
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

        command = 'curl nxtrace.org/nt |bash ; nexttrace 8.8.4.4; nexttrace 2001:4860:4860::64 ; nexttrace youtube.com'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'Your Option', response='0\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return NextTraceTestingResult(result=str(run_result))
