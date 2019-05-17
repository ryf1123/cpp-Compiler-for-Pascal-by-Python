def p_program(p):
        '''program :  program_head  routine  DOT'''
        p[0] = Node("program")([p[1], p[2]])


def p_program_head(p):
        '''program_head :  PROGRAM  ID  SEMI'''
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
        p[0] = Node("label_part")([p[1]])


def p_const_part(p):
        '''const_part :  CONST  const_expr_list  
                    |  empty'''
        if p[] == '':
            p[0] = Node("const_part-const_part")([p[2]])
        elif p[] == '':
            p[0] = Node("const_part-empty")([p[1]])



def p_const_expr_list(p):
        '''const_expr_list :  const_expr_list  NAME  EQUAL  const_value  SEMI
                    |  NAME  EQUAL  const_value  SEMI'''
        if p[] == '':
            p[0] = Node("const_expr_list-const_expr_list")([p[1], p[4]])
        elif p[] == '':
            p[0] = Node("const_expr_list-NAME")([p[3]])



def p_const_value(p):
        '''const_value :  INTEGER  
                    |  REAL  
                    |  CHAR  
                    |  STRING  
                    |  SYS_CON'''
        if p[] == '':
            p[0] = Node("const_value-const_value")([])
        elif p[] == '':
            p[0] = Node("const_value-REAL")([])
        elif p[] == '':
            p[0] = Node("const_value-CHAR")([])
        elif p[] == '':
            p[0] = Node("const_value-STRING")([])
        elif p[] == '':
            p[0] = Node("const_value-SYS_CON")([])



def p_type_part(p):
        '''type_part :  TYPE type_decl_list  
                    |  empty'''
        if p[] == '':
            p[0] = Node("type_part-type_part")([p[2]])
        elif p[] == '':
            p[0] = Node("type_part-empty")([p[1]])



def p_type_decl_list(p):
        '''type_decl_list :  type_decl_list  type_definition  
                    |  type_definition'''
        if p[] == '':
            p[0] = Node("type_decl_list-type_decl_list")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("type_decl_list-type_definition")([p[1]])



def p_type_definition(p):
        '''type_definition :  NAME  EQUAL  type_decl  SEMI'''
        p[0] = Node("type_definition")([p[3]])


def p_type_decl(p):
        '''type_decl :  simple_type_decl  
                    |  array_type_decl  
                    |  record_type_decl'''
        if p[] == '':
            p[0] = Node("type_decl-type_decl")([p[1]])
        elif p[] == '':
            p[0] = Node("type_decl-array_type_decl")([p[1]])
        elif p[] == '':
            p[0] = Node("type_decl-record_type_decl")([p[1]])



def p_simple_type_decl(p):
        '''simple_type_decl :  SYS_TYPE  
                    |  NAME  
                    |  LP  name_list  RP  
                    |  const_value  DOTDOT  const_value  
                    |  MINUS  const_value  DOTDOT  const_value
                    |  MINUS  const_value  DOTDOT  MINUS  const_value
                    |  NAME  DOTDOT  NAME'''
        if p[] == '':
            p[0] = Node("simple_type_decl-simple_type_decl")([])
        elif p[] == '':
            p[0] = Node("simple_type_decl-NAME")([])
        elif p[] == '':
            p[0] = Node("simple_type_decl-LP")([p[2]])
        elif p[] == '':
            p[0] = Node("simple_type_decl-const_value")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("simple_type_decl-MINUS")([p[2], p[4]])
        elif p[] == '':
            p[0] = Node("simple_type_decl-MINUS")([p[2], p[5]])
        elif p[] == '':
            p[0] = Node("simple_type_decl-NAME")([])



def p_array_type_decl(p):
        '''array_type_decl :  ARRAY  LB  simple_type_decl  RB  OF  type_decl'''
        p[0] = Node("array_type_decl")([p[3], p[6]])


def p_record_type_decl(p):
        '''record_type_decl :  RECORD  field_decl_list  END'''
        p[0] = Node("record_type_decl")([p[2]])


def p_field_decl_list(p):
        '''field_decl_list :  field_decl_list  field_decl  
                    |  field_decl'''
        if p[] == '':
            p[0] = Node("field_decl_list-field_decl_list")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("field_decl_list-field_decl")([p[1]])



def p_field_decl(p):
        '''field_decl :  name_list  COLON  type_decl  SEMI'''
        p[0] = Node("field_decl")([p[1], p[3]])


def p_name_list(p):
        '''name_list :  name_list  COMMA  ID  
                    |  ID'''
        if p[] == '':
            p[0] = Node("name_list-name_list")([p[1], ])
        elif p[] == '':
            p[0] = Node("name_list-ID")([])



def p_var_part(p):
        '''var_part :  VAR  var_decl_list  
                    |  empty'''
        if p[] == '':
            p[0] = Node("var_part-var_part")([p[2]])
        elif p[] == '':
            p[0] = Node("var_part-empty")([p[1]])



