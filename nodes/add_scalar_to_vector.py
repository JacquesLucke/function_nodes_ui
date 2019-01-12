import bpy
from .. base import FunctionNode
from .. import ir

class AddScalarToVectorNode(FunctionNode, bpy.types.Node):
    bl_idname = "fn_AddScalarToVectorNode"
    bl_label = "Add Scalar to Vector"

    def create(self):
        self.inputs.new("fn_VectorSocket", "Vector")
        self.inputs.new("fn_FloatSocket", "Value")
        self.outputs.new("fn_VectorSocket", "Result")

    def build_graph(self):
        combine = ir.Node("combine_vec3", "Combine")
        add = ir.Node("add_vec3", "Add Vectors", amount=2)
        graph = ir.PartialGraph()

        graph.add_node(combine)
        graph.add_node(add)

        graph.add_link(combine.Output(0), add.Input(1))

        graph.add_link_hint(combine.Input(0), self.inputs[1])
        graph.add_link_hint(combine.Input(1), self.inputs[1])
        graph.add_link_hint(combine.Input(2), self.inputs[1])
        graph.add_link_hint(add.Input(0), self.inputs[0])
        graph.add_link_hint(add.Output(0), self.outputs[0])

        return graph