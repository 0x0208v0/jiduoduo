from typing import Callable

from invoke import Responder
from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService
from jiduoduo.utils.fabric_utils import StreamFlusher


class OneClickVirtECSTestingParams(TestingParams):
    timeout: int = Field(60 * 10 * 3)  # seconds


class OneClickVirtECSTestingResult(TestingResult):
    pass


class OneClickVirtECSTestingService(TestingService):
    testing_type: TestingType = TestingType.ONECLICKVIRT_ECS
    testing_params_cls: type[OneClickVirtECSTestingParams] = OneClickVirtECSTestingParams
    testing_result_cls: type[OneClickVirtECSTestingResult] = OneClickVirtECSTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: OneClickVirtECSTestingParams,
            flush_callback: Callable[[str], None] | None = None,
    ) -> OneClickVirtECSTestingResult:
        # https://github.com/oneclickvirt/ecs

        command = 'curl -L https://cdn.spiritlhl.net/https://raw.githubusercontent.com/oneclickvirt/ecs/master/goecs.sh -o goecs.sh && chmod +x goecs.sh && bash goecs.sh env && bash goecs.sh install && goecs'

        run_result = vps.run(
            command,
            timeout=params.timeout,
            warn=True,
            pty=True,
            watchers=[
                Responder(pattern=r'[y]/n', response='y\n'),
                Responder(pattern=r'Y/n', response='Y\n'),
                Responder(pattern=r'your choice', response='1\n'),
            ],
            out_stream=StreamFlusher(flush_callback=flush_callback),
        )

        return OneClickVirtECSTestingResult(result=str(run_result))
