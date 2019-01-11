import bpy
from bpy.props import *
from .. base import Socket
from .. ir import IRNode

class VectorSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "fn_VectorSocket"
    color = (0.3, 0.3, 0.8, 1)

    value: FloatVectorProperty(name="Value", size=3)

    def draw_property(self, layout, text, node):
        layout.column(align=True).prop(self, "value", text=text)

    def build_input_graph(self):
        irnode = IRNode("vec3_input", x=self.value[0], y=self.value[1], z=self.value[2])
        irnode.map_output(0, self)
        yield irnode

    def build_final_graph(self):
        irnode = IRNode("pass_through_vec3")
        irnode.map_input(0, self)
        yield irnode