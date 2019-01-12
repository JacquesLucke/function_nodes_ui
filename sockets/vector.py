import bpy
from bpy.props import *
from .. base import Socket
from .. import ir

class VectorSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "fn_VectorSocket"
    color = (0.3, 0.3, 0.8, 1)

    value: FloatVectorProperty(name="Value", size=3, update=Socket.property_changed)

    def draw_property(self, layout, text, node):
        layout.column(align=True).prop(self, "value", text=text)

    def build_input_graph(self):
        irnode = ir.Node("vec3_input", x=self.value[0], y=self.value[1], z=self.value[2])
        graph = ir.PartialGraph()
        graph.add_node(irnode)
        graph.add_socket_note(irnode.Output(0), (self, "INPUT"))
        return graph

    def build_pass_through_graph(self):
        irnode = ir.Node("pass_through_vec3")
        graph = ir.PartialGraph()
        graph.add_node(irnode)
        graph.add_socket_note(irnode.Input(0), (self, "PASS_IN"))
        graph.add_socket_note(irnode.Output(0), (self, "PASS_OUT"))
        return graph