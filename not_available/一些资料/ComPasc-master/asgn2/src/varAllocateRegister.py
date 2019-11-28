import os
import sys
from SymTable import SymTableEntry as SymTableEntry

class varAllocateRegister:
    '''
    Class holding the register allocated and the next use information for a symbol in the given scope
    '''

    def __init__(self,SymTable,ThreeAddrCode):

        # nextUse maps every basic block to a list of  dictionaries containing next use info for every symbol in the block
        self.nextUse = []
        self.registerToSymbol = {}                                       # stores register to symbol mapping
        self.symbolToRegister = {}                                       # symbol to register mapping
        self.unusedRegisters = ["eax","ebx","ecx","edx"]
        self.usedRegisters = []
        self.SymTable = SymTable
        self.basicBlocks = []
        self.blocksToLabels = {}                                         # key value is the [startline,endline] for a block and value is the label name
        self.leaders = []                                                # This will determine the basic blocks 
        self.code = ThreeAddrCode.code

        for reg in self.unusedRegisters:
            self.registerToSymbol[reg] = ""
        for sym in self.SymTable.table['Ident'].keys():
            self.symbolToRegister[sym] = ""

        # self.getBasicBlocks()
        # self.iterateOverBlocks()
        
    def labelToLine(self,labelName):
        '''
            Now being used
            args:
                Takes the labelName for which you want the linenumber

            ISSUE: Will FAIL if multiple labels are present with same name in different scopes
        '''
        # print labelName
        for i in range(len(self.code)):
            if self.code[i][1] == "LABEL":
                # print self.code[i]
                if self.code[i][3] == None:
                    if self.code[i][5] == labelName:
                        return self.code[i][0]
                else:
                    if self.code[i][3].name == labelName:
                        return self.code[i][0]

    def blockToLabel(self):
        '''
        Mapping every block to a label name in which that block is present
        '''

        for block in self.basicBlocks:
            self.blocksToLabels[block] = ""

        for index,block in enumerate(self.basicBlocks):

            if self.code[block[0]][1] == "label":
                labelName = self.code[block[0]][3]
                self.blocksToLabels[block] = labelName

            for j in range(index+1,len(self.basicBlocks)):                  # all blocks under the same label should get the same mapping
                block = self.basicBlocks[j]
                if self.code[block[0]][1] != "label":                                   
                    self.blocksToLabels[block] = labelName
                else:                                                        #break as soon as we get a new label name. This will be dealt with in the outer loop     
                    break
 
        for block in self.basicBlocks:
            if self.blocksToLabels[block] == "":
                self.blocksToLabels[block] = "Main"
        
    def getBasicBlocks(self):
        '''
            Stores the basic blocks as [startline,endline] pairs in the list self.basicBlocks
        '''
        code = self.code
        #print(code)
        self.leaders.append(1)                         # first statement is a leader


        for i in range(len(code)):
            # print (self.leaders)
            codeLine = code[i]
            print "#"+str(codeLine)
            if codeLine[1].lower() in ["jmp","je","jne","jz","jg","jl","jge","jle"]:

                # Store the linenumber of the target label
                # print codeLine
                if codeLine[3] == None:
                    self.leaders.append(int(self.labelToLine(codeLine[5])))
                else:
                    self.leaders.append(int(self.labelToLine(codeLine[3])))

                # Add the statement that follows as a leader, if not already the last line
                if (i != (len(code) - 1)):
                    self.leaders.append(int(code[i+1][0]))         # 0 represents the linenumber

        self.leaders = list(set(self.leaders))         # removes duplicates
        self.leaders.sort()

        # Convert the leader list to get the basic block indexes, with start and endline
        for i in range(len(self.leaders)):
            if (i != (len(self.leaders) - 1)):
                self.basicBlocks.append([self.leaders[i],self.leaders[i+1]-1]) # -1 because the leader is not a basic block line for previous block
            else:
                self.basicBlocks.append([self.leaders[i],int(self.code[-1][0])])

        # Check if the labels are not SHITE.
        # print self.basicBlocks


    def blockAssignNextUse(self,blockIndex):
        '''
        Reading the code from last line to first line in the given block and updating the next use information.
        '''
        self.nextUse[blockIndex] = [];                                       # This is a list of dictionaries. Each dictionary corresponds to a line

        block = self.basicBlocks[blockIndex]
        start = block[0]
        end = block[1]
        code = self.code[start-1:end]                                        # Line numbers start from 1 but code list index starts from 0
        # print (code)
        prevLine = {}                                                        # Stores the next use info for the next line (next to the current line in the loop)
        symbols = self.SymTable.table['Ident'].keys()                        # This is the list of all symbols
        # print (symbols)
        for sym in symbols:
            prevLine[sym] = float("inf")
        
        i = len(code)
        for i in range(len(code),0,-1):
            lineDict = {}
            codeLine = code[i-1]
            # print (codeLine)

            lhs = codeLine[2]
            op1 = codeLine[3]
            op2 = codeLine[4]
        
            if isinstance(lhs, SymTableEntry):
                lineDict[lhs.name] = float("inf")
            if op1 != None:
                lineDict[op1.name] = codeLine[0]
                # print ('ZZZ = ', lineDict[op1])
            if op2 != None:
                lineDict[op2.name] = codeLine[0]

            # print (lineDict)

            for sym in symbols:
                op1_s = ""
                op2_s = ""
                lhs_s = ""
                if (op1 != None):
                    op1_s = op1.name
                if (op2 != None):
                    op2_s = op2.name
                if (isinstance(lhs, SymTableEntry)):
                    lhs_s = lhs.name
                # if ((op1 != None and sym != op1.name) or (op2 != None and sym != op2.name) or (lhs != None and sym != lhs.name)):
                #     lineDict[sym] = prevLine[sym]
                if sym not in [op1_s,op2_s,lhs_s]:
                    lineDict[sym] = prevLine[sym]                            # Rest of the symbols will get the next use info of the next line

            self.nextUse[blockIndex].append(lineDict)                        # These dictionaries will be appended in reverse order of the line number
            prevLine = lineDict.copy()                                              # We need this for updating the next use for every symbol
        
        self.nextUse[blockIndex] = list(reversed(self.nextUse[blockIndex]))

    def iterateOverBlocks(self):
        '''
            This is being used to calculate next use line numbers for variables in a basic block
        '''
        code = self.code

        for i,block in enumerate(self.basicBlocks):
            self.nextUse.append([])
            self.blockAssignNextUse(i)
    
    def getBlockMaxUse(self,blockIndex, linenumber):
        '''
            This returns the symbol with the maximum value of next use in the given basic block such that the symbol has been allocated a register
        '''

        blockMaxNext = 0
        blockMaxSymbol = ""

        blockNextUse = self.nextUse[blockIndex][linenumber]                              # This is a dictionary

        symbols = self.SymTable.table['Ident'].keys()

        for sym in symbols:
            if blockNextUse[sym] > blockMaxNext and self.symbolToRegister[sym] != "":     # Return only the symbol which is held in some register
                blockMaxNext = blockNextUse[sym]
                blockMaxSymbol = sym
        
        return blockMaxSymbol

    def line2Block (self, line):
        for i in range(len(self.basicBlocks)):
            block = self.basicBlocks[i]
            if (line <= block[1] and line >= block[0]):
                return i


    def getReg(self, blockIndex, line, all_mem = False):
        '''
            Refer to slide 29, CodeGen.pdf for the cases
        '''

        reg = ""
        msg = ""
        codeLine = self.code[line-1]
        
        lhs = codeLine[2] # x
        op1 = codeLine[3] # y
        op2 = codeLine[4] # z

        # x = y OP z
        if (line < self.basicBlocks[blockIndex][1]): # less than endline index
            nextUseInBlock = self.nextUse[blockIndex][line + 1 - self.basicBlocks[blockIndex][0]]
        else:
            nextUseInBlock = {}
            for sym in self.SymTable.table['Ident'].keys():
                nextUseInBlock[sym] = float("inf")

        # float("inf") means that variable has no next use after that particular line in the block
        if ( op1 != None and self.symbolToRegister[op1.name] != "" and nextUseInBlock[op1.name] == float("inf") ):
            reg = self.symbolToRegister[op1.name]
            #self.symbolToRegister[op1.name] = ""
            msg = "Replaced op1"
        elif ( op2 != None and self.symbolToRegister[op2.name] != "" and nextUseInBlock[op2.name] == float("inf") ):
            reg = self.symbolToRegister[op2.name]
            #self.symbolToRegister[op2.name] = ""
            msg = "Replaced op2"
        elif ( len(self.unusedRegisters) > 0 ):
            reg = self.unusedRegisters[0]
            self.unusedRegisters.remove(reg)
            self.usedRegisters.append(reg)
            msg = "Did not replace"
        elif (( lhs != None and nextUseInBlock[lhs.name] != float("inf")) or all_mem == True):
            MU_var = self.getBlockMaxUse(blockIndex, line)
            reg = self.symbolToRegister[MU_var]
            #self.symbolToRegister[MU_var] = ""
            msg = "Replaced NextUse , " + MU_var
        else:
            reg = lhs.name # var
            msg = "Replaced Nothing"
        return (reg, msg)
