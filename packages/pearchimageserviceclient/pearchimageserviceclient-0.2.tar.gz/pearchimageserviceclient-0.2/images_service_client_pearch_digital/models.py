from dataclasses import dataclass
from typing import Dict, List


class Automap:
    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)


@dataclass
class StatusResponse(Automap):
    code: int
    msg: str


@dataclass
class HeaderResponse(Automap):
    method: str
    service: str
    time: int


@dataclass
class ImageData(Automap):

    created_datetime: str
    image_hash_md5: str
    image_height_size_px: str
    image_local_path: str
    image_mime_type: str
    image_size: str
    uploaded_to_bucket: str
    is_active: str
    is_object_detected: str
    inactive_by: str
    inactive_on: str
    set_inactive_for: str


@dataclass
class ElasticClass(Automap):
    prob: int
    cat: str
    image_id: int


@dataclass
class ElasticPrediction(Automap):
    classes: List[ElasticClass]
    uri: str
    image_data: ImageData


@dataclass
class BodyResponse(Automap):
    predictions: List[ElasticPrediction]


@dataclass
class ElasticImageResponse:
    index: str
    type: str
    id: str
    score: float
    # status: StatusResponse
    # head: HeaderResponse
    body: BodyResponse

    @property
    def predictions(self) -> Dict[str, List[ElasticClass]]:

        response: Dict[str, List[ElasticClass]] = {}
        for x in self.body.predictions.values():
            for y in x:
                for z in y.classes:
                    if y.uri not in response.keys():
                        response[y.uri] = [z]
                    else:
                        response[y.uri].append(z)

        return response
