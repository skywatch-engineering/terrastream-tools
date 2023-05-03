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

logger = logging.getLogger()

from ts_sdk.api.client import AuthenticatedClient
from ts_sdk.api.client import Client
from ts_sdk.api.endpoints.authentication import login_access_token_post
from ts_sdk.api.errors import ApiResponseError
from ts_sdk.mappers.authentication import AuthenticationMapper
from ts_sdk.models.api.model import Token
from ts_sdk.models.provider import ConfigModel


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ClientController(metaclass=Singleton):
    def __init__(self, config: ConfigModel = None) -> None:
        self._config = config
        self._token: Token = None
        self._auth_client: AuthenticatedClient = None

    def update_config(self, config: ConfigModel):
        self._config = config

    def force_renew(self):
        self._token = None

    def _auth(self) -> Token:
        form_data = AuthenticationMapper.map_config_auth(self._config)
        client_model = Client.from_config(self._config)

        try:
            return login_access_token_post(client=client_model, form_data=form_data)
        except ApiResponseError:
            logger.exception(
                "An error ocurred while trying to generate authentication token!"
            )
            raise

    def auth(self, force_renew=False) -> AuthenticatedClient:
        if force_renew:
            self.force_renew()

        if self._token is not None and self._token.has_expired:
            logger.debug("Token has expired!")
            self._token = None

        if not self._token:
            logger.debug("Token obj is not defined, creating...")
            self._token = self._auth()
            self._auth_client = None

        if not self._auth_client:
            self._auth_client = AuthenticatedClient.from_auth(
                self._token.access_token, self._config
            )
            logger.debug("Authenticated client created!")

        return self._auth_client
