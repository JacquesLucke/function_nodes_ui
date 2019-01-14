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

class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.link_hints_by_socket = defaultdict(list)
        self.sockets_by_link_hint = defaultdict(list)

    def add_node(self, irnode):
        self.nodes.append(irnode)

    def add_link(self, from_socket, to_socket):
        self.links.append(Link(from_socket, to_socket))

    def add_link_hint(self, socket, link_hint):
        self.link_hints_by_socket[socket].append(link_hint)
        self.sockets_by_link_hint[link_hint].append(socket)

    def get_socket_with_link_hint(self, link_hint):
        sockets = self.get_sockets_with_link_hint(link_hint)
        if len(sockets) != 1:
            raise Exception(f"excepted there to be exactly one socket with hint {repr(link_hint)}, there are {len(sockets)}")
        return sockets[0]

    def get_sockets_with_link_hint(self, link_hint):
        return self.sockets_by_link_hint[link_hint]

    def get_link_hint_of_socket(self, socket):
        hints = self.link_hints_by_socket[socket]
        assert len(hints) == 1
        return hints[0]

    def add_graph(self, graph):
        self.nodes += graph.nodes
        self.links += graph.links
        for link_hint, sockets in graph.sockets_by_link_hint.items():
            self.sockets_by_link_hint[link_hint].extend(sockets)
        for socket, link_hints in graph.link_hints_by_socket.items():
            self.link_hints_by_socket[socket].extend(link_hints)

    @classmethod
    def join(cls, graphs):
        full_graph = Graph()
        for graph in graphs:
            full_graph.add_graph(graph)
        return full_graph

def do_linking(graph, orig_tree):
    input_node = find_node_of_type(orig_tree, "fn_FunctionInputNode")
    for socket in input_node.outputs:
        graph.add_graph(socket.build_input_graph())
        graph.add_link_hint(graph.get_socket_with_link_hint((socket, "INPUT")), socket)

    output_node = find_node_of_type(orig_tree, "fn_FunctionOutputNode")
    for socket in output_node.inputs:
        graph.add_graph(socket.build_pass_through_graph())
        graph.add_link_hint(graph.get_socket_with_link_hint((socket, "PASS_IN")), socket)

    for orig_link in orig_tree.links:
        from_socket = graph.get_socket_with_link_hint(orig_link.from_socket)
        for to_socket in graph.get_sockets_with_link_hint(orig_link.to_socket):
            graph.add_link(from_socket, to_socket)

    for orig_node in orig_tree.nodes:
        for orig_socket in orig_node.inputs:
            if orig_socket.is_linked:
                continue

            graph.add_graph(orig_socket.build_input_graph())

            from_socket = graph.get_socket_with_link_hint((orig_socket, "INPUT"))
            for to_socket in graph.get_sockets_with_link_hint(orig_socket):
                graph.add_link(from_socket, to_socket)

    time_input = Node("float_input", "Time", number=0)
    graph.add_node(time_input)
    graph._time_input_node = time_input
    for socket in graph.get_sockets_with_link_hint("TIME"):
        graph.add_link(time_input.Output(0), socket)


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
        s = graph.get_socket_with_link_hint((socket, "INPUT"))
        yield {
            "node" : index_by_node[s.node],
            "is_output" : s.is_output,
            "index" : s.index
        }

    yield {
        "node" : index_by_node[graph._time_input_node],
        "is_output" : True,
        "index" : 0
    }

def to_blender_format__outputs(graph, index_by_node, orig_tree):
    output_node = find_node_of_type(orig_tree, "fn_FunctionOutputNode")
    for socket in output_node.inputs:
        s = graph.get_socket_with_link_hint((socket, "PASS_IN"))
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

