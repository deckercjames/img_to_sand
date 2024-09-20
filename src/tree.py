
from collections import namedtuple

# TreeNode = namedtuple("TreeNode", ["node_data", "children"])

class TreeNode:
    def __init__(self, node_data, children=[]):
        self.node_data = node_data
        self.children = children
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def print_tree(self, indent=0):
        print("    "*indent + str(self.node_data))
        for child in self.children:
            child.print_tree(indent+1)
        