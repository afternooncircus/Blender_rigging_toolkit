from bpy.types import Context, Operator
from bpy import ops
import bpy


def set_name(armature, context: Context):
    armature.name = armature.name.strip()
    if not armature.name.endswith('-RIG'):
            armature.name = f'{armature.name}-RIG'
            
    return armature.name

class AC_OT_Set_ArmatureProp(Operator):
    """Setting properties and naming convention for active Armature object"""

    bl_idname = "rigtoolkit.set_armature_properties"
    bl_label = "Armature Property Settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if hasattr(context.active_object, "type"):
            return context.active_object.type == "ARMATURE"
        return False
        # return context.active_object.type == "ARMATURE"
        # return context.active_object.type == "ARMATURE" and context.area.type == 'VIEW_3D'
    
    @staticmethod
    def set_armature_collection(context: Context):
        if not context.mode == "OBJECT":
            ops.object.mode_set(mode="OBJECT")

        armature = bpy.context.active_object
        armature.name = set_name(armature, context)

        if armature.name not in bpy.context.scene.collection.children.keys():
            coll = bpy.data.collections.new(f'{armature.name}')
            context.scene.collection.children.link(coll)

            coll.objects.link(armature)
            context.scene.collection.objects.unlink(armature)

    @staticmethod
    def set_object_data(context: Context,):
        """Sets object data, it returns armature name"""

        armature = context.active_object

        if not context.mode == "EDIT":
            ops.object.mode_set(mode="EDIT")

        # Armature name.
        armature.name = set_name(armature, context)

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

    @staticmethod
    def set_armature_data(context: Context):
        """It sets viewport display data for armatures object."""
                
        if not context.mode == "POSE":
            ops.object.mode_set(mode="POSE")

        # Copy object name into data name.
        armature = bpy.context.active_object
        armature.data.name = f'{armature.name.replace(" ", "_").replace("RIG","DATA").strip().lower()}'

        # Viewport Display data settings.
        armature.data.display_type = "BBONE"
        armature.data.show_names = False
        armature.data.show_bone_custom_shapes = True
        armature.data.show_bone_colors = True
        armature.data.show_axes = False
        armature.data.axes_position = 0
        armature.data.relation_line_position = "TAIL"

        return {"FINISHED"}

    def execute(self, context):
        self.set_armature_collection(context)        
        self.set_object_data(context)
        self.set_armature_data(context)

        self.report({"INFO"}, f"Armature Settings Apply")
        return {"FINISHED"}
