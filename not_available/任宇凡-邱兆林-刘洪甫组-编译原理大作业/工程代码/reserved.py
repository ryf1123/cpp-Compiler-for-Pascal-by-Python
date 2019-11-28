# /usr/bin/env python
# -*- coding: UTF-8 -*-

# 编译原理大作业 SPL based on Python
# 任宇凡 刘洪甫 邱兆林

# This file is the reserved token set, which will be includes in the lex part.

reserved = {
    'int': "INTEGER",
    # 'real':"REAL",
    # 'char':"CHAR",
    'string': "STRING",
    # 其中不需要实现的已经注释掉了
    "and": "AND",
    "array": "ARRAY",
    "begin": "BEGIN",
    "case": "CASE",
    "const": "CONST",
    "div": "DIV",
    "do": "DO",
    "downto": "DOWNTO",
    "else": "ELSE",
    "end": "END",
    "for": "FOR",
    "function": "FUNCTION",
    "goto": "GOTO",
    "if": "IF",
    # "in":"IN",
    "mod": "MOD",
    "not": "NOT",  # "KEY_WORD_NOT",
    "of": "OF",
    "or": "OR",
    "packed": "PACKED",
    "procedure": "PROCEDURE",
    "program": "PROGRAM",
    "record": "RECORD",
    "repeat": "REPEAT",
    # "set":"",
    "then": "THEN",
    "to": "TO",
    "type": "TYPE",
    "until": "UNTIL",
    "var": "VAR",
    "while": "WHILE",


    "write": "SYS_PROC",
    "writeln": "SYS_PROC",


    "boolean": "SYS_TYPE",
    "char": "SYS_TYPE",
    "integer": "SYS_TYPE",
    "real": "SYS_TYPE",
    # "with":""

    "true": "true",
    "false": "false",

    "read": "READ"
}
