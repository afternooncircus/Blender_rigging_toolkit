from bpy.utils import register_class, unregister_class

from .ui_custom_properties import VIEW3D_PT_ArmatureNameUI, VIEW3D_PT_BonePropertiesUI


classes: list = [
    VIEW3D_PT_ArmatureNameUI,
    VIEW3D_PT_BonePropertiesUI,
]


def register_ui() -> None:
    for cls in classes:
        register_class(cls)

def unregister_ui() -> None:
    for cls in reversed(classes):
        unregister_class(cls)