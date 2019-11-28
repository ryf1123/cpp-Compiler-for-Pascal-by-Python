import ply.yacc as yacc
import sys
import ply.lex as lex
from tokens import *
from lexer import *
from SymTable import SymTable
from ThreeAddrCode import ThreeAddrCode

# Use of Pointer Type Statement in Grammar? Since we are not working with pointers[?]
# Warning displayed when unassigned variable is used
# Scope of functions?

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

#These are global variables which store the beginning (before expression) and end labels for loops (in sequence where last element is the labels for the innermost loop)
loopBegin = []
loopEnd = []

#Getting the integer value of an Id (constant) or a number
def getValue(Id):
    entry = symTab.Lookup(symTab.currScope + "_" + Id,'Ident')
    if entry == None:
        return int(Id)
    else:
        if entry.cat != 'constant':
            sys.exit("Error: Array range Ids (Id..Id) can either be numbers or constants")
        else:
            return int(entry.params)


def handleFuncCall(p, ifAssign = False):

    name = symTab.Lookup(p[1]['place'],'Func')
        # Name is a symbolTableEntry and thus should have attributes accessible via a DOT.

    if ifAssign and p[1]['place'] == symTab.currScope + '_WRITELN':
            sys.exit("Wrong use of WRITELN")

    elif p[1]['place'] == symTab.currScope + '_WRITELN':
        for argument in p[3]:
            # argument is a dict
            tac.emit('PRINT','',argument['place'],'')
            
    elif name != None:
        if name.cat == 'function':
            arg_count = 0
            if p[3] != None:
                # p[3] is a list of dicts
                arg_count = len(p[3])
                
            if name.num_params == arg_count:
                if arg_count > 0:
                    p[3] = p[3][::-1]
		    for argument in p[3]:
                        # argument is a dict
                        tac.emit('PARAM','',argument['place'],'' )

                if ifAssign:
                    lhs = symTab.getTemp()
                    tac.emit('CALL', lhs, p[1]['place'], '')
                    p[0]['place'] = lhs
                else:
                    tac.emit('CALL','', p[1]['place'], '')
            else:
                print "ERROR: Line", p.lineno(1), "Function", p[1]['place'], "needs exactly", name.num_params, "parameters, given", arg_count
                print "Compilation Terminated"
                exit()
        else:
            print "ERROR: Line", p.lineno(1), "Function", p[1]['place'], "not defined as a function"
            print "Compilation Terminated"
            exit()
    else:
        print "ERROR: Line", p.lineno(1), "Function", p[1]['place'], "not defined"
        print "Compilation Terminated"
        exit()
    
def resolveRHSArray(factor):

    entry = symTab.Lookup(factor['place'],'Ident')
    
    if entry != None and entry.cat == 'variable' and entry.assigned == False:
        print "Warning : Variable " + factor['place'] + " used before assignment"
        
    if entry != None and entry.cat == 'array':

        # this is temporary for array index calculation
        indexTemp = symTab.getTemp()
        # this is temporary for additional calculations
        temp = symTab.getTemp()
        lhs = symTab.getTemp()

        tac.emit('+',indexTemp,'0','0')

        for i in range(len(entry.params)-1):

            currIndex = factor['ArrayIndices'][i]['place']
            Range = entry.params[i]
            tac.emit('-',temp,currIndex,str(Range['start']))
            tac.emit('+',indexTemp,indexTemp,temp)
            nextRange = entry.params[i+1]
            # Look at (https://stackoverflow.com/questions/789913/array-offset-calculations-in-multi-dimensional-array-column-vs-row-major?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa) for this calculation
            tac.emit('-',temp,str(nextRange['end']+1),str(nextRange['start']))
            tac.emit('*',indexTemp,indexTemp,temp)

        tac.emit('-',temp,factor['ArrayIndices'][-1]['place'],str(entry.params[-1]['start']))
        tac.emit('+',indexTemp,indexTemp,temp)
        tac.emit('LOADREF', lhs, factor['place'], indexTemp)

        factor['place'] = lhs
        
