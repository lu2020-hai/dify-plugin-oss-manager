from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.oss_utils import get_client


class DownloadStorageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        path = tool_parameters.get("path")
        client = get_client(self, tool_parameters)
        client.delete(path)
        yield self.create(f"SUCCESS")
