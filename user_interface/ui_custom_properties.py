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
    # --- self define attributes ---
    ac_custom_bone = "Properties"
    ac_ikfk_bone = "-IK|FK"
    ac_fk_hinge_bone = "-FK_hinge"
    ac_mask_prop = "-mask"
    ac_foot_roll = "Foot Roll"
    ac_rhose = "-rubber_hose"
    ac_ik_pole = "-IK_pole_follow"
    ac_ik_stretch = "-IK_stretch"
    ac_mouth_zip = "-zipper"
    ac_teeth_follow = "-follow_rot"
    ac_sticky_eye = "-sticky_eyelips"
    ac_side = {
        "left": ".L",
        "right": ".R",
        "center": ".C",
        "top": ".top",
        "bot": ".bot",
    }

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
        property_name: str, source_bone: str, context: Context, property_suffix: str
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
            _
            for _ in context.active_object.pose.bones[source_bone].keys()
            if property_suffix in _
        }:
            return property_name

    @staticmethod
    def is_custom_suffix(
        source_bone: str, context: Context, property_suffix: str
    ) -> bool:
        """Check on whether custom property name exists on source_bone.

        :param source_bone: properties bone.
        :type source_bone: str
        :param context: context.active_object.
        :type context: Context
        :param property_suffix: "-string" type of property.
        :type property_suffix: str
        :return: True if there is a property with the property_suffix, False if not.
        :rtype: bool
        """
        return bool(
            {
                _
                for _ in context.active_object.pose.bones[source_bone].keys()
                if property_suffix in _
            }
        )

    def draw_custom_property(
        self, custom_prop: str, context: Context, text: str, split
    ):
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
        id_prop = context.active_object.pose.bones[self.ac_custom_bone][custom_prop]
        if type(id_prop) == bool:
            icon = "CHECKBOX_HLT" if id_prop else "CHECKBOX_DEHLT"
            col = split.column(align=True)

            return col.prop(
                context.active_object.pose.bones[self.ac_custom_bone],
                f'["{custom_prop}"]',
                toggle=True,
                text=text,
                icon=icon,
            )

        elif "." in custom_prop:  # It is going to check for side suffix.
            col = split.column(align=True)
            return col.prop(
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

    

# ----- Main Panel -----
class VIEW3D_PT_CustomBonePropertiesUI(ArmaturePanel, Panel):
    """Draws main UI tab for all properties under the label 'Custom Properties Settings'."""

    bl_label = "Custom Properties Settings"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_idname = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context)

    def draw(self, context: Context):
        layout = self.layout
        layout.label(
            text=f"{context.active_object.data.name}",
            icon="ARMATURE_DATA",
        )


class VIEW3D_PT_IkFkSwitchUI(ArmaturePanel, Panel):
    """Draws UI tab for 'IK|FK Switch' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "IK|FK Switch"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IkFkSwitchUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_ikfk_bone)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_ikfk_bone):
            layout = self.layout

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ikfk_bone}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ikfk_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ikfk_bone}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ikfk_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ikfk_bone}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ikfk_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ikfk_bone}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ikfk_bone,
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
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_fk_hinge_bone)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_fk_hinge_bone):

            layout = self.layout
            split = layout.split()

        if custom_prop := super().is_custom_property(
            property_name=f"head{self.ac_fk_hinge_bone}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Head", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"neck{self.ac_fk_hinge_bone}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Neck", split=split
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_fk_hinge_bone}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_fk_hinge_bone}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_fk_hinge_bone}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_fk_hinge_bone}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_fk_hinge_bone,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Leg", split=split
            )


# ----- Main Panel -----
class VIEW3D_PT_LimbSettingsUI(ArmaturePanel, Panel):
    """Draws main UI tab for 'Limbs Settings' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "Limbs Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_LimbSettingsUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(icon="COLLAPSEMENU")

    def draw(self, context: Context):
        pass


class VIEW3D_PT_FootRollUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Foot Roll' properties. A child of 'Limbs Settings' Tab."""

    bl_label = "Foot Roll"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_FootRollUI"
    bl_parent_id = "VIEW3D_PT_LimbSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_foot_roll)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_foot_roll):
            layout = self.layout
            # layout.label(text="Foot Roll")

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"{self.ac_foot_roll}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_foot_roll,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Foot Roll",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"{self.ac_foot_roll}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_foot_roll,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Foot Roll",
                split=split,
            )


class VIEW3D_PT_RubberHoselUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Rubber Hose' properties. A child of 'Limbs Settings' Tab."""

    bl_label = "Rubber Hose"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_RubberHoselUI"
    bl_parent_id = "VIEW3D_PT_LimbSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_rhose)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_rhose):
            layout = self.layout

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_rhose}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_rhose,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Arm Curvature",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_rhose}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_rhose,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Arm Curvature",
                split=split,
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_rhose}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_rhose,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Leg Curvature",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_rhose}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_rhose,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Leg Curvature",
                split=split,
            )


