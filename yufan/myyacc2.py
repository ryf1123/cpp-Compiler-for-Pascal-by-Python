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
def p_program(p):
        # '''program :  program_head  routine  DOT
        #         | factor '''
        '''program :  program_head  routine  DOT '''
        p[0] = Node("program")([p[1], p[2]])
        
def p_program_head(p):
        '''program_head :  PROGRAM  NAME  SEMI'''
        p[0] = Node("program_head")([])
        
def p_routine(p):
        '''routine :  routine_head  routine_body'''
        p[0] = Node("routine")([p[1], p[2]])

def p_sub_routine(p):
        '''sub_routine :  routine_head  routine_body'''
        p[0] = Node("sub_routine")([p[1], p[2]])

        
def p_routine_head(p):
        '''routine_head :  label_part  const_part  type_part  var_part  routine_part'''
        p[0] = Node("routine_head")([p[1], p[2], p[3], p[4], p[5]])

        
def p_label_part(p):
        '''label_part :  empty'''


        
def p_const_part(p):
        '''const_part :  CONST  const_expr_list  
                    |  empty'''
        if len(p) == 3:
            p[0] = Node("const_part-const_part")([p[2]])
        elif len(p) == 2:
            p[0] = Node("const_part-empty")([])    

        
def p_const_expr_list(p):
        '''const_expr_list :  const_expr_list  const_expr
                    |  const_expr'''
        if len(p) == 3:
            p[0] = Node("const_expr_list-const_expr_list")([p[1], p[2]])
        elif len(p) == 2:
            p[0] = Node("const_expr_list-const_expr")([p[1]])       
        
def p_const_expr(p):
        """const_expr : NAME EQUAL const_value SEMI"""
        p[0] = Node("const_expr")([p[1],[3]])

        
def p_const_value(p):
        '''const_value :  INTEGER  
                    |  REAL  
                    |  CHAR  
                    |  STRING  
                    |  SYS_CON'''
        p[0] = Node("const_value")([])

        
def p_type_part(p):
        '''type_part :  TYPE type_decl_list  
                    |  empty'''


        
def p_type_decl_list(p):
        '''type_decl_list :  type_decl_list  type_definition  
                    |  type_definition'''


        
def p_type_definition(p):
        '''type_definition :  NAME  EQUAL  type_decl  SEMI'''


        
def p_type_decl(p):
        '''type_decl :  simple_type_decl  
                    |  array_type_decl  
                    |  record_type_decl'''


        
def p_simple_type_decl(p):
        '''simple_type_decl :  SYS_TYPE  
                    |  NAME  
                    |  LP  name_list  RP  
                    |  const_value  DOTDOT  const_value  
                    |  MINUS  const_value  DOTDOT  const_value
                    |  MINUS  const_value  DOTDOT  MINUS  const_value
                    |  NAME  DOTDOT  NAME'''


        
def p_array_type_decl(p):
        '''array_type_decl :  ARRAY  LB  simple_type_decl  RB  OF  type_decl'''


        
def p_record_type_decl(p):
        '''record_type_decl :  RECORD  field_decl_list  END'''


        
def p_field_decl_list(p):
        '''field_decl_list :  field_decl_list  field_decl  
                    |  field_decl'''


        
def p_field_decl(p):
        '''field_decl :  name_list  COLON  type_decl  SEMI'''


        
def p_name_list(p):
        '''name_list :  name_list  COMMA  NAME  
                    |  NAME'''


        
def p_var_part(p):
        '''var_part :  VAR  var_decl_list  
                    |  empty'''


        
def p_var_decl_list(p):
        '''var_decl_list :  var_decl_list  var_decl  
                    |  var_decl'''


        
def p_var_decl(p):
        '''var_decl :  name_list  COLON  type_decl  SEMI'''


        
def p_routine_part(p):
        '''routine_part :  routine_part  function_decl  
                    |  routine_part  procedure_decl
                    |  function_decl  
                    |  procedure_decl  
                    | empty'''


        
def p_function_decl(p):
        '''function_decl : function_head  SEMI  sub_routine  SEMI'''


        
def p_function_head(p):
        '''function_head :  FUNCTION  NAME  parameters  COLON  simple_type_decl '''


        
def p_procedure_decl(p):
        '''procedure_decl :  procedure_head  SEMI  sub_routine  SEMI'''


        
def p_procedure_head(p):
        '''procedure_head :  PROCEDURE NAME parameters '''


        
def p_parameters(p):
        '''parameters :  LP  para_decl_list  RP  
                    |  empty'''


        
def p_para_decl_list(p):
        '''para_decl_list :  para_decl_list  SEMI  para_type_list 
                    | para_type_list'''


        
def p_para_type_list(p):
        '''para_type_list :  var_para_list COLON  simple_type_decl  
        |  val_para_list  COLON  simple_type_decl'''


        
def p_var_para_list(p):
        '''var_para_list :  VAR  name_list'''


        
def p_val_para_list(p):
        '''val_para_list :  name_list
                        '''


        
def p_routine_body(p):
        '''routine_body :  compound_stmt'''


        
def p_compound_stmt(p):
        '''compound_stmt :  BEGIN  stmt_list  END'''


        
