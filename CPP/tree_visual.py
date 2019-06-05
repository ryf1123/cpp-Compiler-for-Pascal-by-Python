# -*- coding: UTF-8 -*-

'''Vizualize a tree'''

import random
from itertools import (repeat, starmap)
from operator import (add)

import pydot

visu_path = './visulization/AST_graph.png'


def drawTree(tree):
    graph = pydot.Dot(graph_type='graph')
    traversal(graph, tree)
    graph.write_png(visu_path)

# FIXME: move random into utils.py


class Node(object):
    def __init__(self, t, c):
        self._type = t
        self._children = c
        self._id = "%s: %08d" % (
            self._type, round(random.random() * 100000000))

    @property
    def children(self):
        return self._children

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

# FIXME: routine_head 的其他几个分支现在全部是None
# init a pydot.graph
# traversal(order does not matters) the tree and add every edge into the graph
# draw and save the graph


def traversal(graph, node):
    print()
    print("node.type:", node.type)
    if node.children != None and node.type != "empty_production":
        print(123)
        print(node.type)
        print("node.children:", node.children)
        for child in node.children:
            # FIXME: 用于完善代码时取消忽略判断，但是真实情况应该忽略None
            if (not isinstance(child, str)):
                # if (not child == None) and (not isinstance(child, str)):
                print("node.id, child:", node.id, child, node.type)
                try:
                    edge = pydot.Edge(node.id, child.id)
                    graph.add_edge(edge)
                    traversal(graph, child)
                except Exception as identifier:
                    print("[Exception]: ", identifier)
                    # pass
            else:
                # 是str
                # FIXME: 由于常量数字非常容易重复，所以需要加上一个随机数
                edge = pydot.Edge(node.id, child+"%10d" %
                                  (round(random.random() * 100000000)))
                graph.add_edge(edge)
        print("[End of for]")