# ----- Main Panel -----
class VIEW3D_PT_IKSettingsUI(ArmaturePanel, Panel):
    """Draws main UI tab for 'IK Settings' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "IK Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IKSettingsUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(icon="COLLAPSEMENU")

    def draw(self, context: Context):
        pass


class VIEW3D_PT_IKFollowUI(ArmaturePanel, Panel):
    """Draws UI tab for 'IK Follow' properties. A child of 'IK Settings' Tab."""

    bl_label = "IK Follow"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IKFollowUI"
    bl_parent_id = "VIEW3D_PT_IKSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_ik_pole)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_ik_pole):
            layout = self.layout

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ik_pole}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_pole,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Arm IK",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ik_pole}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_pole,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Arm IK",
                split=split,
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ik_pole}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_pole,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Leg IK",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ik_pole}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_pole,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Leg IK",
                split=split,
            )


class VIEW3D_PT_IKStretchUI(ArmaturePanel, Panel):
    """Draws UI tab for 'IK Stretch' properties. A child of 'IK Settings' Tab."""

    bl_label = "IK Stretch"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_IKStretchUI"
    bl_parent_id = "VIEW3D_PT_IKSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_ik_stretch)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_ik_stretch):
            layout = self.layout

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ik_stretch}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_stretch,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Arm IK",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_ik_stretch}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_stretch,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Arm IK",
                split=split,
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ik_stretch}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_stretch,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Left Leg IK",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_ik_stretch}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_ik_stretch,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Right Leg IK",
                split=split,
            )


# ----- Main Panel -----
class VIEW3D_PT_FaceSettingsUI(ArmaturePanel, Panel):
    """Draws main UI tab for 'Face Settings' properties. A child of 'Custom Properties Settings' Tab."""

    bl_label = "Face Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_FaceSettingsUI"
    bl_parent_id = "VIEW3D_PT_CustomBonePropertiesUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context) and super().is_bone(cls.ac_custom_bone, context)

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(icon="COLLAPSEMENU")

    def draw(self, context: Context):
        pass


class VIEW3D_PT_MouthPropUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Mouth Settings' properties. A child of 'Character Properties' Tab."""

    bl_label = "Mouth Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_MouthPropUI"
    bl_parent_id = "VIEW3D_PT_FaceSettingsUI"
    ac_custom_bone = "Properties"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_mouth_zip)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_mouth_zip):
            layout = self.layout
            split = layout.split()

        if custom_prop := super().is_custom_property(
            property_name=f"mouth{self.ac_mouth_zip}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_mouth_zip,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Mouth Zipper",
                split=split,
            )

        if custom_prop := super().is_custom_property(
            property_name=f"teeth{self.ac_teeth_follow}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_teeth_follow,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Teeth Follow Mouth",
                split=split,
            )


class VIEW3D_PT_EyesPropUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Eyes Settings' properties. A child of 'Character Properties' Tab."""

    bl_label = "Eyes Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_EyesPropUI"
    bl_parent_id = "VIEW3D_PT_FaceSettingsUI"
    ac_custom_bone = "Properties"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_sticky_eye)
        )

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_sticky_eye):
            layout = self.layout
            split = layout.split()

        if custom_prop := super().is_custom_property(
            property_name=f"eyes{self.ac_sticky_eye}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_sticky_eye,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop,
                context=context,
                text="Sticky Eyelips",
                split=split,
            )


# ----- Main Panel -----
class VIEW3D_PT_CharacterSettingsUI(ArmaturePanel, Panel):
    """Draws main tab for all properties under the label 'Character Properties'."""

    bl_label = "Character Properties"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_CharacterSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return super().poll(context)

    def draw(self, context: Context):
        layout = self.layout
        layout.label(
            text=f"{context.active_object.name}",
            icon="OUTLINER_OB_ARMATURE",
        )


class VIEW3D_PT_BonesMaskPropUI(ArmaturePanel, Panel):
    """Draws UI tab for 'Mask Settings' properties. A child of 'Character Properties' Tab."""

    bl_label = "Mask Settings"
    bl_options = {"DEFAULT_CLOSED"}
    bl_idname = "VIEW3D_PT_BonesMaskPropUI"
    bl_parent_id = "VIEW3D_PT_CharacterSettingsUI"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return (
            super().poll(context)
            and super().is_bone(cls.ac_custom_bone, context)
            # and super().is_custom_suffix(cls.ac_custom_bone, context, cls.ac_mask_prop)
        )

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(icon="MOD_MASK")

    def draw(self, context: Context):
        if self.is_custom_suffix(self.ac_custom_bone, context, self.ac_mask_prop):
            layout = self.layout
            split = layout.split()

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_mask_prop}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_mask_prop,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Arm", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"arm{self.ac_mask_prop}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_mask_prop,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Arm", split=split
            )

            # New split of pair columns
            split = layout.split()
        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_mask_prop}{self.ac_side['left']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_mask_prop,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Left Leg", split=split
            )

        if custom_prop := super().is_custom_property(
            property_name=f"leg{self.ac_mask_prop}{self.ac_side['right']}",
            source_bone=self.ac_custom_bone,
            context=context,
            property_suffix=self.ac_mask_prop,
        ):
            super().draw_custom_property(
                custom_prop=custom_prop, context=context, text="Right Leg", split=split
            )