def p_stmt_list(p):
        '''stmt_list :  stmt_list  stmt  SEMI  
                    |  empty'''


        
def p_stmt(p):
        '''stmt :  INTEGER  COLON  non_label_stmt  
                    |  non_label_stmt'''


        
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


        
def p_assign_stmt(p):
        '''assign_stmt :  NAME  ASSIGN  expression
                    | NAME LB expression RB ASSIGN expression
                    | NAME  DOT  NAME  ASSIGN  expression'''


        
def p_proc_stmt(p):
        '''proc_stmt :  NAME
                    |  NAME  LP  args_list  RP
                    |  SYS_PROC
                    |  SYS_PROC  LP  expression_list  RP
                    |  READ  LP  factor  RP'''


        
def p_if_stmt(p):
        '''if_stmt :  IF  expression  THEN  stmt  else_clause'''


        
def p_else_clause(p):
        '''else_clause :  ELSE stmt 
                    |  empty'''


        
def p_repeat_stmt(p):
        '''repeat_stmt :  REPEAT  stmt_list  UNTIL  expression'''


        
def p_while_stmt(p):
        '''while_stmt :  WHILE  expression  DO stmt'''


        
def p_for_stmt(p):
        '''for_stmt :  FOR  NAME  ASSIGN  expression  direction  expression  DO stmt'''


        
def p_direction(p):
        '''direction :  TO 
                    | DOWNTO'''


        
def p_case_stmt(p):
        '''case_stmt :  CASE expression OF case_expr_list  END'''


        
def p_case_expr_list(p):
        '''case_expr_list :  case_expr_list  case_expr  
                    |  case_expr'''


        
def p_case_expr(p):
        '''case_expr :  const_value  COLON  stmt  SEMI
                    |  ID  COLON  stmt  SEMI'''


        
def p_goto_stmt(p):
        '''goto_stmt :  GOTO  INTEGER'''


        
def p_expression_list(p):
        '''expression_list :  expression_list  COMMA  expression   
                    |  expression'''
        if len(p) == 4:
            p[0] = Node("expression_list-expression_list")([p[1], p[3]])
        elif len(p) == 2:
            p[0] = Node("expression_list-expression")([p[1]])

        
def p_expression(p):
        '''expression :  expression  GE  expr  
                    |  expression  GT  expr  
                    |  expression  LE  expr
                    |  expression  LT  expr  
                    |  expression  EQUAL  expr  
                    |  expression  UNEQUAL  expr  
                    |  expr'''
        if len(p) == 4:
            p[0] = Node("expression")([p[1], p[3]])
        else:
            p[0] = Node("expression")([p[1]])
        
def p_expr(p):
        '''expr :  expr  PLUS  term  
                    |  expr  MINUS  term  
                    |  expr  OR  term  
                    |  term'''
        if len(p) == 2:
            p[0] = Node("expr-term")([p[1]])
        elif p[2] == '+':
            p[0] = Node("expr-PLUS")([p[1], p[3]])
        elif p[2] == '-':
            p[0] = Node("expr-MINUS")([p[1], p[3]])
        elif p[2] == '|':
            p[0] = Node("expr-OR")([p[1], p[3]])
        

        
def p_term(p):
        '''term :  term  MUL  factor  
                    |  term  DIV  factor  
                    |  term  MOD  factor 
                    |  term  AND  factor  
                    |  factor'''
        if len(p) == 2:
            p[0] = Node("term-factor")([p[1]])
        elif p[2] == '*':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[2] == '/':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[2] == 'MOD':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[2] == 'and':
            p[0] = Node("term-term")([p[1], p[3]])


        
def p_factor(p):
        '''factor :  NAME  
                    |  NAME  LP  args_list  RP  
                    |  SYS_FUNCT  
                    |  SYS_FUNCT  LP  args_list  RP  
                    |  const_value  
                    |  LP  expression  RP
                    |  NOT  factor  
                    |  MINUS  factor  
                    |  NAME  LB  expression  RB
                    |  NAME  DOT  NAME'''
        if len(p) == 1:
            p[0] = Node("factor")([p[1]])
        else:
            p[0] = Node("factor")([])
        
def p_args_list(p):
    """args_list :  args_list  COMMA  expression  
            |  expression"""
    if len(p) == 4:
        p[0] = Node("args_list")([p[1],p[3]])
    elif len(p) == 2:
        p[0] = Node("expression")([p[1]])

# def p_myfunc(p):
#     """a : NOT"""


######## End of auto generated
        
# def p_if_stmt(p):
#     'if_stmt: IF  expression  THEN  stmt  else_clause'
#     p[0] = Node("if_stmt")([p[2], p[4], p[5]])

# def p_factor_num(p):
#     'factor : NUMBER'
#     p[0] =  Node("num")([])

# 空产生式
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print ("Syntax error")

if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
        result = parser.parse(data, debug=1)
        print(result)
        
        print(drawTree(result, ignore_error=True))
    else:
        while True:    
            try:
                data = raw_input('Type here > ')
            except EOFError:
                break
            if data == "q" or data =="quit":
                break
            if not data:continue

            result = parser.parse(data, debug=1)    
            print(result)
            




















