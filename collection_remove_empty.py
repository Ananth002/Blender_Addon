import bpy

class ClearParentKeepLocalTransformOperator(bpy.types.Operator):
    """Clear Parent and Keep Local Transform for Selected Collection"""
    bl_idname = "object.clear_parent_keep_local_transform_collection"
    bl_label = "Clear Parent (Keep Local Transform)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_collection = context.scene.selected_collection
        if not selected_collection:
            self.report({'WARNING'}, "No collection selected!")
            return {'CANCELLED'}

        objects = selected_collection.objects  # Objects in the selected collection
        if not objects:
            self.report({'WARNING'}, "No objects in the selected collection!")
            return {'CANCELLED'}

        for obj in objects:
            if obj.parent:  # Check if the object has a parent
                # Save the world transform before clearing parent
                world_matrix = obj.matrix_world.copy()
                # Clear the parent relationship
                obj.parent = None
                # Set the local matrix to the world matrix to maintain the same position/rotation/scale
                obj.matrix_world = world_matrix

        self.report({'INFO'}, f"Parenting cleared for objects in '{selected_collection.name}'!")
        return {'FINISHED'}


class DeleteEmptiesInCollectionOperator(bpy.types.Operator):
    """Delete Specified Number of Empty Objects in Selected Collection"""
    bl_idname = "object.delete_specified_empties_in_collection"
    bl_label = "Delete Specified Number of Empties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_collection = context.scene.selected_collection
        if not selected_collection:
            self.report({'WARNING'}, "No collection selected!")
            return {'CANCELLED'}

        num_to_delete = context.scene.num_empties_to_delete  # Get the number of empties to delete
        empties_deleted = 0
        empties = [obj for obj in selected_collection.objects if obj.type == 'EMPTY']

        # Limit the number of empties to delete based on user input
        for obj in empties[:num_to_delete]:
            selected_collection.objects.unlink(obj)  # Unlink the empty from the collection
            bpy.data.objects.remove(obj)  # Delete the empty object
            empties_deleted += 1

        if empties_deleted > 0:
            self.report({'INFO'}, f"Deleted {empties_deleted} empty objects from '{selected_collection.name}'!")
        else:
            self.report({'INFO'}, f"No empty objects found or invalid number in '{selected_collection.name}'.")

        return {'FINISHED'}


class RemoveAllEmptiesInCollectionOperator(bpy.types.Operator):
    """Remove All Empties from the Selected Collection"""
    bl_idname = "object.remove_all_empties_in_collection"
    bl_label = "Remove All Empties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_collection = context.scene.selected_collection
        if not selected_collection:
            self.report({'WARNING'}, "No collection selected!")
            return {'CANCELLED'}

        empties = [obj for obj in selected_collection.objects if obj.type == 'EMPTY']
        if not empties:
            self.report({'INFO'}, f"No empties found in '{selected_collection.name}'!")
            return {'CANCELLED'}

        # Remove all empties in the selected collection
        for obj in empties:
            selected_collection.objects.unlink(obj)  # Unlink the empty from the collection
            bpy.data.objects.remove(obj)  # Delete the empty object

        self.report({'INFO'}, f"All empty objects removed from '{selected_collection.name}'!")
        return {'FINISHED'}


class ClearParentAndRemoveAllEmptiesOperator(bpy.types.Operator):
    """Clear Parent (Keep Local Transform) and Remove All Empties from Selected Collection"""
    bl_idname = "object.clear_parent_and_remove_empties"
    bl_label = "Clear Parent & Remove All Empties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_collection = context.scene.selected_collection
        if not selected_collection:
            self.report({'WARNING'}, "No collection selected!")
            return {'CANCELLED'}

        # Clear Parent and Keep Local Transform
        objects = selected_collection.objects  # Objects in the selected collection
        for obj in objects:
            if obj.parent:  # Check if the object has a parent
                # Save the world transform before clearing parent
                world_matrix = obj.matrix_world.copy()
                # Clear the parent relationship
                obj.parent = None
                # Set the local matrix to the world matrix to maintain the same position/rotation/scale
                obj.matrix_world = world_matrix

        # Remove all empties in the selected collection
        empties = [obj for obj in selected_collection.objects if obj.type == 'EMPTY']
        for obj in empties:
            selected_collection.objects.unlink(obj)  # Unlink the empty from the collection
            bpy.data.objects.remove(obj)  # Delete the empty object

        self.report({'INFO'}, f"Parenting cleared and all empty objects removed from '{selected_collection.name}'!")
        return {'FINISHED'}


class ClearParentPanel(bpy.types.Panel):
    """Creates a panel in the Object Properties tab"""
    bl_label = "Collection --> Empty Remove"
    bl_idname = "OBJECT_PT_clear_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Xtreame'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Section for Collection Selection and Info
        layout.label(text="Collection Info:", icon='OUTLINER')
        
        # Collection selector
        layout.prop(scene, "selected_collection", text="Select ")
        
        selected_collection = scene.selected_collection
        if selected_collection:
            # Show the number of empties in the selected collection
            empties_count = sum(1 for obj in selected_collection.objects if obj.type == 'EMPTY')
            layout.label(text=f"Empties: {empties_count}")

        layout.separator()

        # Section for Parent Clear Operation
        layout.label(text="Clear Parent (Keep Local Transform)", icon='MODIFIER')
        layout.operator("object.clear_parent_keep_local_transform_collection", text="Clear Parent")

        layout.separator()

        # Section for Empty Deletion and Remove All Empties
        layout.label(text="Remove Empty !", icon='TRASH')
        
        # Delete specific number of empties
        layout.prop(scene, "num_empties_to_delete", text="Remove No : ")
        layout.operator("object.delete_specified_empties_in_collection", text="Remove Empties")

        # Remove all empties button
        layout.operator("object.remove_all_empties_in_collection", text="Remove All Empties")

        layout.separator()

        # New section for the combined action
        layout.label(text="Clear : Parent with Empty", icon='MODIFIER')
        layout.operator("object.clear_parent_and_remove_empties", icon='TRASH', text="")

def register():
    # Add properties for selected collection and number of empties to delete
    bpy.types.Scene.selected_collection = bpy.props.PointerProperty(
        type=bpy.types.Collection,
        name="Selected Collection",
        description="Select a collection to process"
    )
    bpy.types.Scene.num_empties_to_delete = bpy.props.IntProperty(
        name="Number of Empties to Remove",
        description="Specify how many empty objects to delete from the selected collection",
        default=1,  # Default to deleting 1 empty
        min=1,      # Minimum of 1 empty
    )
    bpy.utils.register_class(ClearParentKeepLocalTransformOperator)
    bpy.utils.register_class(DeleteEmptiesInCollectionOperator)
    bpy.utils.register_class(RemoveAllEmptiesInCollectionOperator)
    bpy.utils.register_class(ClearParentAndRemoveAllEmptiesOperator)
    bpy.utils.register_class(ClearParentPanel)


def unregister():
    del bpy.types.Scene.selected_collection
    del bpy.types.Scene.num_empties_to_delete
    bpy.utils.unregister_class(ClearParentKeepLocalTransformOperator)
    bpy.utils.unregister_class(DeleteEmptiesInCollectionOperator)
    bpy.utils.unregister_class(RemoveAllEmptiesInCollectionOperator)
    bpy.utils.unregister_class(ClearParentAndRemoveAllEmptiesOperator)
    bpy.utils.unregister_class(ClearParentPanel)


if __name__ == "__main__":
    register()
