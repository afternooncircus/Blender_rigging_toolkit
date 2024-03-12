from bpy.types import Context, Operator
from bpy import ops

def stretchto_bconstraint(bone, subtarget: object, space: str, context: Context):
    bconstraint = bone.constraints.new('STRETCH_TO')
    bconstraint.target = context.active_object
    bconstraint.subtarget = subtarget
    bconstraint.target_space = space
    bconstraint.owner_space = space
    bconstraint.influence = 1.0
    return {'FINISHED'}

def bone_properties(context:Context):
    for bone in context.active_object.pose.bones.values():
        bone.rotation_mode = 'XYZ'
        bone.bbone_easein = 1
        bone.bbone_easeout = 1
    return {'FINISHED'}


class AC_OT_NewBBones(Operator):
    """Adding Bbones Handles"""

    bl_idname = "rigtoolkit.create_single_bbone"
    bl_label = "Create Single Bbone Chain"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if hasattr(context.active_object, "type") and context.mode == "EDIT_ARMATURE":
            return context.active_object.type == "ARMATURE"
        return False
    
    @staticmethod
    def deselect_nonbbones(context: Context):
        for bone in context.selected_editable_bones:
            if bone.bbone_segments < 2:
                bone.select = False
        return {'FINISHED'}

    def bbone_handles(self, bone: object, bone_name: str, bone_head: tuple, context: Context):
        new_bone: str = context.object.data.edit_bones.new(bone_name) #To Create a new bone it needs a name as parameter.
        new_bone.head = bone_head
        # new_bone.head = ((bone.vector * 0.5) + bone.head) #places bone in the middle.    
        new_bone.tail = ((bone.vector) + bone.tail)
        new_bone.length = 0.25 #length Float
        new_bone.roll = bone.roll
        new_bone.bbone_x = 0.17
        new_bone.bbone_z = new_bone.bbone_x

        new_bone.use_deform = False

        bone.bbone_easein = 0.0
        bone.bbone_easeout = 0.0
        bone.bbone_handle_type_start = 'TANGENT'
        bone.bbone_handle_type_end = 'TANGENT'
        if new_bone.name.endswith('strHandle'):
            bone.bbone_custom_handle_start = new_bone
            bone.parent = new_bone
            return {'FINISHED'}
        
        elif new_bone.name.endswith('endHandle'):
            bone.bbone_custom_handle_end = new_bone
            return {'FINISHED'}

    def execute(self, context):
        if not context.mode == "EDIT":
            ops.object.mode_set(mode="EDIT")

        # self.deselect_nonbbones(context)
        
        if not context.selected_editable_bones:
            self.report({"ERROR"}, f"No BBones selected, add BBone segments")  
            return {"CANCELLED"}
         
        for bone in context.selected_editable_bones[:]:
            self.bbone_handles(bone, bone_name=f'{bone.name}_strHandle', bone_head=bone.head, context=context)
            self.bbone_handles(bone, bone_name=f'{bone.name}_endHandle', bone_head=bone.tail, context=context)
        
        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")

        bone_properties(context=context)
        
        for bone in context.selected_pose_bones:
            stretchto_bconstraint(bone=bone, subtarget=f'{bone.name}_endHandle', space='WORLD', context=context)


        self.report({"INFO"}, f"BBones handles added")
        return {"FINISHED"} 
