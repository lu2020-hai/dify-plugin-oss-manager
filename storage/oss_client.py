from typing import Type

from pydantic import BaseModel

from storage.aliyun_oss_storage import AliyunOssStorage
from storage.aws_s3_storage import AwsS3Storage
from storage.base_storage import BaseStorage
from storage.google_cloud_storage import GoogleCloudStorage
from storage.huawei_obs_storage import HuaweiObsStorage
from storage.opendal_storage import OpenDALStorage
from storage.supabase_storage import SupabaseStorage
from storage.volcengine_tos_storage import VolcengineTosStorage


class StorageClientManager:
    """
    统一管理存储客户端的类。
    根据传入的存储类型和配置，动态加载并返回对应的存储客户端。
    """

    def __init__(self, storage_type: str, config: BaseModel):
        """
        初始化存储客户端管理器。

        :param storage_type: 存储类型（如 "s3", "aliyun-oss" 等）
        :param config: 配置对象，继承自 BaseStorage
        """
        self.storage_type = storage_type
        self.client = self._load_client(storage_type, config)

    @staticmethod
    def _load_client(storage_type: str, config: BaseModel) -> BaseStorage:
        """
        根据存储类型和配置动态加载对应的存储客户端。

        :param storage_type: 存储类型
        :param config: 配置对象
        :return: 存储客户端实例
        """
        # 定义存储类型与客户端类的映射关系
        config_class_map: dict[str, Type[BaseStorage]] = {
            "s3": AwsS3Storage,
            "aliyun-oss": AliyunOssStorage,
            # "baidu-obs": BaiduObsStorage,
            "google-storage": GoogleCloudStorage,
            "huawei-obs": HuaweiObsStorage,
            "oci-storage": OpenDALStorage,
            # "tencent-cos": TencentCosStorage,
            "volcengine-tos": VolcengineTosStorage,
            "supabase": SupabaseStorage,
        }

        # 检查存储类型是否支持
        if storage_type not in config_class_map:
            raise ValueError(f"Unsupported storage type: {storage_type}")

        # 获取对应的客户端类并实例化
        client_class = config_class_map[storage_type]
        return client_class(config)

    def get_client(self) -> BaseStorage:
        """
        获取存储客户端实例。

        :return: 存储客户端实例
        """
        return self.client
