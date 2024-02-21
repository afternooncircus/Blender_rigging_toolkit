from bpy.types import Context, Panel, UILayout

class ArmaturePanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigging Toolkit"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.active_object.type == 'ARMATURE'


class VIEW3D_PT_PropertyBoneUI(ArmaturePanel, Panel): #Fix naming convention!!!!!!
    """
    Draw UI for all the properties in bone named 'Properties'. 
    """
    bl_label = "UI Custom Properties"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context):
        return context.active_object.pose.bones.get('Properties')
    
    def draw(self, context: Context) -> bool:
        properties_bone = context.active_object.pose.bones["Properties"]

        layout = self.layout
        layout.label(
            # text=f'{context.active_object.name} | {context.active_object.data.name}',
            text=f'{properties_bone.keys()}',
            icon='ARMATURE_DATA')