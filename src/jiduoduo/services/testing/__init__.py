import logging
import uuid

from jiduoduo.models import Testing
from jiduoduo.models import TestingType
from jiduoduo.models import VPS
from jiduoduo.services.testing.base import TestingParams
from jiduoduo.services.testing.base import TestingService
from jiduoduo.services.testing.ecs import ECSTestingService
from jiduoduo.services.testing.gb5 import GB5TestingService
from jiduoduo.services.testing.ip_check import IPCheckTestingService
from jiduoduo.services.testing.login import LoginTestingService

logger = logging.getLogger(__name__)


def get_testing_service_cls(testing_type: TestingType | str) -> type[TestingService]:
    testing_type = TestingType(testing_type)

    if testing_type == TestingType.LOGIN:
        testing_service_cls = LoginTestingService

    elif testing_type == TestingType.ECS:
        testing_service_cls = ECSTestingService

    elif testing_type == TestingType.IP_CHECK:
        testing_service_cls = IPCheckTestingService

    elif testing_type == TestingType.GB5:
        testing_service_cls = GB5TestingService

    else:
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
