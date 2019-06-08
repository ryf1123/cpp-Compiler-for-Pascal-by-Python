class CodeGen(objective):
    def __init__(self, symtable, threeAC, alloc):
        self.symtable = symtable
        self.threeAC = threeAC
        self.alloc = alloc

        self.code = threeAC.code
        self.asmcode = []

        