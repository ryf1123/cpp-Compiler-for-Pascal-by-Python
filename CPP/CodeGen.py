from Rule import op32_dict, op32_dict_i, register_list, binary_list, unused_register_list
from symbol_table import Symbol


class CodeGen():

    def __init__(self, symtable, threeAC, allocReg):
        self.symtable = symtable
        self.threeAC = threeAC
        self.allocReg = allocReg

        self.code = threeAC.code
        self.asmcode = []
        self.symbol_register = self.allocReg.symbol_register
        # self.register_symbol = self.allocReg.register_symbol

        self.allocReg.get_basic_block()
        self.allocReg.iterate_block()
        self.paraCounter = 0
        self.scopeStack = ['main']

        # self.allocReg.block2label()

        self.tacToasm()

        self.asmcode.append('li $v0, 10')
        self.asmcode.append('syscall')
        self.display_asm()

    def handle_term(self, op, block_index, line_num):

        out = None
        if type(op) == Symbol:
            out, code = self.allocReg.getReg(
                op, block_index, line_num, self.scopeStack[-1].lower())
            self.asmcode += code

        elif type(op) == int:
            out = op
        elif type(op) == str:
            if len(op) == 1:
                out = ord(op)
            else:
                out = op
        elif type(op) == bool:
            out = [False, True].index(op)
        return out

    def handle_binary(self, codeline):
        self.asmcode.append('\n# handle_binary')

        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)
        reg_op1 = self.handle_term(op1, block_index, line_num)
        reg_op2 = self.handle_term(op2, block_index, line_num)
        reg_lhs = self.handle_term(lhs, block_index, line_num)

        if type(op1) != int and type(op2) != int:
            inst = op32_dict[operation]
        else:
            inst = op32_dict_i[operation]

        const_type = [int, str, bool]
        if type(op1) in const_type and type(op2) in const_type:
            if operation.lower() == 'mod':
                operation = '%'
            const = eval(str(op1)+' '+operation.lower()+' '+str(op2))
            if type(const) == bool:
                const = [False, True].index(const)
            self.asmcode.append('addi'+' '+reg_lhs+', '+'$0, '+str(const))

        elif type(op1) == Symbol and type(op2) in const_type:
            const = reg_op2
            if type(const) == bool:
                const = [False, True].index(const)
            if operation.lower() != 'mod':
                if operation.lower() == 'div' and const == 0:
                    raise ValueError("除数不能为0！！")
                self.asmcode.append(inst+' '+reg_lhs+', ' +
                                    reg_op1+', '+str(const))
            else:
                if const == 0:
                    raise ValueError("除数不能为0！！")
                self.asmcode.append('li '+'$t8, '+str(const))
                self.asmcode.append('div '+reg_op1+', '+'$t8')
                self.asmcode.append('mfhi '+reg_lhs)

        elif type(op1) == Symbol and type(op2) == Symbol:
            if operation.lower() != 'mod':
                self.asmcode.append(inst+' '+reg_lhs+', '+reg_op1+', '+reg_op2)
            else:
                self.asmcode.append('bne '+reg_op2+', '+'$0, '+'0')
                self.asmcode.append('break')
                self.asmcode.append('div '+reg_op1+', '+reg_op2)
                self.asmcode.append('mfhi '+reg_lhs)

        elif type(op1) in const_type and op2 == None:
            const = op1
            if type(const) == bool:
                const = [False, True].index(const)
            self.asmcode.append('not {}, {}'.format(reg_lhs, reg_op1))

        elif type(op1) == Symbol and op2 == None:
            self.asmcode.append('not {}, {}'.format(reg_lhs, reg_op1))

    def handle_input(self, codeline):
        self.asmcode.append('\n# handle_input')
        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)
        reg_lhs = self.handle_term(lhs, block_index, line_num)

        # TODO 只考虑输入整数
        self.asmcode.append('li $v0, 5')  # read int
        self.asmcode.append('syscall')
        self.asmcode.append('addi {}, $v0, 0'.format(reg_lhs))

    def handle_print(self, codeline):
        self.asmcode.append('\n# handle_print')

        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)

        if operation == 'PRINTLN':
            self.asmcode.append('li $v0, 11')
            self.asmcode.append('addi $a0, $0, 32')
            self.asmcode.append('syscall')
            return

        if type(op1) == Symbol:
            reg_op1 = self.handle_term(op1, block_index, line_num)
            print(op1, reg_op1)
            # TODO 只考虑输出整数
            self.asmcode.append('li $v0, 1')
            self.asmcode.append('addi $a0, {}, 0'.format(reg_op1))
            self.asmcode.append('syscall')

        else:
            # TODO 只考虑输出整数
            self.asmcode.append('li $v0, 1')
            self.asmcode.append('addi $a0, $0, {}'.format(op1))
            self.asmcode.append('syscall')

    def handle_cmp(self, codeline):
        self.asmcode.append('\n# handle_cmp')

        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)
        reg_op1 = self.handle_term(op1, block_index, line_num)
        reg_op2 = self.handle_term(op2, block_index, line_num)
        reg_lhs = self.handle_term(lhs, block_index, line_num)

        if type(op1) in [str, int] and type(op2) in [str, int]:
            if operation == '=':
                operation = '=='
            const = eval(str(op1)+' '+operation+' '+str(op2))
            const = [False, True].index(const)
            self.asmcode.append('addi {}, $0, {}'.format(reg_lhs, str(const)))
        elif type(op1) == Symbol and type(op2) in [str, int]:
            self.asmcode.append('li $t8, {}'.format(str(reg_op2)))
            self.asmcode.append('{} {}, {}, $t8'.format(
                op32_dict[operation], reg_lhs, reg_op1))

        elif type(op1) == Symbol and type(op2) == Symbol:
            self.asmcode.append('{} {}, {}, {}'.format(
                op32_dict[operation], reg_lhs, reg_op1, reg_op2))

    def handle_jmp(self, codeline):
        self.asmcode.append('\n# handle_jmp')

        line_num, operation, lhs, op1, op2 = codeline
        block_index = self.allocReg.line_block(line_num)

        print(lhs, op1, op2)
        reg_op1 = self.handle_term(op1, block_index, line_num)
        reg_op2 = self.handle_term(op2, block_index, line_num)
        reg_lhs = self.handle_term(lhs, block_index, line_num)

        const_type = [int, str, bool]
        if operation.lower() == 'jmp':
            self.asmcode.append('j {}'.format(reg_lhs))
        else:
            if type(op1) in const_type and type(op2) in const_type:
                if operation.lower() == 'beq':
                    if op1 == op2:
                        self.asmcode.append('j {}'.format(reg_lhs))
                if operation.lower() == 'bne':
                    if op1 != op2:
                        self.asmcode.append('j {}'.format(reg_lhs))

            elif type(op1) == Symbol and type(op2) in const_type:
                self.asmcode.append('li $t8, {}'.format(str(reg_op2)))
                self.asmcode.append('{} {}, $t8, {}'.format(
                    operation.lower(), reg_op1, reg_lhs))

            elif type(op1) == Symbol and type(op2) == Symbol:
                self.asmcode.append('{} {}, {}, {}'.format(
                    operation.lower(), reg_op1, reg_op2, reg_lhs))

    def handle_label(self, codeline):
        self.asmcode.append('\n# handle_label')
        print("[*** This line]: ", codeline)
        # TODO: 保存ra，保存所有寄存器（临时寄存器和s寄存器）

        if codeline[3] != None:

            # bassAddr = str(self.symtable[codeline[3]].width)
            self.scopeStack.append(self.scopeStack[-1]+'.'+codeline[2])
            self.asmcode.append(codeline[2]+':')
        else:
            # 真的是一个label
            self.asmcode.append(codeline[2]+':')
            # self.asmcode.append(inst+' '+reg_lhs+', '+reg_op1+', '+str(const))
            pass
        pass

    def load_mem(self, op, reg, scope):
        return "lw {}, {}($fp)".format(reg, -self.symtable[scope].get(op.name).offset)

    def store_mem(self, op, reg, scope):
        return "sw {}, {}($fp)".format(reg, -self.symtable[scope].get(op.name).offset)

    def handle_call(self, codeline):

        print("[This line]: ", codeline)

        for op in self.symbol_register.keys():
            reg = self.symbol_register[op]
            self.asmcode.append(self.store_mem(
                op, reg, self.scopeStack[-1].lower()))

        self.symbol_register.clear()
        self.allocReg.unused_register = unused_register_list.copy()

        self.paraCounter = 0

        self.asmcode.append('\n# handle_call')
        # TODO: 访问链：判断两个scope之间的关系
        self.scopeStack[-1]
        print("****")
        print(codeline[4])
        print(self.scopeStack[-1])
        print('.'.join(self.scopeStack[-1].split('.')[:-1]))
        # if codeline[4] == self.scopeStack[-1]:
        #     # 访问控制 = fp
        #     pass

        if codeline[4] == '.'.join(self.scopeStack[-1].split('.')[:-1]):
            # 访问控制 = 当前活动访问控制
            # sp - 4 =
            self.asmcode.append("# = parent's")
            self.asmcode.append('lw $t8, 76($fp)')
            self.asmcode.append('sw $t8, 0($sp)')
        else:
            self.asmcode.append('# = fp')
            self.asmcode.append('sw $fp, 0($sp)')
            # 访问控制 = fp

        # 控制链
        self.asmcode.append('sw $fp, -4($sp)')

        # ra
        self.asmcode.append('sw $ra, -8($sp)')
        # sw  $ra -8($sp)

        # reg
        for index in range(8, 24):
            # SW R1, 0(R2)
            # FIXME:
            self.asmcode.append("sw $%s, %d($sp)" % (index, -12 - (index-8)*4))

        # param 参数中处理

        #
        self.asmcode.append('addi $fp $sp -76')
        self.asmcode.append('addi $sp $sp %d' %
                            (- self.symtable[codeline[4]].width - 76))

        # jal
        # self.asmcode.append("jal %s"%self.symtable[codeline[3]])
        self.asmcode.append("jal %s" % codeline[3])

        # 将返回值从 $v0 中取出
        if codeline[2]:
            block_index = self.allocReg.line_block(codeline[0])
            reg_lhs = self.handle_term(codeline[2], block_index, codeline[0])

            self.asmcode.append("move, {}, $v0".format(reg_lhs))

    def handle_params(self, codeline):
        print("[This line]: ", codeline)
        self.asmcode.append('\n# handle_params')
        # TODO: 只支持传基础类型
        # if codeline
        line_num, _, _, op1, _ = codeline
        block_index = self.allocReg.line_block(line_num)
        reg_op1 = self.handle_term(op1, block_index, line_num)

        const_type = [int, str, bool]
        if type(op1) in const_type:
            self.asmcode.append('li $t8, %d' % reg_op1)
            self.asmcode.append('sw $t8, -%d($sp)' % (76 + self.paraCounter*4))
        else:
            self.asmcode.append('sw %s, -%d($sp)' %
                                (reg_op1, 76 + self.paraCounter*4))
        # sw  -76($sp)

        self.paraCounter += 1

    def handle_return(self, codeline):
        self.asmcode.append('\n# handle_return')
        line_num, _, lhs, _, _ = codeline

        topDeleted = self.scopeStack.pop().lower()

        print("[This line]: ", codeline)

        # 指针
        self.asmcode.append('addi $sp, $sp, %d' %
                            (self.symtable[topDeleted].width + 76))
        self.asmcode.append('addi $fp, $sp, 76')

        # TODO 恢复参数 （引用传递
        # : 将返回值放到v0

        if lhs == None:
            pass
        else:
            self.asmcode.append('lw $v0, -%d($fp)' %
                                self.symtable[topDeleted].get("_return").offset)

        #  恢复寄存器
        for index in range(8, 24):
            # SW R1, 0(R2)
            # FIXME:
            self.asmcode.append("lw $%s, %d($sp)" % (index, -12 - (index-8)*4))

        # 恢复返回地址 ra
        self.asmcode.append('move $t8, $ra')

        # ra'
        self.asmcode.append('lw $ra, -8($sp)')

        # FIXME: 需要填好返回值，然后放回ra，最后返还stack上分配的内存，返回

        self.asmcode.append('jr $t8')  # 这个地方不是跳转到ra，因为ra已经恢复成跳转之后的返回地址了

        self.symbol_register.clear()
        self.allocReg.unused_register = unused_register_list.copy()

    def handle_loadref(self, codeline):
        print("[This line]: ", codeline)
        pass

    def handle_storeref(self, codeline):
        print("[This line]: ", codeline)
        print(codeline)
        pass

    def tacToasm(self):
        print(self.allocReg.basic_blocks)
        for i in range(len(self.allocReg.basic_blocks)):
            start, end = self.allocReg.basic_blocks[i]
            block_code = self.code[start:end+1]

            for codeline in block_code:
                operation = codeline[1]
                if operation in binary_list:
                    self.handle_binary(codeline)
                elif operation in ['>', '<', '>=', '<=', '=']:
                    self.handle_cmp(codeline)
                elif operation in ['BNE', 'BEQ', 'JMP']:
                    self.handle_jmp(codeline)
                elif operation == 'LABEL':
                    self.handle_label(codeline)
                elif operation == 'CALL':
                    self.handle_call(codeline)
                elif operation == 'PARAM':
                    self.handle_params(codeline)
                elif operation == 'RETURN':
                    self.handle_return(codeline)
                elif operation == 'INPUT':
                    self.handle_input(codeline)
                elif operation in ['PRINT', 'PRINTLN']:
                    self.handle_print(codeline)
                elif operation == 'LOADREF':
                    self.handle_loadref(codeline)
                elif operation == 'STOREREF':
                    self.handle_storeref(codeline)

            print(self.symbol_register)
            for op in self.symbol_register:
                reg = self.symbol_register[op]
                self.asmcode.append(self.store_mem(
                    op, reg, self.scopeStack[-1].lower()))
            self.symbol_register.clear()
            self.allocReg.unused_register = unused_register_list.copy()

    def display_asm(self):
        for line in self.asmcode:
            print(line)
