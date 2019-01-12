import bpy
from .. base import FunctionNode
from .. import ir

class SwitchNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_SwitchNode"
    bl_label = "Switch"

    def create(self):
        self.inputs.new("fn_IntegerSocket", "Selector")
        self.inputs.new("fn_FloatSocket", "Default")
        self.inputs.new("fn_FloatSocket", "Case 0")
        self.inputs.new("fn_FloatSocket", "Case 1")
        self.inputs.new("fn_FloatSocket", "Case 2")
        self.outputs.new("fn_FloatSocket", "Result")

    def build_graph(self):
        return self.graph_from_self("switch_float", self.name, amount=3)