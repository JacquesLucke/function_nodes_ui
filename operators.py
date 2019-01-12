import bpy
from bpy.props import *
import json
import functions
from pprint import pprint
from dataclasses import dataclass
from . import ir
from . base import FunctionNode

@dataclass
class SocketID:
    node_index : int
    is_output : bool
    socket_index : int

class CompileFunctionOperator(bpy.types.Operator):
    bl_idname = "fn.compile_function"
    bl_label = "Compile Function"

    tree_name: StringProperty()

    def execute(self, context):
        tree = bpy.data.node_groups[self.tree_name]
        graphs = [node.build_graph() for node in tree.nodes if isinstance(node, FunctionNode)]
        graph = ir.Graph.join(graphs)
        ir.do_linking(graph, tree)
        blender_format = ir.to_blender_format(graph, tree)
        print(json.dumps(blender_format, indent=2))
        functions.set_function_graph(blender_format)
        return {'FINISHED'}
