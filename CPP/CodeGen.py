from Rule import op32_dict, register_list, binary_list
from symbol_table import Symbol

class CodeGen():
    def __init__(self, symtable, threeAC, allocReg):
        self.symtable = symtable
        self.threeAC = threeAC
        self.allocReg = allocReg

        self.code = threeAC.code
        self.asmcode = []
        self.symbol_register = self.allocReg.symbol_register
        self.register_symbol = self.allocReg.register_symbol

        self.allocReg.get_basic_block()
        self.allocReg.iterate_block()

        #self.allocReg.block2label()

        self.test = self.handle_binary(self.code[1])
        
        print(self.asmcode)

    
    def handle_binary(self, codeline):
        line_num, operation, lhs, op1, op2 = codeline
        
        if isinstance(lhs, Symbol):
            block_index = self.allocReg.line_block(line_num)
            reg, msg = self.allocReg.getReg(block_index, line_num)


        inst = op32_dict[operation]
        if type(op1) == int and type(op2) == int:
            const = op1 + op2
            self.asmcode.append(inst+' '+reg+', '+'$zero, '+str(const))
        


        


        
        print(reg, msg)
        # op1 = self.handle_term(op1)
        # op2 = self.handle_term(op2)

        
        

    
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


    def tacToasm(self):
        for codeline in self.code:
            operation = codeline[1]
            if operation in binary_list:
                handle_binary(codeline)
            elif operation == 'CALL':
                pass#handle_funccall


