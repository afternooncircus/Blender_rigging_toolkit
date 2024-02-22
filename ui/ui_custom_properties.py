from bpy.types import Context, Panel, UILayout
import bpy

def is_bone(bone_name: str) -> bool:
    return bone_name in set(bone.name for bone in bpy.context.active_object.data.bones)

def is_armature(context) -> bool:
    if hasattr(context.active_object, 'type'):
        return context.active_object.type == 'ARMATURE'
    return False

class ArmaturePanel():
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rigging Toolkit"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return is_armature(context) 

class VIEW3D_PT_ArmatureNameUI(ArmaturePanel, Panel):
    bl_label = "Armature Name"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context: Context):
        layout = self.layout
        layout.label(
            text=f'{context.active_object.name}',
            icon='ARMATURE_DATA')

class VIEW3D_PT_BonePropertiesUI(ArmaturePanel, Panel):
    """
    Draw UI for all the properties in bone named 'Properties'. 
    """
    bl_label = "UI Custom Properties"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context) -> bool:
        
        return (super().poll(context) and is_bone('Properties'))
    
    def draw(self, context: Context):
        # selected_bones = set(bone.name for bone in context.selected_pose_bones) #set for the custom properties
        properties_bone = context.active_object.pose.bones['Properties']   
        layout = self.layout
        layout.label(
            text=f'a',
            icon='ARMATURE_DATA')