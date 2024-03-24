from bpy.utils import register_class, unregister_class

from . import single_bbone_chain
from . import single_control
from . import torso_chain

classes: list = [
    single_bbone_chain.AC_OT_NewBBones,
    single_control.AC_OT_SingleControl,
    single_control.AC_OT_SingleControlConstraint,
    torso_chain.AC_OT_TorsoChain,
]


def register_bone_presets() -> None:
    for cls in classes:
        register_class(cls)


def unregister_bone_presets() -> None:
    for cls in classes:
        unregister_class(cls)
