class Node(object):
    def __init__(self, t, c):
        self._children = c
        self._type = t
        
    @property
    def children(self):
        return self._children

    @property
    def type(self):
        return self._type

a = Node(t='a',c=None)
# print(a.children, a.type)

c = Node(t='c',c=None)
# print(a.children, a.type)

b = Node(t='b',c=[a, c])
print(b.children, b.type)

def traversal(node):
    print(node.type)
    if not node.children == None:
        for child in node.children:
            
            traversal(child)

traversal(b)