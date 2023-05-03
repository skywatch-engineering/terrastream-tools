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
from typing import Optional

from modules.credentials import CredentialsHandler
from ts_sdk.api.client import AuthenticatedClient
from ts_sdk.api.endpoints.products import confirm_product_upload_patch
from ts_sdk.api.endpoints.products import create_custom_product_post
from ts_sdk.controllers.client_controller import ClientController
from ts_sdk.models.api.generated.base_model import CreateCustomProductPayload
from ts_sdk.models.api.generated.base_model import CustomProductResponse
from ts_sdk.models.api.generated.base_model import ProductUploadCompletePayload
from ts_sdk.models.api.model import ProductUploadCompleteResponse
from ts_sdk.wrappers.auth import call_with_auth


class ApiHandler:
    def __init__(self) -> None:
        credentials = CredentialsHandler()
        self.client_controller = ClientController(credentials.api)

    @call_with_auth
    def create_custom_product(
        self,
        model: CreateCustomProductPayload,
        auth_client: Optional[AuthenticatedClient] = None,
    ) -> CustomProductResponse:
        return create_custom_product_post(client=auth_client, form_data=model)

    @call_with_auth
    def confirm_product_upload(
        self,
        product_id: str,
        model: ProductUploadCompletePayload,
        auth_client: Optional[AuthenticatedClient] = None,
    ) -> ProductUploadCompleteResponse:
        return confirm_product_upload_patch(
            client=auth_client, product_id=product_id, form_data=model
        )