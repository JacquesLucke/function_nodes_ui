import bpy
from .. base import FunctionNode
from .. import ir

class FloatMathNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_FloatMathNode"
    bl_label = "Float Math"

    def create(self):
        self.inputs.new("fn_FloatSocket", "A")
        self.inputs.new("fn_FloatSocket", "B")
        self.outputs.new("fn_FloatSocket", "Result")

    def build_graph(self):
        return self.graph_from_self("add_floats", amount=2)