import itertools
from dataclasses import dataclass
from collections import defaultdict
from pprint import pprint

@dataclass
class AnySocket:
    node: "IRNode"
    is_output: bool
    index: int

    def __hash__(self):
        return hash((id(self.node), self.is_output, self.index))

@dataclass
class Link:
    from_socket: AnySocket
    to_socket: AnySocket

class Node:
    def __init__(self, type_name, debug_name="", **settings):
        self.type_name = type_name
        self.debug_name = debug_name
        self.settings = settings

    def Input(self, index):
        return AnySocket(self, False, index)

    def Output(self, index):
        return AnySocket(self, True, index)

    def to_blender_format(self):
        data = {"type" : self.type_name, **self.settings}
        if self.debug_name is not None:
            data["debug_name"] = self.debug_name
        return data

class PartialGraph:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.notes_by_socket = defaultdict(list)
        self.sockets_by_note = defaultdict(list)

    def add_node(self, irnode):
        self.nodes.append(irnode)

    def add_link(self, from_socket, to_socket):
        self.links.append(Link(from_socket, to_socket))

    def add_socket_note(self, socket, note):
        self.notes_by_socket[socket].append(note)
        self.sockets_by_note[note].append(socket)

    def get_socket_with_note(self, note):
        sockets = self.sockets_by_note[note]
        assert len(sockets) == 1
        return sockets[0]

    def get_note_with_socket(self, socket):
        notes = self.notes_by_socket[socket]
        assert len(notes) == 1
        return notes[0]

    def add_graph(self, graph):
        self.nodes += graph.nodes
        self.links += graph.links
        for note, sockets in graph.sockets_by_note.items():
            self.sockets_by_note[note].extend(sockets)
        for socket, notes in graph.notes_by_socket.items():
            self.notes_by_socket[socket].extend(notes)

    @classmethod
    def join(cls, graphs):
        full_graph = PartialGraph()
        for graph in graphs:
            full_graph.add_graph(graph)
        return full_graph

def do_linking(graph, orig_tree):
    input_node = find_node_of_type(orig_tree, "fn_FunctionInputNode")
    for socket in input_node.outputs:
        graph.add_graph(socket.build_input_graph())
        graph.add_socket_note(graph.get_socket_with_note((socket, "INPUT")), socket)

    output_node = find_node_of_type(orig_tree, "fn_FunctionOutputNode")
    for socket in output_node.inputs:
        graph.add_graph(socket.build_pass_through_graph())
        graph.add_socket_note(graph.get_socket_with_note((socket, "PASS_IN")), socket)

    for orig_link in orig_tree.links:
        from_socket = graph.get_socket_with_note(orig_link.from_socket)
        to_socket = graph.get_socket_with_note(orig_link.to_socket)
        graph.add_link(from_socket, to_socket)

    for orig_node in orig_tree.nodes:
        for socket in orig_node.inputs:
            if socket.is_linked:
                continue

            graph.add_graph(socket.build_input_graph())
            graph.add_link(
                graph.get_socket_with_note((socket, "INPUT")),
                graph.get_socket_with_note(socket))

def to_blender_format(graph, orig_tree):
    index_by_node = {node : i for i, node in enumerate(graph.nodes)}
    return {
        "nodes" : list(to_blender_format__nodes(graph)),
        "links" : list(to_blender_format__links(graph, index_by_node)),
        "inputs" : list(to_blender_format__inputs(graph, index_by_node, orig_tree)),
        "outputs" : list(to_blender_format__outputs(graph, index_by_node, orig_tree)),
    }

def to_blender_format__nodes(graph):
    for node in graph.nodes:
        yield node.to_blender_format()

def to_blender_format__links(graph, index_by_node):
    for link in graph.links:
        yield {
            "from_node" : index_by_node[link.from_socket.node],
            "from_index" : link.from_socket.index,
            "to_node" : index_by_node[link.to_socket.node],
            "to_index" : link.to_socket.index,
        }

def to_blender_format__inputs(graph, index_by_node, orig_tree):
    input_node = find_node_of_type(orig_tree, "fn_FunctionInputNode")
    for socket in input_node.outputs:
        s = graph.get_socket_with_note((socket, "INPUT"))
        yield {
            "node" : index_by_node[s.node],
            "is_output" : s.is_output,
            "index" : s.index
        }

def to_blender_format__outputs(graph, index_by_node, orig_tree):
    output_node = find_node_of_type(orig_tree, "fn_FunctionOutputNode")
    for socket in output_node.inputs:
        s = graph.get_socket_with_note((socket, "PASS_IN"))
        yield {
            "node" : index_by_node[s.node],
            "is_output" : s.is_output,
            "index" : s.index
        }


def find_node_of_type(tree, idname):
    for node in tree.nodes:
        if node.bl_idname == idname:
            return node
    return None

