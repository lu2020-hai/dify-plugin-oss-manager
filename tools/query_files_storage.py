from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.oss_utils import get_client


class QueryFilesStorageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        path = tool_parameters.get("path")
        suffix = tool_parameters.get("suffix")

        client = get_client(self, tool_parameters)

        if suffix:
            suffix = f".{suffix}"
            result_dict: dict[str, Any] = client.query_files(path, suffix)
        else:
            result_dict: dict[str, Any] = client.query_files(path)

        yield self.create_json_message(result_dict)
