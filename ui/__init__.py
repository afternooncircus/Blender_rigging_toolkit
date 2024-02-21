from bpy.utils import register_class, unregister_class

from .ui_custom_properties import VIEW3D_PT_PropertyBoneUI
classes: list = [
    VIEW3D_PT_PropertyBoneUI,

]

def register_ui() -> None:
    for cls in classes:
        register_class(cls)

def unregister_ui() -> None:
    for cls in reversed(classes):
        unregister_class(cls)