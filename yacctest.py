#/usr/bin/env python
# -*- coding: UTF-8 -*-
# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens
from tree_visual import *

# def p_expression_plus(p):
#     'expression : expression PLUS term'
#     p[0] = p[1] + p[3]

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = Node("plus")([p[1], p[3]])

# def p_expression_minus(p):
#     'expression : expression MINUS term'
#     p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = Node("term")([p[1]])

# def p_term_times(p):
#     'term : term TIMES factor'
#     p[0] = p[1] * p[3]

# def p_term_div(p):
#     'term : term DIVIDE factor'
#     p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = Node("factor")([])

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = Node("num")([])

# def p_factor_expr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print ("Syntax error in input!")

# class Node:
#     def __init__(self,type,children=None,leaf=None):
#         self.type = type
#         if children:
#             self.children = children
#         else:
#             self.children = [ ]
#         self.leaf = leaf
#     def display(self):
#         if self!= None:     
#             print(self.type)
#         if self.children!=None:
#             for index in range(len(self.children)):
#                 #print(index, self.children)
#                 try:
#                     self.children[index].display()
#                 except Exception as e:
#                     pass
#                 else:
#                     pass
#                     #print("error", self.children, self.children[index])
#                 finally:
#                     pass
#                 print()


# def p_expression_binop(p):
#     '''expression  : expression PLUS expression
#                    | expression MINUS expression
#                    | expression TIMES expression
#                    | expression DIVIDE expression'''

#     p[0] = Node("binop", [p[1],p[3]], p[2])

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(drawTree(result))
   # result.display()
   #print (result)