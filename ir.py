INPUT = False
OUTPUT = True

class IRNode:
    def __init__(self, name, **settings):
        self.name = name
        self.settings = settings
        self.mappings = dict()
        self.debug_name = None

    def map_input(self, index, socket):
        self.mappings[(INPUT, index)] = socket

    def map_output(self, index, socket):
        self.mappings[(OUTPUT, index)] = socket

    def to_json(self):
        data = {"type" : self.name, **self.settings}
        if self.debug_name is not None:
            data["debug_name"] = self.debug_name
        return data

    def set_debug_name(self, name):
        self.debug_name = name
