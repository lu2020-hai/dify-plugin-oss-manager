import json
from collections.abc import Generator
from typing import Any, List

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.oss_utils import get_client


class SaveStorageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取工具参数
            content = tool_parameters.get("content")
            path = tool_parameters.get("path", "")  # 如果未提供路径，默认为空字符串
            file_name = tool_parameters.get("file_name")

            # 初始化 OSS 客户端
            client = get_client(self, tool_parameters)
            # 拼接完整文件路径
            full_path = f"{path}/{file_name}" if path else file_name

            client.save(full_path, content.encode("utf-8"))
            yield self.create_text_message(f"SUCCESS")
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
