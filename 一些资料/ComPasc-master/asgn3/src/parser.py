import ply.yacc as yacc
import sys
import ply.lex as lex
from tokens import *
from lexer import *

### ------------ ISSUES ----------- ###

# Ambiguity checking?
# Remove the Lexer error that Goutham said
# Use of Pointer Type Statement in Grammar? Since we are not working with pointers[?]
# Do we need to expand rules like Identifier, which is a token? NO

### ------------------------------- ###
reverse_output = []

precedence = (
    ('nonassoc','ELSETOK'),
    ('nonassoc','ELSE'),
    ('nonassoc','IDTOK'),
    ('nonassoc','ID'),
    ('nonassoc','ENDTOK'),
    ('nonassoc','END'),
    ('nonassoc', 'TOK'),
    ('nonassoc','PROCEDURE'),
    ('nonassoc','FUNCTION'),
    ('nonassoc','CONSTRUCTOR')
)

def p_Goal(p):
    ''' Goal : Program '''
    reverse_output.append(p.slice)

def p_Program(p):
    ''' Program : PROGRAM ID SEMICOLON Block 
    | PROGRAM ID LPAREN IdentList RPAREN SEMICOLON Block'''
    reverse_output.append(p.slice)

def p_Block(p):
    ''' Block : DeclSection CompoundStmt'''
    reverse_output.append(p.slice)

def p_DeclSection(p):
    ''' DeclSection : DeclSection WhichSection
    | '''
    reverse_output.append(p.slice)

def p_WhichSection(p):
    ''' WhichSection : ConstSection
    | TypeSection
    | VarSection
    | ProcedureDeclSection '''
    reverse_output.append(p.slice)

def p_CompoundStmt(p):
    ''' CompoundStmt : BEGIN StmtList END SEMICOLON '''
    reverse_output.append(p.slice)

def p_StmtList(p):
    ''' StmtList : Statement StmtList 
    | Statement'''
    reverse_output.append(p.slice)

def p_Statement(p):
    ''' Statement : SimpleStatement SEMICOLON
    | StructStmt '''
    reverse_output.append(p.slice)

def p_SimpleStatement(p):
    ''' SimpleStatement : Designator
    | Designator LPAREN ExprList RPAREN
    | Designator ASSIGNTO Expression
    | INHERITED
    | LPAREN Expression RPAREN
    | BREAK
    | CONTINUE'''
    reverse_output.append(p.slice)

def p_StructStmt(p):
    ''' StructStmt : CompoundStmt
    | ConditionalStmt 
    | LoopStmt '''
    reverse_output.append(p.slice)

# Removed semicolon from if and case
def p_ConditionalStmt(p):
    ''' ConditionalStmt : IfStmt
    | CaseStmt '''
    reverse_output.append(p.slice)

def p_IfStmt(p):
    ''' IfStmt : IF Expression THEN CompoundStmt ELSE CompoundStmt
    | IF Expression THEN CompoundStmt %prec ELSETOK '''
    reverse_output.append(p.slice)

def p_CaseStmt(p):
    ''' CaseStmt : CASE Expression OF CaseSelector ColonCaseSelector END
    | CASE Expression OF CaseSelector ColonCaseSelector ELSE CompoundStmt SEMICOLON END '''
    reverse_output.append(p.slice)

def p_ColonCaseSelector(p):
    ''' ColonCaseSelector : ColonCaseSelector SEMICOLON CaseSelector 
    | '''
    reverse_output.append(p.slice)

def p_CaseSelector(p):
    ''' CaseSelector : CaseLabel COLON Statement '''
    reverse_output.append(p.slice)


def p_CaseLabel(p):
    # THIS IS NOT CORRECT. WILL PUT INTEGER/NUMBER
    ''' CaseLabel : NUMBER '''
    reverse_output.append(p.slice)

def p_LoopStmt(p):
    ''' LoopStmt : RepeatStmt
    | WhileStmt '''
    reverse_output.append(p.slice)

def p_RepeatStmt(p):
    ''' RepeatStmt : REPEAT Statement UNTIL Expression SEMICOLON '''
    reverse_output.append(p.slice)

#No need of semicolon after WhileStmt because CompoundStmt will handle it
def p_WhileStmt(p):
    ''' WhileStmt : WHILE Expression DO CompoundStmt '''
    reverse_output.append(p.slice)

def p_Expression(p):
    ''' Expression : SimpleExpression RelSimpleStar 
    | LambFunc'''
    reverse_output.append(p.slice)

def p_RelSimpleStar(p):
    ''' RelSimpleStar : RelOp SimpleExpression RelSimpleStar
    | '''
    reverse_output.append(p.slice)

def p_SimpleExpression(p):
    ''' SimpleExpression : PLUS Term AddTermStar
    | MINUS Term AddTermStar 
    | Term AddTermStar '''
    reverse_output.append(p.slice)

