import logging
from abc import ABC
from abc import abstractmethod

logger = logging.getLogger(__name__)


class ImageBedService(ABC):

    @abstractmethod
    def upload(self, image):
        pass
