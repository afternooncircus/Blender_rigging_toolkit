from bpy.utils import register_class, unregister_class
from . import creator_custom_properties


classes: list = [
    creator_custom_properties.AC_OT_add_CustomProp,
]


def register_operators() -> None:
    for cls in classes:
        register_class(cls)


def unregister_operators() -> None:
    for cls in classes:
        unregister_class(cls)
