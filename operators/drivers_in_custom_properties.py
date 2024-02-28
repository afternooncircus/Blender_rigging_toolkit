from bpy.types import Context, Operator

from bpy import context


######TO DO####
def add_bone_constraints_drivers(
    source_bone: str,
    constraints_name: str,
    constraint_property: str,
    target_bone_property_name: str,
    target_datapath: str,
    context: Context,
    driver_type: str,
    bone_driver_expression: str,
    variable_type="SINGLE_PROP",
):

    add_driver = (
        context.active_object.pose.bones[source_bone]
        .constraints[constraints_name]
        .driver_add(constraint_property)
    )
    add_driver.driver.variables.new().name
    add_driver.driver.type = driver_type
    expression: str = ""
    add_driver.type.expression

    bone_driver = (
        context.active_object.active_object.pose.bones[source_bone]
        .constraints[constraints_name]
        .driver_add(constraint_property)
        .driver.variables.new()
    )
    bone_driver.name = target_bone_property_name  # custom_bone_name
    bone_driver.type = variable_type
    bone_driver.targets[0].id = context  # target
    bone_driver.targets[0].data_path = target_datapath  # datapath

    context.active_object.active_object.pose.bones[source_bone].constraints[
        constraints_name
    ].driver_add(constraint_property).driver.type = driver_type
    bone_driver_expression_source_bone = (
        context.active_object.pose.bones[source_bone]
        .constraints[constraints_name]
        .driver_add(constraint_property)
        .driver
    )
    bone_driver_expression_source_bone.expression = bone_driver_expression

    # -------------------------------------------------------------
    fcurve = (
        context.active_object.pose.bones["Bone"]
        .constraints["Copy Location"]
        .driver_add("influence")
    )
    driver = fcurve.driver

    driver.expression = "var"

    variables_driver = driver.variables.new()
    variables_driver.targets[0].id = context.active_object
    variables_driver.targets[0].data_path = 'pose.bones["Bone"]["prop"]'
