import bpy
import os

from . import Addon
 addon_directory=os.path.dirname(__Addon__)
bl_info={
  "name": "Scene status",
}
addon_keymaps = []
def register():
  Addon.register()
def unregister():
  Addon.unregister()
if __name__=="__main__":
  register()
