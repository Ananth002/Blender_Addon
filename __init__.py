bl_info = {
    "name": "Xtreame",
    "author": "Ananth",
    "version": (1, 2),
    "blender": (3, 6, 0),
    "description": "Saving Tools",
    "category": "Object",
}

import bpy
import os
import platform
from threading import Timer

# Import the necessary operators and panels for the addon
from .Addon import render_auto_shutdown
from .Addon import collection_remove_empty
from .Addon import render_keyframe

def register():
    # Register the operators and panels
    render_auto_shutdown.register()
    collection_remove_empty.register()
    render_keyframe.register()

def unregister():
    # Unregister the operators and panels
    render_auto_shutdown.unregister()
    collection_remove_empty.unregister()
    render_keyframe.unregister()

if __name__ == "__main__":
    register()
