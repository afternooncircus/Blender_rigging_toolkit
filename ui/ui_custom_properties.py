from bpy.types import Context, Panel, UILayout


class ArmaturePanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rigging Toolkit"
    ac_custom_bone = "Properties"
    ac_ikfk_bone = "-IK|FK"
    ac_fk_hinge_bone = "-FK_hinge"
    ac_mask_prop = "-mask"
    ac_foot_roll = "Foot Roll"

    @classmethod
    def poll(cls, context: Context) -> bool:
        if hasattr(context.active_object, "type"):
            return context.active_object.type == "ARMATURE"
        return False

    @staticmethod
    def is_bone(bone_name: str, context: Context) -> bool:
        if bone_name in set(bone.name for bone in context.active_object.data.bones):
            return bone_name

    @staticmethod
    def is_custom_property(
        property_name: str, source_bone: str, context: Context
    ) -> str:
        if property_name in {
            _ for _ in context.active_object.pose.bones[source_bone].keys()
        }:
            return property_name


class VIEW3D_PT_CustomBonePropertiesUI(ArmaturePanel, Panel):
    """
    Draw UI for all the properties in bone named 'Properties'.
    """

    bl_label = "Custom Properties Settings"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_idname = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text=f"{self.ac_custom_bone}", icon="ARMATURE_DATA")


class VIEW3D_PT_IkFkSwitchUI(ArmaturePanel, Panel):
    bl_label = "IK|FK Switch"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IkFkSwitchUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout
        split = layout.split()

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_ikfk_bone}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Arm",
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_ikfk_bone}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Arm",
            )

        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_ikfk_bone}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Leg",
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_ikfk_bone}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Leg",
            )


class VIEW3D_PT_FkHingeUI(ArmaturePanel, Panel):
    bl_label = "FK Hinge"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_FkHingeUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout

        if custom_prop := super().is_custom_property(
            f"head{self.ac_fk_hinge_bone}", self.ac_custom_bone, context
        ):
            col = layout.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Head",
            )

        if custom_prop := super().is_custom_property(
            f"neck{self.ac_fk_hinge_bone}", self.ac_custom_bone, context
        ):
            col = layout.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Neck",
            )

        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"arm{self.ac_fk_hinge_bone}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Arm",
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_fk_hinge_bone}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Arm",
            )

        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_fk_hinge_bone}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Leg",
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_fk_hinge_bone}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Leg",
            )


class VIEW3D_PT_LimbsSettingsUI(ArmaturePanel, Panel):
    bl_label = "Limbs Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_LimbsSettingsUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text="Foot Roll")
        split = layout.split()

        if custom_prop := super().is_custom_property(
            f"{self.ac_foot_roll}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Foot Roll",
            )

        if custom_prop := super().is_custom_property(
            f"{self.ac_foot_roll}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Foot Roll",
            )


class VIEW3D_PT_CharacterSettingsUI(ArmaturePanel, Panel):
    bl_label = "Character Properties"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_CharacterSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        pass


class VIEW3D_PT_BonesMaskPropUI(ArmaturePanel, Panel):
    bl_label = "Mask Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_BonesMaskPropUI"
    bl_parent_id = "VIEW3D_PT_CharacterSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(icon="MOD_MASK")

    def draw(self, context: Context):
        layout = self.layout

        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"arm{self.ac_mask_prop}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Arm",
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_mask_prop}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Arm",
            )

        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_mask_prop}.L", self.ac_custom_bone, context
        ):
            col = split.column()
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Left Leg",
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_mask_prop}.R", self.ac_custom_bone, context
        ):
            col = split.column(align=True)
            col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text="Right Leg",
            )
