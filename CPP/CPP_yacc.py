# -*- coding: UTF-8 -*-
# 编译原理大作业 SPL based on Python
# 任宇凡 刘洪甫 邱兆林

# This file is the yacc parse part of the whole project
import symbol
import ply.yacc as yacc
import sys
from CPP_mylex import tokens
from tree_visual import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    # ('left', 'MUL', 'DIV', 'kDIV', 'kMOD')
    ('left', 'MUL', 'DIV', 'MOD')
)

table = symbol.Table()

scopes = []  # 调试用


def p_program(p):
    # '''program :  program_head  routine  DOT
    #         | factor '''
    '''program :  program_head  routine  DOT '''
    p[0] = Node("program", [p[1], p[2]])


def p_program_head(p):
    '''program_head :  PROGRAM  NAME  SEMI'''
    p[0] = Node("program_head", [p[1], p[2], p[3]])


def p_routine(p):
    '''routine :  routine_head  routine_body'''
    p[0] = Node("routine", [p[1], p[2]])


def p_sub_routine(p):
    '''sub_routine :  routine_head  routine_body'''
    p[0] = Node("sub_routine", [p[1], p[2]])


def p_routine_head(p):
    '''routine_head :  label_part  const_part  type_part  var_part  routine_part'''
    p[0] = Node("routine_head", [p[1], p[2], p[3], p[4], p[5]])


def p_label_part(p):
    '''label_part :  empty'''
    p[0] = Node("label_part", [p[1]])


def p_const_part(p):
    '''const_part :  CONST  const_expr_list
                |  empty'''
    if len(p) == 3:
        p[0] = Node("const_part", [p[2]])
    elif len(p) == 2:
        p[0] = Node("const_part", [])


