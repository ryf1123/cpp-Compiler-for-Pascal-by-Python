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
        self.type = t
        self.children = c
        self.id = "%s: %08d" % (
            self.type, round(random.random() * 100000000))

# FIXME: routine_head 的其他几个分支现在全部是None
# init a pydot.graph
# traversal(order does not matters) the tree and add every edge into the graph
# draw and save the graph


def traversal(graph, node):
    if node.children != None and node.type != "empty_production":
        for child in node.children:
            #: 用于完善代码时取消忽略判断，但是真实情况应该忽略None
            if (not isinstance(child, str)):
                try:
                    edge = pydot.Edge(node.id, child.id)
                    graph.add_edge(edge)
                    traversal(graph, child)
                except Exception as identifier:
                    print("[Exception]: ", identifier)
                    # pass
            else:
                #: 由于常量数字非常容易重复，所以需要加上一个随机数
                edge = pydot.Edge(node.id, child+"%10d" %
                                  (round(random.random() * 100000000)))
                graph.add_edge(edge)
