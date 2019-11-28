import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self, symTable):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.symTable = symTable
        self.jump_list = ["JMP","JL","JG","JGE","JLE","JNE","JE","JZ"]
        self.binary_list = ["+","-","*","/","MOD","OR","AND","SHL","SHR","CMP"]
        self.operator_list = ["UNARY","=","LOADREF","STOREREF","CALL","LABEL","PARAM","RETURN","RETRUNVAL","PRINT","SCAN"]

    def RepresentsNum(self,s):
        '''
        Checks if the given entry is a number entry.
        '''
        try: 
            float(s)
            return True
        except ValueError:
            return False

    def symTabOp (self, x, typ = 'int', varfunc = 'var'):
        '''
        args:
            x: If it is a constant, then return nothing as the object to be appended to 3Ac line.
               Else, define it in the table, and return the symbolTable entry

        '''
        xEntry = None
        if (self.RepresentsNum(x) == True):
            return None
        if (x != ''):
            xEntry = self.symTable.Lookup(x)
        if (xEntry == None and x != ''):
            xEntry = self.symTable.Define(x, typ, varfunc)
        return xEntry

    def addTo3AC (self, listCode):
        '''
            We need to refer to the symbol table objects, which holds variable objects for scope resolutions
            Args:
                listcode element: Format: LineNumber, Operation, Left Hand Side, Operand 1, Operand 2
            LineNumber, Operation are never NULL/None
        '''
        # Assignment translates to addition with 0

        for codeLine in listCode:

            temp = [None] * 7 # 3 AC rep
            # print ('code = ', codeLine)
            lineno, operator, lhs, op1, op2 = codeLine
            temp[0] = lineno
            temp[1] = operator

            if (operator in self.jump_list):
                temp[5] = op1
            elif (operator == 'LABEL'):
                temp[2] = lhs
                if (lhs == 'FUNC'):
                    temp[3] = self.symTabOp (op1, 'int', 'func')
                else:
                    temp[5] = op1
            elif (operator in self.binary_list):
                temp[2] = self.symTabOp (lhs)
                temp[3] = self.symTabOp (op1, 'int', 'var') 
                if (temp[3] == None):
                    temp[5] = op1
                temp[4] = self.symTabOp (op2, 'int', 'var')
                if (temp[4] == None):
                    temp[6] = op2
            elif (operator == 'RETURN'):
                # print (op1)
                if op1 == '':
                    temp[3] = None
                else:
                    temp[3] = self.symTabOp (op1, 'int', 'var')
            elif (operator == "PRINT"):
                temp[3] = self.symTabOp (op1, 'int', 'var')
                if (temp[3] == None):
                    temp[5] = op1
            elif (operator == "SCAN"):
                temp[2] = self.symTabOp (lhs, 'int', 'var')
            elif (operator == "DEC_ARR"):
                temp[2] = self.symTabOp (lhs, 'int_arr', 'var')
                temp[2].memsize = int(op1)*4
            elif (operator == "LOADREF"): # x = a[i]
                temp[2] = self.symTabOp (lhs, 'int', 'var') # x
                temp[3] = self.symTabOp (op1, 'int_arr', 'var') # a = assume that this is always declared
                temp[4] = self.symTabOp (op2, 'int', 'var') # index
                if (temp[4] == None):
                    temp[6] = op2
            elif (operator == "STOREREF"): # a[i] = x
                temp[2] = self.symTabOp (lhs, 'int_arr', 'var') # a = assume that this is always declared
                temp[3] = self.symTabOp (op1, 'int', 'var') # index
                if (temp[3] == None):
                    temp[5] = op1
                temp[4] = self.symTabOp (op2, 'int', 'var') # x
                if (temp[4] == None):
                    temp[6] = op2

            
            self.code.append(temp) # Storing it to the global code store


    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. has objects refering to symbol table
        '''

        print ("=========================================")
        print ('      Displaying three-address-code      ')
        print ("=========================================")

        for code in self.code:
            # print (code)
            lineno, op, op3, op1, op2 = code

            if op == '=':
                print (lineno, '\t', op3, '<-', op1)
            if op == '+':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '-':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '*':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '/':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '**':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == 'ret':
                print (lineno, '\t', op)
            if op == 'goto':
                # op3 holds the line number to go to
                print (lineno, '\t', op, op3)
            if op == 'if':
                # op3 is the comparison condition
                print (lineno, '\t', op, op1, op3, op2)
            if op == 'label':
                # op3 is function name
                print (lineno, '\t', op, op3)
        print ("=========================================")

