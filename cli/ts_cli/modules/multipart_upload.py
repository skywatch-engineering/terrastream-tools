import threading
from itertools import cycle
from queue import Queue
from time import sleep
from time import time
from typing import List
from urllib import parse

import requests
from models.multipart_upload import MultipartUploadInfo
from models.multipart_upload import PartItemInfo
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FileManager:
    def __init__(self, file_path: str, chunk_size: int) -> None:
        self.file_path = file_path
        self.chunk_size = chunk_size

    def read_file_chunks(self) -> bytes:
        logger.info(f"Reading chunk size: {self.chunk_size}")
        with open(self.file_path, "rb") as f:
            while True:
                piece = f.read(self.chunk_size)
                if not piece:
                    break
                yield piece


class SequentialUploader:
    def __init__(self, mp_info: MultipartUploadInfo, urls: List[str]) -> None:
        self.mp_info: MultipartUploadInfo = mp_info
        self.start_time = time()
        self.parts_uploaded: List[PartItemInfo] = []
        self.urls = urls
        self.file_manager: FileManager = None

    def prepare(self):
        self.file_manager = FileManager(
            file_path=self.mp_info.file_path, chunk_size=self.mp_info.part_size_bytes
        )

    def upload(self) -> List[PartItemInfo]:
        chunk = self.file_manager.read_file_chunks()
        for url in self.urls:
            data = next(chunk)
            self._upload_part(url, data)

        logger.info("Sequential upload finished!")
        return self.parts_uploaded

    def _upload_part(self, url: str, data: bytes) -> dict:
        part_number = int(parse.parse_qs(url)["partNumber"][0])
        part_start_time = time()
        logger.info(
            f"Uploading part: {part_number}/{self.mp_info.parts}, size: {len(data)}"
        )
        put_response = requests.put(url=url, headers={}, data=data)
        if put_response.status_code != 200:
            logger.error(
                f"Status code: {put_response.status_code}. Response: {put_response.text}"
            )
        else:
            logger.info(f"part {part_number} uploaded!")

        part_info = PartItemInfo(
            etag=put_response.headers["ETag"], part_number=part_number
        )
        self.parts_uploaded.append(part_info)

        logger.info(
            f"Part {part_number} uploaded! took: {round(time() - part_start_time, 2)}s, total: {round(time() - self.start_time,2)}s "
        )
        return part_info


class ParallelUploader(SequentialUploader):
    def __init__(
        self, mp_info: MultipartUploadInfo, urls: List[str], num_threads=10
    ) -> None:
        super().__init__(mp_info, urls)
        self.execution_queue: Queue = None
        self.threads = []
        self.num_threads = num_threads
        self.stop_thread = False

    def prepare(self):
        super().prepare()
        self.threads = []
        self.execution_queue = Queue()

        self.num_threads = (
            self.num_threads if len(self.urls) > self.num_threads else len(self.urls)
        )

    def upload(self) -> List[PartItemInfo]:
        p = threading.Thread(target=self.producer_thread, args=())
        p.start()
        self.threads.append(p)

        logger.info(f"Buffering, threads: {self.num_threads}")
        sleep(10)

        for i in range(1, self.num_threads + 1):
            x = threading.Thread(target=self.consumer_thread, args=(str(i),))
            x.start()
            self.threads.append(x)

        for t in self.threads:
            t.join()

        logger.info("Parallel upload finished!")
        return self.parts_uploaded

    def producer_thread(self):
        max_items = len(self.urls)
        iter_urls = cycle(self.urls)
        max_queue_items = self.num_threads * 2

        chunk = self.file_manager.read_file_chunks()

        processed_items = 0
        not_finished = True
        while not_finished:
            new_item = False
            if self.execution_queue.qsize() <= max_queue_items:
                data = next(chunk)
                url = next(iter_urls)
                self.execution_queue.put(dict(url=url, chunk=data))
                processed_items = processed_items + 1
                left = max_items - processed_items
                logger.info(f"New queue item, {left} left")
                new_item = True
                not_finished = left > 0

            if not new_item:
                sleep(1)
            if self.stop_thread:
                logger.warning("Producer thread stopped due to an error!")
                break
        logger.info("Producer finished!")

    def consumer_thread(self, name: str):
        logger.info(f"thread {name} started!")
        while not self.execution_queue.qsize() == 0:
            if self.stop_thread:
                break
            logger.info(f"queue items: {self.execution_queue.qsize()}")
            try:
                content = self.execution_queue.get()
                self._upload_part(url=content["url"], data=content["chunk"])
            except Exception:
                logger.exception(f"Error running thread {name}")
                self.stop_thread = True

        logger.info(f"thread {name} finished!")


class MultipartUploadManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.mp_info: MultipartUploadInfo = None
        self.start_time = None

    def prepare(self, chunk_size_mb: int = 50) -> MultipartUploadInfo:
        self.mp_info = MultipartUploadInfo.calculate(
            file_path=self.file_path, part_size_mb=chunk_size_mb
        )
        logger.info(
            f"Parts: {self.mp_info.parts}, size(mb): {self.mp_info.part_size_mb}"
        )
        return self.mp_info

    def upload(
        self, urls: List[str], parallel: bool = True, thread_num: int = 10
    ) -> List[PartItemInfo]:
        self.start_time = time()

        if not parallel:
            seq_uploader = SequentialUploader(self.mp_info, urls)
            seq_uploader.prepare()
            response = seq_uploader.upload()
        else:
            parl_uploader = ParallelUploader(self.mp_info, urls, thread_num)
            parl_uploader.prepare()
            response = parl_uploader.upload()

        logger.info(f"Overall took: {round(time() - self.start_time)}s")
        return response