def updateStar(p):

    p[0] = {}
    p[0]['place'] = p[2]['place']
    p[0]['previousOp'] = p[1]
    p[0]['ExprList'] = []
    resolveRHSArray(p[2])
    
    if p[3]!={}:
        p[0]['ExprList'] = p[3]['ExprList']
        p[0]['ExprList'].append([p[3]['previousOp'],p[2]['place'],p[3]['place']])

def handleTerm(p, termIndex=1, starIndex=2, whetherRelational=False):

    p[0]={}
    p[0]['ExprList'] = p[starIndex]['ExprList']
    p[0]['ExprList'].append([p[starIndex]['previousOp'],p[termIndex]['place'],p[starIndex]['place']])
    #reversing the list for left associativity 
    p[0]['ExprList'] = p[0]['ExprList'][::-1]
    #expr is of the form [op,op1,op2]
    for i,expr in enumerate(p[0]['ExprList']):
        lhs = symTab.getTemp()
        if whetherRelational:
            l1 = symTab.getLabel()
            l2 = symTab.getLabel()
            tac.emit('CMP','',expr[1],expr[2])
            if expr[0] == '<':
                tac.emit('JGE','',l1,'')
            elif expr[0] == '>':
                tac.emit('JLE','',l1,'')
            elif expr[0] == '>=':
                tac.emit('JL','',l1,'')
            elif expr[0] == '<=':
                tac.emit('JG','',l1,'')
            elif expr[0] == '<>':
                tac.emit('JE','',l1,'')
            else :
                tac.emit('JNE','',l1,'')
            tac.emit('+',lhs,'1','0')
            tac.emit('JMP','',l2,'')
            tac.emit('LABEL','',l1,'')
            tac.emit('+',lhs,'0','0')
            tac.emit('LABEL','',l2,'')
        else:
            tac.emit(expr[0],lhs,expr[1],expr[2])
        if i != len(p[0]['ExprList'])-1:
            p[0]['ExprList'][i+1][1] = lhs
    p[0]['place'] = lhs
    #I'm making this False because array will be handled in MulFacStar (no need to handle it for term)
    p[0]['isArray'] = False
        
def p_Goal(p):
    ''' Goal : Program '''
    reverse_output.append(p.slice)

def p_Program(p):
    ''' Program : PROGRAM ID SEMICOLON Block 
    | PROGRAM ID LPAREN IdentList RPAREN SEMICOLON Block'''
    reverse_output.append(p.slice)

