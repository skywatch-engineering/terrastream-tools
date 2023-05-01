from __future__ import annotations

import logging
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import Field

logger = logging.getLogger()

import ts_sdk.models.api.generated.base_model as shared
from ts_sdk.models.api.generated.base_model import OrderState  # type: ignore # noqa
from ts_sdk.models.api.generated.base_model import Status  # type: ignore # noqa
from ts_sdk.models.api.generated.base_model import Status1 as OrderStatus  # type: ignore # noqa

"""
This file imports only the required models auto generated from TS openapi.json schema without changing them
Any import, changes, fixes or improvements should be implemented here
"""


class PolygonGeom(shared.PolygonGeom):
    coordinates: List[List[List[float]]] = Field(
        [],
        title="Coordinates",
    )


class Geometry(PolygonGeom):
    pass


### auth


class Token(shared.Token):
    created_at = datetime.utcnow()

    @property
    def has_expired(self) -> bool:
        logger.debug(f"created_at: {self.created_at}")
        return (datetime.utcnow() - self.created_at).seconds >= self.expires_in

    @staticmethod
    def from_api(data: dict) -> Token:
        return Token(**data, created_at=datetime.utcnow())


class BodyLoginAccessTokenApiV1LoginAccessTokenPost(
    shared.BodyLoginAccessTokenApiV1LoginAccessTokenPost
):
    pass


### requests


class CreateRequestArchivePayload(shared.CreateRequestArchivePayload):
    pass


class CreateRequestArchiveResponse(shared.CreateRequestArchiveResponse):
    pass


class RequestArchiveResponse(shared.RequestArchiveResponse):
    pass


class OrderRequestArchivePayload(shared.OrderRequestArchivePayload):
    pass


class OrderRequestArchiveResponse(shared.Msg):
    pass


class CancelRequestArchivePayload(shared.CancelRequestArchivePayload):
    pass


class OnBehalfOf(shared.OnBehalfOf):
    pass


class CreateRequestTaskingPayload(shared.CreateRequestTaskingPayload):
    pass


class RequestTaskingResponse(shared.RequestTaskingResponse):
    pass


class CreateRequestTaskingResponse(shared.RequestTaskingResponse):
    pass


class OrderRequestTaskingResponse(shared.RequestTaskingResponse):
    pass


class CancelRequestTaskingResponse(shared.RequestTaskingResponse):
    pass


class GetRequestTaskingResponse(shared.RequestTaskingResponse):
    pass


class ResultTaskingResponse(shared.ResultTaskingResponse):
    pass


class GetResultTaskingResponse(ResultTaskingResponse):
    pass


### results


class ResultArchiveResponse(shared.ResultArchiveResponse):
    pass


class ListResultArchiveResponse(shared.ListResultArchiveResponse):
    pass


class SecureDownloadResponse(shared.SecureDownloadResponse):
    pass


### validations


class HTTPValidationError(shared.HTTPValidationError):
    detail: Optional[str] = Field(None, title="Detail")


### products


class CreateCustomProductPayload(shared.CreateCustomProductPayload):
    pass


class CustomProductResponse(shared.CustomProductResponse):
    pass


class ProductUploadCompletePayload(shared.ProductUploadCompletePayload):
    pass


class ProductUploadCompleteResponse(shared.Msg):
    pass
