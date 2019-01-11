import bpy
from .. base import FunctionNode
from .. ir import IRNode

class FloatMathNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_FloatMathNode"
    bl_label = "Float Math"

    def create(self):
        self.inputs.new("fn_FloatSocket", "A")
        self.inputs.new("fn_FloatSocket", "B")
        self.outputs.new("fn_FloatSocket", "Result")

    def build_graph(self):
        irnode = IRNode("add_floats", amount=2)
        irnode.map_input(0, self.inputs[0])
        irnode.map_input(1, self.inputs[1])
        irnode.map_output(0, self.outputs[0])
        yield irnode