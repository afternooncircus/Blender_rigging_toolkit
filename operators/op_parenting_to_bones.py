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

    # Function by batFINGER. I feel like this person has save me quite a few times.
    @staticmethod
    def apply_transfrom(ob, use_location=True, use_rotation=True, use_scale=False):
        mb = ob.matrix_basis
        I = Matrix()
        loc, rot, scale = mb.decompose()

        # rotation
        T = Matrix.Translation(loc)
        R = mb.to_3x3().normalized().to_4x4()
        S = Matrix.Diagonal(scale).to_4x4()

        transform = [I, I, I]
        basis = [T, R, S]

        def swap(i):
            transform[i], basis[i] = basis[i], transform[i]

        if use_location:
            swap(0)
        if use_rotation:
            swap(1)
        if use_scale:
            swap(2)

        M = transform[0] @ transform[1] @ transform[2]
        if hasattr(ob.data, "transform"):
            ob.data.transform(M)
        for c in ob.children:
            c.matrix_local = M @ c.matrix_local

        ob.matrix_basis = basis[0] @ basis[1] @ basis[2]

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
            # Set bone to bone head and apply transforms.
            obj.location = arm.pose.bones[obj.name].head
            self.apply_transfrom(obj)

            posebone = arm.pose.bones.get(obj.name)

            if not posebone:
                self.report({"ERROR"}, f"There's no bone name {obj.name}")
                return {'CANCELLED'}
            
            original_wmatrix = obj.matrix_world.copy()
            obj.parent = arm
            obj.parent_bone = bone.name
            obj.parent_type = 'BONE'
            obj.matrix_world = original_wmatrix

        return {"FINISHED"}
