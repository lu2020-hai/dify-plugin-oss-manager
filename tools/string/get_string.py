from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetStringTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = tool_parameters["key"]
        group = tool_parameters.get("group")

        if group:
            value = self.session.storage.get(group + "-" + key + ":group")
            yield self.create_text_message(value.decode())
        else:
            value = self.session.storage.get(key+":default")
            yield self.create_text_message(value.decode())
