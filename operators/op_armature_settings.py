from bpy.types import Context, Operator
from bpy import ops


def set_object_data(armature: str, context: Context):
    """Sets object data, it returns armature name"""

    if not context.mode == "EDIT":
        ops.object.mode_set(mode="EDIT")

    # Armature name.
    armature.name = armature.name.strip()

    # Visibility Settings.
    armature.hide_select = False
    armature.hide_viewport = False
    armature.hide_render = True

    # Viewport Display settings.
    armature.show_name = False
    armature.show_axis = False
    armature.show_in_front = True
    armature.display_type = "SOLID"
    return {"FINISHED"}


def set_armature_data(armature: str, context: Context):
    """It sets viewport display data for armatures object."""

    if not context.mode == "POSE":
        ops.object.mode_set(mode="POSE")

    # Copy object name into data name.
    armature.data.name = armature.name.lower().strip().replace(" ", "_")

    # Viewport Display data settings.
    armature.data.display_type = "BBONE"
    armature.data.show_names = False
    armature.data.show_bone_custom_shapes = True
    armature.data.show_bone_colors = True
    armature.data.show_axes = False
    armature.data.axes_position = 0
    armature.data.relation_line_position = "TAIL"

    return {"FINISHED"}


class AC_OT_Set_ArmatureProp(Operator):
    """Setting properties and naming convention for active Armature object"""

    bl_idname = "rigtoolkit.set_armature_properties"
    bl_label = "Armature Property Settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.active_object.type == "ARMATURE"
        # return context.active_object.type == "ARMATURE" and context.area.type == 'VIEW_3D'

    def execute(self, context):

        armature_object: str = context.active_object
        set_object_data(armature_object, context)
        set_armature_data(armature_object, context)

        self.report({"INFO"}, f"Armature Settings Apply")
        return {"FINISHED"}