def p_Block(p):
    ''' Block : DeclSection CompoundStmt'''

    # Need to check here the ReturnType, if it is a function, that there exists a variable with same name, and same type
    if symTab.table[symTab.currScope]['Type'] == 'function':
        if symTab.table[symTab.currScope]['ReturnType'] != None:
            if symTab.table[symTab.currScope]['ReturnSet'] == False:
                print "ERROR: Line",p.lineno(1),",Function",symTab.table[symTab.currScope]['Name'],"is not returning as per convention."
                print "Compilation Terminated"
                exit()

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
    | CONTINUE
    | SCAN LPAREN Designator RPAREN'''

    if p[1] == 'SCAN':
        tac.emit('SCAN',p[3]['place'],'','')

    elif p[1] == 'BREAK':
        if loopBegin == []:
            print "Wrong use of BREAK. Enter within a loop"
            exit
        else:
            tac.emit("JMP",'',loopEnd[-1],'')

    elif p[1] == 'CONTINUE':
        if loopBegin == []:
            print "Wrong use of CONTINUE. Enter within a loop"
            exit
        else:
            tac.emit("JMP",'',loopBegin[-1],'')
            
    # This is for handling cases where assignment happens
    elif len(p) == 4 and p[2] == ':=':

        entry = symTab.Lookup(p[1]['place'],'Ident')
        if entry.cat == 'constant':
            sys.exit("ERROR : Trying to assign constant variable "+p[1]['place'])
            
        if p[1]['isArray']:
            
            indexTemp = symTab.getTemp()
            temp = symTab.getTemp()
            tac.emit('+',indexTemp,'0','0')
            for i in range(len(entry.params)-1):

                currIndex = p[1]['ArrayIndices'][i]['place']
                Range = entry.params[i]
                tac.emit('-',temp,currIndex,str(Range['start']))
                tac.emit('+',indexTemp,indexTemp,temp)
                nextRange = entry.params[i+1]
                tac.emit('-',temp,str(nextRange['end']+1),str(nextRange['start']))
                tac.emit('*',indexTemp,indexTemp,temp)

            tac.emit('-',temp,p[1]['ArrayIndices'][-1]['place'],str(entry.params[-1]['start']))
            tac.emit('+',indexTemp,indexTemp,temp)
            tac.emit('STOREREF', p[1]['place'], indexTemp, p[3]['place'])
        else:
            tac.emit('+',p[1]['place'],p[3]['place'],'0')

        # This is for knowing that a variable has been assigned    
        if entry.cat == 'variable':
            entry.assigned = True

        scope_table = symTab.table[symTab.currScope]

        if scope_table['Type'] == 'function' and scope_table['ReturnType'] != None:

            # if the variable name matches the name of the function
            if p[1]['place'].split("_")[1] == scope_table['Name'].split("_")[1] and p[1]['type'] == scope_table['ReturnType']:
                scope_table['ReturnSet'] = True

    # This is for handling a function CALL
    elif len(p) == 5:
        handleFuncCall(p)
            
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
    ''' IfStmt : IF Expression THEN IfMark1 CompoundStmt ELSE IfMark3 CompoundStmt IfMark4
    | IF Expression THEN IfMark1 CompoundStmt IfMark2 %prec ELSETOK '''
    reverse_output.append(p.slice)

## --------------------------------- IF DEFS ----------------------- ###
def p_IfMark1(p):
    ''' IfMark1 : '''
    l1 = symTab.getLabel()
    tac.emit('CMP','',p[-2]['place'],'0')
    tac.emit('JE','',l1,'')
    p[0] = l1

def p_IfMark2(p):
    ''' IfMark2 :  '''
    label = p[-2]
    tac.emit('LABEL','',label,'')

def p_IfMark3(p):
    ''' IfMark3 :  '''
    l1 = symTab.getLabel()
    label = p[-3]
    tac.emit('JMP','',l1,'')
    tac.emit('LABEL','',label,'')
    p[0] = l1

def p_IfMark4(p):
    ''' IfMark4 : '''
    tac.emit('LABEL','',p[-2],'')
## ------------------------ IF DEFS END ------------------------------ ###

#testMark is for the function test as in Sir's slides
def p_CaseStmt(p):
    ''' CaseStmt : CASE CaseMark1 Expression OF CaseSelector ColonCaseSelector CaseTest END SEMICOLON
    | CASE CaseMark1 Expression OF CaseSelector ColonCaseSelector CaseTest2 ELSE CaseMark2 CompoundStmt CaseMark3 END SEMICOLON'''
    reverse_output.append(p.slice)

def p_CaseMark1(p):
    ''' CaseMark1 : '''
    temp = symTab.getLabel()
    tac.emit('JMP','',temp,'')
    p[0] = temp

def p_CaseMark2(p):
    ''' CaseMark2 : '''
    tac.emit('LABEL','',p[-2],'')

def p_CaseMark3(p):
    ''' CaseMark3 :  '''
    tac.emit('LABEL','',p[-5]['next'],'')


def p_CaseTest2(p):
    ''' CaseTest2 : '''
    
    tac.emit('LABEL','',p[-5],'')
    
    # For first CaseSelector
    tac.emit('CMP','',p[-4]['place'],p[-2]['value'])
    tac.emit('JE','',p[-2]['label'],'')

    
    # Testing the value which matches, and then jumping
    for key in p[-1]['map'].keys():
        tac.emit('CMP','',p[-4]['place'],key)
        tac.emit('JE','',p[-1]['map'][key],'')

    # Unconditionally jump to the ELSE label
    temp = symTab.getLabel()
    tac.emit('JMP','',temp,'')
    p[0] = temp

def p_CaseTest(p):
    ''' CaseTest : '''
    
    tac.emit('LABEL','',p[-5],'')
    
    # For first CaseSelector
    tac.emit('CMP','',p[-4]['place'],p[-2]['value'])
    tac.emit('JE','',p[-2]['label'],'')

    
    # Testing the value which matches, and then jumping
    for key in p[-1]['map'].keys():
        tac.emit('CMP','',p[-4]['place'],key)
        tac.emit('JE','',p[-1]['map'][key],'')

    tac.emit('LABEL','',p[-1]['next'],'')


def p_ColonCaseSelector(p):
    ''' ColonCaseSelector : ColonCaseSelector CaseSelector
    | '''

    if len(p) == 1:
        lab = symTab.getLabel()
        p[0] = {}
        p[0]['next'] = lab
        # gstack.append(lab)
        p[0]['map'] = {}
        tac.emit('JMP','',p[0]['next'],'')
    else:
        p[0] = p[1]
        p[0]['map'][p[2]['value']] = p[2]['label']
        tac.emit('JMP','',p[1]['next'],'')

    reverse_output.append(p.slice)

def p_CaseSelector(p):
    ''' CaseSelector : CaseLabel COLON Statement '''
    p[0] = p[1]
    # tac.emit('JMP','',gstack[-1],'')
    reverse_output.append(p.slice)


def p_CaseLabel(p):
    ''' CaseLabel : NUMBER '''
    lab = symTab.getLabel()
    tac.emit('LABEL','',lab,'')
    p[0] = {}
    p[0]['label'] = lab
    p[0]['value'] = p[1]
    # p[0] = p[1]
    reverse_output.append(p.slice)

### ----------------------------------- CASE DEFS END ------------------------------ ###

def p_LoopStmt(p):
    ''' LoopStmt : RepeatStmt
    | WhileStmt '''
    reverse_output.append(p.slice)

#Introducing a label at the end of repeat to do same thing as while for break/continue
def p_RepeatStmt(p):
    ''' RepeatStmt : REPEAT RepMark1 Statement UNTIL Expression RepMark2 SEMICOLON '''

    global loopBegin
    global loopEnd
    loopBegin = loopBegin[:-1]
    loopEnd = loopEnd[:-1]

    reverse_output.append(p.slice)

def p_RepMark1(p):
    ''' RepMark1 : '''
    l1 = symTab.getLabel()
    l2 = symTab.getLabel()
    tac.emit('LABEL','',l1,'')
    p[0] = l1

    loopBegin.append(l1)
    loopEnd.append(l2)

def p_RepMark2(p):
    ''' RepMark2 : '''
    tac.emit('CMP','',p[-1]['place'],'1')
    tac.emit('JE','',p[-4],'')

### ------------------------ REP DEFS END --------------------------- ###

#No need of semicolon after WhileStmt because CompoundStmt will handle it
def p_WhileStmt(p):
    ''' WhileStmt : WHILE WhileMark1 Expression DO WhileMark2 CompoundStmt WhileMark3'''

    global loopBegin
    global loopEnd
    loopBegin = loopBegin[:-1]
    loopEnd = loopEnd[:-1]

    reverse_output.append(p.slice)

def p_WhileMark1(p):
    ''' WhileMark1 :  '''
    l1 = symTab.getLabel()
    l2 = symTab.getLabel()
    tac.emit('LABEL','',l1,'')
    p[0] = [l1,l2]

    loopBegin.append(l1)
    loopEnd.append(l2)
    
def p_WhileMark2(p):
    ''' WhileMark2 :  '''
    tac.emit('CMP','',p[-2]['place'],'0')
    tac.emit('JE','',p[-3][1],'') # Jump to l2, that is exit

def p_WhileMark3(p):
    ''' WhileMark3 :  '''
    tac.emit('JMP','',p[-5][0],'') # Go back to l1
    tac.emit('LABEL','',p[-5][1],'') # l2, This is exit

### -------------------- WHILE DEFS END --------------------------- ###

def p_Expression(p):
    ''' Expression : SimpleExpression RelSimpleStar 
    | LambFunc '''

    # Expression has dictionary attribute
    if len(p) == 3:

        if p[2] != {}:
            handleTerm(p,1,2,True)

        else:
            p[0] = p[1]
            
    reverse_output.append(p.slice)

# def p_InvocationExpression(p):
    # ''' InvocationExpression : ID LPAREN IdentList RPAREN'''
    # reverse_output.append(p.slice)

def p_RelSimpleStar(p):
    ''' RelSimpleStar : RelOp SimpleExpression RelSimpleStar
    | '''

    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
            
    reverse_output.append(p.slice)

def p_SimpleExpression(p):
    ''' SimpleExpression : Term AddTermStar
    | MINUS Term AddTermStar '''

    if len(p) == 3:
        starIndex = 2
        termIndex = 1
    else:
        starIndex = 3
        termIndex = 2
    
    if p[starIndex] != {}:
        handleTerm(p, termIndex, starIndex)

    else:
        p[0] = p[1]

    if len(p) == 4:
        tac.emit('-',p[0]['place'],'0',p[0]['place'])
        
    reverse_output.append(p.slice)

def p_AddTermStar(p):
    ''' AddTermStar : AddOp Term AddTermStar
    | '''

    # p[0] is dictionary here
    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
        
    reverse_output.append(p.slice)

def p_Term(p):
    ''' Term : Factor MulFacStar '''
    
    if p[2] != {}:
        handleTerm(p)

    else:
        p[0] = p[1]
        resolveRHSArray(p[1])
        
    reverse_output.append(p.slice)

def p_MulFacStar(p):
    ''' MulFacStar : MulOp Factor MulFacStar
    | '''

    # p[0] is dictionary here
    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
            
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

    p[0] = {}

    if len(p) == 5 and type(p[1]) is dict:
        handleFuncCall(p, True)
        p[0]['isArray'] = False
    elif len(p) == 2 and type(p[1]) is dict:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0]['place'] = p[1]
        p[0]['isArray'] = False

    reverse_output.append(p.slice)

# Added ID as a form of type for handling objects and classes
# Attribute for Type is a dictionary with key 'type' denoting the type string and in case of Array it also has the key 'ranges' specifying rowRanges and columnRanges
def p_Type(p):
    ''' Type : TypeID
    | PointerType
    | StringType
    | ProcedureType 
    | Array 
    | ID'''

    p[0] = {}
    p[0]['type'] = p[1]
    
    # This will happen only when Type is Array, else it will be string
    if type(p[1]) == type({}):

        p[0] = {}
        p[0]['type'] = 'ARRAY'
        p[0]['ranges'] = p[1]['ranges']
        p[0]['dataType'] = p[1]['dataType']

    reverse_output.append(p.slice)

def p_PointerType(p):
    ''' PointerType : POWER ID '''

    p[0] = 'POINTER'
    reverse_output.append(p.slice)

def p_StringType(p):
    ''' StringType : STRING '''

    p[0] = p[1]
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
    | DOUBLE
    | CHAR '''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_TypeSection(p):
    ''' TypeSection : TYPE ColonTypeDecl '''
    reverse_output.append(p.slice)

