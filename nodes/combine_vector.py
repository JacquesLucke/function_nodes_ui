import bpy
from .. base import FunctionNode
from .. ir import IRNode

class CombineVectorNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_CombineVectorNode"
    bl_label = "Combine Vector"

    def create(self):
        self.inputs.new("fn_FloatSocket", "X")
        self.inputs.new("fn_FloatSocket", "Y")
        self.inputs.new("fn_FloatSocket", "Z")
        self.outputs.new("fn_VectorSocket", "Result")

    def build_graph(self):
        irnode = IRNode("combine_vec3")
        irnode.map_input(0, self.inputs[0])
        irnode.map_input(1, self.inputs[1])
        irnode.map_input(2, self.inputs[2])
        irnode.map_output(0, self.outputs[0])
        yield irnode