import json
from typing import Type

from pydantic import BaseModel, Field

from config.storage.aliyun_oss_storage_config import AliyunOSSStorageConfig
from config.storage.amazon_s3_storage_config import S3StorageConfig
from config.storage.azure_blob_storage_config import AzureBlobStorageConfig
from config.storage.baidu_obs_storage_config import BaiduOBSStorageConfig
from config.storage.base_storage_config import BaseStorageConfig
from config.storage.google_cloud_storage_config import GoogleCloudStorageConfig
from config.storage.huawei_obs_storage_config import HuaweiCloudOBSStorageConfig
from config.storage.oci_storage_config import OCIStorageConfig
from config.storage.supabase_storage_config import SupabaseStorageConfig
from config.storage.tencent_cos_storage_config import TencentCloudCOSStorageConfig
from config.storage.volcengine_tos_storage_config import VolcengineTOSStorageConfig


# 统一管理类
class StorageConfigManager:

    def __init__(self, storage_type: str, config_data: dict):
        self.storage_type = storage_type
        self.config = self._load_config(storage_type, config_data)

    @staticmethod
    def _load_config(storage_type: str, config_data: dict) -> BaseModel:
        config_class_map: dict[str, Type[BaseModel]] = {
            "s3": S3StorageConfig,
            "aliyun-oss": AliyunOSSStorageConfig,
            "azure-blob": AzureBlobStorageConfig,
            "baidu-obs": BaiduOBSStorageConfig,
            "google-storage": GoogleCloudStorageConfig,
            "huawei-obs": HuaweiCloudOBSStorageConfig,
            "oci-storage": OCIStorageConfig,
            "tencent-cos": TencentCloudCOSStorageConfig,
            "volcengine-tos": VolcengineTOSStorageConfig,
            "supabase": SupabaseStorageConfig,
        }

        # 获取配置类
        config_class = config_class_map.get(storage_type)
        if not config_class:
            raise ValueError(f"Unsupported storage type: {storage_type}")

        # 将 storage_type 添加到配置数据中
        config_data_with_type = {"storage_type": storage_type, **config_data}

        # 创建实例
        return config_class(**config_data_with_type)

    @classmethod
    def from_json(cls, storage_type: str,json_data: str) -> "StorageConfigManager":

        try:
            data = json.loads(json_data)
            return cls(storage_type=storage_type, config_data=data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load configuration from JSON: {e}")

    def get_config(self) -> BaseModel:
        return self.config