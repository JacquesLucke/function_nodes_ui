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
        return self.graph_from_self("float_to_int", self.name)