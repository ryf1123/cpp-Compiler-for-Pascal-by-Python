#/usr/bin/env python
# -*- coding: UTF-8 -*-
# 编译原理大作业 SPL based on Python
# 任宇凡 刘洪甫 邱兆林

# This file is the lex parse part of the whole project

import ply.lex as lex
import sys
from reserved import reserved

tokens = [
    # from not reserved
    # 其他不在下面正则表达式中定义的
    'NUMBER',
    'ID',
    'empty',# 不确定是不是这么写

    # 这些是从下面的正则表达式中的
    'LP',         
    'RP',         
    'LB',         
    'RB',         
    'DOT',         
    'COMMA',     
    'COLON',     
    'MUL',         
    'DIV',         
    'UNEQUAL',     
    'OPERATOR_NOT',         
    'PLUS',         
    'MINUS',     
    'GE',         
    'GT',         
    'LE',         
    'LT',         
    'EQUAL',     
    'ASSIGN',     
    'MOD',         
    'DOTDOT',     
    'SEMI'         
] + list(reserved.values())

print(tokens)
print()
print(reserved)

class lexer:
    tokens = tokens
    # 简单token的正则表达式
    # 第一列 
    t_LP            = r'\(' 
    t_RP            = r'\)' 
    t_LB            = r'\[' 
    t_RB            = r'\]' 
    t_DOT           = r'\.'# 是这个吧？ 
    t_COMMA         = r'\,' 
    t_COLON         = r'\;' 
    t_MUL           = r'\*' 
    t_DIV           = r'\/' 
    t_UNEQUAL       = r'\<\>' 
    t_OPERATOR_NOT  = 'NOT'  # 其实应该是和Keyword的not不同的，所以不会重复
    # 第二列
    t_PLUS          = r'\+'
    t_MINUS         = r'\-'
    t_GE            = r'\>\='
    t_GT            = r'\>'
    t_LE            = r'\<\='
    t_LT            = r'\<'
    t_EQUAL         = r'\='
    t_ASSIGN        = r'\:\='
    t_MOD           = 'MOD'
    t_DOTDOT        = r'\.\.'
    t_SEMI          = r'\;'

    # 系统函数还未实现
    def t_ID(self, t):
        r'[A-Za-z](_?[A-Za-z0-9])*'#(\.[A-Za-z](_?[A-Za-z0-9])*)?'
        t.type = reserved.get(t.value.lower(), 'ID')
        return t

    def t_NUMBER(self, t):
        r'[-]?[0-9]*[0-9]+'
        return t

    def t_error(self, t):
        print("[  Illegal character  ] '%s'" % t.value[0])
        t.lexer.skip(1)
    
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore  = ' \t'

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    
    def test(self, data):
        
        self.lexer.input(data)
        # while True:
        #      tok = lexer.token()
        #      if not tok: break
        #      print tok
        # 上面一种写法的简写
        for tok in self.lexer:
            print (tok)

lexer = lexer()
lexer.build()
#lexer = lex.lex()

if __name__ == '__main__':  
    m = mylexer()
    m.build()
    #m.test(" + ")
    print("\n\n\nBegins~")
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
    else:
        data = ""
        while 1:
            try:
                data += raw_input() + "\n"
            except:
                break
    m.test(data)

