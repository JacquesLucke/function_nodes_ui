import bpy
from bpy.props import *
from .. base import Socket
from .. import ir

class IntegerSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "fn_IntegerSocket"
    color = (0.4, 0.4, 0.7, 1)

    value: IntProperty(name="Value", default=0, update=Socket.property_changed)

    def draw_property(self, layout, text, node):
        layout.prop(self, "value", text=text)

    def build_input_graph(self):
        irnode = ir.Node("int_input", f"Int: {self.name}", number=self.value)
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Output(0), (self, "INPUT"))
        return graph

    def build_pass_through_graph(self):
        irnode = ir.Node("pass_through_int", "Int Pass")
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Input(0), (self, "PASS_IN"))
        graph.add_link_hint(irnode.Output(0), (self, "PASS_OUT"))
        return graph