def p_AddTermStar(p):
    ''' AddTermStar : AddOp Term AddTermStar
    | '''
    reverse_output.append(p.slice)

def p_Term(p):
    ''' Term : Factor MulFacStar '''
    reverse_output.append(p.slice)

def p_MulFacStar(p):
    ''' MulFacStar : MulOp Factor MulFacStar
    | '''
    reverse_output.append(p.slice)

def p_Factor(p):
    ''' Factor : Designator 
    | Designator LPAREN ExprList RPAREN
    | USERSTRING
    | NUMBER
    | LPAREN Expression RPAREN
    | NOT Factor
    | INHERITED Designator
    | INHERITED
    | TypeID LPAREN Expression RPAREN '''
    reverse_output.append(p.slice)

# Added ID as a form of type for handling objects and classes
def p_Type(p):
    ''' Type : TypeID
    | SimpleType
    | PointerType
    | StringType
    | ProcedureType 
    | Array 
    | ID'''
    reverse_output.append(p.slice)

def p_SimpleType(p):
    ''' SimpleType : DOUBLE '''
    reverse_output.append(p.slice)

def p_PointerType(p):
    ''' PointerType : POWER ID '''
    reverse_output.append(p.slice)

def p_StringType(p):
    ''' StringType : STRING '''
    reverse_output.append(p.slice)

def p_ProcedureType(p):
    ''' ProcedureType : ProcedureHeading
    | FuncHeading
    '''
    reverse_output.append(p.slice)

def p_TypeArgs(p):
    ''' TypeArgs : LPAREN TypeID RPAREN
    | LPAREN STRING RPAREN '''
    reverse_output.append(p.slice)

def p_TypeID(p):
    ''' TypeID : INTEGER
    | REAL
    | CHAR '''
    reverse_output.append(p.slice)

# def p_OrdinalType(p):
#     ''' OrdinalType : INTEGER'''
#     reverse_output.append(p.slice)

# def p_RealType(p):
    # ''' RealType : DOUBLE'''
    # reverse_output.append(p.slice)

# Added without the keyword TYPE for classes and objects
def p_TypeSection(p):
    ''' TypeSection : TYPE ColonTypeDecl '''
    reverse_output.append(p.slice)

def p_ColonTypeDecl(p):
    ''' ColonTypeDecl : ColonTypeDecl TypeDecl SEMICOLON 
    | TypeDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_TypeDecl(p):
    ''' TypeDecl : ID EQUALS Type
    | ID EQUALS RestrictedType
    | ID EQUALS TYPE Type
    | ID EQUALS TYPE RestrictedType '''
    reverse_output.append(p.slice)

def p_RestrictedType(p):
    ''' RestrictedType : ObjectType
    | ClassType '''
    reverse_output.append(p.slice)

def p_RelOp(p):
    ''' RelOp : LANGLE
    | RANGLE
    | GEQ
    | LEQ
    | NOTEQUALS
    | EQUALS'''
    reverse_output.append(p.slice)

def p_AddOp(p):
    ''' AddOp : PLUS
    | MINUS
    | OR
    | XOR '''
    reverse_output.append(p.slice)

def p_MulOp(p):
    ''' MulOp : MULTIPLY
    | DIVIDE
    | DIV
    | MOD
    | AND
    | SHL
    | SHR 
    | DOUBLESTAR '''
    reverse_output.append(p.slice)

def p_CommaExpression(p):
    ''' CommaExpression : CommaExpression COMMA Expression
    | '''
    reverse_output.append(p.slice)

def p_ExprList(p):
    ''' ExprList : Expression CommaExpression'''
    reverse_output.append(p.slice)

def p_Designator(p):
    ''' Designator : ID DesSubEleStar'''
    reverse_output.append(p.slice)

def p_DesSubEleStar(p):
    ''' DesSubEleStar : DesSubEleStar DesignatorSubElem 
    | '''
    reverse_output.append(p.slice)

def p_DesignatorSubElem(p):
    ''' DesignatorSubElem : DOT ID
    | LSQUARE ExprList RSQUARE
    | POWER '''
    reverse_output.append(p.slice)

# Added without keyword CONSTANT for classes and objects
def p_ConstSection(p):
    ''' ConstSection : CONSTANT ColonConstDecl '''
    reverse_output.append(p.slice)

#Making this left recursive helps to remove a shift-reduce conflict
def p_ColonConstDecl(p):
    ''' ColonConstDecl : ColonConstDecl ConstDecl SEMICOLON
    | ConstDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_ConstDecl(p):
    ''' ConstDecl : ID EQUALS ConstExpr
    | ID COLON TypeID EQUALS TypedConst '''
    reverse_output.append(p.slice)

