import bpy
from bpy.props import *
import functions
from pprint import pprint
from dataclasses import dataclass

@dataclass
class SocketID:
    node_index : int
    is_output : bool
    socket_index : int

class CompileFunctionOperator(bpy.types.Operator):
    bl_idname = "fn.compile_function"
    bl_label = "Compile Function"

    tree_name = StringProperty()

    def execute(self, context):
        tree = bpy.data.node_groups[self.tree_name]
        graph = generate_node_graph_json(tree)
        pprint(graph)
        functions.set_function_graph(graph)
        return {'FINISHED'}


def generate_node_graph_json(tree):
    json_nodes, socket_mappings = gen_json_nodes(tree)
    json_links = gen_json_links(tree, socket_mappings)
    json_inputs = gen_json_inputs(tree, socket_mappings)
    json_outputs = gen_json_outputs(tree, socket_mappings)
    fix_unlinked_inputs(tree, socket_mappings, json_nodes, json_links)
    return {
        "nodes" : json_nodes,
        "links" : json_links,
        "inputs" : json_inputs,
        "outputs" : json_outputs,
    }

def gen_json_nodes(tree):
    json_nodes = []
    socket_mappings = dict()
    for node in tree.nodes:
        for irnode in gen_irnodes_for_node(node):
            irnode.set_debug_name(node.name)
            node_index = len(json_nodes)
            json_nodes.append(irnode.to_json())
            for (is_output, index), socket in irnode.mappings.items():
                socket_mappings[socket] = SocketID(node_index, is_output, index)
    return json_nodes, socket_mappings

def gen_json_links(tree, socket_mappings):
    json_links = []

    for link in tree.links:
        output = socket_mappings[link.from_socket]
        input = socket_mappings[link.to_socket]
        json_links.append({
            "from_node" : output.node_index,
            "from_index" : output.socket_index,
            "to_node" : input.node_index,
            "to_index" : input.socket_index,
        })

    return json_links

def gen_json_inputs(tree, socket_mappings):
    for node in tree.nodes:
        if node.bl_idname == "fn_FunctionInputNode":
            json_inputs = []
            for s in node.outputs:
                json_inputs.append({
                    "node" : socket_mappings[s].node_index,
                    "is_output" : socket_mappings[s].is_output,
                    "index" : socket_mappings[s].socket_index,
                })
            return json_inputs
    assert False

def gen_json_outputs(tree, socket_mappings):
    for node in tree.nodes:
        if node.bl_idname == "fn_FunctionOutputNode":
            json_outputs = []
            for s in node.inputs:
                json_outputs.append({
                    "node" : socket_mappings[s].node_index,
                    "is_output" : socket_mappings[s].is_output,
                    "index" : socket_mappings[s].socket_index,
                })
            return json_outputs
    assert False

def fix_unlinked_inputs(tree, socket_mappings, json_nodes, json_links):
    for node in tree.nodes:
        for socket in node.inputs:
            if socket.is_linked:
                continue

            final_node_index = None
            final_socket_index = None
            for irnode in socket.build_input_graph():
                irnode.set_debug_name("unlinked input")
                node_index = len(json_nodes)
                json_nodes.append(irnode.to_json())
                for (is_output, index), _ in irnode.mappings.items():
                    assert is_output
                    final_node_index = node_index
                    final_socket_index = index

            json_links.append({
                "from_node" : final_node_index,
                "from_index" : final_socket_index,
                "to_node" : socket_mappings[socket].node_index,
                "to_index" : socket_mappings[socket].socket_index,
            })

def gen_irnodes_for_node(node):
    if node.bl_idname == "fn_FunctionInputNode":
        for socket in node.outputs:
            yield from socket.build_input_graph()
    elif node.bl_idname == "fn_FunctionOutputNode":
        for socket in node.inputs:
            yield from socket.build_final_graph()
    else:
        yield from node.build_graph()