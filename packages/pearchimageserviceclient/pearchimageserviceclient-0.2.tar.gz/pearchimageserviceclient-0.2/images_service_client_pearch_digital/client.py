from .abstractions import AImagesClient
import requests
from typing import Generator
from .models import ElasticImageResponse
from .generators import images_generator


class ImagesClient(AImagesClient):
    def __init__(self, service_host: str, api_key: str):
        self.service_host = service_host
        self.api_key = api_key
        self.headers = {"Api-Key": self.api_key}

    def search_images(
        self, kw: str, page: int
    ) -> Generator[ElasticImageResponse, None, None]:

        r = requests.get(
            f"{self.service_host}/images/get_images_by_search/{kw}/{page}",
            headers=self.headers,
        )
        if r.status_code == 200:
            return images_generator(r.json()["hits"])
        else:
            raise Exception(r.text)
