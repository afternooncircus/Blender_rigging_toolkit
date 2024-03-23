from bpy.types import Context, Operator, PoseBone
import bpy
from mathutils import Matrix
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras import object_utils

from bpy.props import (
    FloatProperty,
)


def add_box(width, height, depth):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = [
        (+1.0, +1.0, -1.0),
        (+1.0, -1.0, -1.0),
        (-1.0, -1.0, -1.0),
        (-1.0, +1.0, -1.0),
        (+1.0, +1.0, +1.0),
        (+1.0, -1.0, +1.0),
        (-1.0, -1.0, +1.0),
        (-1.0, +1.0, +1.0),
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7),
    ]

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


class ParentingToBone(Operator, AddObjectHelper):
    """Parent objects to bones."""
    bl_idname = "rigtoolkit.parenting_to_bones"
    bl_label = "Parent objects to bones"
    bl_description = "Parent objects to bones"
    bl_options = {"REGISTER", "UNDO"}

    width: FloatProperty(
        name="Width",
        description="Box Width",
        min=0.01, max=100.0,
        default=0.2,
    )  # type: ignore
    height: FloatProperty(
        name="Height",
        description="Box Height",
        min=0.01, max=100.0,
        default=0.2,
    )  # type: ignore
    depth: FloatProperty(
        name="Depth",
        description="Box Depth",
        min=0.01, max=100.0,
        default=0.2,
    )  # type: ignore

    @staticmethod
    def active_armature(context: Context) -> list:
        if context.active_object.type == 'ARMATURE':
            return context.active_object
        else:
            return False

    @classmethod
    def poll(cls, context: Context) -> bool:
        if hasattr(context.active_object, "type") and context.mode == "OBJECT":
            return context.active_object.type == "ARMATURE"
        return False

    def execute(self, context):
        arm = self.active_armature(context)

        # Add Box code from example files.
        for bone in arm.pose.bones:
            verts_loc, faces = add_box(
                self.width,
                self.height,
                self.depth,
            )

            if bpy.data.meshes.get(bone.name):
                mesh = bpy.data.meshes[bone.name]
                bpy.data.meshes.remove(mesh)

            mesh = bpy.data.meshes.new(bone.name)

            bm = bmesh.new()

            for v_co in verts_loc:
                bm.verts.new(v_co)

            bm.verts.ensure_lookup_table()
            for f_idx in faces:
                bm.faces.new([bm.verts[i] for i in f_idx])

            bm.to_mesh(mesh)
            mesh.update()

            # add the mesh as an object into the scene with this utility module
            object_utils.object_data_add(context, mesh, operator=self)
            obj = bpy.data.objects.get(mesh.name)

            posebone = arm.pose.bones.get(obj.name)

            if not posebone:
                self.report({"ERROR"}, f"There's no bone name {obj.name}")
                return {'CANCELLED'}

            obj.parent = arm
            obj.parent_bone = bone.name
            obj.parent_type = 'BONE'

            obj.matrix_world = arm.pose.bones[obj.name].matrix

        return {"FINISHED"}