def p_TypedConst(p):
    ''' TypedConst : ConstExpr
    | ArrayConst '''
    reverse_output.append(p.slice)
    
def p_Array(p):
    ''' Array : ARRAY LSQUARE ArrayBetween RSQUARE OF TypeArray '''
    reverse_output.append(p.slice)

def p_ArrayBetween(p):
    ''' ArrayBetween : NUMBER DOT DOT NUMBER
    | NUMBER DOT DOT ID
    | ID DOT DOT ID
    | ID DOT DOT NUMBER '''
    reverse_output.append(p.slice)

def p_TypeArray(p):
    ''' TypeArray : TypeID
    | PointerType '''
    reverse_output.append(p.slice)

def p_ArrayConst(p):
    ''' ArrayConst : LPAREN TypedConst CommaTypedConst RPAREN '''
    reverse_output.append(p.slice)

def p_CommaTypedConst(p):
    ''' CommaTypedConst : COMMA TypedConst CommaTypedConst
    | '''
    reverse_output.append(p.slice)

def p_ConstExpr(p):
    ''' ConstExpr : NUMBER'''
    reverse_output.append(p.slice)

#the identList for procedure definition and var declaration is not the same
def p_IdentList(p):
    ''' IdentList : ID TypeArgs CommaIDTypeArgs
    | ID CommaIDTypeArgs'''
    reverse_output.append(p.slice)

def p_CommaIDTypeArgs(p):
    ''' CommaIDTypeArgs : COMMA ID TypeArgs CommaIDTypeArgs
    | COMMA ID CommaIDTypeArgs                 
    | '''
    reverse_output.append(p.slice)

#ParamIdentList and ParamIdent are added for handling Formal Parameters for function or procedure declaration
def p_ParamIdentList(p):
    ''' ParamIdentList : ParamIdent SEMICOLON ParamIdentList
    | ParamIdent
    | '''
    reverse_output.append(p.slice)

def p_ParamIdent(p):
    ''' ParamIdent : IdentList COLON Type
    | IdentList '''
    reverse_output.append(p.slice)
    
# Added VarSection without starting with the keyword VAR for classes and objects
def p_VarSection(p):
    ''' VarSection : VAR ColonVarDecl '''
    reverse_output.append(p.slice)

def p_ColonVarDecl(p):
    ''' ColonVarDecl : ColonVarDecl VarDecl SEMICOLON
    | VarDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_VarDecl(p):
    ''' VarDecl : IdentList COLON Type'''
    reverse_output.append(p.slice)

def p_ProcedureDeclSection(p):
    ''' ProcedureDeclSection : ProcedureDecl
    | FuncDecl
    | ConstrucDecl '''
    reverse_output.append(p.slice)

# Don't need to add SEMICOLON after Block
def p_ConstrucDecl(p):
    ''' ConstrucDecl : ConstrucHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

def p_ConstrucHeading(p):
    ''' ConstrucHeading : CONSTRUCTOR Designator FormalParams '''
    reverse_output.append(p.slice)

def p_ConstrucHeadingSemicolon(p):
    ''' ConstrucHeadingSemicolon : CONSTRUCTOR Designator FormalParams SEMICOLON '''
    reverse_output.append(p.slice)

def p_FuncDecl(p):
    ''' FuncDecl : FuncHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

def p_FuncHeading(p):
    ''' FuncHeading : FUNCTION Designator FormalParams COLON Type '''
    reverse_output.append(p.slice)

def p_FuncHeadingSemicolon(p):
    ''' FuncHeadingSemicolon : FUNCTION Designator FormalParams COLON Type SEMICOLON '''
    reverse_output.append(p.slice)

#Included LPAREN and RPAREN in the definition of FORMALPARAMS
def p_FormalParams(p):
    ''' FormalParams : LPAREN ParamIdentList RPAREN
    | '''
    reverse_output.append(p.slice)

def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

#replaced ID by designator for dealing with Object.Function
def p_ProcedureHeading(p):
    ''' ProcedureHeading : PROCEDURE Designator FormalParams '''
    reverse_output.append(p.slice)

def p_ProcedureHeadingSemicolon(p):
    ''' ProcedureHeadingSemicolon : PROCEDURE Designator FormalParams SEMICOLON '''
    reverse_output.append(p.slice)

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFunc(p):
    ''' LambFunc : LAMBDA ID COLON SimpleExpression '''
    reverse_output.append(p.slice)

# def p_LambFunc(p):
#     ''' LambFunc : ID LPAREN ConstExpr RPAREN '''
#     reverse_output.append(p.slice)

### ------------------------------------------- ###


### ---------------- OBJECT DEFS -------------- ###

def p_ObjectType(p):
    ''' ObjectType : OBJECT ObjectHeritage ObjectVis ObjectBody END'''
    reverse_output.append(p.slice)

def p_ObjectHeritage(p):
    ''' ObjectHeritage : LPAREN IdentList RPAREN
    | '''
    reverse_output.append(p.slice)

# The problem here is that the first Identifier list is being identified as that in VarSection rather than type section
def p_ObjectBody(p): 
    ''' ObjectBody : ObjectBody ObjectTypeSection ObjectVarSection ObjectConstSection ObjectMethodList
    | '''
    reverse_output.append(p.slice)
    
def p_ObjectVis(p):
    ''' ObjectVis : PUBLIC
    | '''
    reverse_output.append(p.slice)

def p_ObjectVarSection(p):
    ''' ObjectVarSection : ColonVarDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ObjectTypeSection(p):
    ''' ObjectTypeSection : ColonTypeDecl %prec IDTOK
    | %prec ENDTOK '''
    reverse_output.append(p.slice)

