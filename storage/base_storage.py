"""Abstract interface for file storage implementations."""

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Dict, List


class BaseStorage(ABC):
    """Interface for file storage."""

    @abstractmethod
    def save(self, filename, data):
        raise NotImplementedError

    @abstractmethod
    def load_once(self, filename: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def load_stream(self, filename: str) -> Generator:
        raise NotImplementedError

    @abstractmethod
    def download(self, filename, target_filepath):
        raise NotImplementedError

    @abstractmethod
    def exists(self, filename):
        raise NotImplementedError

    @abstractmethod
    def delete(self, filename):
        raise NotImplementedError

    # @abstractmethod
    def query_files(self, prefix: str = None, suffix: str = None) -> Dict[str, List[Dict[str, str]]]:
        raise NotImplementedError

    # @abstractmethod
    def get_file_metadata(self, filename: str) -> dict:
        raise NotImplementedError