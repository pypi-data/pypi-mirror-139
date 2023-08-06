from __future__ import annotations
from functools import reduce
from typing import Any, Dict, Tuple, List, Union

from attrs import define

from attrs_mek.key import BaseKey, Key, ChildKey, SiblingKey
from attrs_mek.value import Value

StrOrList = Dict[str, Union[str, List[str]]]


def _update_current_directory(key: BaseKey, current_path: List[str]):
    """Use key type to update the current directory"""
    key.update_path(current_path)


def _remove_key(cls, name: str):
    """Remove Key from object and annotations"""
    if name in cls.__annotations__:
        del cls.__annotations__[name]

    delattr(cls, name)


def _add_map_element(
    mapping: Dict[str, StrOrList], name: str, value: Value, current_path: List[str]
):
    """Add Value path to mapping dictionary"""
    # use string in Value over attribute name:
    mapping_name = name if value.name is None else value.name

    # add to mapping:
    mapping[mapping_name] = current_path + [mapping_name]


def _transform_value(cls, name: str, value_field: Value):
    """Convert mek.Value to attrs.field"""
    # convert Value type to attrs field:
    setattr(cls, name, value_field.to_field())


def _format_list(
    unformatted_list: List[str], variables: Dict[str, Dict[str, StrOrList]]
):
    """Apply variables to value path from the mapping dictionary"""
    output = []

    for element in unformatted_list:
        if (
            element[0] + element[-1] == "{}"
            and (format_key := element[1:-1]) in variables
        ):
            # If list element is of the format: {name}
            # fill in variable
            format_value = variables[format_key]

            if isinstance(format_value, list):
                # variable is a list
                output.extend(format_value)
            else:
                # variable is a single name
                output.append(format_value)
        else:
            output.append(element)

    return output


def _get_value_from_path(
    dictionary: Dict[str, Any],
    path_to_field: List[str],
    variables: Dict[str, StrOrList],
) -> Tuple[Any, bool]:
    """Get single field value from path"""
    try:
        path_to_field = _format_list(path_to_field, variables)

        def reduce_func(nested_dictionary, nested_key):
            return nested_dictionary[nested_key]

        return reduce(reduce_func, path_to_field, dictionary), True
    except (KeyError, TypeError):
        return None, False


def _from_dict(mapping: Dict[str, List[str]], global_variables: Dict[str, StrOrList]):
    """Factory function for the attached from_dict"""

    @classmethod
    def from_dict(
        cls,
        input_dictionary: Dict[str, Any],
        variables: Dict[str, StrOrList] = {},
    ):
        """ """
        output = {}
        variables = {**global_variables, **variables}

        for name, path in mapping.items():
            val, keep = _get_value_from_path(input_dictionary, path, variables)
            if keep:
                output[name] = val

        # Create attrs object:
        return cls(**output)

    return from_dict


def _mek_tranformations(
    cls,
    dict_items: List[Tuple[str, str]],
    mapping: Dict[str, StrOrList],
    current_directory: List[str],
):
    """Transform object to attrs compatible object"""
    for name, key_value_field in dict_items:
        if isinstance(key_value_field, Value):
            _add_map_element(mapping, name, key_value_field, current_directory)
            _transform_value(cls, name, key_value_field)
        elif isinstance(key_value_field, BaseKey):
            _update_current_directory(key_value_field, current_directory)
            _remove_key(cls, name)


def mek(cls=None, variables: Dict[str, StrOrList] = {}, **attrs_kwargs):
    """Main entry point"""

    mapping = {}

    global_variables = variables.copy()

    def mek_with_class(cls):
        """mek decorator function"""
        current_directory = []

        annotations = list(cls.__annotations__.items())
        attributes = cls.__dict__.copy()

        if len(annotations) > 0:
            dict_items = {}

            for name, type in annotations:
                if name in attributes:
                    dict_items[name] = attributes[name]
                    continue

                if isinstance(Key(), type):
                    set_value = Key(name, from_annotation=True)
                elif isinstance(ChildKey(), type):
                    set_value = ChildKey(name, from_annotation=True)
                elif isinstance(SiblingKey(), type):
                    set_value = SiblingKey(name, from_annotation=True)
                else:
                    print("NAME", name)
                    set_value = Value(name)
                    print(set_value.field_property_kwargs)

                dict_items[name] = set_value
                setattr(cls, name, set_value)

            dict_items = dict_items.items()
        else:
            dict_items = cls.__dict__.copy().items()

        _mek_tranformations(cls, dict_items, mapping, current_directory)

        attrs_cls = define(cls, **attrs_kwargs)
        attrs_cls.from_dict = _from_dict(mapping, global_variables)

        return attrs_cls

    return mek_with_class if cls is None else mek_with_class(cls)
