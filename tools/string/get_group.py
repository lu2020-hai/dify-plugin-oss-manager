import json
from collections.abc import Generator
from typing import Any, List

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetGroupTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        group = tool_parameters.get("group")
        groups_encoded = self.session.storage.get(group + ":groupKey")
        groups: List[str] = []
        if groups_encoded:
            groups = json.loads(groups_encoded.decode())

        for key in groups:
            value = self.session.storage.get(group + "-" + key + ":group")
            yield self.create_json_message({
                key:value
            })