def p_var_decl_list(p):
        '''var_decl_list :  var_decl_list  var_decl  
                    |  var_decl'''
        if p[] == '':
            p[0] = Node("var_decl_list-var_decl_list")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("var_decl_list-var_decl")([p[1]])



def p_var_decl(p):
        '''var_decl :  name_list  COLON  type_decl  SEMI'''
        p[0] = Node("var_decl")([p[1], p[3]])


def p_routine_part:(p):
        '''routine_part:  routine_part  function_decl  
                    |  routine_part  procedure_decl
                    |  function_decl  
                    |  procedure_decl  
                    | empty'''
        if p[] == '':
            p[0] = Node("routine_part:-routine_part:")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("routine_part:-routine_part")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("routine_part:-function_decl")([p[1]])
        elif p[] == '':
            p[0] = Node("routine_part:-procedure_decl")([p[1]])
        elif p[] == '':
            p[0] = Node("routine_part:-empty")([p[1]])



def p_function_decl(p):
        '''function_decl : function_head  SEMI  sub_routine  SEMI'''
        p[0] = Node("function_decl")([p[1], p[3]])


def p_function_head(p):
        '''function_head :  FUNCTION  NAME  parameters  COLON  simple_type_decl '''
        p[0] = Node("function_head")([p[3], p[5]])


def p_procedure_decl(p):
        '''procedure_decl :  procedure_head  SEMI  sub_routine  SEMI'''
        p[0] = Node("procedure_decl")([p[1], p[3]])


def p_procedure_head(p):
        '''procedure_head :  PROCEDURE NAME parameters '''
        p[0] = Node("procedure_head")([p[3]])


def p_parameters(p):
        '''parameters :  LP  para_decl_list  RP  
                    |  empty'''
        if p[] == '':
            p[0] = Node("parameters-parameters")([p[2]])
        elif p[] == '':
            p[0] = Node("parameters-empty")([p[1]])



def p_para_decl_list(p):
        '''para_decl_list :  para_decl_list  SEMI  para_type_list 
                    | para_type_list'''
        if p[] == '':
            p[0] = Node("para_decl_list-para_decl_list")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("para_decl_list-para_type_list")([p[1]])



def p_para_type_list(p):
        '''para_type_list :  var_para_list COLON  simple_type_decl  
        |  val_para_list  COLON  simple_type_decl'''
        if p[] == '':
            p[0] = Node("para_type_list-para_type_list")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("para_type_list-val_para_list")([p[1], p[3]])



def p_var_para_list(p):
        '''var_para_list :  VAR  name_list'''
        p[0] = Node("var_para_list")([p[2]])


def p_val_para_list(p):
        '''val_para_list :  name_list'''
        p[0] = Node("val_para_list")([p[1]])


def p_routine_body(p):
        '''routine_body :  compound_stmt'''
        p[0] = Node("routine_body")([p[1]])


def p_compound_stmt(p):
        '''compound_stmt :  BEGIN  stmt_list  END'''
        p[0] = Node("compound_stmt")([p[2]])


def p_stmt_list(p):
        '''stmt_list :  stmt_list  stmt  SEMI  
                    |  empty'''
        if p[] == '':
            p[0] = Node("stmt_list-stmt_list")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("stmt_list-empty")([p[1]])



def p_stmt(p):
        '''stmt :  INTEGER  COLON  non_label_stmt  
                    |  non_label_stmt'''
        if p[] == '':
            p[0] = Node("stmt-stmt")([p[3]])
        elif p[] == '':
            p[0] = Node("stmt-non_label_stmt")([p[1]])



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
        if p[] == '':
            p[0] = Node("non_label_stmt-non_label_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-proc_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-compound_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-if_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-repeat_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-while_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-for_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-case_stmt")([p[1]])
        elif p[] == '':
            p[0] = Node("non_label_stmt-goto_stmt")([p[1]])



def p_assign_stmt(p):
        '''assign_stmt :  ID  ASSIGN  expression
                    | ID LB expression RB ASSIGN expression
                    | ID  DOT  ID  ASSIGN  expression'''
        if p[] == '':
            p[0] = Node("assign_stmt-assign_stmt")([p[3]])
        elif p[] == '':
            p[0] = Node("assign_stmt-ID")([p[3], p[6]])
        elif p[] == '':
            p[0] = Node("assign_stmt-ID")([p[5]])



def p_proc_stmt(p):
        '''proc_stmt :  ID
                    |  ID  LP  args_list  RP
                    |  SYS_PROC
                    |  SYS_PROC  LP  expression_list  RP
                    |  READ  LP  factor  RP'''
        if p[] == '':
            p[0] = Node("proc_stmt-proc_stmt")([])
        elif p[] == '':
            p[0] = Node("proc_stmt-ID")([p[3]])
        elif p[] == '':
            p[0] = Node("proc_stmt-SYS_PROC")([])
        elif p[] == '':
            p[0] = Node("proc_stmt-SYS_PROC")([p[3]])
        elif p[] == '':
            p[0] = Node("proc_stmt-READ")([p[3]])



