from bpy.types import Context, Operator
from bpy import ops


def stretchto_bconstraint(bone, subtarget: object, space: str, context: Context):
    """Adds a Stretch to Constraint"""
    bconstraint = bone.constraints.new("STRETCH_TO")
    bconstraint.target = context.active_object
    bconstraint.subtarget = subtarget
    bconstraint.target_space = space
    bconstraint.owner_space = space
    bconstraint.influence = 1.0
    return {"FINISHED"}


def bone_properties(context: Context):
    """Set Properties for bones in Pose Mode"""
    for bone in context.active_object.pose.bones.values():
        bone.rotation_mode = "XYZ"
        bone.bbone_easein = 1
        bone.bbone_easeout = 1
    return {"FINISHED"}


def create_bones(
    bone: object,
    bone_name: str,
    bone_head: tuple,
    bbone_size: float,
    length: float,
    context: Context,
):
    new_bone: str = context.object.data.edit_bones.new(
        bone_name
    )  # To Create a new bone it needs a name as parameter.
    new_bone.head = bone_head
    # new_bone.head = ((bone.vector * 0.5) + bone.head) #places bone in the middle.
    new_bone.tail = (bone.vector) + bone.tail
    new_bone.length = length
    new_bone.roll = bone.roll
    new_bone.bbone_x = bbone_size
    new_bone.bbone_z = new_bone.bbone_x
    new_bone.use_deform = False


def bbones_properties(bone: object, bone_name: str, context: Context):
    """Adds custom bones as start/end handles for bbones."""
    edit_bones = context.active_object.data.edit_bones
    bone.bbone_easein = 0.0
    bone.bbone_easeout = 0.0
    bone.bbone_handle_type_start = "TANGENT"
    bone.bbone_handle_type_end = "TANGENT"
    # bone_handle = f'{bone.name}_strHandle' if edit_bones.get(f'{bone.name}_strHandle') else f'{bone.name}_endHandle'
    if edit_bones.get(f"CTRL-{bone.name}"):
        edit_bones[bone_name].parent = edit_bones[f"CTRL-{bone.name}"]
    else:
        edit_bones[bone_name].parent = edit_bones[bone.name].parent.parent

    if bone_name.endswith("strHandle"):
        bone.bbone_custom_handle_start = edit_bones[bone_name]
        bone.parent = edit_bones[bone_name]
        return {"FINISHED"}

    elif bone_name.endswith("endHandle"):
        bone.bbone_custom_handle_end = edit_bones[bone_name]
        return {"FINISHED"}


class AC_OT_NewBBones(Operator):
    """Adding BBones Handles"""

    bl_idname = "rigtoolkit.create_single_bbone"
    bl_label = "Create Single Bbone Chain"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if hasattr(context.active_object, "type") and context.mode == "EDIT_ARMATURE":
            return context.active_object.type == "ARMATURE"
        return False

    def execute(self, context):
        if not context.mode == "EDIT":
            ops.object.mode_set(mode="EDIT")

        if not context.selected_editable_bones:
            self.report({"ERROR"}, f"No Bones selected")
            return {"CANCELLED"}

        for bone in context.selected_editable_bones:
            str_handle = f"{bone.name}_strHandle"
            end_handle = f"{bone.name}_endHandle"
            ctrl_bone = f"CTRL-{bone.name}"

            if bone.parent and bone.use_connect:
                bone.bbone_custom_handle_start = bone.parent.bbone_custom_handle_end
                bone.parent = bone.parent.bbone_custom_handle_end

                create_bones(
                    bone,
                    bone_name=end_handle,
                    bone_head=bone.tail,
                    bbone_size=0.17,
                    length=0.25,
                    context=context,
                )
                bbones_properties(bone=bone, bone_name=end_handle, context=context)
                
            else:
                create_bones(
                    bone,
                    bone_name=ctrl_bone,
                    bone_head=bone.head,
                    bbone_size=0.25,
                    length=0.16,
                    context=context,
                )

                create_bones(
                    bone,
                    bone_name=str_handle,
                    bone_head=bone.head,
                    bbone_size=0.17,
                    length=0.25,
                    context=context,
                )
                bbones_properties(bone=bone, bone_name=str_handle, context=context)

                create_bones(
                    bone,
                    bone_name=end_handle,
                    bone_head=bone.tail,
                    bbone_size=0.17,
                    length=0.25,
                    context=context,
                )
                bbones_properties(bone=bone, bone_name=end_handle, context=context)

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")

        bone_properties(context=context)

        for bone in context.selected_pose_bones:
            stretchto_bconstraint(
                bone=bone,
                subtarget=f"{bone.name}_endHandle",
                space="WORLD",
                context=context,
            )

        self.report({"INFO"}, f"BBones handles added")
        return {"FINISHED"}
