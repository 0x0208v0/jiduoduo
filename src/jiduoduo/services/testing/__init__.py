import logging
import uuid

from jiduoduo.models import Testing
from jiduoduo.models import TestingType
from jiduoduo.models import VPS
from jiduoduo.services.testing.backtrace import BacktraceTestingService
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingService
from jiduoduo.services.testing.bash_icu_gb5 import BashICUGB5TestingService
from jiduoduo.services.testing.ecs import ECSTestingService
from jiduoduo.services.testing.ip_check_place import IPCheckPlaceTestingService
from jiduoduo.services.testing.login import LoginTestingService
from jiduoduo.services.testing.yabs_basic_sys_info import YABSBasicSysInfoTestingService
from jiduoduo.services.testing.yabs_default import YABSDefaultTestingService
from jiduoduo.services.testing.yabs_disk import YABSDiskTestingService
from jiduoduo.services.testing.yabs_gb5 import YABSGB5TestingService

logger = logging.getLogger(__name__)

TESTING_SERVICE_CLS_DICT = {
    TestingType.LOGIN: LoginTestingService,
    TestingType.ECS: ECSTestingService,
    TestingType.IP_CHECK_PLACE: IPCheckPlaceTestingService,
    TestingType.BASH_ICU_GB5: BashICUGB5TestingService,
    TestingType.BACKTRACE: BacktraceTestingService,
    # yabs 系列
    TestingType.YABS_DEFAULT: YABSDefaultTestingService,
    TestingType.YABS_BASIC_SYS_INFO: YABSBasicSysInfoTestingService,
    TestingType.YABS_DISK: YABSDiskTestingService,
    TestingType.YABS_GB5: YABSGB5TestingService,
}


def get_testing_service_cls(testing_type: TestingType | str) -> type[TestingService]:
    testing_type = TestingType(testing_type)

    testing_service_cls = TESTING_SERVICE_CLS_DICT.get(testing_type)

    if testing_service_cls is None:
        raise ValueError(f'不支持 {testing_type}')

    return testing_service_cls


def run_testing(
        testing_or_id: Testing | uuid.UUID,
        params: TestingParams | dict | None = None,
        dry_run: bool = False,
) -> Testing:
    if isinstance(testing_or_id, uuid.UUID):
        testing = Testing.get(testing_or_id)
        if not testing:
            raise ValueError(f'not found testing, testing_id={testing_or_id}')

    else:
        testing = testing_or_id

    testing_service_cls = get_testing_service_cls(testing.type)
    service = testing_service_cls(dry_run=dry_run)
    return service.run(testing=testing, params=params)


def run_testing_on_vps(
        testing_type: TestingType | str,
        vps_or_id: VPS | uuid.UUID,
        params: TestingParams | dict | None = None,
        dry_run: bool = False,
):
    if isinstance(vps_or_id, uuid.UUID):
        vps = VPS.get(vps_or_id)
        if not vps:
            raise ValueError(f'not found vps, vps_id={vps_or_id}')
    else:
        vps = vps_or_id

    testing_service_cls = get_testing_service_cls(testing_type)
    service = testing_service_cls(dry_run=dry_run)
    return service.run_on_vps(vps=vps, params=params)