def p_if_stmt(p):
        '''if_stmt :  IF  expression  THEN  stmt  else_clause'''
        p[0] = Node("if_stmt")([p[2], p[4], p[5]])


def p_else_clause(p):
        '''else_clause :  ELSE stmt 
                    |  empty'''
        if p[] == '':
            p[0] = Node("else_clause-else_clause")([p[2]])
        elif p[] == '':
            p[0] = Node("else_clause-empty")([p[1]])



def p_repeat_stmt(p):
        '''repeat_stmt :  REPEAT  stmt_list  UNTIL  expression'''
        p[0] = Node("repeat_stmt")([p[2], p[4]])


def p_while_stmt(p):
        '''while_stmt :  WHILE  expression  DO stmt'''
        p[0] = Node("while_stmt")([p[2], p[4]])


def p_for_stmt(p):
        '''for_stmt :  FOR  ID  ASSIGN  expression  direction  expression  DO stmt'''
        p[0] = Node("for_stmt")([p[4], p[5], p[6], p[8]])


def p_direction(p):
        '''direction :  TO 
                    | DOWNTO'''
        if p[] == '':
            p[0] = Node("direction-direction")([])
        elif p[] == '':
            p[0] = Node("direction-DOWNTO")([])



def p_case_stmt(p):
        '''case_stmt :  CASE expression OF case_expr_list  END'''
        p[0] = Node("case_stmt")([p[2], p[4]])


def p_case_expr_list(p):
        '''case_expr_list :  case_expr_list  case_expr  
                    |  case_expr'''
        if p[] == '':
            p[0] = Node("case_expr_list-case_expr_list")([p[1], p[2]])
        elif p[] == '':
            p[0] = Node("case_expr_list-case_expr")([p[1]])



def p_case_expr(p):
        '''case_expr :  const_value  COLON  stmt  SEMI
                    |  ID  COLON  stmt  SEMI'''
        if p[] == '':
            p[0] = Node("case_expr-case_expr")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("case_expr-ID")([p[3]])



def p_goto_stmt(p):
        '''goto_stmt :  GOTO  INTEGER'''
        p[0] = Node("goto_stmt")([])


def p_expression_list(p):
        '''expression_list :  expression_list  COMMA  expression   
                    |  expression'''
        if p[] == '':
            p[0] = Node("expression_list-expression_list")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression_list-expression")([p[1]])



def p_expression(p):
        '''expression :  expression  GE  expr  
                    |  expression  GT  expr  
                    |  expression  LE  expr
                    |  expression  LT  expr  
                    |  expression  EQUAL  expr  
                    |  expression  UNEQUAL  expr  
                    |  expr'''
        if p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expression")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expression-expr")([p[1]])



def p_expr(p):
        '''expr :  expr  PLUS  term  
                    |  expr  MINUS  term  
                    |  expr  OR  term  
                    |  term'''
        if p[] == '':
            p[0] = Node("expr-expr")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expr-expr")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expr-expr")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("expr-term")([p[1]])



def p_term(p):
        '''term :  term  MUL  factor  
                    |  term  DIV  factor  
                    |  term  MOD  factor 
                    |  term  AND  factor  
                    |  factor'''
        if p[] == '':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("term-term")([p[1], p[3]])
        elif p[] == '':
            p[0] = Node("term-factor")([p[1]])



def p_factor(p):
        '''factor :  NAME  
                    |  NAME  LP  args_list  RP  
                    |  SYS_FUNCT 
                    |  SYS_FUNCT  LP  args_list  RP  
                    |  const_value  
                    |  LP  expression  RP
                    |  NOT  factor  
                    |  MINUS  factor  
                    |  ID  LB  expression  RB
                    |  ID  DOT  ID'''
        if p[] == '':
            p[0] = Node("factor-factor")([])
        elif p[] == '':
            p[0] = Node("factor-NAME")([p[3]])
        elif p[] == '':
            p[0] = Node("factor-SYS_FUNCT")([])
        elif p[] == '':
            p[0] = Node("factor-SYS_FUNCT")([p[3]])
        elif p[] == '':
            p[0] = Node("factor-const_value")([p[1]])
        elif p[] == '':
            p[0] = Node("factor-LP")([p[2]])
        elif p[] == '':
            p[0] = Node("factor-NOT")([p[2]])
        elif p[] == '':
            p[0] = Node("factor-MINUS")([p[2]])
        elif p[] == '':
            p[0] = Node("factor-ID")([p[3]])
        elif p[] == '':
            p[0] = Node("factor-ID")([])



