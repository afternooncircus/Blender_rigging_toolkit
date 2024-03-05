def DATA_MT_HumanArmaturePreset(self, context):
    layout = self.layout
    col = layout.column(align=True)
    col.operator(
        "rigtoolkit.human_armature_preset",
        text="Human Armature Preset",
        icon="ARMATURE_DATA",
    )
