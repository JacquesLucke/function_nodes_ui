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
        irnode = ir.Node("separate_vec3", self.name)
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Input(0), self.inputs[0])
        graph.add_link_hint(irnode.Output(0), self.outputs[0])
        graph.add_link_hint(irnode.Output(1), self.outputs[1])
        graph.add_link_hint(irnode.Output(2), self.outputs[2])
        return graph