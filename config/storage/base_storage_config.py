# 抽象基类：定义通用字段
from pydantic import BaseModel, Field


class BaseStorageConfig(BaseModel):
    """
    Base configuration for storage services.
    """
    storage_type: str = Field(description="Type of storage service (e.g., 's3', 'aliyun')")

