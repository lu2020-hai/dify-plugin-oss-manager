from pydantic import Field
from config.storage.base_storage_config import BaseStorageConfig


class OpenDALStorageConfig(BaseStorageConfig):
    OPENDAL_SCHEME: str = Field(
        default="fs",
        description="OpenDAL scheme.",
    )