def p_ColonTypeDecl(p):
    ''' ColonTypeDecl : ColonTypeDecl TypeDecl SEMICOLON 
    | TypeDecl SEMICOLON'''
    reverse_output.append(p.slice)

# What is the need of the last two?
def p_TypeDecl(p):
    ''' TypeDecl : ID EQUALS Type
    | ID EQUALS RestrictedType '''
    #| ID EQUALS TYPE Type
    #| ID EQUALS TYPE RestrictedType '''

    # Not prepending this with current scope because array type can be globally defined
    if p[3]['type'] == 'ARRAY':
        symTab.Define(p[1], p[3]['dataType'], 'ARRAY', p[3]['ranges'])
        p[3]['type'] = p[1]
    
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

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_AddOp(p):
    ''' AddOp : PLUS
    | MINUS
    | OR
    | XOR '''
    p[0] = p[1]
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

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_CommaExpression(p):
    ''' CommaExpression : COMMA Expression CommaExpression
    | '''

    if len(p) == 1:
        p[0] = []

    else:

        p[0] = p[3]
        p[0].append(p[2])
        # pass
    reverse_output.append(p.slice)

def p_ExprList(p):
    ''' ExprList : Expression CommaExpression 
    | '''

    if len(p) == 3:

        p[0] = p[2]
        p[0].append(p[1])
        # The expressions were getting appended in the reverse order
        p[0] = p[0][::-1]

    reverse_output.append(p.slice)

