from bpy.types import Context, Operator
from bpy import ops
from . import set_bone
from . import set_bcontraints

class AC_OT_SingleControl(Operator):
    """Adding BBones Handles"""

    bl_idname = "rigtoolkit.create_single_control"
    bl_label = "Add a single control to selected bones."
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
        #----------------------Operation----------------
        for bone in context.selected_editable_bones:
            ctrl_bone = set_bone.create(
                    bone,
                    bone_type='CTRL',
                    bone_head=bone.head,
                    bbone_size=0.18,
                    length=0.15,
                    context=context,
                )
            set_bone.parenting(bone, ctrl_bone, context)

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")
                    

        for bone in context.active_object.pose.bones.values():
            set_bone.pbone_properties(bone=bone)
        self.report({"INFO"}, f"Control added")
        return {"FINISHED"}
    

class AC_OT_SingleControlConstraint(Operator):
    """Adding BBones Handles"""

    bl_idname = "rigtoolkit.create_single_control_constraint"
    bl_label = "Add a single control to selected bones with Copy Transform constraint."
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
            if bone.parent and bone.use_connect:
                self.report({"ERROR"}, f"{bone.name} is connected")
                return {"CANCELLED"}

        #----------------------Operation----------------
        for bone in context.selected_editable_bones:
            ctrl_bone = set_bone.create(
                    bone,
                    bone_type='CTRL',
                    bone_head=bone.head,
                    bbone_size=0.18,
                    length=0.15,
                    context=context,
                )

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")
                    

        for bone in context.active_object.pose.bones.values():
            set_bone.pbone_properties(bone=bone)

        #Add Constraints
        for bone in context.selected_pose_bones:
            ctrlbone = f'CTRL-{bone.name}' if 'DEF' not in bone.name else bone.name.replace('DEF', 'CTRL')

            set_bcontraints.copytransform_bconstraint(
                bone,
                subtarget=ctrlbone,
                space="WORLD",
                context=context,
            )
        self.report({"INFO"}, f"Control Copy Transform added")
        return {"FINISHED"}

