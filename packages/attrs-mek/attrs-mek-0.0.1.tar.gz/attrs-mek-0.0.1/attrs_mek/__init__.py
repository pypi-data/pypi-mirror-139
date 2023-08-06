from attrs_mek.key import Key, SiblingKey, ChildKey
from attrs_mek.mek import mek
from attrs_mek.value import Value

__version__ = "0.0.1"

__title__ = "attrs-mek"
__description__ = "Clean nested deserialization for attrs"
__url__ = "https://www.attrs.org/"
__uri__ = __url__
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Alex Rudolph"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 Alex Rudolph"

__all__ = ["mek", "Value", "Key", "SiblingKey", "ChildKey"]