def p_Designator(p):
    ''' Designator : ID DesSubEleStar'''
    
    p[0] = p[2]
    p[0]['place'] = symTab.currScope + "_" + p[1]

    if p[2]['isArray']:

        entry = symTab.Lookup(symTab.currScope + "_" + p[1],'Ident')
        
        if len(entry.params) > p[2]['dimension']:
            sys.exit("Array index missing")

        elif len(entry.params) < p[2]['dimension']:
            sys.exit("Extra Array Index")
    
    if symTab.Lookup(symTab.currScope + "_" + p[1],'Ident') != None:
        # We are only concerned about identifiers at the moment
        p[0]['type'] = symTab.Lookup(symTab.currScope + "_" + p[1],'Ident').typ 

    elif p[-1] in ['FUNCTION','CONSTRUCTOR','PROCEDURE'] or symTab.Lookup(symTab.currScope + "_" + p[1],'Func') != None or p[1] in ['READLN','WRITELN']:
        pass

    else :
        sys.exit("Error : Symbol " + p[1] + " is used without declaration")

    reverse_output.append(p.slice)

# Removed recrsion from this
def p_DesSubEleStar(p):
    ''' DesSubEleStar : DesignatorSubElem 
    | '''
    
    if len(p) == 1:
        p[0] = {}
        p[0]['isArray'] = False
    else:
        p[0] = p[1]

    reverse_output.append(p.slice)

