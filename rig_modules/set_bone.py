from bpy.types import Context, EditBone, PoseBone, BoneCollection
from pathlib import Path
import bpy
import math

def naming(bone: EditBone, bone_type: str) -> str:
    '''Puts preffix to bone name. It replaces its previous one if it has.'''
    bname = bone.name.split('-')
    if len(bname) < 2:
        return f'{bone_type}-{bone.name}'
    bname[0] = bone_type
    return '-'.join(bname)

def parenting(bone: EditBone, parentbone: EditBone, context: Context) -> any:
    bone.use_connect = False
    bone.parent = parentbone

def create(
bone: EditBone,
bone_type: str,
bone_head: tuple,
bbone_size: float,
length: float,
context: Context,
bone_name: str = '',
) -> EditBone:
    if bone_name:
        bname = bone_name
    else:
        bname = naming(bone, bone_type)
        
    new_bone: str = context.object.data.edit_bones.new(bname)
    new_bone.head = bone_head
    new_bone.tail = (bone.vector) + bone.tail
    new_bone.length = length
    new_bone.roll = bone.roll
    new_bone.bbone_x = bbone_size
    new_bone.bbone_z = new_bone.bbone_x
    new_bone.use_deform = False
    new_bone.inherit_scale = 'AVERAGE'

    return new_bone


def bbones_prop(bone: EditBone) -> any:
    if bone.bbone_segments == 1:
        bone.bbone_segments = 3

    bone.bbone_easein = 0.0
    bone.bbone_easeout = 0.0
    bone.bbone_handle_type_start = "TANGENT"
    bone.bbone_handle_type_end = "TANGENT"

    bone.bbone_handle_use_scale_start[0] = True
    bone.bbone_handle_use_scale_start[1] = False
    bone.bbone_handle_use_scale_start[2] = True

    bone.bbone_handle_use_scale_end[0] = True
    bone.bbone_handle_use_scale_end[1] = False
    bone.bbone_handle_use_scale_end[2] = True


def bbone_handles(bone: EditBone, bhandle: EditBone, context: Context) -> any:
    """Adds custom bones as start/end handles for bbones."""
    edit_bones = context.active_object.data.edit_bones
    if bone.head == bhandle.head:
        bone.bbone_custom_handle_start = edit_bones[bhandle.name]

    elif bone.tail == bhandle.head:
        bone.bbone_custom_handle_end = edit_bones[bhandle.name]

def bone_prop(bone: EditBone, type_inscale: str = 'ALIGNED') -> any:
    '''Set bone properties in Edit Mode.'''
    bone.inherit_scale = type_inscale
    return {"FINISHED"}

def pbone_properties(bone: PoseBone) -> any:
    """Set bone properties in Pose Mode."""
    bone.rotation_mode = "XYZ"

    # if bone.bone.use_deform:
    #     bone.bbone_easein = 1
    #     bone.bbone_easeout = 1
    return {"FINISHED"}

def collection(bone: EditBone, colname: str, context: Context) -> any:
    arm = context.active_object.data
    if colname not in arm.collections: 
        arm.collections.new(name=colname)
    arm.collections[colname].assign(bone)
    return {'FINISHED'}

def widget(widget_name: str, context: Context) -> EditBone:
    current_dir = Path(__file__).parent.parent
    folder = Path('/armature_presets/widgets.blend')
    preset_folder = f'{current_dir}{folder}'

    for obj in bpy.data.objects.values():
        if obj.name == widget_name:
            return obj
        
    with bpy.data.libraries.load(preset_folder, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if not name in bpy.data.objects.keys() and name in widget_name]

    widgetcoll = context.active_object.name.replace('RIG', 'WIDGET')
    for obj in data_to.objects:
        context.scene.collection.objects.link(obj)
        bpy.data.collections[widgetcoll].objects.link(obj)
        context.scene.collection.objects.unlink(obj)  
        return obj
    
def assign_widget(bone: PoseBone, shape) -> any:               
    bone.custom_shape = shape
    bone.custom_shape_rotation_euler[0] = math.radians(90)
    if bone.name.startswith('strHandle') or bone.name.startswith('endHandle'):
        bone.custom_shape_scale_xyz[0] = 0.5
        bone.custom_shape_scale_xyz[1] = bone.custom_shape_scale_xyz[0]
        bone.custom_shape_scale_xyz[2] = bone.custom_shape_scale_xyz[0]
        return {'FINISHED'}
    bone.custom_shape_scale_xyz[0] = 1.3
    bone.custom_shape_scale_xyz[1] = bone.custom_shape_scale_xyz[0]
    bone.custom_shape_scale_xyz[2] = bone.custom_shape_scale_xyz[0]
    