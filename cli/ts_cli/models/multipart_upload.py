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

import os
from typing import List

from pydantic import BaseModel


class MultipartUploadInfo(BaseModel):

    file_path: str = None
    parts: int = None
    part_size_mb: int = None
    part_size_bytes: int = None
    remain_part_size: int = None

    @staticmethod
    def calculate(file_path: str, part_size_mb: int = 50) -> MultipartUploadInfo:
        part_size_bytes = part_size_mb * 1024 * 1024
        file_size_bytes = os.path.getsize(file_path)
        parts = int(file_size_bytes / part_size_bytes)

        remain_part_size = file_size_bytes % part_size_bytes
        if remain_part_size > 0:
            parts = parts + 1

        if parts > 10000:
            raise Exception("Number of parts cannot exceed 10000!")

        return MultipartUploadInfo(
            file_path=file_path,
            part_size_bytes=part_size_bytes,
            parts=parts,
            part_size_mb=part_size_mb,
            remain_part_size=remain_part_size,
        )


class PartItemInfo(BaseModel):
    etag: str
    part_number: int


class PartsInfo(BaseModel):
    parts: List[PartItemInfo]

    def to_json(self) -> list:
        items = []
        for item in self.parts:
            items.append(item.dict())

        items = sorted(items, key=lambda d: d["part_number"])
        return items