#replaced ExprList by Expression for simplicity
def p_DesignatorSubElem(p):
    ''' DesignatorSubElem : DOT ID
    | LSQUARE ExprList RSQUARE
    | POWER '''

    if len(p) == 4:
        p[0] = {}
        p[0]['isArray'] = True
        p[0]['ArrayIndices'] = p[2]
        p[0]['dimension'] = len(p[2])

    else:
        p[0] = {}
        p[0]['isArray'] = False
        
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

    if len(p) == 4:
        tac.emit('+',symTab.currScope + "_" + p[1],p[3],'0')
        #print symTab.Lookup(p[1],'Ident')
        entry = symTab.Lookup(symTab.currScope + "_" + p[1],'Ident')
        if entry == None:
            symTab.Define(symTab.currScope + "_" + p[1],'integer','CONST',p[3])
        else:
            entry.cat = 'constant'
            entry.params = p[3]
        
    reverse_output.append(p.slice)

def p_TypedConst(p):
    ''' TypedConst : ConstExpr
    | ArrayConst '''
    reverse_output.append(p.slice)
    
def p_Array(p):
    ''' Array : ARRAY LSQUARE ArrayRange ArrayBetween RSQUARE OF TypeArray '''

    p[0] = {}
    p[0]['ranges'] = p[4]
    p[0]['ranges'].append(p[3])
    p[0]['ranges'] = p[0]['ranges'][::-1]
    p[0]['dataType'] = p[7]

    reverse_output.append(p.slice)

