from bpy.types import Context, Panel


class MainAccessArmatureSetting(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context: Context):
        return context.armature


class DATA_PT_ArmatureSettings(MainAccessArmatureSetting, Panel):
    bl_label = "Rigging Toolkit"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "DATA_PT_ArmatureSettings"

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True
        layout.operator(
            "rigtoolkit.set_armature_properties",
            text="Apply Armature Settings",
            icon="WORLD",
        )
