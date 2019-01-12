import bpy
from . events import property_changed

class FunctionNodeTree(bpy.types.NodeTree):
    bl_idname = "FunctionNodeTree"
    bl_icon = "MOD_DATA_TRANSFER"
    bl_label = "Functions"

class Node:
    def init(self, context):
        self.create()

    def create(self):
        pass

    def property_changed(self, context=None):
        property_changed()

class Socket:
    color = (0, 0, 0, 0)

    def draw_color(self, context, node):
        return self.color

    def draw(self, context, layout, node, text):
        if not (self.is_linked or self.is_output) and hasattr(self, "draw_property"):
            self.draw_property(layout, text, node)
        else:
            layout.label(text=text)

    def build_input_graph(self):
        assert False

    def build_pass_through_graph(self):
        assert False

    def property_changed(self, context=None):
        property_changed()

class FunctionNode(Node):
    def build_graph(self):
        pass