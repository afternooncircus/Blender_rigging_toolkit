from bpy.utils import register_class, unregister_class

classes: list = [

]

def register_operators() -> None:
    for cls in classes:
        register_class(cls)

def unregister_operators() -> None:
    for cls in reversed(classes):
        unregister_class(cls)