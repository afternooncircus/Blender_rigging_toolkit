from bpy.types import Context, Panel


class ArmaturePanel(Panel):
    """Contains Methods to check on whether UI would be display or not.

    -- Default Values --
    :ac_custom_bone = "Properties"
    :ac_ikfk_bone = "-IK|FK"
    :ac_fk_hinge_bone = "-FK_hinge"
    :ac_mask_prop = "-mask"
    :ac_foot_roll = "Foot Roll"
    :ac_side = {"left": ".L", "right": ".R", "center": ".C"}
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rigging Toolkit"
    ac_custom_bone = "Properties"
    ac_ikfk_bone = "-IK|FK"
    ac_fk_hinge_bone = "-FK_hinge"
    ac_mask_prop = "-mask"
    ac_foot_roll = "Foot Roll"
    ac_side = {"left": ".L", "right": ".R", "center": ".C"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Draws UI if armature is selected.

        :param context: .active_object
        :type context: Context
        :return: True if active object is an Armature object
        :rtype: bool
        """ """"""

        if hasattr(context.active_object, "type"):
            return context.active_object.type == "ARMATURE"
        return False

    @staticmethod
    def is_bone(bone_name: str, context: Context) -> bool:
        """Check if bone exists in armature object.

        :param bone_name: bone name
        :type bone_name: str
        :param context: active armature
        :type context: Context
        :return: bone name if it is in armature object.
        :rtype: bool
        """
        if bone_name in set(bone.name for bone in context.active_object.data.bones):
            return bone_name

    @staticmethod
    def is_custom_property(
        property_name: str, source_bone: str, context: Context
    ) -> str:
        """Check if custom property exists in bone.

        :param property_name: name of the custom property
        :type property_name: str
        :param source_bone: name of the bone that has the custom properties
        :type source_bone: str
        :param context: custom property bone
        :type context: Context
        :return: property name if it is in custom property bone
        :rtype: str
        """
        if property_name in {
            _ for _ in context.active_object.pose.bones[source_bone].keys()
        }:
            return property_name

    def draw_custom_property(self, custom_prop: str, context: Context, text: str, split):
        """Draws button for a custom property. 

        :param custom_prop: name of custom property
        :type custom_prop: str
        :param context: Properties bone
        :type context: Context
        :param text: string that will appear in slider
        :type text: str
        :param split: pass the split function to be able to separate Left and Right
        :type split: _type_
        :return: the input fields as a column
        :rtype: _type_
        """        
        if custom_prop.endswith(".L"):
            col = split.column(align=True)
            return col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=text,
            )

        elif custom_prop.endswith(".R"):
            subcol = split.column(align=True)
            return subcol.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=text,
            )

        else:
            col = self.layout.column(align=True)
            return col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                slider=True,
                text=text,
            )


class VIEW3D_PT_CustomBonePropertiesUI(ArmaturePanel, Panel):
    """Draws main UI tab for all properties under the label 'Custom Properties Settings'."""

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
    """Draws UI tab for 'IK|FK Switch' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "IK|FK Switch"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IkFkSwitchUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"arm{self.ac_ikfk_bone}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_ikfk_bone}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_ikfk_bone}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_ikfk_bone}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Leg", split=split
            )


class VIEW3D_PT_FkHingeUI(ArmaturePanel, Panel):
    """Draws UI tab for 'FK Hinge' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "FK Hinge"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_FkHingeUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        layout = self.layout
        split = layout.split()

        if custom_prop := super().is_custom_property(
            f"head{self.ac_fk_hinge_bone}", self.ac_custom_bone, context
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Head", split=split
            )

        if custom_prop := super().is_custom_property(
            f"neck{self.ac_fk_hinge_bone}", self.ac_custom_bone, context
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Neck", split=split
            )

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"arm{self.ac_fk_hinge_bone}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_fk_hinge_bone}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_fk_hinge_bone}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_fk_hinge_bone}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Leg", split=split
            )


class VIEW3D_PT_LimbsSettingsUI(ArmaturePanel, Panel):
    """Draws main UI tab for 'Limbs Settings' properties. A child of 'Custom Properties Settings' Tab."""

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

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"{self.ac_foot_roll}{self.ac_side['left']}", self.ac_custom_bone, context
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Foot Roll",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            f"{self.ac_foot_roll}{self.ac_side['right']}", self.ac_custom_bone, context
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Foot Roll",
                split=split,
            )


class VIEW3D_PT_CharacterSettingsUI(ArmaturePanel, Panel):
    """Draws main tab for all properties under the label 'Character Properties'."""

    bl_label = "Character Properties"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_CharacterSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw(self, context: Context):
        pass


class VIEW3D_PT_BonesMaskPropUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Mask Settings' properties. A child of 'Character Properties' Tab."""

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
            f"arm{self.ac_mask_prop}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            f"arm{self.ac_mask_prop}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

        # New split of pair columns
        split = layout.split()
        if custom_prop := super().is_custom_property(
            f"leg{self.ac_mask_prop}{self.ac_side['left']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            f"leg{self.ac_mask_prop}{self.ac_side['right']}",
            self.ac_custom_bone,
            context,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Leg", split=split
            )
