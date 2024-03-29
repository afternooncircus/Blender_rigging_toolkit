from bpy.types import Context, Operator
from pathlib import Path
import bpy

class HumanArmaturePreset(Operator):
    """Appends Human Preset"""
    bl_idname = "rigtoolkit.human_armature_preset"
    bl_label = "Appends Human Armature Preset" 
    bl_description = "Appends an human armature preset" 
    bl_options = {"REGISTER", "UNDO"} 
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.mode == "OBJECT"
    
    def execute(self, context):
        current_dir = Path(__file__).parent.parent
        folder = Path('/armature_presets/human_preset.blend')
        preset_folder = f'{current_dir}{folder}'
        armature_name = 'human_preset'

        #Code by Zender on Blenderartist. Edited to work specifically on this.
        with bpy.data.libraries.load(preset_folder, link=False) as (data_from, data_to):
            if not armature_name in {name for name in data_from.objects}:
                self.report({"ERROR"}, f"There is no armature named '{armature_name}'")
                return {"CANCELLED"}
            
            data_to.objects = [name for name in data_from.objects if name in armature_name]

        for obj in data_to.objects:
            context.scene.collection.objects.link(obj)
            
        self.report({"INFO"}, f"Succesfully imported armature '{armature_name}'")
        return {"FINISHED"} 
    

