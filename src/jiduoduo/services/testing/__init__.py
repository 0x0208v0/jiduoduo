import logging
import uuid

from jiduoduo.models import Testing
from jiduoduo.models import TestingType
from jiduoduo.models import VPS
from jiduoduo.services.testing.backtrace import BacktraceTestingService
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingService
from jiduoduo.services.testing.bash_icu_gb5 import BashIcuGB5TestingService
from jiduoduo.services.testing.bash_icu_speed_test import BashIcuSpeedTestTestingService
from jiduoduo.services.testing.check_unlock_media import CheckUnlockMediaTestingService
from jiduoduo.services.testing.dd import DDTestingService
from jiduoduo.services.testing.df_h import DFHTestingService
from jiduoduo.services.testing.free_h import FREEHTestingService
from jiduoduo.services.testing.ip_check_place import IPCheckPlaceTestingService
from jiduoduo.services.testing.ip_info_io import IPInfoIOTestingService
from jiduoduo.services.testing.ip_sb_4 import IPSB4TestingService
from jiduoduo.services.testing.ip_sb_6 import IPSB6TestingService
from jiduoduo.services.testing.login import LoginTestingService
from jiduoduo.services.testing.memory_check import MemoryCheckTestingService
from jiduoduo.services.testing.next_trace import NextTraceTestingService
from jiduoduo.services.testing.nws_global import NWSGlobalDefaultTestingService
from jiduoduo.services.testing.region_restriction_check import RegionRestrictionCheckTestingService
from jiduoduo.services.testing.spiritlhls_ecs import SpiritLHLSECSTestingService
from jiduoduo.services.testing.spiritlhls_ecs_speed import SpiritLHLSECSSpeedTestingService
from jiduoduo.services.testing.yabs_basic_sys_info import YABSBasicSysInfoTestingService
from jiduoduo.services.testing.yabs_default import YABSDefaultTestingService
from jiduoduo.services.testing.yabs_disk import YABSDiskTestingService
from jiduoduo.services.testing.yabs_gb5 import YABSGB5TestingService

logger = logging.getLogger(__name__)

TESTING_SERVICE_CLS_DICT = {
    TestingType.LOGIN: LoginTestingService,
    TestingType.MEMORY_CHECK: MemoryCheckTestingService,
    TestingType.SPIRITLHLS_ECS: SpiritLHLSECSTestingService,
    TestingType.SPIRITLHLS_ECS_SPEED: SpiritLHLSECSSpeedTestingService,
    TestingType.NWS_GLOBAL: NWSGlobalDefaultTestingService,
    TestingType.BASH_ICU_GB5: BashIcuGB5TestingService,
    TestingType.BASH_ICU_SPEED_TEST: BashIcuSpeedTestTestingService,
    TestingType.DF_H: DFHTestingService,
    TestingType.DD: DDTestingService,
    TestingType.FREE_H: DFHTestingService,
    # IP 相关
    TestingType.NEXT_TRACE: NextTraceTestingService,
    TestingType.BACKTRACE: BacktraceTestingService,
    TestingType.IP_CHECK_PLACE: IPCheckPlaceTestingService,
    TestingType.REGION_RESTRICTION_CHECK: RegionRestrictionCheckTestingService,
    TestingType.CHECK_UNLOCK_MEDIA: CheckUnlockMediaTestingService,
    TestingType.IP_SB_4: IPSB4TestingService,
    TestingType.IP_SB_6: IPSB6TestingService,
    TestingType.IP_INFO_IO: IPInfoIOTestingService,
    # YABS 相关
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
