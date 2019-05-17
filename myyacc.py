#/usr/bin/env python
# -*- coding: UTF-8 -*-
# 编译原理大作业 SPL based on Python
# 任宇凡 刘洪甫 邱兆林

# This file is the yacc parse part of the whole project
import ply.yacc as yacc
import sys
from mylex import tokens
from tree_visual import *

######## auto generated (使用脚本生成的，校对时需要小心)



######## End of auto generated

def p_if_stmt(p):
    'if_stmt: IF  expression  THEN  stmt  else_clause'
    p[0] = Node("if_stmt")([p[2], p[4], p[5]])



def p_factor_num(p):
    'factor : NUMBER'
    p[0] = # Node("num")([])

# 空产生式
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print ("Syntax error in input!")

if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
        result = parser.parse(data)
        print(result)
    else:
        while True:    
            try:
                data = raw_input('Type here > ')
            except EOFError:
                break
            if data == "q" or data =="quit":
                break
            if not data:continue

            result = parser.parse(data)    
            print(result)




















