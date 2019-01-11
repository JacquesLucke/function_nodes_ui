import bpy
from .. base import Node

class FunctionInputNode(Node, bpy.types.Node):
    bl_idname = "fn_FunctionInputNode"
    bl_label = "Function Input"

    def create(self):
        self.outputs.new("fn_VectorSocket", "Position")
        self.outputs.new("fn_FloatSocket", "Control")