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
            group = tool_parameters.get("group")
            groups_encoded = self.session.storage.get(group + ":groupKey")

            path = tool_parameters.get("path", "")  # 如果未提供路径，默认为空字符串
            file_name = tool_parameters.get("file_name")

            groups: List[str] = []
            if groups_encoded:
                groups = json.loads(groups_encoded.decode())

            string_values: List[str] = []
            for key in groups:
                value = self.session.storage.get(group + "-" + key + ":group")
                if value:
                    string_values.append(value.decode())

            # 初始化 OSS 客户端
            client = get_client(self, tool_parameters)
            # 拼接完整文件路径
            full_path = f"{path}/{file_name}" if path else file_name
            file_content = "\n".join(string_values)  # 每个字符串占一行

            client.save(full_path, file_content.encode("utf-8"))
            yield self.create_text_message(f"SUCCESS")
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
