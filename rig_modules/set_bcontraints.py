from bpy.types import Context, PoseBone

def copyloc_bconstraint(bone, subtarget: PoseBone, space: str, context: Context):
        bconstraint = bone.constraints.new(type='COPY_LOCATION')
        bconstraint.target = context.active_object
        bconstraint.subtarget = subtarget
        bconstraint.target_space = space
        bconstraint.owner_space = space
        bconstraint.influence = 1.0
        return {'FINISHED'}

#def loc first bone in chain.
def stretchto_bconstraint(bone, subtarget: PoseBone, space: str, context: Context):
    """Adds a Stretch to Constraint"""
    bconstraint = bone.constraints.new("STRETCH_TO")
    bconstraint.target = context.active_object
    bconstraint.subtarget = subtarget
    bconstraint.target_space = space
    bconstraint.owner_space = space
    bconstraint.influence = 1.0
    return {"FINISHED"}