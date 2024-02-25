from bpy.utils import register_class, unregister_class

from . import ui_custom_properties as ac_custom_prop_ui

classes: list = [
    ac_custom_prop_ui.VIEW3D_PT_CustomBonePropertiesUI,
    ac_custom_prop_ui.VIEW3D_PT_CharacterSettingsUI,
    ac_custom_prop_ui.VIEW3D_PT_FaceSettingsUI,
    ac_custom_prop_ui.VIEW3D_PT_EyesPropUI,
    ac_custom_prop_ui.VIEW3D_PT_MouthPropUI,
    ac_custom_prop_ui.VIEW3D_PT_FkHingeUI,
    ac_custom_prop_ui.VIEW3D_PT_IkFkSwitchUI,
    ac_custom_prop_ui.VIEW3D_PT_BonesMaskPropUI,
    ac_custom_prop_ui.VIEW3D_PT_IKSettingsUI,
    ac_custom_prop_ui.VIEW3D_PT_LimbSettingsUI,
    ac_custom_prop_ui.VIEW3D_PT_RubberHoselUI,
    ac_custom_prop_ui.VIEW3D_PT_FootRollUI,
    ac_custom_prop_ui.VIEW3D_PT_IKStretchUI,
    ac_custom_prop_ui.VIEW3D_PT_IKFollowUI,
]


def register_ui() -> None:
    for cls in classes:
        register_class(cls)


def unregister_ui() -> None:
    for cls in reversed(classes):
        unregister_class(cls)
