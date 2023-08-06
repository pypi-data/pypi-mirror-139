from functools import reduce

from attrs import define

from key import BaseKey
from value import Value

def _update_current_directory():
    pass

def _add_map_element():
    pass

def _format_list(unformatted_list, variables):
    output = []

    for element in unformatted_list:

        if (element[0] + element[-1] == "{}" and (format_key := element[1:-1]) in variables):

            format_value = variables[format_key]

            if isinstance(format_value, list):
                output.extend(format_value)
            else:
                output.append(format_value)

        else:
            output.append(element)

    return output


def _get_value_from_path(dictionary, path_to_field, variables):
    try:
        path_to_field = _format_list(path_to_field, variables)
        
        def reduce_func(nested_dictionary, nested_key):
            return nested_dictionary[nested_key]

        return reduce(reduce_func, path_to_field, dictionary), True
    except (KeyError, TypeError):
        return None, False

def _from_dict(mapping, variables):
    
    def from_dict():
        pass

    return from_dict

def mek(cls, variables, kwargs):

    def mek_with_class(cls):
            
        mapping = {}
        global_variables = variables.copy()
        current_directory = []

        obj_dict = cls.__dict__.copy()

        # setattr with type annotations

        for name, value_field in cls.__dict__.copy().items():
            if isinstance(value_field, Value):
                _add_map_element(name, value_field)
            elif isinstance(value_field, BaseKey):
                _update_current_directory(name, value_field)

        attrs_cls = define(cls, **kwargs)

        attrs_cls.from_dict = classmethod(_from_dict(mapping, variables))

        return cls

    return mek_with_class if cls is not None else mek_with_class(cls)