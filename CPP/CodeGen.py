from Rule import op32_dict, register_list

class CodeGen(objective):
    def __init__(self, symtable, threeAC, allocReg):
        self.symtable = symtable
        self.threeAC = threeAC
        self.allocReg = allocReg

        self.code = threeAC.code
        self.asmcode = []

    
    def handle_binary(self):
        pass

    
    def handle_division(self):
        pass

    
    def handle_input(self):
        pass
    

    def handle_print(self):
        pass
    

    def handle_cmp(self):
        pass


    def handle_jmp(self):
        pass
    

    def handle_label(self):
        pass
    

    def handle_funccall(self):
        pass

    
    def handle_params(self):
        pass
    

    def handle_return(self):
        pass
    

    def handle_loadref(self):
        pass
    

    def handle_storeref(self):
        pass

