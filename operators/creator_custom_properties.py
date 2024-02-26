import bpy
from bpy.types import Context, Operator
import rna_prop_ui


def main()-> None:
    ''' Stores all the custom properties that would get call. '''

    foot_roll = CustomPropertiesAccess(prop_name="Foot Roll", source_bone="Properties", default=1.0, suffix=".L")
    arm_fk_hinge = CustomPropertiesAccess(prop_name="arm-FK_hinge", source_bone="Properties", default=1.0, suffix=".L")
    leg_fk_hinge = CustomPropertiesAccess(prop_name="leg-FK_hinge", source_bone="Properties", default=1.0, suffix=".L")
    arm_ik_pole_follow = CustomPropertiesAccess(prop_name="arm-IK_pole_follow", source_bone="Properties", default=1.0, suffix=".L")
    leg_ik_pole_follow = CustomPropertiesAccess(prop_name="leg-IK_pole_follow", source_bone="Properties", default=1.0, suffix=".L")
    arm_ik_stretch = CustomPropertiesAccess(prop_name="arm-IK_stretch", source_bone="Properties", default=1.0, suffix=".L")
    leg_ik_stretch = CustomPropertiesAccess(prop_name="leg-IK_stretch", source_bone="Properties", default=1.0, suffix=".L")
    arm_ik_fk_switch = CustomPropertiesAccess(prop_name="arm-IK|FK_switch", source_bone="Properties", default=1.0, suffix=".L")
    leg_ik_fk_switch = CustomPropertiesAccess(prop_name="leg-IK|FK_switch", source_bone="Properties", default=1.0, suffix=".L")
    arm_rubber_hose = CustomPropertiesAccess(prop_name="arm-rubber_hose", source_bone="Properties", default=1.0, suffix=".L")
    leg_rubber_hose = CustomPropertiesAccess(prop_name="leg-rubber_hose", source_bone="Properties", default=1.0, suffix=".L")
    arm_mask = CustomPropertiesAccess(prop_name="arm-mask", source_bone="Properties", default=False, suffix=".L")
    leg_mask = CustomPropertiesAccess(prop_name="leg-mask", source_bone="Properties", default=False, suffix=".L")
    

    all_props = {foot_roll, arm_fk_hinge, leg_fk_hinge, arm_ik_pole_follow, arm_ik_pole_follow, leg_ik_pole_follow, arm_ik_stretch, leg_ik_stretch, 
                arm_ik_fk_switch, leg_ik_fk_switch, arm_rubber_hose, leg_rubber_hose, arm_mask, leg_mask}
    
    properties_to_ui(all_props)


def properties_to_ui(all_custom_props: set) -> None:
    for custom_property in all_custom_props:
        proper_dict = make_dict_pairs(nameprop=custom_property.prop_name, default=custom_property.default,
                              source_bone=custom_property.source_bone, suffix=custom_property.suffix)
        ultimate_dict = buffer_custom_prop(custom_property.source_bone, proper_dict)

        for key in ultimate_dict:
            rna_prop_ui.rna_idprop_ui_create(
                overridable=True, **ultimate_dict[key])


def buffer_custom_prop(source_bone: str, buffer_dict: dict) -> dict:
    """Return dict with custom properties that do not exist in source bone."""

    ultimate_dict = {}
    for key in buffer_dict:
        if key in {_ for _ in bpy.context.active_object.pose.bones[source_bone].keys()}:
            # print(f'{key} already in {source_bone} Custom Properties')
            continue
        else:
            ultimate_dict[key] = buffer_dict[key]

    return ultimate_dict


def make_dict_pairs(nameprop: str, default: str | float | int | bool, source_bone: str, suffix: str | None = None,) -> dict:
    """If suffix is given returns a pair of prop L, R or top,bot or returns a single value if suffix is not given."""
    
    assert is_bone(source_bone), f"{source_bone} not in current Armature."
    
    full_name = is_suffix_in_custom_prop(
        prop_name=nameprop, suffix_side=suffix)
    dict_customprop = {}

    if isinstance(full_name, tuple):
        for name in full_name:
            dict_customprop[name] = dict(item=bpy.context.active_object.pose.bones[source_bone], prop=name, default=default)
        return dict_customprop

    dict_customprop[full_name] = dict(item=bpy.context.active_object.pose.bones[source_bone], prop=full_name, default=default)
    return dict_customprop


def is_suffix_in_custom_prop(prop_name: str, suffix_side: str | None):
    """Return name plus suffix if it has some."""

    if suffix_side == None:
        return prop_name

    elif suffix_side == ".L":
        left_side = f"{prop_name}{suffix_side}"
        right_side = f"{prop_name}.R"
        return left_side, right_side

    elif suffix_side == ".top":
        top_side = f"{prop_name}{suffix_side}"
        bot_side = f"{prop_name}.bot"
        return top_side, bot_side

    elif suffix_side == ".C":
        return f"{prop_name}{suffix_side}"


def is_bone(bone_name: str) -> bool:
    """Check if bone exists in armature object."""
    if bone_name in set(bone.name for bone in bpy.context.active_object.data.bones):
        return bone_name


class CustomPropertiesAccess():
    ''' Sets instances of properties for bone custom properties. '''
    def __init__(
            self,
            prop_name: str,
            source_bone: str,
            default: str | float | int | bool,
            suffix: str | None = None,) -> None:

        self.prop_name = prop_name
        self.source_bone = source_bone
        self.default = default
        self.suffix = suffix

    def __str__(self) -> None:
        return f"{self.prop_name}, {self.source_bone}, {self.default}, {self.suffix}"


class AC_OT_add_CustomProp(Operator):
    """Operator to set Custom Properties in a given source bone."""

    bl_idname = "ac.set_bone_custom_properties"
    bl_label = "Bone Custom Property Settings"
    bl_options = {"REGISTER", "PRESET"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            context.active_object.type == "ARMATURE" and context.area.type == "VIEW_3D"
        )

    def execute(self, context):
        main()
        return {"FINISHED"}
