from abc import ABC, abstractmethod
from typing import Generator
from .models import ElasticImageResponse


class AImagesClient(ABC):
    @abstractmethod
    def search_images(
        self, kw: str, page: int
    ) -> Generator[ElasticImageResponse, None, None]:
        """"""
