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
import json
import os
import logging

from exceptions.auth import CredentialsNotFoundError
from models.cli_config import CliConfigModel
from ts_sdk.models.provider import ConfigModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CredentialsHandler:
    CLI_CONFIG_FILE_NAME = ".tscfg"

    def __init__(self) -> None:
        self._config_model: ConfigModel = None
        self._cli_config: CliConfigModel = None

    @property
    def api(self) -> ConfigModel:
        if not self._config_model:
            self._config_model = self.retrieve_api_credentials()
        return self._config_model

    @property
    def config_path(self) -> str:
        path = os.path.join(os.path.abspath(os.curdir), CredentialsHandler.CLI_CONFIG_FILE_NAME)
        return path

    @property
    def cli_config(self) -> CliConfigModel:
        if (
            os.path.exists(self.config_path)
            and not self._cli_config
        ):
            with open(self.config_path, "r") as f:
                return CliConfigModel(**json.loads(f.read()))
        else:
            logger.error(
                f"Could not find .tscfg file to retrieve credentials. Example: {CliConfigModel.example()}"
            )
            raise CredentialsNotFoundError(
                "Could not find .tscfg file to retrieve credentials"
            )

    def retrieve_api_credentials(self) -> ConfigModel:
        return ConfigModel(
            base_url=self.cli_config.api_base_url,
            password=self.cli_config.api_password,
            username=self.cli_config.api_username,
            name="test"
        )

