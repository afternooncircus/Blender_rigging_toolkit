from bpy.types import Context, Operator
import rna_prop_ui


def all_custom_properties() -> dict:
    """Stores all the custom properties that would get call."""

    # ---------- Custom Property Settings ----------
    mouth_zipper = CustomPropertiesAccess(
        prop_name="mouth-zipper", source_bone="Properties", default=1.0
    )
    teeth_follow_rot = CustomPropertiesAccess(
        prop_name="teeth-follow_rot", source_bone="Properties", default=1.0
    )
    eyes_sticky_eyelips = CustomPropertiesAccess(
        prop_name="eyes-sticky_eyelips", source_bone="Properties", default=1.0
    )
    foot_roll = CustomPropertiesAccess(
        prop_name="Foot Roll", source_bone="Properties", default=1.0, suffix=".L"
    )
    arm_fk_hinge = CustomPropertiesAccess(
        prop_name="arm-FK_hinge", source_bone="Properties", default=1.0, suffix=".R"
    )
    leg_fk_hinge = CustomPropertiesAccess(
        prop_name="leg-FK_hinge", source_bone="Properties", default=1.0, suffix=".L"
    )
    arm_ik_pole_follow = CustomPropertiesAccess(
        prop_name="arm-IK_pole_follow",
        source_bone="Properties",
        default=1.0,
        suffix=".L",
    )
    leg_ik_pole_follow = CustomPropertiesAccess(
        prop_name="leg-IK_pole_follow",
        source_bone="Properties",
        default=1.0,
        suffix=".L",
    )
    arm_ik_stretch = CustomPropertiesAccess(
        prop_name="arm-IK_stretch", source_bone="Properties", default=1.0, suffix=".L"
    )
    leg_ik_stretch = CustomPropertiesAccess(
        prop_name="leg-IK_stretch", source_bone="Properties", default=1.0, suffix=".L"
    )
    arm_ik_fk_switch = CustomPropertiesAccess(
        prop_name="arm-IK|FK", source_bone="Properties", default=1.0, suffix=".L"
    )
    leg_ik_fk_switch = CustomPropertiesAccess(
        prop_name="leg-IK|FK", source_bone="Properties", default=1.0, suffix=".L"
    )
    arm_rubber_hose = CustomPropertiesAccess(
        prop_name="arm-rubber_hose", source_bone="Properties", default=1.0, suffix=".L"
    )
    leg_rubber_hose = CustomPropertiesAccess(
        prop_name="leg-rubber_hose", source_bone="Properties", default=1.0, suffix=".L"
    )

    # ---------- Character Settings ----------
    arm_mask = CustomPropertiesAccess(
        prop_name="arm-mask", source_bone="Properties", default=False, suffix=".L"
    )
    leg_mask = CustomPropertiesAccess(
        prop_name="leg-mask", source_bone="Properties", default=False, suffix=".L"
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
    for custom_property in all_custom_props:
        proper_dict = make_dict_pairs(
            nameprop=custom_property.prop_name,
            default=custom_property.default,
            source_bone=custom_property.source_bone,
            suffix=custom_property.suffix,
            context=context,
        )
        ultimate_dict = buffer_custom_prop(
            custom_property.source_bone, proper_dict, context
        )

        for key in ultimate_dict:
            rna_prop_ui.rna_idprop_ui_create(overridable=True, **ultimate_dict[key])

    return {"FINISHED"}


def buffer_custom_prop(source_bone: str, buffer_dict: dict, context: Context) -> dict:
    """Return dict with custom properties that do not exist in source bone."""

    ultimate_dict = {}
    for key in buffer_dict:
        if key in {_ for _ in context.active_object.pose.bones[source_bone].keys()}:
            # print(f'{key} already in {source_bone} Custom Properties')
            continue
        else:
            ultimate_dict[key] = buffer_dict[key]

    return ultimate_dict


def make_dict_pairs(
    nameprop: str,
    default: str | float | int | bool,
    source_bone: str,
    context: Context,
    suffix: str | None = None,
) -> dict:
    """If suffix is given returns a pair of prop L, R or top,bot or returns a single value if suffix is not given."""

    assert is_bone(
        source_bone, context
    ), f"'{source_bone}' bone not in active Armature."

    full_name = is_suffix_in_custom_prop(prop_name=nameprop, suffix_side=suffix)
    dict_customprop = {}

    if isinstance(full_name, tuple):
        for name in full_name:
            dict_customprop[name] = dict(
                item=context.active_object.pose.bones[source_bone],
                prop=name,
                default=default,
            )
        return dict_customprop

    dict_customprop[full_name] = dict(
        item=context.active_object.pose.bones[source_bone],
        prop=full_name,
        default=default,
    )
    return dict_customprop


def is_suffix_in_custom_prop(prop_name: str, suffix_side: str | None):
    """Return custom property name.suffix if it has some."""

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


def is_bone(bone_name: str, context: Context) -> bool:
    """Check if bone exists in armature object."""
    if bone_name in set(bone.name for bone in context.active_object.data.bones):
        return bone_name


class CustomPropertiesAccess:
    """Sets instances of properties for bone custom properties."""

    def __init__(
        self,
        prop_name: str,
        source_bone: str,
        default: str | float | int | bool,
        suffix: str | None = None,
    ) -> None:

        self.prop_name = prop_name
        self.source_bone = source_bone
        self.default = default
        self.suffix = suffix
        self.__source_bone = "Properties"

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


class AC_OT_add_CustomProp(Operator):
    """Operator to set Custom Properties in a given source bone."""

    bl_idname = "rigtoolkit.set_bone_custom_properties"
    bl_label = "Bone Custom Property Settings"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            context.active_object.type == "ARMATURE"
            and context.mode == "POSE"
            and context.area.type == "VIEW_3D"
        )

    def execute(self, context):
        properties_to_ui(all_custom_properties(), context)

        self.report({"INFO"}, f"Custom Properties added in 'Properties' bone")
        return {"FINISHED"}
