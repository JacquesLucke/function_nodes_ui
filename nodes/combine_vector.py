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
        irnode = ir.Node("combine_vec3", self.name)
        graph = ir.PartialGraph()
        graph.add_node(irnode)
        graph.add_socket_note(irnode.Input(0), self.inputs[0])
        graph.add_socket_note(irnode.Input(1), self.inputs[1])
        graph.add_socket_note(irnode.Input(2), self.inputs[2])
        graph.add_socket_note(irnode.Output(0), self.outputs[0])
        return graph