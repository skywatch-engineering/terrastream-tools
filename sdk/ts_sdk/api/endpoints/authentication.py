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
from ts_sdk.api.client import Client
from ts_sdk.api.errors import ApiInvalidCredentialsError
from ts_sdk.api.errors import ApiNotFoundError
from ts_sdk.api.errors import ApiResponseError
from ts_sdk.models.api.model import BodyLoginAccessTokenApiV1LoginAccessTokenPost
from ts_sdk.models.api.model import Token

logger = logging.getLogger()


def login_access_token_post(
    *,
    client: Client,
    form_data: BodyLoginAccessTokenApiV1LoginAccessTokenPost,
) -> Token:

    """OAuth2 compatible token login, get an access token for future requests"""
    url = "{}/api/v1/login/access-token".format(client.base_url)
    headers = client.get_headers()
    data = form_data.dict(exclude_none=True, exclude_defaults=True)
    logger.info(f"POST:{url} headers:{headers} data:<username, password REDACTED> ")

    response = requests.post(url=url, headers=client.get_headers(), data=data)

    logger.info(f"Auth Response: {response.json()}")

    if response.status_code == 200:
        return Token.from_api(response.json())
    if response.status_code == 404:
        raise ApiNotFoundError(response=response)
    if response.status_code == 400:
        raise ApiInvalidCredentialsError(response=response)
    else:
        raise ApiResponseError(response=response)
