import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symTab):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.jump_list = ["JMP","JL","JG","JGE","JLE","JNE","JE","JZ"]
        self.binary_list = ["+","-","*","/","MOD","OR","AND","SHL","SHR","CMP"]
        self.operator_list = ["UNARY","=","LOADREF","STOREREF","CALL","LABEL","PARAM","RETURN","RETRUNVAL","PRINT","SCAN"]
        # This is for stack handling of all local variables of a function
        self.tempToOffset = {}
        self.symTab = symTab

    def mapOffset(self):

        #print self.symTab.localVals
        for scope in self.symTab.table.keys():

            offset = 0 # Begin at -4, as -4 is the base
            scope_entry = self.symTab.table[scope]
            func_name = scope_entry['Name']
            self.tempToOffset[func_name] = {}
            mapDick = self.tempToOffset[func_name]

            width = 0
            #print "Scope:",scope

            # First adding the local variables
            for var in scope_entry['Ident'].keys():
                varEntry = self.symTab.Lookup(var, 'Ident')
                if func_name != 'main':
                    if varEntry.parameter == False:
                        #print "Var in mapping, offset: ",var, offset
                        # First fetch the variables from the scope
                        mapDick[var] = offset
                        # Now upadate the offset
                        offset = offset - self.symTab.width(varEntry.typ, var)
                        varEntry.offset = offset
                        width = width + self.symTab.width(varEntry.typ, var)
                        #print "var : ", var, " , offset : ", str(offset)

            # Now handling the temporaries.
            for temp in self.symTab.localVals[func_name]:
                #print "Temp in mapping, offset: ",temp, offset
                objectVar = temp.split("_")

                if len(objectVar) == 2:
                    # This local variable corresponds to an object variable
                    objName = objectVar[0]
                    varName = objectVar[1]
                    objEntry = self.symTab.Lookup(func_name + "_" + objName, 'Ident')
                    objOffset = objEntry.offset
                    for param in objEntry.params:
                        if param[0] == varName:
                            offset = objOffset + param[3]
                            mapDick[temp] = offset
                            break
                    offset = objOffset
                    continue
                
                offset = offset - 4 # temporaries are size 4
                mapDick[temp] = offset
                width = width + 4

            # This is for keeping the stack size for a local function
            scope_entry['width'] = width

        #print self.tempToOffset

    def emit(self,op,lhs,op1,op2):
        '''
            Writes the proper 3AC code: removes strings from symbol table entries
        '''
        self.code.append([op,lhs,op1,op2])

    def addlineNumbers(self):

        for i,code in enumerate(self.code):

            #print (code)
            op, lhs, op1, op2 = code
            self.code[i] = [str(i+1)] + code
        
    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. Has objects refering to symbol table

            The point of this to finally emit all the code generated, in the way desired.
        '''
        
        for i, code in enumerate(self.code):

            # print "In 3ADR, display: ",code
            LineNumber, op, lhs, op1, op2 = code

            if type(lhs) != type(""):
                lhs = lhs.name

            if type(op1) != type(""):
                op1 = op1.name

            if type(op2) != type(""):
                op2 = op2.name
            
            print ("#" + LineNumber + ", " + op + ", " + lhs + ", " + op1 + ", " + op2)