def p_ArrayBetween(p):
    ''' ArrayBetween : COMMA ArrayRange ArrayBetween
    | '''
    
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[3]
        p[0].append(p[2])
    
    reverse_output.append(p.slice)
    
def p_ArrayRange(p):
    ''' ArrayRange : NUMBER DOT DOT NUMBER
    | NUMBER DOT DOT ID
    | ID DOT DOT ID
    | ID DOT DOT NUMBER '''

    p[0] = {}
    p[0]['start'] = getValue(p[1])
    p[0]['end'] = getValue(p[4])
    
    reverse_output.append(p.slice)

def p_TypeArray(p):
    ''' TypeArray : TypeID
    | PointerType '''
    p[0] = p[1]
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
    p[0] = p[1]
    reverse_output.append(p.slice)

#the identList for procedure definition and var declaration is not the same
def p_IdentList(p):
    ''' IdentList : ID TypeArgs CommaIDTypeArgs
    | ID CommaIDTypeArgs'''

    if len(p) == 3:

        if p[2] == None:
            p[0] = []

        else:
            p[0] = p[2]

        p[0].append(p[1])

    reverse_output.append(p.slice)

def p_CommaIDTypeArgs(p):
    ''' CommaIDTypeArgs : COMMA ID TypeArgs CommaIDTypeArgs
    | COMMA ID CommaIDTypeArgs                 
    | '''
    
    if len(p) == 4:

        if p[3] == None:
            p[0] = []

        else:
            p[0] = p[3]

        p[0].append(p[2])

    reverse_output.append(p.slice)

#ParamIdentList and ParamIdent are added for handling Formal Parameters for function or procedure declaration

def p_ParamIdentList(p):
    ''' ParamIdentList : ParamIdent SEMICOLON ParamIdentList
    | ParamIdent
    | '''

    if len(p) == 1:
        p[0] = []

    elif len(p) == 2:
        p[0] = []
        p[0].append(p[1])

    elif len(p) == 4:
        p[0] = p[3]
        p[0].append(p[1])
        
    reverse_output.append(p.slice)

def p_ParamIdent(p):
    ''' ParamIdent : IdentList COLON Type
    | IdentList '''

    if len(p) == 4:
        p[0] = [p[1],p[3]['type']]
    else:
        p[0] = [p[1]]

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

    typeEntry = symTab.Lookup(p[3]['type'],'Ident')

    if typeEntry != None:
        for elem in p[1]:
            symTab.Define(symTab.currScope + "_" + elem,p[3]['type'],'ARRAY',typeEntry.params)
    else:
        for elem in p[1]:
            symTab.Define(symTab.currScope + "_" + elem,p[3]['type'],'VAR')
    
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
    ''' FuncDecl : FuncHeading SEMICOLON Block FMark2'''
    reverse_output.append(p.slice)

def p_FMark2(p):
    ''' FMark2 : '''
    symTab.endScope()
    tac.emit('RETURN','',p[-3]['place'],p[-3]['place'])

def p_FMark1(p):
    ''' FMark1 : '''
    tac.emit('LABEL','FUNC',p[-1]['place'],'')

