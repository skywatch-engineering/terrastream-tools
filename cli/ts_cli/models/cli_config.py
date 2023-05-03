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
from pydantic import BaseModel
from pydantic import Field


class CliConfigModel(BaseModel):
    api_base_url: str = Field(description="Api base url")
    api_username: str = Field(description="Api user name. Example: user@domain.com")
    api_password: str = Field(description="TS user api password")

    @staticmethod
    def example() -> dict:
        return {
            "api_base_url": "https://api.provider-stage.terrastream.ca",
            "api_password": "<password here>",
            "api_username": "user@domain.com",
        }
