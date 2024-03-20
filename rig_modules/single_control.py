from bpy.types import Context, Operator
from bpy import ops
from . import set_bone
from . import set_bcontraints

class AC_OT_SingleControl(Operator):
    """Adding CTRL Bones to selected bones."""

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
            set_bone.bone_prop(bone)
            set_bone.parenting(bone, ctrl_bone, context)
            set_bone.collection(bone=ctrl_bone, colname='CTRL',context=context)    

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")
                    

        CTRLwidget = set_bone.widget(widget_name='WGT-CTRL', context=context)
        
        for bone in context.active_object.pose.bones.values():
            if bone.name.startswith('CTRL'):
                set_bone.assign_widget(bone=bone, shape=CTRLwidget)
            set_bone.pbone_properties(bone=bone)
        
        self.report({"INFO"}, f"Control added")
        return {"FINISHED"}
    

class AC_OT_SingleControlConstraint(Operator):
    """Adding a CTRL Bone with Copy Transform to selected bones. Use it when bone hierarchy is needed."""

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
            
            set_bone.collection(bone=ctrl_bone, colname='CTRL',context=context)    

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")
                    
        CTRLwidget = set_bone.widget(widget_name='WGT-CTRL', context=context)
        
        for bone in context.active_object.pose.bones.values():
            if bone.name.startswith('CTRL'):
                set_bone.assign_widget(bone=bone, shape=CTRLwidget)
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

