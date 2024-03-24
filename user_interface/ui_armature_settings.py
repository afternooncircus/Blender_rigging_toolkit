from bpy.types import Context, Panel
import bpy

class MainAccessArmatureSetting(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context: Context):
        return context.armature


class DATA_PT_ArmatureSettings(MainAccessArmatureSetting, Panel):
    bl_label = "Rigging Toolkit"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "DATA_PT_ArmatureSettings"

    def draw(self, context: Context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(
            "rigtoolkit.set_armature_properties",
            text="Apply Armature Settings",
            icon="WORLD",
        )
        col.operator(
            "rigtoolkit.set_bone_custom_properties",
            text="Custom Bone Settings",
        )
        col.operator(
            "rigtoolkit.create_single_bbone",
            text="Single Bbone Chain",
        )
        col.operator(
            "rigtoolkit.create_single_control",
            text="Single Control",
        )
        col.operator(
            "rigtoolkit.create_single_control_constraint",
            text="Single Control Copy Constraint",
        )
        col.operator(
            "rigtoolkit.parenting_to_bones",
            text="Parent Cubes to bones",
        )
        col.operator(
            "rigtoolkit.create_torso_chain",
            text="Torso Chain",
        )