def p_FuncHeading(p):
    ''' FuncHeading : FUNCTION Designator FMark1 FormalParams COLON Type '''
    # p[0] = p[2]

    # Declare new scope here
    symTab.AddScope(p[2]['place'],'function')
    symTab.table[symTab.currScope]['ReturnType'] = p[6]['type']
    symTab.Define(p[2]['place'],p[6]['type'],'VAR') # Define a variable with same return type as function

    # Add the variables into symbol Table
    param_list = p[4]
    params = []

    for item in param_list:
        idents = item[0]
        id_type = item[1]
        for ids in idents:
            # print "ID is: ",ids
            # print "Type is: ",id_type
            params.append(id_type)

            # For assigning params of an array as the array type
            typeEntry =  symTab.Lookup(id_type,'Ident')
            if typeEntry != None:
                symTab.Define(symTab.currScope + "_" + ids,id_type,'ARRAY',typeEntry.params)
            else:
                symTab.Define(symTab.currScope + "_" + ids,id_type,'VAR')


    save_scope = symTab.currScope # Save to revert back
    symTab.endScope() # Go to the parent, and define this function as an entry in Func
    to_insert = symTab.Define(p[2]['place'],p[6]['type'],'FUNC',params)
    symTab.currScope = save_scope # Load back the current scope

    p[0] = p[2] # Giving the designator to Procedure Heading

    reverse_output.append(p.slice)

def p_FuncHeadingSemicolon(p):
    ''' FuncHeadingSemicolon : FUNCTION Designator FormalParams COLON Type SEMICOLON '''
    reverse_output.append(p.slice)

#Included LPAREN and RPAREN in the definition of FORMALPARAMS
def p_FormalParams(p):
    ''' FormalParams : LPAREN ParamIdentList RPAREN
    | '''

    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []
        
    # p[2] is a list of lists. p[2][0] will have two elements: p[2][0][0]: id's, p[2][0][1]: types

    reverse_output.append(p.slice)

def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHeading SEMICOLON Block PMark2'''
    reverse_output.append(p.slice)

def p_PMark1(p):
    ''' PMark1 : '''
    tac.emit('LABEL','FUNC',p[-1]['place'],'')

def p_PMark2(p):
    ''' PMark2 : '''
    symTab.endScope()
    tac.emit('RETURN','','',p[-3]['place'])

#replaced ID by designator for dealing with Object.Function
def p_ProcedureHeading(p):
    ''' ProcedureHeading : PROCEDURE Designator PMark1 FormalParams '''

    # Declare new scope here
    symTab.AddScope(p[2]['place'],'function')
    symTab.table[symTab.currScope]['ReturnType'] = None

    # Add the variables into symbol Table
    param_list = p[4]
    params = []
    for item in param_list:
        idents = item[0]
        id_type = item[1]
        for ids in idents:
            # print "ID is: ",ids
            # print "Type is: ",id_type
            params.append(id_type)

            typeEntry =  symTab.Lookup(id_type,'Ident')
            if typeEntry != None:
                symTab.Define(symTab.currScope + "_" + ids,id_type,'ARRAY',typeEntry.params)
            else:
                symTab.Define(symTab.currScope + "_" + ids,id_type,'VAR')

    save_scope = symTab.currScope # Save to revert back
    symTab.endScope() # Go to the parent, and define this function as an entry in Func
    to_insert = symTab.Define(p[2]['place'],'void','FUNC',params)
    symTab.currScope = save_scope # Load back the current scope

    p[0] = p[2] # Giving the designator to Procedure Heading

    reverse_output.append(p.slice)

def p_ProcedureHeadingSemicolon(p):
    ''' ProcedureHeadingSemicolon : PROCEDURE Designator FormalParams SEMICOLON '''
    reverse_output.append(p.slice)

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFunc(p):
    ''' LambFunc : LAMBDA ID COLON SimpleExpression '''
    reverse_output.append(p.slice)




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
    # print(output)

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

parser = yacc.yacc()

symTab = SymTable()
tac = ThreeAddrCode()

# Do the things that we want to here
inputfile = open(sys.argv[1],'r').read()
yacc.parse(inputfile, debug = 1)

tac.display_code()
