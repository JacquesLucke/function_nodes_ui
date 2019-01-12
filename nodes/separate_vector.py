import bpy
from .. base import FunctionNode
from .. import ir

class SeparateVectorNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_SeparateVectorNode"
    bl_label = "Separate Vector"

    def create(self):
        self.inputs.new("fn_VectorSocket", "Result")
        self.outputs.new("fn_FloatSocket", "X")
        self.outputs.new("fn_FloatSocket", "Y")
        self.outputs.new("fn_FloatSocket", "Z")

    def build_graph(self):
        return self.graph_from_self("separate_vec3", self.name)