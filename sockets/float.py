import bpy
from bpy.props import *
from .. base import Socket
from .. import ir

class FloatSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "fn_FloatSocket"
    color = (0, 0, 0, 1)

    value: FloatProperty(name="Value", default=0.0, update=Socket.property_changed)

    def draw_property(self, layout, text, node):
        layout.prop(self, "value", text=text)

    def build_input_graph(self):
        irnode = ir.Node("float_input", f"Float: {self.name}", number=self.value)
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Output(0), (self, "INPUT"))
        return graph

    def build_pass_through_graph(self):
        irnode = ir.Node("pass_through_float", "Float Pass")
        graph = ir.Graph()
        graph.add_node(irnode)
        graph.add_link_hint(irnode.Input(0), (self, "PASS_IN"))
        graph.add_link_hint(irnode.Output(0), (self, "PASS_OUT"))
        return graph