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
from ts_sdk.models.api.model import BodyLoginAccessTokenApiV1LoginAccessTokenPost
from ts_sdk.models.provider import ConfigModel


class AuthenticationMapper:
    @staticmethod
    def map_config_auth(
        payload: ConfigModel,
    ) -> BodyLoginAccessTokenApiV1LoginAccessTokenPost:

        request_payload = BodyLoginAccessTokenApiV1LoginAccessTokenPost(
            username=payload.username,
            password=payload.password,
        )
        return request_payload
