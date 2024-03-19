from bpy.types import Context, EditBone, PoseBone

def naming(bone: EditBone, bone_type: str) -> str:
    '''Puts preffix to bone name. It replaces its previous one if it has.'''
    bname = bone.name.split('-')
    if len(bname) < 2:
        return f'{bone_type}-{bone.name}'
    bname[0] = bone_type
    return '-'.join(bname)

def parenting(bone: EditBone, parentbone: EditBone, context: Context):
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
    bone.use_connect = False
    bone.inherit_scale = type_inscale
    return {"FINISHED"}

def pbone_properties(bone: PoseBone) -> any:
    """Set bone properties in Pose Mode."""
    bone.rotation_mode = "XYZ"

    if bone.bone.use_deform:
        bone.bbone_easein = 1
        bone.bbone_easeout = 1
    return {"FINISHED"}

