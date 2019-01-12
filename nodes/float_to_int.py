import bpy
from .. base import FunctionNode
from .. import ir

class FloatToIntNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_FloatToIntNode"
    bl_label = "Float to Int"

    def create(self):
        self.inputs.new("fn_FloatSocket", "In")
        self.outputs.new("fn_IntegerSocket", "Out")

    def build_graph(self):
        irnode = ir.Node("float_to_int", self.name)
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Input(0), self.inputs[0])
        graph.add_link_hint(irnode.Output(0), self.outputs[0])
        return graph