import logging

import requests

logger = logging.getLogger()

from ts_sdk.api.client import AuthenticatedClient
from ts_sdk.api.errors import ApiResponseError
from ts_sdk.models.api.model import (
    CreateCustomProductPayload,
    ProductUploadCompleteResponse,
)
from ts_sdk.models.api.model import CustomProductResponse, ProductUploadCompletePayload


def create_custom_product_post(
    *,
    client: AuthenticatedClient,
    form_data: CreateCustomProductPayload,
) -> CustomProductResponse:
    url = "{}/api/v1/products/upload/create".format(client.base_url)
    data = form_data.json(exclude_none=True)
    headers = client.get_headers()
    logger.info(f"POST:{url} headers:{headers} data:{data}")

    response = requests.post(url=url, headers=headers, data=data)
    logger.debug(f"Response from api: {response.text}")

    if response.status_code in [200, 206]:
        return CustomProductResponse(**response.json())
    else:
        raise ApiResponseError(response=response)


def confirm_product_upload_patch(
    *,
    client: AuthenticatedClient,
    product_id: str,
    form_data: ProductUploadCompletePayload,
) -> ProductUploadCompleteResponse:
    """ """
    url = "{}/api/v1/products/{product_id}/upload/confirm".format(
        client.base_url, product_id=product_id
    )

    data = form_data.json(exclude_none=True)
    headers = client.get_headers()
    logger.info(f"PATCH:{url} headers:{headers} data:{data}")

    response = requests.patch(url=url, headers=headers, data=data)
    logger.debug(f"Response from api: {response.text}")

    if response.status_code in [200, 202]:
        return ProductUploadCompleteResponse(**response.json())
    else:
        raise ApiResponseError(response=response)
