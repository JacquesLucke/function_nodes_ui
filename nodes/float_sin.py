import bpy
from .. base import FunctionNode
from .. import ir

class SinFloatNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_SinFloatNode"
    bl_label = "Sin Float"

    def create(self):
        self.inputs.new("fn_FloatSocket", "Value")
        self.outputs.new("fn_FloatSocket", "Result")

    def build_graph(self):
        return self.graph_from_self("sin_float")

class SinTimeNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_SinTimeNode"
    bl_label = "Sin Time"

    def create(self):
        self.inputs.new("fn_FloatSocket", "Offset")
        self.outputs.new("fn_FloatSocket", "Sin Time")

    def build_graph(self):
        sin = ir.Node("sin_float", "Sin")
        add = ir.Node("add_floats", "Add", amount=2)

        graph = ir.Graph()
        graph.add_node(sin)
        graph.add_node(add)

        graph.add_link(sin.Output(0), add.Input(1))

        graph.add_link_hint(sin.Input(0), "TIME")
        graph.add_link_hint(add.Input(0), self.inputs[0])
        graph.add_link_hint(add.Output(0), self.outputs[0])

        return graph