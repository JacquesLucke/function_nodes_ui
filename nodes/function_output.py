import bpy
from .. base import Node

class FunctionOutputNode(Node, bpy.types.Node):
    bl_idname = "fn_FunctionOutputNode"
    bl_label = "Function Output"

    def create(self):
        self.inputs.new("fn_VectorSocket", "Result")