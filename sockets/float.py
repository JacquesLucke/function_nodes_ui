import bpy
from bpy.props import *
from .. base import Socket
from .. ir import IRNode

class FloatSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "fn_FloatSocket"
    color = (0, 0, 0, 1)

    value: FloatProperty(name="Value", default=0.0, update=Socket.property_changed)

    def draw_property(self, layout, text, node):
        layout.prop(self, "value", text=text)

    def build_input_graph(self):
        irnode = IRNode("float_input", number=self.value)
        irnode.map_output(0, self)
        yield irnode

    def build_final_graph(self):
        irnode = IRNode("pass_through_float")
        irnode.map_input(0, self)
        yield irnode
