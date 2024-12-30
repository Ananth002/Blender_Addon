import bpy

class OBJECT_PT_render_visibility_panel(bpy.types.Panel):
    bl_label = "Add Render Keyframe"
    bl_idname = "OBJECT_PT_render_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Xtreame"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        if obj:
            row = layout.row()
            row.prop(obj, "hide_render", text="Show in Render", toggle=True)
            row = layout.row()
            row.operator("object.set_unhide_render_keyframe", text="Render Key" ,icon='RESTRICT_RENDER_OFF')
        
            row = layout.row()
            row.operator("object.set_hide_render_keyframe", text="Render Key", icon='RESTRICT_RENDER_ON')

class OBJECT_OT_set_unhide_render_keyframe(bpy.types.Operator):
    bl_label = "Set Unhide in Render Keyframe"
    bl_idname = "object.set_unhide_render_keyframe"
    bl_description = "Unhide in Render and set keyframe for Show in Render option for selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            # Ensure object is visible in render
            obj.hide_render = False
            # Set a keyframe for the unhidden state
            obj.keyframe_insert(data_path="hide_render")
        
        self.report({'INFO'}, f"Keyframe added to Unhide in Render for {len(selected_objects)} objects")
        return {'FINISHED'}

class OBJECT_OT_set_hide_render_keyframe(bpy.types.Operator):
    bl_label = "Set Hide in Render Keyframe"
    bl_idname = "object.set_hide_render_keyframe"
    bl_description = "Hide in Render and set keyframe for Show in Render option for selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            # Ensure object is hidden in render
            obj.hide_render = True
            # Set a keyframe for the hidden state
            obj.keyframe_insert(data_path="hide_render")
        
        self.report({'INFO'}, f"Keyframe added to Hide in Render for {len(selected_objects)} objects")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_PT_render_visibility_panel)
    bpy.utils.register_class(OBJECT_OT_set_unhide_render_keyframe)
    bpy.utils.register_class(OBJECT_OT_set_hide_render_keyframe)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_render_visibility_panel)
    bpy.utils.unregister_class(OBJECT_OT_set_unhide_render_keyframe)
    bpy.utils.unregister_class(OBJECT_OT_set_hide_render_keyframe)

if __name__ == "__main__":
    register()
