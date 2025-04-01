from collections.abc import Generator
from typing import Any, Optional, Union
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from config.storage_config import StorageConfigManager
from storage.base_storage import BaseStorage
from storage.oss_client import StorageClientManager


def get_client(tool: Tool, tool_parameters: dict[str, Any]) -> BaseStorage:
    parameters_storage_type = tool_parameters.get("storage_type")

    storage_type = None
    if parameters_storage_type and parameters_storage_type.strip():
        storage_type = parameters_storage_type
        config_json = tool_parameters.get("config_json")
    else:
        storage_type = tool.runtime.credentials.get("storage_type")
        config_json = tool.runtime.credentials.get("config_json")

    # 从 JSON 创建 S3 配置对象
    manager = StorageConfigManager.from_json(storage_type,config_json)
    config = manager.get_config()
    return StorageClientManager(storage_type, config).get_client()