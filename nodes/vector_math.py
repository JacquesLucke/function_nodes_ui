import bpy
from .. base import FunctionNode
from .. import ir

class VectorMathNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_VectorMathNode"
    bl_label = "Vector Math"

    def create(self):
        self.inputs.new("fn_VectorSocket", "A")
        self.inputs.new("fn_VectorSocket", "B")
        self.outputs.new("fn_VectorSocket", "Result")

    def build_graph(self):
        return self.graph_from_self("add_vec3", amount=2)