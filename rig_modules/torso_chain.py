from bpy.types import Context, Operator
from bpy import ops
from . import set_bone
from . import set_bcontraints

class AC_OT_TorsoChain(Operator):
    """Adding Torso Chain."""

    bl_idname = "rigtoolkit.create_torso_chain"
    bl_label = "Adding Torso Chain."
    bl_options = {"REGISTER", "UNDO"}

    #------- Parameters ------- 
    tweakcol = 'Tweak Torso'
    ctrlcol = 'Control Torso'
    fkcol = 'FK Torso'
    mchcol = 'Mechanism Chain'
    fkhinge = False
    
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
        
        if len(context.selected_editable_bones) < 2:
            self.report({"ERROR"}, f"2 or more bones are necessary")
            return {"CANCELLED"}
        
        for bone in context.selected_editable_bones:
            if bone.parent and not bone.use_connect:
                self.report({"ERROR"}, f"{bone.name} is not connected")
                return {"CANCELLED"}
            
       #---------------------- Operation ----------------------
        
        # Sorting bone chain by hierarchy.
        bone_chain = set_bone.sorting(bone_chain= context.selected_editable_bones)
        
        if not bone_chain:
            self.report({"ERROR"}, f"All Bones are parented, unparent root of the chain.")
            return {"CANCELLED"}
        
        # Creating bones.
        parenting_chain: list = []
        bhandles: list = []
        for bone in bone_chain:
            # To be only apply on the first bone in the chain.
            if not bone.parent:
                twk_bone = set_bone.create(
                        bone,
                        bone_type='TWK',
                        bone_head=bone.head,
                        bbone_size=bone.bbone_x*1.5,
                        length=bone.length*0.3,
                        context=context,
                    )
                ctrl_cog = set_bone.create(
                        bone,
                        bone_type='CTRL',
                        bone_head=bone.tail,
                        bbone_size=bone.bbone_x*1.9,
                        length=bone.length*0.12,
                        context=context,
                        bone_name='COG',
                        align_world=True,
                    )
                ctrl_bone = set_bone.create(
                        bone,
                        bone_type='CTRL',
                        bone_head=bone.tail,
                        bbone_size=bone.bbone_x*1.8,
                        length=bone.length*0.14,
                        context=context,
                        bone_name='Hips'
                    )

                #---------------------- Setting BBones Handles. ----------------------
                bhandles.append(twk_bone)
                set_bone.bbone_handles(bone, bhandle=bhandles[-1], context=context)

                #---------------------- Setting bone parenting. ----------------------
                set_bone.parenting(bone=twk_bone, parentbone=ctrl_bone, context=context)
                set_bone.parenting(bone=ctrl_bone, parentbone=ctrl_cog, context=context)
                parenting_chain.append(ctrl_cog)

                #---------------------- Setting Collection. ----------------------
                set_bone.collection(bone=twk_bone, colname=self.tweakcol, context=context)
                set_bone.collection(bone=ctrl_bone, colname=self.ctrlcol, context=context)
                set_bone.collection(bone=ctrl_cog, colname=self.ctrlcol, context=context)

            # To be only apply on the chain.
            else:
                twk_bone = set_bone.create(
                    bone,
                    bone_type='TWK',
                    bone_head=bone.head,
                    bbone_size=bone.bbone_x*1.5,
                    length=bone.length*0.3,
                    context=context,
                )
                #Demeter cloudrig idea to deal with torso stretchy hierarchy.
                ORG_bone = set_bone.create(
                        bone,
                        bone_type='ORG',
                        bone_head=bone.head,
                        bbone_size=bone.bbone_x*1.2,
                        length=bone.length*0.5,
                        context=context,
                    )
                
                fk_bone = set_bone.create(
                        bone,
                        bone_type='FK',
                        bone_head=bone.head,
                        bbone_size=bone.bbone_x*1.7,
                        length=bone.length*0.2,
                        context=context,
                    )
                
                # To be only apply on the penultimate bone in the chain.
                if self.fkhinge and len(bone.children_recursive) == 1:
                    hinge_bone = set_bone.create(
                    bone,
                    bone_type='MCH',
                    bone_head=bone.head,
                    bbone_size=bone.bbone_x*0.2,
                    length=bone.length*0.2,
                    context=context,
                    )
                    #---------------------- Setting bone parenting. ----------------------
                    set_bone.parenting(bone=hinge_bone, parentbone=parenting_chain[-1], context=context)
                    parenting_chain.append(hinge_bone)

                    #---------------------- Setting Collection. ----------------------
                    set_bone.collection(bone=hinge_bone, colname=self.mchcol, context=context)


                #---------------------- Setting BBones Handles. ----------------------
                bhandles.append(twk_bone)
                set_bone.bbone_handles(bone.parent, bhandle=bhandles[-1], context=context)
                set_bone.bbone_handles(bone, bhandle=bhandles[-1], context=context)
                set_bone.bbone_handles(bone, bhandle=bhandles[-1], context=context)

                #---------------------- Setting bone parenting. ----------------------
                set_bone.parenting(bone=twk_bone, parentbone=parenting_chain[-1], context=context)
                set_bone.parenting(bone=fk_bone, parentbone=parenting_chain[-1], context=context)
                parenting_chain.append(fk_bone)

                #---------------------- Setting Collection. ----------------------
                set_bone.collection(bone=twk_bone, colname=self.tweakcol, context=context)
                set_bone.collection(bone=fk_bone, colname=self.fkcol, context=context)
                set_bone.collection(bone=fk_bone, colname=self.fkcol, context=context)
                set_bone.collection(bone=ORG_bone, colname=self.mchcol, context=context)



                # To be only apply on the last bone in the chain.
                if not bone.children:
                    top_bone = set_bone.create(
                    bone,
                    bone_type='TWK',
                    bone_head=bone.tail,
                    bbone_size=bone.bbone_x*1.5,
                    length=bone.length*0.3,
                    context=context,
                    bone_name='TWK-top',
                    )

                    #---------------------- Setting BBones Handles. ----------------------
                    bhandles.append(top_bone)
                    set_bone.bbone_handles(bone, bhandle=top_bone, context=context)

                    #---------------------- Setting bone parenting. ----------------------
                    set_bone.parenting(bone=top_bone, parentbone=ORG_bone, context=context)

                    #---------------------- Setting Collection. ----------------------
                    set_bone.collection(bone=top_bone, colname=self.tweakcol, context=context)


            #---------------------- Setting Properties. ----------------------
            set_bone.bbones_prop(bone)
            set_bone.bone_prop(bone)

        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")
        
        #---------------------- Applying widgets. ----------------------
        CTRLwidget = set_bone.widget(widget_name='WGT-CTRL', context=context)            
        FKwidget = set_bone.widget(widget_name='WGT-FK', context=context)
        TWKwidget = set_bone.widget(widget_name='WGT-sphere', context=context)
        HIPSwidget = set_bone.widget(widget_name='WGT-saddle', context=context)
        for bone in context.active_object.pose.bones.values():
            if bone.name.startswith('COG'):
                set_bone.assign_widget(bone=bone, shape=CTRLwidget)
            elif bone.name.startswith('CTRL'):
                set_bone.assign_widget(bone=bone, shape=CTRLwidget)
            elif bone.name.startswith('FK'):
                set_bone.assign_widget(bone=bone, shape=FKwidget)
            elif bone.name.startswith('TWK'):
                set_bone.assign_widget(bone=bone, shape=TWKwidget)
            elif bone.name == 'Hips':
                set_bone.assign_widget(bone=bone, shape=HIPSwidget)


            #Setting bone properties in pose mode.
            set_bone.pbone_properties(bone=bone)
        
        if self.fkhinge:
            for bone in context.active_object.pose.bones:
                if bone.name.startswith('MCH'):
                    set_bcontraints.copyrot_bconstraint(
                    bone,
                    subtarget='COG',
                    space="WORLD",
                    context=context,
                    )
        for bone in context.active_object.pose.bones:
            if bone.name.startswith('ORG'):
                set_bcontraints.copytransform_bconstraint(
                bone,
                subtarget=bone.name.replace('ORG','FK'),
                space="WORLD",
                context=context,
            )
        for bone in context.selected_pose_bones:
            # Add Constraints
            tweakbone = f'TWK-{bone.name}' if 'DEF' not in bone.name else bone.name.replace('DEF', 'TWK')
            if not bone.parent:
                set_bcontraints.copyloc_bconstraint(
                bone,
                subtarget= tweakbone,
                space="WORLD",
                context=context,
                )


            if bone.child:
                tweak_tail = f'TWK-{bone.child.name}' if 'DEF' not in bone.child.name else bone.child.name.replace('DEF', 'TWK')
                
                set_bcontraints.stretchto_bconstraint(
                bone,
                subtarget=tweak_tail,
                space="WORLD",
                context=context,
                )

            else:
                set_bcontraints.stretchto_bconstraint(
                bone,
                subtarget='TWK-top',
                space="WORLD",
                context=context,
                )
        

        self.report({"INFO"}, f"Control added")
        return {"FINISHED"}