from typing import Callable

from pydantic import Field

from jiduoduo.models import VPS
from jiduoduo.models.testing import TestingType
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingResult
from jiduoduo.services.testing.base import TestingService


class DDTestingParams(TestingParams):
    # 有的NAT鸡速度巨慢，需要227秒以上，速度1.2MB/s
    # 所以延长超时时间
    timeout: int = Field(60 * 5)  # seconds


class DDTestingResult(TestingResult):
    pass


class DDTestingService(TestingService):
    testing_type: TestingType = TestingType.DD
    testing_params_cls: type[DDTestingParams] = DDTestingParams
    testing_result_cls: type[DDTestingResult] = DDTestingResult

    def run_on_vps(
            self,
            vps: VPS,
            params: DDTestingParams,
            flush_callback: Callable[[str], None],
    ) -> DDTestingResult:
        # https://pickstar.today/2023/07/%E6%96%B0%E8%B4%ADvps%E5%B8%B8%E7%94%A8%E8%AF%84%E6%B5%8B%E8%84%9A%E6%9C%AC%E9%9B%86%E5%90%88/
        # 参考 硬盘专项测试
        run_result = vps.run(
            'dd if=/dev/zero of=256 bs=64K count=4K oflag=dsync',
            timeout=params.timeout,
            warn=True,
        )

        return DDTestingResult(result=str(run_result))
