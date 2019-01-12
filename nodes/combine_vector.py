import bpy
from .. base import FunctionNode
from .. import ir

class CombineVectorNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_CombineVectorNode"
    bl_label = "Combine Vector"

    def create(self):
        self.inputs.new("fn_FloatSocket", "X")
        self.inputs.new("fn_FloatSocket", "Y")
        self.inputs.new("fn_FloatSocket", "Z")
        self.outputs.new("fn_VectorSocket", "Result")

    def build_graph(self):
        return self.graph_from_self("combine_vec3", self.name)