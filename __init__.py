bl_info = {
    "name":        "Function Nodes",
    "description": "",
    "author":      "Jacques Lucke",
    "version":     (0, 0, 1),
    "blender":     (2, 80, 0),
    "location":    "Node Editor",
    "category":    "Node",
    "warning":     "This is only a prototype."
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
