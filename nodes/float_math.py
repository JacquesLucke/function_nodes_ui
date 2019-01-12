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
        irnode = ir.Node("add_floats", amount=2)
        graph = ir.PartialGraph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Input(0), self.inputs[0])
        graph.add_link_hint(irnode.Input(1), self.inputs[1])
        graph.add_link_hint(irnode.Output(0), self.outputs[0])
        return graph