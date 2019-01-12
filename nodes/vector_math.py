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
        irnode = ir.Node("add_vec3", amount=2)
        graph = ir.PartialGraph()
        graph.add_node(irnode)
        graph.add_socket_note(irnode.Input(0), self.inputs[0])
        graph.add_socket_note(irnode.Input(1), self.inputs[1])
        graph.add_socket_note(irnode.Output(0), self.outputs[0])
        return graph