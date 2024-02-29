from bpy.types import Context, Operator
from bpy.props import StringProperty
import rna_prop_ui
import bpy

def all_custom_properties(bone_properties: str) -> dict:
    """Stores all the custom properties that would get call.

    :return: return a dictionary with all custom properties.
    :rtype: dict
    """
    # ---------- Custom Property Settings ----------
    mouth_zipper = CustomPropertiesAccess(
        prop_name="mouth-zipper", source_bone=bone_properties, default=1.0, max_value=5.0
    )
    teeth_follow_rot = CustomPropertiesAccess(
        prop_name="teeth-follow_rot", source_bone=bone_properties, default=1.0
    )
    eyes_sticky_eyelips = CustomPropertiesAccess(
        prop_name="eyes-sticky_eyelips", source_bone=bone_properties, default=1.0
    )
    foot_roll = CustomPropertiesAccess(
        prop_name="Foot Roll", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    arm_fk_hinge = CustomPropertiesAccess(
        prop_name="arm-FK_hinge", source_bone=bone_properties, default=1.0, suffix=".R"
    )
    leg_fk_hinge = CustomPropertiesAccess(
        prop_name="leg-FK_hinge", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    arm_ik_pole_follow = CustomPropertiesAccess(
        prop_name="arm-IK_pole_follow",
        source_bone=bone_properties,
        default=1.0,
        suffix=".L",
    )
    leg_ik_pole_follow = CustomPropertiesAccess(
        prop_name="leg-IK_pole_follow",
        source_bone=bone_properties,
        default=1.0,
        suffix=".L",
    )
    arm_ik_stretch = CustomPropertiesAccess(
        prop_name="arm-IK_stretch", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    leg_ik_stretch = CustomPropertiesAccess(
        prop_name="leg-IK_stretch", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    arm_ik_fk_switch = CustomPropertiesAccess(
        prop_name="arm-IK|FK", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    leg_ik_fk_switch = CustomPropertiesAccess(
        prop_name="leg-IK|FK", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    arm_rubber_hose = CustomPropertiesAccess(
        prop_name="arm-rubber_hose", source_bone=bone_properties, default=1.0, suffix=".L"
    )
    leg_rubber_hose = CustomPropertiesAccess(
        prop_name="leg-rubber_hose", source_bone=bone_properties, default=1.0, suffix=".L"
    )

    # ---------- Character Settings ----------
    arm_mask = CustomPropertiesAccess(
        prop_name="arm-mask", source_bone=bone_properties, default=False, suffix=".L"
    )
    leg_mask = CustomPropertiesAccess(
        prop_name="leg-mask", source_bone=bone_properties, default=False, suffix=".L"
    )

    all_props = {
        foot_roll,
        arm_fk_hinge,
        leg_fk_hinge,
        arm_ik_pole_follow,
        arm_ik_pole_follow,
        leg_ik_pole_follow,
        arm_ik_stretch,
        leg_ik_stretch,
        arm_ik_fk_switch,
        leg_ik_fk_switch,
        arm_rubber_hose,
        leg_rubber_hose,
        arm_mask,
        leg_mask,
        mouth_zipper,
        teeth_follow_rot,
        eyes_sticky_eyelips,
    }

    return all_props


def properties_to_ui(all_custom_props: set, context: Context) -> None:
    """Takes the dictionary of custom properties and creates them in the 'Properties' bone custom properties panel.

    :param all_custom_props: A set of dictionary of custom properties.
    :type all_custom_props: set
    :param context: context.active_object
    :type context: Context
    :return: None
    :rtype: None
    """
    for custom_property in all_custom_props:
        proper_dict = make_dict_pairs(
            nameprop=custom_property.prop_name,
            default=custom_property.default,
            source_bone=custom_property.source_bone,
            suffix=custom_property.suffix,
            context=context,
            min_value=custom_property.min,
            max_value=custom_property.max,
        )

        if proper_dict:
            for key in proper_dict:
                rna_prop_ui.rna_idprop_ui_create(overridable=True, **proper_dict[key])

    return {"FINISHED"}

def make_dict_pairs(
    nameprop: str,
    default: str | float | int | bool,
    source_bone: str,
    context: Context,
    min_value: float | int,
    max_value: float | int,
    suffix: str | None = None,
) -> dict:
    """Return a dictionary with custom properties. If suffix paramater is given returns a pair of prop L, R or top, bot.

    :param nameprop: name of the custom property
    :type nameprop: str
    :param default: type of custom property
    :type default: str | float | int | bool
    :param source_bone: bone in which custom property are stored
    :type source_bone: str
    :param context: context.active_object
    :type context: Context
    :param suffix: '.L', '.R', '.C', '.top', '.bot', defaults to None
    :type suffix: str | None, optional
    :return: dictionary with custom properties
    :rtype: dict
    """    

    # Might not be neccessary, but keep it for now.
    # assert is_bone(source_bone, context), f"'{source_bone}' bone not in active Armature." 

    full_name = is_suffix_in_custom_prop(prop_name=nameprop, suffix_side=suffix)
    dict_customprop = {}

    if isinstance(full_name, tuple):
        for name in full_name:
            if name in context.active_object.pose.bones[source_bone].keys():
                continue
            dict_customprop[name] = dict(
                item=context.active_object.pose.bones[source_bone],
                prop=name,
                default=default,
                min=min_value,
                max=max_value,
            )
        return dict_customprop
    
    elif full_name in context.active_object.pose.bones[source_bone].keys():
        return
    
    dict_customprop[full_name] = dict(
        item=context.active_object.pose.bones[source_bone],
        prop=full_name,
        default=default,
        min=min_value,
        max=max_value,
    )
    return dict_customprop


def is_suffix_in_custom_prop(prop_name: str, suffix_side: str | None) -> str:
    """Return custom property with a suffix in the if it is given.

    :param prop_name: name of property
    :type prop_name: str
    :param suffix_side: suffix can be '.L', '.R', '.C', '.top', '.bot'
    :type suffix_side: str | None
    :return: name of property + suffix side
    :rtype: str
    """    

    if suffix_side == None:
        return prop_name

    elif suffix_side == ".L" or suffix_side == ".R":
        opposite_side = ".R" if suffix_side == ".L" else ".L"
        original_side = f"{prop_name}{suffix_side}"
        opposite_side = f"{prop_name}{opposite_side}"
        return original_side, opposite_side

    elif suffix_side == ".top" or suffix_side == "bot":
        opposite_side = ".bot" if suffix_side == ".top" else ".bot"
        original_side = f"{prop_name}{suffix_side}"
        opposite_side = f"{prop_name}{opposite_side}"
        return original_side, opposite_side

    elif suffix_side == ".C":
        return f"{prop_name}{suffix_side}"

class CustomPropertiesAccess:
    """Sets instances of properties for bone custom properties. 
    """    

    def __init__(
        self,
        prop_name: str,
        source_bone: str,
        default: str | float | int | bool,
        suffix: str | None = None,
        min_value: float | int = 0.0,
        max_value: float | int = 1.0,
    ) -> None:

        self.prop_name = prop_name
        self.source_bone = source_bone
        self.default = default
        self.suffix = suffix
        self.min = min_value
        self.max = max_value
        
    def __str__(self) -> None:
        return f"Property Name: {self.prop_name}, Source Bone: {self.source_bone}, Default: {self.default}, Suffix: {self.suffix}"

    @property
    def prop_name(self):
        return self._prop_name

    @prop_name.setter
    def prop_name(self, prop_name):
        if not isinstance(prop_name, str) or not prop_name:
            raise ValueError(
                f"Property Name: '{prop_name}' was not given or valid. Expects 'str' type not {type(prop_name)}"
            )
        self._prop_name = prop_name

    @property
    def source_bone(self):
        return self._source_bone

    @source_bone.setter
    def source_bone(self, source_bone):
        if not isinstance(source_bone, str) or not source_bone:
            raise ValueError(
                f"Source bone Paramater: '{source_bone}' was not given or valid. Expects 'str' type, not {type(source_bone)}"
            )
        self._source_bone = source_bone

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default):
        if default == None:
            raise ValueError(
                f"Default Paramater: '{default}' was not given or valid. Expected 'str', 'int', 'float', or 'bool' types, not {type(default)}"
            )
        self._default = default

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        if isinstance(min_value, float) or isinstance(min_value, int):
            raise ValueError(
                f"Default Paramater: '{min_value}' was not given or valid. Expected 'int', 'float', types, not {type(min_value)}"
            )
        self._default = min_value

    @property
    def max_value(self):
        return self._max_value

    @min_value.setter
    def max_value(self, max_value):
        if isinstance(max_value, float) or isinstance(max_value, int):
            raise ValueError(
                f"Default Paramater: '{max_value}' was not given or valid. Expected 'int', 'float', types, not {type(max_value)}"
            )
        self._default = max_value

class AC_OT_add_CustomProp(Operator):
    """Operator to set Custom Properties in a given source bone """

    bl_idname = "rigtoolkit.set_bone_custom_properties"
    bl_label = "Bone Custom Property Settings"
    bl_options = {"REGISTER"}

    source_bone_name: StringProperty(
        name='Properties',
        description='Bone name in which custom properties will be stored.',
        default='Properties',
    ) # type: ignore

    

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            context.active_object.type == "ARMATURE"
            # and context.mode == "POSE"
            # and context.area.type == "VIEW_3D"
        )

    def execute(self, context):
        source_bone_properties = "Properties"

        if not source_bone_properties in {bone.name for bone in context.active_object.data.bones}:
            self.report({"ERROR"}, f"There is no bone named '{source_bone_properties}'")
            return {"CANCELLED"}
        
        properties_to_ui(all_custom_properties(source_bone_properties), context)

        self.report({"INFO"}, f"Custom Properties added in '{source_bone_properties}' bone")
        return {"FINISHED"}
