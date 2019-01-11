import bpy
from . base import FunctionNodeTree

class FunctionNodesPanel(bpy.types.Panel):
    bl_idname = "an_PT_function_nodes"
    bl_label = "Function Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Node"

    @classmethod
    def poll(cls, context):
        return isinstance(context.space_data.node_tree, FunctionNodeTree)

    def draw(self, context):
        layout = self.layout
        layout.operator("fn.compile_function")