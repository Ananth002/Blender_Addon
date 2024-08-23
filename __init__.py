import bpy

from . import Addon
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
