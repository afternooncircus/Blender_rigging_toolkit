from bpy.utils import register_class, unregister_class

from . import op_custom_properties
# from . import drivers_in_custom_properties
from . import op_armature_settings

from . import op_import_armature_presets
classes: list = [
    op_custom_properties.AC_OT_add_CustomProp,
    op_armature_settings.AC_OT_Set_ArmatureProp,
    op_import_armature_presets.HumanArmaturePreset
]


def register_operators() -> None:
    for cls in classes:
        register_class(cls)


def unregister_operators() -> None:
    for cls in classes:
        unregister_class(cls)
