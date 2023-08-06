from typing import List

from attrs import define, field


@define
class BaseKey:
    path: List[str]
    type: str
    from_annotation: bool = field(default=False)

    def __attrs_post_init__(self):
        if not self.from_annotation:
            self.path = self.str_list_converter(self.path)
            return

        if self.path[0] == "_":
            self.path = []
            return

        self.path = self.str_list_converter(self.path.split("_"))

    def update_path(self, current_path):
        if self.type == "root":
            current_path[:] = self.path
        if self.type == "sibling":
            current_path.pop()
            current_path.extend(self.path)
        if self.type == "child":
            current_path.extend(self.path)

    @staticmethod
    def str_list_converter(string):
        if string is None or string == "":
            return []

        if isinstance(string, str):
            return [string]

        return string


class Key(BaseKey):
    type: str = "root"

    def __init__(self, path=None, **kwargs):
        super().__init__(path, self.type, **kwargs)


class SiblingKey(BaseKey):
    type: str = "sibling"

    def __init__(self, path=None, **kwargs):
        super().__init__(path, self.type, **kwargs)


class ChildKey(BaseKey):
    type: str = "child"

    def __init__(self, path=None, **kwargs):
        super().__init__(path, self.type, **kwargs)
