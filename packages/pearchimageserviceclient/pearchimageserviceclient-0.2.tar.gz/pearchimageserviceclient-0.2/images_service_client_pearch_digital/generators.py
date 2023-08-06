from typing import Generator
from .models import (
    ElasticImageResponse,
    ElasticPrediction,
    ElasticClass,
    ImageData,
    StatusResponse,
    HeaderResponse,
    BodyResponse,
)


def images_generator(
    query_result,
) -> Generator[ElasticImageResponse, None, None]:
    for x in query_result:
        #head = HeaderResponse(*x["_source"]["head"].values())
        #status = StatusResponse(*x["_source"]["status"].values())
        classes = [
            ElasticClass(
                *{
                    "prob": y["prob"],
                    "cat": y["cat"],
                    "image_id": y["image_id"],
                    "image_data": None
                }.values()
            )
            for y in x["_source"]["body"]["predictions"][0]["classes"]
        ]
        predictions = [
            ElasticPrediction(
                *{
                    "classes": classes,
                    "uri": x["_source"]["body"]["predictions"][0]["uri"],
                    "image_data": ImageData(*y["image_data"].values())
                }.values()
            )
        ]
        body = BodyResponse({"predictions": predictions})
        yield ElasticImageResponse(
            *{
                "index": x["_index"],
                "type": "",
                "id": x["_id"],
                "score": x["_score"],
                # "status": status,
                # "head": head,
                "body": body,
            }.values()
        )
