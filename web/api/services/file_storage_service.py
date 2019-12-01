import logging
import os

from web.api.utils import Service


class FileStorageService(Service):
    logger = logging.getLogger(__name__)

    def save_file(self, file_path: str, file_source: bytes):
        logging.debug("Saving file %s", file_path)
        with open(file_path, "wb") as f:
            f.write(file_source)

    def read_file(self, file_path: str) -> bytes:
        logging.debug("Reading file %s", file_path)
        with open(file_path, "rb") as f:
            bts = f.read()
        return bts

    def remove_file(self, file_path):
        logging.debug("Removing file %s", file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)


file_storage_service = FileStorageService()
