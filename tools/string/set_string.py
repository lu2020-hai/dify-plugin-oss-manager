import json
from collections.abc import Generator
from multiprocessing import Lock
from typing import Any, List

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class SetStringTool(Tool):

    _group_locks = {}
    _global_lock = Lock()

    def _get_group_lock(self, group: str) -> Lock:
        """获取或创建指定 group 的锁"""
        with self._global_lock:
            if group not in self._group_locks:
                self._group_locks[group] = Lock()
            return self._group_locks[group]

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        value = tool_parameters["value"]
        size = tool_parameters.get("size")

        if size and len(value) > size:
            raise ValueError("String size too large")

        group = tool_parameters.get("group")
        key = tool_parameters["key"]

        if group:
            # 获取该 group 的锁
            group_lock = self._get_group_lock(group)

            # 加锁：确保对 groups_decode 的读取、修改和写回是线程安全的
            with group_lock:
                groups_decode: List[str] = []
                try:
                    # 读取 group 数据
                    groups_encoded = self.session.storage.get(group + ":groupKey")
                    if groups_encoded:
                        groups_decode = json.loads(groups_encoded.decode())
                except Exception as e:
                    print(f"Failed to decode group data for group: {group}. Initializing empty list. Error: {e}")

                # 修改 group 数据
                if key not in groups_decode:
                    groups_decode.append(key)

                # 写回 group 数据
                self.session.storage.set(group + ":groupKey", json.dumps(groups_decode).encode())

            self.session.storage.set(group + "-" + key + ":group", value.encode())
            yield self.create_text_message("SUCCESS")
        else:
            self.session.storage.set(key + ":default", value.encode())
            yield self.create_text_message("SUCCESS")
