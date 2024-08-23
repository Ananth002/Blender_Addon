bl_info = {
    "name": "Scene Status",
    "blender": (2, 80, 0),
    "category": "Scene",
    "author": "Ananth",
    "description": "Counts various types of objects and displays statistics including vertices, edges, faces, triangles, image textures, and materials in the scene. Provides an option to delete non-used materials.",
    "version": (2, 1),
    "location": "View3D > N-panel > Scene Stats",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy
import requests
import os
import zipfile

UPDATE_URL = "https://raw.githubusercontent.com/Ananth002/Blender_Addon/main/version.txt"
DOWNLOAD_URL = "https://github.com/user-attachments/files/16724438/Scence.status.zip

class SceneStatsProperties(bpy.types.PropertyGroup):
    show_selected_stats: bpy.props.BoolProperty(
        name="Selected Object Statistics",
        description="Enable to display statistics for the selected object",
        default=False
    )
    show_objects: bpy.props.BoolProperty(
        name="Show Objects",
        description="Enable to display statistics for the objects",
        default=False
    )
    show_statics: bpy.props.BoolProperty(
        name="Show Statistics",
        description="Enable to display statistics for the objects",
        default=False
    )
    calculate_modifiers: bpy.props.BoolProperty(
        name="Statistics with Modifiers",
        description="Enable statistics including modifiers (may affect performance)",
        default=False
    )

class OBJECT_PT_scene_stats(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport's Tool Shelf"""
    bl_label = "Scene Statistics"
    bl_idname = "OBJECT_PT_scene_status"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Xtreame"
    
    @staticmethod
    def get_mesh_data(obj, use_modifiers):
        """Returns evaluated mesh data if use_modifiers is True, else returns original data."""
        if use_modifiers:
            depsgraph = bpy.context.evaluated_depsgraph_get()
            object_eval = obj.evaluated_get(depsgraph)
            return object_eval.to_mesh()
        else:
            return obj.data
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        # Scene Statistics
        total_objects = len(scene.objects)
        mesh_objects = [obj for obj in scene.objects if obj.type == 'MESH']
        light_count = len([obj for obj in scene.objects if obj.type == 'LIGHT'])
        camera_count = len([obj for obj in scene.objects if obj.type == 'CAMERA'])
        empty_count = len([obj for obj in scene.objects if obj.type == 'EMPTY'])
        curve_count = len([obj for obj in scene.objects if obj.type == 'CURVE'])
        
        total_faces = sum(len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).polygons) for obj in mesh_objects if obj.data)
        total_edges = sum(len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).edges) for obj in mesh_objects if obj.data)
        total_vertices = sum(len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).vertices) for obj in mesh_objects if obj.data)
        total_triangles = sum(len(poly.vertices) - 2 for obj in mesh_objects for poly in self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).polygons if obj.data)
        
        material_set = {slot.material.name for obj in mesh_objects for slot in obj.material_slots if slot.material}
        total_materials = len(material_set)

        image_textures = {node.image.name for mat in bpy.data.materials for node in (mat.node_tree.nodes if mat.node_tree else []) if node.type == 'TEX_IMAGE' and node.image}
        total_image_textures = len(image_textures)

        used_materials = {slot.material for obj in mesh_objects for slot in obj.material_slots if slot.material}
        non_used_material_count = len(set(bpy.data.materials) - used_materials)

        layout.label(text="Scene Overview", icon='SCENE_DATA')
        row = layout.row()
        row.prop(context.scene.scene_stats_props, "show_objects", text="Objects")
        if context.scene.scene_stats_props.show_objects and obj:
            layout.label(text=f"Total Objects: {total_objects}", icon='OBJECT_DATAMODE')
            layout.label(text=f"Mesh Objects: {len(mesh_objects)}", icon='MESH_DATA')
            layout.label(text=f"Lights: {light_count}", icon='LIGHT')
            layout.label(text=f"Cameras: {camera_count}", icon='CAMERA_DATA')
            layout.label(text=f"Empties: {empty_count}", icon='EMPTY_DATA')
            layout.label(text=f"Curves: {curve_count}", icon='OUTLINER_DATA_CURVE')
            layout.separator()
        row = layout.row()
        row.prop(context.scene.scene_stats_props, "show_statics", text="Statistics")
        if context.scene.scene_stats_props.show_statics and obj:
            layout.label(text="Mesh Statistics", icon='MESH_CUBE')
            layout.label(text=f"Total Vertices: {total_vertices}", icon='VERTEXSEL')
            layout.label(text=f"Total Edges: {total_edges}", icon='EDGESEL')
            layout.label(text=f"Total Faces: {total_faces}", icon='FACESEL')
            layout.label(text=f"Total Triangles: {total_triangles}", icon='TRIA_RIGHT')
            layout.separator()
        layout.label(text=f"Total Materials: {total_materials}", icon='MATERIAL_DATA')
        layout.label(text=f"Image Textures: {total_image_textures}", icon='TEXTURE')
        layout.label(text=f"Non-Used Materials: {non_used_material_count}", icon='CANCEL')

        row = layout.row()
        row.prop(context.scene.scene_stats_props, "show_selected_stats", text="Selected Object Statistics")
        row = layout.row()
        row.prop(context.scene.scene_stats_props, "calculate_modifiers", text="Statistics with Modifiers")

        if context.scene.scene_stats_props.show_selected_stats and obj and obj.type == 'MESH':
            layout.separator()
            layout.label(text=f"Selected Object: {obj.name}", icon='OBJECT_DATA')
            layout.label(text=f"Vertices: {len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).vertices)}", icon='VERTEXSEL')
            layout.label(text=f"Edges: {len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).edges)}", icon='EDGESEL')
            layout.label(text=f"Faces: {len(self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).polygons)}", icon='FACESEL')
            layout.label(text=f"Triangles: {sum(len(poly.vertices) - 2 for poly in self.get_mesh_data(obj, context.scene.scene_stats_props.calculate_modifiers).polygons)}", icon='TRIA_RIGHT')

            obj_image_textures = {node.image.name for slot in obj.material_slots if slot.material and slot.material.node_tree for node in slot.material.node_tree.nodes if node.type == 'TEX_IMAGE' and node.image}
            obj_image_texture_count = len(obj_image_textures)
            layout.label(text=f"Image Textures: {obj_image_texture_count}", icon='TEXTURE')
            layout.label(text=f"Materials: {len(obj.material_slots)}", icon='MATERIAL')

        # Add an update button
        layout.separator()
        layout.label(text="Update Add-on", icon='FILE_REFRESH')
        row = layout.row()
        row.operator("wm.check_for_update", text="Check for Update", icon='URL')


