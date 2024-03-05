from bpy.types import Context, Operator
from pathlib import Path, PurePath
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
        #Addon Folder
        current_dir = Path.cwd()
        #going to SubFolder
        preset_folder = rf'{current_dir}\armature_presets\human_preset.blend'
        blendpath = preset_folder
        namelist = ['Armature']

        #Code by Zender on Blenderartist.
        with bpy.data.libraries.load(blendpath, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name in namelist] 
        for obj in data_to.objects:
            context.scene.collection.objects.link(obj)
        return {"FINISHED"} 
    

