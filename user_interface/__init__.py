from bpy.utils import register_class, unregister_class
import bpy
from . import ui_armature_settings
from . import ui_custom_properties
from . import ui_import_armature_preset
classes: list = [
    ui_armature_settings.DATA_PT_ArmatureSettings,
    ui_custom_properties.VIEW3D_PT_CustomBonePropertiesUI,
    ui_custom_properties.VIEW3D_PT_CharacterSettingsUI,
    ui_custom_properties.VIEW3D_PT_FaceSettingsUI,
    ui_custom_properties.VIEW3D_PT_EyesPropUI,
    ui_custom_properties.VIEW3D_PT_MouthPropUI,
    ui_custom_properties.VIEW3D_PT_FkHingeUI,
    ui_custom_properties.VIEW3D_PT_IkFkSwitchUI,
    ui_custom_properties.VIEW3D_PT_BonesMaskPropUI,
    ui_custom_properties.VIEW3D_PT_IKSettingsUI,
    ui_custom_properties.VIEW3D_PT_LimbSettingsUI,
    ui_custom_properties.VIEW3D_PT_RubberHoselUI,
    ui_custom_properties.VIEW3D_PT_FootRollUI,
    ui_custom_properties.VIEW3D_PT_IKStretchUI,
    ui_custom_properties.VIEW3D_PT_IKFollowUI,
]


def register_ui() -> None:
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_armature_add.append(ui_import_armature_preset.DATA_MT_HumanArmaturePreset)

def unregister_ui() -> None:
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_MT_armature_add.remove(ui_import_armature_preset.DATA_MT_HumanArmaturePreset)