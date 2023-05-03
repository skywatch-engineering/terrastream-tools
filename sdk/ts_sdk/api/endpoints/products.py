# Copyright 2023 Skywatch Space Applciations Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
