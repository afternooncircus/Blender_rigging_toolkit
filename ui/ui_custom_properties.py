from bpy.types import Context, Panel, UILayout


def is_armature(context: Context) -> bool:
    if hasattr(context.active_object, "type"):
        return context.active_object.type == "ARMATURE"
    return False


def is_bone(bone_name: str, context: Context) -> bool:
    return bone_name in set(bone.name for bone in context.active_object.data.bones)


def is_custom_property(property_name: str, source_bone: str, context: Context) -> bool:
    return property_name in {
        _ for _ in context.active_object.pose.bones[source_bone].keys()
    }


class ArmaturePanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rigging Toolkit"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return is_armature(context)


class VIEW3D_PT_ArmatureNameUI(ArmaturePanel, Panel):
    bl_label = "Armature Name"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text=f"{context.active_object.name}", icon="ARMATURE_DATA")


class VIEW3D_PT_BonePropertiesUI(ArmaturePanel, Panel):
    """
    Draw UI for all the properties in bone named 'Properties'.
    """

    bl_label = "UI Custom Properties"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and is_bone("Properties", context)

    def draw(self, context: Context):
        custom_prop_bone: str = "Properties"

        self.layout.label(text="Arm Switch")
        custom_prop: str = "L_arm_IK_FK_switch"
        if is_custom_property(custom_prop, custom_prop_bone, context):
            col = self.layout.split()
            col.prop(
                context.active_object.pose.bones[custom_prop_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=f"{custom_prop}".replace("_", " "),
            )
        custom_prop: str = "R_arm_IK_FK_switch"
        if is_custom_property(custom_prop, custom_prop_bone, context):
            col.prop(
                context.active_object.pose.bones[custom_prop_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=f"{custom_prop}".replace("_", " "),
            )

        self.layout.label(text="Leg Switch")
        custom_prop: str = "L_leg_IK_FK_switch"
        if is_custom_property(custom_prop, custom_prop_bone, context):
            col = self.layout.split()
            col.prop(
                context.active_object.pose.bones[custom_prop_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=f"{custom_prop}".replace("_", " "),
            )
        custom_prop: str = "R_leg_IK_FK_switch"
        if is_custom_property(custom_prop, custom_prop_bone, context):
            col.prop(
                context.active_object.pose.bones[custom_prop_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=f"{custom_prop}".replace("_", " "),
            )
