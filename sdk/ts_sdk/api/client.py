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
from __future__ import annotations

from typing import Dict

from pydantic import BaseModel
from ts_sdk.models.provider import ConfigModel


class Client(BaseModel):
    """A class for keeping track of data related to the API"""

    base_url: str

    @staticmethod
    def from_config(config: ConfigModel) -> Client:
        return Client(base_url=config.base_url)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in auth endpoints"""
        return {"Content-Type": "application/x-www-form-urlencoded"}


class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    token: str

    @staticmethod
    def from_auth(token: str, config: ConfigModel) -> AuthenticatedClient:
        return AuthenticatedClient(token=token, base_url=config.base_url)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
