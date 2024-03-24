from bpy.types import Context, Operator
from bpy import ops
from . import set_bone
from . import set_bcontraints


class AC_OT_NewBBones(Operator):
    """Adding BBones Handles and a FK chain to selected bones."""

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
            if bone.parent and not bone.use_connect:
                self.report({"ERROR"}, f"{bone.name} is not connected")
                return {"CANCELLED"}
            
        #----------------------Operation----------------
        
        #sorting bone chain by hierarchy.
        bone_chain = set_bone.sorting(bone_chain= context.selected_editable_bones)
        
        if not bone_chain:
            self.report({"ERROR"}, f"All Bones are parented, unparent root of the chain.")
            return {"CANCELLED"}
        
        # Creating bones.
        fk_parents: list = []
        bhandles: list = []
        for bone in bone_chain:
            if bone.parent and bone.use_connect:
                bone.bbone_custom_handle_start = bone.parent.bbone_custom_handle_end

                handle_bone = set_bone.create(
                    bone,
                    bone_type='endHandle',
                    bone_head=bone.tail,
                    bbone_size=0.28,
                    length=0.25,
                    context=context,
                )

                fk_bone = set_bone.create(
                    bone,
                    bone_type='FK',
                    bone_head=bone.head,
                    bbone_size=0.38,
                    length=0.15,
                    context=context,
                )
                
                set_bone.parenting(bone=fk_bone, parentbone=fk_parents[-1], context=context)
                fk_parents.append(fk_bone)
                set_bone.parenting(bone=bhandles[-1], parentbone=fk_parents[-1], context=context)
                bhandles.append(handle_bone)

            else:
                str_bone = set_bone.create(
                    bone,
                    bone_type='strHandle',
                    bone_head=bone.head,
                    bbone_size=0.28,
                    length=0.25,
                    context=context,
                )

                end_bone = set_bone.create(
                    bone,
                    bone_type='endHandle',
                    bone_head=bone.tail,
                    bbone_size=0.28,
                    length=0.25,
                    context=context,
                )

                fk_bone = set_bone.create(
                    bone,
                    bone_type='FK',
                    bone_head=bone.head,
                    bbone_size=0.38,
                    length=0.15,
                    context=context,
                    bone_name='CTRL-Bot'
                )
                
                bhandles.append(str_bone)
                bhandles.append(end_bone)
                fk_parents.append(fk_bone)
                set_bone.parenting(bone=bhandles[0], parentbone=fk_parents[-1], context=context)

            #Adding bone handles.
            for handlbone in bhandles:
                set_bone.bbone_handles(bone, bhandle=handlbone, context=context)
            
            #Setting Properties. 
            set_bone.bbones_prop(bone)
            set_bone.bone_prop(bone)
        
        #Add Top Control to FK Chain.
        if not bhandles[-1].parent:
            fk_bone = set_bone.create(
                bone,
                bone_type='CTRL',
                bone_head=bone.tail,
                bbone_size=0.38,
                length=0.15,
                context=context,
                bone_name='CTRL-Top'
            )

            #Set Parent to previous FK bone in the Chain
            set_bone.parenting(bone=fk_bone, parentbone=fk_parents[-1], context=context)
            #Adds to the list of FK bone Chain.
            fk_parents.append(fk_bone)
            #Parent last handle bone to last FK bone.
            set_bone.parenting(bone=bhandles[-1], parentbone=fk_parents[-1], context=context)

        #Settings collections.
        for handbone in bhandles:
            set_bone.collection(bone=handbone, colname='BB Handles',context=context)    

        for fkbone in fk_parents:
            set_bone.collection(bone=fkbone, colname='FK',context=context)    

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")

        #Applying widgets.
        CTRLwidget = set_bone.widget(widget_name='WGT-CTRL', context=context)            
        FKwidget = set_bone.widget(widget_name='WGT-FK', context=context)
        HANDLEwidget = set_bone.widget(widget_name='WGT-fullsphere', context=context)
        
        for bone in context.active_object.pose.bones.values():
            if bone.name.startswith('CTRL'):
                set_bone.assign_widget(bone=bone, shape=CTRLwidget)
            elif bone.name.startswith('FK'):
                set_bone.assign_widget(bone=bone, shape=FKwidget)
            elif bone.name.startswith('strHandle') or bone.name.startswith('endHandle'):
                set_bone.assign_widget(bone=bone, shape=HANDLEwidget)

            #Setting bone properties in pose mode.
            set_bone.pbone_properties(bone=bone)

        for bone in context.selected_pose_bones:
            #Set Properties in Pose Mode
            #   set_bone.pbone_properties(bone=bone)

            #Add Constraints
            strhandl = f'strHandle-{bone.name}' if 'DEF' not in bone.name else bone.name.replace('DEF', 'strHandle')
            endhandl = f'endHandle-{bone.name}' if 'DEF' not in bone.name else bone.name.replace('DEF', 'endHandle')
            if not bone.parent:
                set_bcontraints.copyloc_bconstraint(
                bone,
                subtarget= strhandl,
                space="WORLD",
                context=context,
                )
                
            set_bcontraints.stretchto_bconstraint(
                bone,
                subtarget=endhandl,
                space="WORLD",
                context=context,
            )
        self.report({"INFO"}, f"BBones handles added")
        return {"FINISHED"}