class WM_OT_check_for_update(bpy.types.Operator):
    """Check for and download the latest version of the add-on"""
    bl_idname = "wm.check_for_update"
    bl_label = "Check for Update"
    
    def execute(self, context):
        try:
            # Get the current version
            current_version = bl_info["version"]
            
            # Get the latest version number from the remote server
            response = requests.get(UPDATE_URL)
            latest_version = tuple(map(int, response.text.strip().split(".")))
            
            if latest_version > current_version:
                # Prompt user to download the latest version
                self.report({'INFO'}, f"New version available: {latest_version}. Downloading...")
                self.download_update()
            else:
                self.report({'INFO'}, "You are already using the latest version.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to check for updates: {str(e)}")
        
        return {'FINISHED'}
    
    def download_update(self):
        try:
            # Download the latest version
            response = requests.get(DOWNLOAD_URL)
            zip_path = os.path.join(bpy.app.tempdir, "Scene status.zip")
            
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # Extract the downloaded zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_path = bpy.utils.user_resource('SCRIPTS', "addons")
                zip_ref.extractall(extract_path)
            
            self.report({'INFO'}, "Update downloaded and installed. Please restart Blender.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to download the update: {str(e)}")


classes = [
    OBJECT_PT_scene_stats,
    SceneStatsProperties,
    WM_OT_check_for_update,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_stats_props = bpy.props.PointerProperty(type=SceneStatsProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_stats_props

if __name__ == "__main__":
    register()