def p_ObjectConstSection(p):
    ''' ObjectConstSection : ColonConstDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ObjectMethodList(p):
    ''' ObjectMethodList : ObjectMethodHeading 
    | %prec TOK '''
    reverse_output.append(p.slice)

def p_ObjectMethodHeading(p):
    ''' ObjectMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon 
    | ConstrucHeadingSemicolon '''
    reverse_output.append(p.slice)

### ------------------------------------------- ###

### --------------------- CLASS DEFS ------------ ###

def p_ClassType(p):
    ''' ClassType : CLASS ClassHeritage ClassVis ClassBody END'''
    reverse_output.append(p.slice)

def p_ClassHeritage(p):
    ''' ClassHeritage : LPAREN IdentList RPAREN
    | '''
    reverse_output.append(p.slice)

def p_ClassBody(p):
    ''' ClassBody : ClassBody ClassTypeSection ClassConstSection ClassVarSection ClassMethodList
    | '''
    reverse_output.append(p.slice)
    
def p_ClassVis(p):
    ''' ClassVis : PUBLIC
    | '''
    reverse_output.append(p.slice)

def p_ClassTypeSection(p):
    ''' ClassTypeSection : ColonTypeDecl %prec IDTOK
    | %prec ENDTOK '''
    reverse_output.append(p.slice)

def p_ClassConstSection(p):
    ''' ClassConstSection : ColonConstDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ClassVarSection(p):
    ''' ClassVarSection : ColonVarDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ClassMethodList(p):
    ''' ClassMethodList : ClassMethodHeading 
    | %prec TOK '''
    reverse_output.append(p.slice)

def p_ClassMethodHeading(p):
    ''' ClassMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon 
    | ConstrucHeadingSemicolon '''
    reverse_output.append(p.slice)

### ---------------------------------------- ###


# def p_Input(p):
    # ''' Input : READ
    # | READLN LPAREN IdentList RPAREN '''

# def p_Output(p):
    # ''' Output : WRITE
    # | WRITELN LPAREN IdentList RPAREN '''

### -------------------------------- ###

def p_error(p):
    print ("Syntax Error at Line: %d, Pos: %d"%(p.lineno,p.lexpos))
    # Add formatters later here, to fetch line number and position

def printpretty(filename):
    output = [i for i in reverse_output[::-1]]

    f = open(filename+".html","w+") 
    f.write("<!DOCTYPE HTML> \n <html> \n \t<head> \n \t\t<title>Rightmost Derivation</title> \n \t<head> \n \t<body>\n")

    runningRule = ""
    pre = ""
    post = ""
    
    for rule in output:
        if runningRule != "":
            for i in range(len(runningRule),-1,-1):
                if runningRule[i:i+len(str(rule[0]))] == str(rule[0]):
                    break
            pre = runningRule[0:i]
            post = runningRule[i+len(str(rule[0])):]

        #print "############## " + str(type(pre)) + " ############## " + str(type(runningRule)) + " ###############"
        f.write("\t\t" + "<br>" + pre + "<b>" + str(rule[0]) + "</b>" + post + ' >>>>>> ')
        runningRule = pre
        f.write(pre + "<u>")
        for symbol in rule[1:]:
            if str(type(symbol)) == "<class 'ply.lex.LexToken'>":
                runningRule = runningRule + symbol.value + ' '
                f.write(symbol.value + ' ')
            else:
                runningRule = runningRule + str(symbol) + ' '
                f.write(str(symbol) + ' ')
                
        runningRule = runningRule + post
        f.write("</u>" + post + "\n")
    f.write("\t</body> \n </html>") 

def main():
    parser = yacc.yacc()

    # Do the things that we want to here
    inputfile = open(sys.argv[1],'r').read()
    yacc.parse(inputfile, debug = 0)

    filename = sys.argv[1].split("/")[1]
    printpretty(filename.split(".")[0])

if __name__ == '__main__':
    main()