def p_const_expr_list(p):
    '''const_expr_list :  const_expr_list  const_expr
                |  const_expr'''
    if len(p) == 3:
        p[0] = Node("const_expr_list", [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node("const_expr_list", [p[1]])


def p_const_expr(p):
    """const_expr : NAME EQUAL const_value SEMI"""
    # print("[ *** ]: ", p[1])
    p[0] = Node("const_expr", [p[1], p[3]])

    table.define(p[1], p[3].type, 'const', p[3].value)


def p_const_value(p):
    '''const_value :  INTEGER
                |  REAL
                |  CHAR
                |  STRING
                |  SYS_CON
                | true
                | false'''
    p[0] = Node("const_value", p[1])

    p[0].value = p[1]

    if type(p[1]) == int:
        p[0].type = 'integer'

    elif type(p[1]) == float:
        p[0].type = 'real'

    elif type(p[1]) == str:
        p[0].type = 'char'

    if str(p[1]).lower() == 'true':
        p[0].type = 'boolean'
        p[0].value = True

    if str(p[1]).lower() == 'false':
        p[0].type = 'boolean'
        p[0].value = False


def p_type_part(p):
    '''type_part :  TYPE type_decl_list
                |  empty'''
    if len(p) == 3:
        p[0] = Node("type_part", [p[2]])
    else:
        p[0] = Node("type_part", [p[1]])


def p_type_decl_list(p):
    '''type_decl_list :  type_decl_list  type_definition
                |  type_definition'''
    if len(p) == 3:
        p[0] = Node("type_decl_list", [p[1], p[2]])
    else:
        p[0] = Node("type_decl_list", [p[1]])


def p_type_definition(p):
    '''type_definition :  NAME  EQUAL  type_decl  SEMI'''
    p[0] = Node("type_definition", [p[3]])

    table.define(p[1], p[3].type, 'type')


def p_type_decl(p):
    '''type_decl :  simple_type_decl
                |  array_type_decl
                |  record_type_decl'''
    p[0] = Node("type_decl", [p[1]])
    p[0].type = p[1].type


# def p_simple_type_decl_1(p):
#         '''simple_type_decl :  SYS_TYPE
#                     |  NAME
#                     |  LP  name_list  RP
#                     |  const_value  DOTDOT  const_value
#                     |  MINUS  const_value  DOTDOT  const_value removed
#                     |  MINUS  const_value  DOTDOT  MINUS  const_value removed
#                     |  NAME  DOTDOT  NAME''' removed


def p_simple_type_decl_1(p):
    '''simple_type_decl :  SYS_TYPE'''
    p[0] = Node("imple_type_decl", [p[1]])
    print(p[0])
    p[0].type = p[1]


def p_simple_type_decl_2(p):
    '''simple_type_decl : NAME'''
    p[0] = Node("imple_type_decl", [p[1]])
    p[0].type = p[1]


def p_simple_type_decl_3(p):
    '''simple_type_decl : LP  name_list  RP'''
    p[0] = Node("imple_type_decl", [p[1], p[2], p[3]])


def p_simple_type_decl_4(p):
    '''simple_type_decl : const_value  DOTDOT  const_value'''
    p[0] = Node("imple_type_decl", [p[1], p[2], p[3]])


def p_array_type_decl(p):
    '''array_type_decl :  ARRAY  LB  INTEGER  DOTDOT  INTEGER  RB  OF  type_decl'''
    #         0             1    2      3       4        5     6   7       8
    # TODO 只支持常数中的整数，并且是单维
    # '''array_type_decl :  ARRAY  LB  simple_type_decl  RB  OF  type_decl'''
    p[0] = Node("array_type_decl", [p[3], p[5], p[8]])

    symbol = table.get_temp('array', 'type', {
        'data_type': p[8].type,
        'dimension': [(p[3], p[5])]
    })

    p[0].type = symbol.name


def p_record_type_decl(p):
    '''record_type_decl :  RECORD  field_decl_list  END'''
    p[0] = Node("record_type_decl", [p[2]])

    symbol = table.get_temp('record', 'type', p[2].list)
    p[0].type = symbol.name


def p_field_decl_list(p):
    '''field_decl_list :  field_decl_list  field_decl
                |  field_decl'''
    if len(p) == 3:
        p[0] = Node("field_decl_list", [p[1], p[2]])
        p[0].list = p[1].list + p[2].list
    else:
        p[0] = Node("field_decl_list", [p[1]])
        p[0].list = p[1].list


def p_field_decl(p):
    '''field_decl :  name_list  COLON  type_decl  SEMI'''
    #      0             1        2        3       4
    p[0] = Node("field_decl", [p[1], p[3]])

    p[0].list = [
        (name, p[3].type)
        for name in p[1].list
    ]


def p_name_list(p):
    '''name_list :  name_list  COMMA  NAME
                |  NAME'''
    if len(p) == 4:
        p[0] = Node("name_list", [p[1]])
        p[0].list = p[1].list + [p[3]]
    else:
        p[0] = Node("name_list", [p[1]])
        p[0].list = [p[1]]


def p_var_part(p):
    '''var_part :  VAR  var_decl_list
                |  empty'''
    if len(p) == 3:
        p[0] = Node("var_part", [p[2]])
    else:
        p[0] = Node("var_part", [p[1]])


def p_var_decl_list(p):
    '''var_decl_list :  var_decl_list  var_decl
                |  var_decl'''
    if len(p) == 3:
        p[0] = Node("var_decl_list", [p[1], p[2]])
    else:
        p[0] = Node("var_decl_list", [p[1]])


def p_var_decl(p):
    '''var_decl :  name_list  COLON  type_decl  SEMI'''
    p[0] = Node("var_decl", [p[1], p[3]])

    for name in p[1].list:
        table.define(name, p[3].type)


def p_routine_part(p):
    '''routine_part :  routine_part  function_decl
                |  routine_part  procedure_decl
                |  function_decl
                |  procedure_decl
                | empty'''
    if len(p) == 3:
        p[0] = Node("routine_part", [p[1], p[2]])
    else:
        p[0] = Node("routine_part", [p[1]])


def p_function_decl(p):
    '''function_decl : function_head  SEMI  sub_routine  SEMI'''
    p[0] = Node("function_decl", [p[1], p[3]])

    scope = table.del_scope()
    scopes.append(scope)


def p_function_head(p):
    '''function_head :  FUNCTION  function_name  parameters  COLON  simple_type_decl '''
    p[0] = Node("function_head", [p[3], p[5]])

    table.define(p[2], p[5].type, 'function', p[3].list)

    for name, type in p[3].list:
        table.define(name, type)

    table.scope().return_type = p[5].type


def p_function_name(p):
    '''function_name : NAME '''
    p[0] = p[1]

    table.add_scope(p[1], 'function', 'integer')


def p_procedure_decl(p):
    '''procedure_decl :  procedure_head  SEMI  sub_routine  SEMI'''
    p[0] = Node("procedure_decl", [p[1], p[3]])

    scope = table.del_scope()
    scopes.append(scope)


def p_procedure_head(p):
    '''procedure_head :  PROCEDURE procedure_name parameters '''
    p[0] = Node("procedure_head", [p[3]])

    table.define(p[2], 'integer', 'procedure', p[3].list)

    for name, type in p[3].list:
        table.define(name, type)


def p_procedure_name(p):
    '''procedure_name :  NAME'''
    p[0] = p[1]

    table.add_scope(p[1], 'function', 'integer')


def p_parameters(p):
    '''parameters :  LP  para_decl_list  RP
                |  empty'''
    if len(p) == 4:
        p[0] = Node("parameters", [p[2]])

        p[0].list = p[2].list
    else:
        p[0] = Node("parameters", [p[1]])

        p[0].list = []


def p_para_decl_list(p):
    '''para_decl_list :  para_decl_list  SEMI  para_type_list
                | para_type_list'''
    if len(p) == 4:
        p[0] = Node("para_decl_list", [p[1], p[3]])

        p[0].list = p[1].list + p[3].list
    else:
        p[0] = Node("para_decl_list", [p[1]])

        p[0].list = p[1].list


def p_para_type_list(p):
    '''para_type_list :  var_para_list  COLON  simple_type_decl
                      |  val_para_list  COLON  simple_type_decl'''

    p[0] = Node("para_type_list", [p[1], p[3]])

    p[0].list = [
        (name, p[3].type)
        for name in p[1].list
    ]


def p_var_para_list(p):
    '''var_para_list :  VAR  name_list'''
    # TODO 引用传递
    p[0] = Node("var_para_list", [p[2]])

    p[0].list = p[2].list


def p_val_para_list(p):
    # 值传递
    '''val_para_list :  name_list
                    '''
    p[0] = Node("val_para_list", [p[1]])

    p[0].list = p[1].list


def p_routine_body_1(p):
    '''routine_body :  compound_stmt'''
    p[0] = Node("routine_body", [p[1]])

# FIXME: 为了testcase专门修改的，让routine body可以全空


def p_routine_body_2(p):
    '''routine_body :  empty'''
    p[0] = Node("routine_body", [p[1]])


def p_compound_stmt(p):
    '''compound_stmt :  BEGIN  stmt_list  END'''
    p[0] = Node("compound_stmt", [p[2]])


def p_stmt_list(p):
    '''stmt_list :  stmt_list  stmt  SEMI
                |  empty'''
    if len(p) == 4:
        p[0] = Node("stmt_list", [p[1], p[2]])
    else:
        p[0] = Node("stmt_list", [p[1]])


def p_stmt(p):
    '''stmt :  INTEGER  COLON  non_label_stmt
                |  non_label_stmt'''
    if len(p) == 4:
        p[0] = Node("stmt", [p[3]])
    else:
        p[0] = Node("stmt", [p[1]])


def p_non_label_stmt(p):
    '''non_label_stmt :  assign_stmt
                | proc_stmt
                | compound_stmt
                | if_stmt
                | repeat_stmt
                | while_stmt
                | for_stmt
                | case_stmt
                | goto_stmt'''
    p[0] = Node("non_label_stmt", [p[1]])


# def p_assign_stmt(p):
#         '''assign_stmt :  NAME  ASSIGN  expression
#                     | NAME LB expression RB ASSIGN expression
#                     | NAME  DOT  NAME  ASSIGN  expression'''
def p_assign_stmt_1(p):
    '''assign_stmt :  NAME  ASSIGN  expression'''
    p[0] = Node("assign_stmt", [p[3]])


def p_assign_stmt_2(p):
    '''assign_stmt :  NAME LB expression RB ASSIGN expression'''
    p[0] = Node("assign_stmt", [p[3], p[6]])


def p_assign_stmt_3(p):
    '''assign_stmt :  NAME  DOT  NAME  ASSIGN  expression'''
    p[0] = Node("assign_stmt", [p[4]])


def p_proc_stmt(p):
    '''proc_stmt :  NAME
                |  NAME  LP  args_list  RP
                |  SYS_PROC
                |  SYS_PROC  LP  expression_list  RP
                |  READ  LP  factor  RP'''
    if len(p) == 2:
        p[0] = Node("proc_stmt", [p[1]])
    else:
        p[0] = Node("proc_stmt", [p[3]])


def p_if_stmt(p):
    '''if_stmt :  IF  expression  THEN  stmt  else_clause'''
    p[0] = Node("if_stmt", [p[2], p[4], p[5]])


def p_else_clause(p):
    '''else_clause :  ELSE stmt
                |  empty'''
    if len(p) == 3:
        p[0] = Node("else_clause", [p[2]])
    else:
        p[0] = Node("else_clause", [p[1]])


def p_repeat_stmt(p):
    '''repeat_stmt :  REPEAT  stmt_list  UNTIL  expression'''
    p[0] = Node("repeat_stmt", [p[2], p[4]])


def p_while_stmt(p):
    '''while_stmt :  WHILE  expression  DO stmt'''
    p[0] = Node("while_stmt", [p[2], p[4]])


def p_for_stmt(p):
    '''for_stmt :  FOR  NAME  ASSIGN  expression  direction  expression  DO stmt'''
    p[0] = Node("while_stmt", [p[4], p[5], p[6], p[8]])


def p_direction(p):
    '''direction :  TO
                | DOWNTO'''
    p[0] = Node("direction", None)


def p_case_stmt(p):
    '''case_stmt :  CASE expression OF case_expr_list  END'''
    p[0] = Node("case_stmt", [p[2], p[4]])


def p_case_expr_list(p):
    '''case_expr_list :  case_expr_list  case_expr
                |  case_expr'''
    if len(p) == 3:
        p[0] = Node("case_expr_list", [p[1], p[2]])
    else:
        p[0] = Node("case_expr_list", [p[1]])


def p_case_expr(p):
    '''case_expr :  const_value  COLON  stmt  SEMI
                |  ID  COLON  stmt  SEMI'''
    p[0] = Node("case_expr", [p[1], p[3]])


def p_goto_stmt(p):
    '''goto_stmt :  GOTO  INTEGER'''
    p[0] = Node("goto_stmt", [p[2]])


def p_expression_list(p):
    '''expression_list :  expression_list  COMMA  expression
                |  expression'''
    if len(p) == 4:
        p[0] = Node("expression_list-expression_list", [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Node("expression_list-expression", [p[1]])


def p_expression(p):
    '''expression :  expression  GE  expr
                |  expression  GT  expr
                |  expression  LE  expr
                |  expression  LT  expr
                |  expression  EQUAL  expr
                |  expression  UNEQUAL  expr
                |  expr'''
    if len(p) == 4:
        p[0] = Node("expression", [p[1], p[3]])
    else:
        p[0] = Node("expression", [p[1]])


def p_expr(p):
    '''expr :  expr  PLUS  term
                |  expr  MINUS  term
                |  expr  OR  term
                |  term'''
    if len(p) == 2:
        p[0] = Node("expr-term", [p[1]])
    elif p[2] == '+':
        p[0] = Node("expr-PLUS", [p[1], p[3]])
    elif p[2] == '-':
        p[0] = Node("expr-MINUS", [p[1], p[3]])
    elif p[2] == '|':
        p[0] = Node("expr-OR", [p[1], p[3]])


def p_term(p):
    '''term :  term  MUL  factor
                |  term  DIV  factor
                |  term  MOD  factor
                |  term  AND  factor
                |  factor'''
    if len(p) == 2:
        p[0] = Node("term-factor", [p[1]])
    elif p[2] == '*':
        p[0] = Node("term-term", [p[1], p[3]])
    elif p[2] == '/':
        p[0] = Node("term-term", [p[1], p[3]])
    elif p[2] == 'MOD':
        p[0] = Node("term-term", [p[1], p[3]])
    elif p[2] == 'and':
        p[0] = Node("term-term", [p[1], p[3]])

# the below codes are modified on this code
# def p_factor(p):
#         '''factor :  NAME
#                     |  NAME  LP  args_list  RP
#                     |  SYS_FUNCT
#                     |  SYS_FUNCT  LP  args_list  RP
#                     |  const_value
#                     |  LP  expression  RP
#                     |  NOT  factor
#                     |  MINUS  factor
#                     |  NAME  LB  expression  RB
#                     |  NAME  DOT  NAME'''
#         if len(p) == 1:
#             p[0] = Node("factor",[p[1]])
#         else:
#             p[0] = Node("factor", None)


def p_factor_func(p):
    '''factor : SYS_FUNCT
                |  SYS_FUNCT  LP  args_list  RP
    '''
    if len(p) == 2:
        p[0] = Node("p_factor_func", [p[1]])
    else:
        p[0] = Node("p_factor_func", [p[3]])


def p_factor_arr(p):
    '''factor : NAME  LP  args_list  RP'''

    p[0] = Node("p_factor_arr", [p[3]])


def p_factor_1(p):
    '''factor :  NAME
                |  const_value
                |  LP  expression  RP
                |  NOT  factor
                |  MINUS  factor
                |  NAME  LB  expression  RB'''
    if len(p) == 2:
        p[0] = Node("factor", [p[1]])
    elif len(p) == 3:
        p[0] = Node("factor", [p[2]])
    elif len(p) == 4:
        p[0] = Node("factor", [p[2]])
    else:
        p[0] = Node("factor", [p[3]])


def p_factor_2(p):
    '''factor : NAME  DOT  NAME'''

    p[0] = Node("p_factor_1", [p[1], p[2], p[3]])


def p_args_list(p):
    """args_list :  args_list  COMMA  expression
            |  expression"""
    if len(p) == 4:
        p[0] = Node("args_list", [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Node("expression", [p[1]])


# 空产生式
def p_empty(p):
    'empty :'
    p[0] = Node("empty_production", None)


def p_error(p):
    print("Syntax error")


if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
        result = parser.parse(data, debug=1)
        print(result)

        # print(drawTree(result))
        print(table.scope())
        for scope in scopes:
            print(scope)

    else:
        while True:
            try:
                data = raw_input('Type here > ')
            except EOFError:
                break
            if data == "q" or data == "quit":
                break
            if not data:
                continue

            result = parser.parse(data, debug=1)
            print(result)
