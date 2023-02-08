"""Node class for a BVH file."""


class BVHnode:
    def __init__(self, name, parent=None):
        self.parent = parent
        """The parent node of this node. None if this is the root node."""
        self.children = []
        self.offset = (0, 0, 0)
        self.channels = []
        self.name = name
        self.position = None
        self.rotation = None
        self.absolute_transformation = None

        if parent is not None:
            parent.children.append(self)

    def __repr__(self): return f'<BVH {self.name}>'

    def __iter__(self): return self.children.__iter__()

    def get_root(self): return self if self.parent is None else self.parent.get_root()
