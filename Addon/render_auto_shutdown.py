import bpy
import os
import platform
from threading import Timer

class RenderAutoShutdownPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport's N-Panel for Auto Shutdown"""
    bl_label = "Render Auto Shutdown"
    bl_idname = "VIEW3D_PT_render_auto_shutdown"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Xtreame"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Checkbox for enabling/disabling auto shutdown
        layout.prop(scene, "auto_shutdown_enabled")
        layout.prop(scene, "shutdown_delay")

def delayed_shutdown():
    os_platform = platform.system()
    if os_platform == 'Windows':
        os.system("shutdown /s /f /t 0")
    elif os_platform == 'Linux' or os_platform == 'Darwin':  # Darwin is macOS
        os.system("sudo shutdown -h now")

def render_complete_handler(scene):
    # If auto shutdown is enabled, wait for the delay and then shut down
    if scene.auto_shutdown_enabled:
        delay = scene.shutdown_delay
        print(f"Render complete. Shutting down in {delay} seconds...")
        Timer(delay, delayed_shutdown).start()

def register():
    bpy.utils.register_class(RenderAutoShutdownPanel)
    bpy.types.Scene.auto_shutdown_enabled = bpy.props.BoolProperty(
        name="Enable Auto Shutdown",
        description="Automatically shut down the computer after render completes",
        default=False
    )
    bpy.types.Scene.shutdown_delay = bpy.props.FloatProperty(
        name="Shutdown Delay",
        description="Delay before shutdown in seconds after render completes",
        default=5.0,
        min=0.0,
        max=60.0
    )
    bpy.app.handlers.render_complete.append(render_complete_handler)

def unregister():
    bpy.utils.unregister_class(RenderAutoShutdownPanel)
    del bpy.types.Scene.auto_shutdown_enabled
    del bpy.types.Scene.shutdown_delay
    bpy.app.handlers.render_complete.remove(render_complete_handler)

if __name__ == "__main__":
    register()
