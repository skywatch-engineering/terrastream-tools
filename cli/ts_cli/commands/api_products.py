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

from models.multipart_upload import PartsInfo
from modules.api import ApiHandler
from modules.multipart_upload import MultipartUploadManager
from ts_sdk.models.api.model import CreateCustomProductPayload
from ts_sdk.models.api.model import ProductUploadCompletePayload
import logging

logger = logging.getLogger()


class ApiProductsCommands:
    def __init__(self) -> None:
        self.api_handler = ApiHandler()

    def create_custom_product(
        self,
        payload_file: str,
        input_file: str,
        skip_upload: bool,
        parallel: bool,
        thread_num: int,
        chunk_size_mb: int,
    ):
        create_model = self._open_payload_file(payload_file)
        upload_manager = MultipartUploadManager(file_path=input_file)
        # calculate number of parts
        mp_info = upload_manager.prepare(chunk_size_mb=chunk_size_mb)
        create_model.properties.num_parts = mp_info.parts

        # call create endpoint
        response_create = self.api_handler.create_custom_product(create_model)

        if skip_upload:
            logger.warning(
                "Skipping upload... Will not be able to confirm product without upload!"
            )
        else:
            # upload and retrieve parts information
            parts_info = PartsInfo(
                parts=upload_manager.upload(
                    urls=response_create.upload_urls,
                    parallel=parallel,
                    thread_num=thread_num,
                )
            )

            # call complete endpoint
            confirm_model = ProductUploadCompletePayload(
                upload_id=response_create.upload_id,
                request_id=str(create_model.request_id),
                result_id=str(response_create.result_id),
                type=create_model.type,
                parts=parts_info.to_json(),
            )
            self.api_handler.confirm_product_upload(
                product_id=response_create.product_id, model=confirm_model
            )

    def _open_payload_file(self, payload_file) -> CreateCustomProductPayload:
        with open(payload_file, "r") as file:
            return CreateCustomProductPayload(**json.loads(file.read()))
