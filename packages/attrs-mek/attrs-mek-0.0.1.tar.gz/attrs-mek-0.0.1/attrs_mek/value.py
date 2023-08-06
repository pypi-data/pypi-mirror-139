from typing import Any, Dict

from attrs import field


class Value:
    def __init__(self, name: str = None, **field_kwargs: Dict[str, Any]):
        self.name = name
        self.field_kwargs = field_kwargs
        self.field_property_kwargs: Dict[str, Any] = {}

    def validator(self, validator):
        self.field_property_kwargs["validator"] = validator

    def default(self, default):
        self.field_property_kwargs["default"] = default

    def converter(self, converter):
        self.field_property_kwargs["converter"] = converter

    def to_field(self):
        return field(**self.field_property_kwargs, **self.field_kwargs)
