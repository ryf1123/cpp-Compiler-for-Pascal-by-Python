from Rule import op32_dict, op32_dict_i, register_list, binary_list
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

        # self.allocReg.block2label()

        # self.handle_binary(self.code[23])
        # self.handle_binary(self.code[24])
        # for i in range(11):
        #     self.handle_binary(self.code[i])
        self.tacToasm()

        self.display_asm()

    def handle_term(self, op, block_index, line_num):
        out = None
        if isinstance(op, Symbol):
            out = self.allocReg.getReg(op, block_index, line_num)
        elif isinstance(op, int):
            out = op
        elif isinstance(op, str):
            out = i
        elif isinstance(op, bool):
            out = [False, True].index(op)
        return out

    def handle_binary(self, codeline):
        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)

        reg_op1 = self.handle_term(op1, block_index, line_num)
        reg_op2 = self.handle_term(op2, block_index, line_num)
        reg_lhs = self.handle_term(lhs, block_index, line_num)

        if type(op1) != int and type(op2) != int:
            inst = op32_dict[operation]
        else:
            inst = op32_dict_i[operation]

        if type(op1) == int and type(op2) == int:
            const = eval(str(op1)+operation+str(op2))
            self.asmcode.append(inst+' '+reg_lhs+', '+'$zero, '+str(const))

        elif type(op1) == Symbol and type(op2) == int:
            const = op2
            self.asmcode.append(inst+' '+reg_lhs+', '+reg_op1+', '+str(const))

        elif type(op1) == Symbol and type(op2) == Symbol:
            self.asmcode.append(inst+' '+reg_lhs+', '+reg_op1+', '+reg_op2)

    def handle_division(self, codeline):
        pass

    def handle_input(self, codeline):
        pass

    def handle_print(self, codeline):
        pass

    def handle_cmp(self, codeline):
        pass

    def handle_jmp(self, codeline):
        pass

    def handle_label(self, codeline):
        pass

    def handle_funccall(self, codeline):
        pass

    def handle_params(self, codeline):
        pass

    def handle_return(self, codeline):
        pass

    def handle_loadref(self, codeline):
        pass

    def handle_storeref(self, codeline):
        pass

    def tacToasm(self):
        for codeline in self.code:
            operation = codeline[1]
            if operation in binary_list:
                self.handle_binary(codeline)
            elif operation in ['BNE', 'BEQ', 'JMP']:
                self.handle_cmp(codeline)
            elif operation == 'LABEL':
                self.handle_label(codeline)
            elif operation == 'CALL':
                self.handle_funccall(codeline)
            elif operation == 'PARAM':
                self.handle_params(codeline)
            elif operation == 'RETURN':
                self.handle_return(codeline)
            elif operation == 'INPUT':
                self.handle_input(codeline)
            elif operation in ['PRINT', 'PRINTLN']:
                self.handle_binary(codeline)
            elif operation == 'LOADREF':
                self.handle_loadref(codeline)
            elif operation == 'STOREREF':
                self.handle_storeref(codeline)

    def display_asm(self):
        for line in self.asmcode:
            print(line)
