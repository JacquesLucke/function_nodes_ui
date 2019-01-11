import bpy
from .. base import FunctionNode
from .. ir import IRNode

class VectorMathNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_VectorMathNode"
    bl_label = "Vector Math"

    def create(self):
        self.inputs.new("fn_VectorSocket", "A")
        self.inputs.new("fn_VectorSocket", "B")
        self.outputs.new("fn_VectorSocket", "Result")

    def build_graph(self):
        irnode = IRNode("add_vec3", amount=2)
        irnode.map_input(0, self.inputs[0])
        irnode.map_input(1, self.inputs[1])
        irnode.map_output(0, self.outputs[0])
        yield irnode