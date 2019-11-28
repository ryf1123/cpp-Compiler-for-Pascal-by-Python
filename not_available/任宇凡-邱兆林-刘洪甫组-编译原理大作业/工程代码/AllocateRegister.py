from Rule import jump_list, unused_register_list
from symbol_table import Symbol


class AllocteRegister():
    def __init__(self, symtable, threeAC):
        self.symtable = symtable
        self.code = threeAC.code

        self.unused_register = unused_register_list.copy()

        # 基本块
        self.basic_blocks = []
        # 接下来使用
        self.next_use = []
        # 每个基本块对应一个label名
        self.block_label = {}
        # {(startline, endline): label_name}

        # symbol 被存在哪些寄存器里
        self.symbol_register = {}

    def get_basic_block(self):
        '''
            get basic blocks
            基本块分割： 
                有条件跳转指令的下一个指令
                跳转指令的目标位置
                自带lable
                第一条指令开始到第二个基本块之前为第一个基本块
        '''
        block_part = []
        block_part.append(0)

        for i in range(len(self.code)):
            code_line = self.code[i]
            if code_line[1].lower() in ['bne', 'beq', 'jmp']:
                if code_line[2] != None:
                    block_part.append(self.label_line(code_line[2]))

                if i != len(self.code)-1:
                    block_part.append(self.code[i+1][0])
            elif code_line[1].lower() in ['label']:
                block_part.append(code_line[0])
            elif code_line[1].lower() in ['call', 'return'] and i != len(self.code)-1:
                block_part.append(self.code[i+1][0])

        block_part = list(set(block_part))
        block_part.sort()

        for i in range(len(block_part)):
            if i != len(block_part)-1:
                self.basic_blocks.append((block_part[i], block_part[i+1]-1))
            else:
                self.basic_blocks.append((block_part[i], self.code[-1][0]))

        # print(self.basic_blocks)

    def block2label(self):
        '''
            map every block into a label name 
        '''
        label_name = ''
        # for block in self.basic_blocks:
        #     self.block_label[block] = ''

        for index, block in enumerate(self.basic_blocks):
            if self.code[block[0]][1].lower() == 'label':
                label_name = self.code[block[0]][2]
                self.block_label[block] = label_name

            for i in range(index+1, len(self.basic_blocks)):
                block = self.basic_blocks[i]
                if self.code[block[0]][1].lower() != 'label':
                    self.block_label[block] = label_name
                else:
                    break

        # for block in self.basic_blocks:
        #     print(self.block_label[block])
        #     if self.block_label[block] == None:
        #         self.block_label = 'main'

        # print(self.block_label)

    def label_line(self, label_name):
        '''
            find line num by label name 
        '''
        for i in range(len(self.code)):
            if self.code[i][1].lower() == 'label':
                if self.code[i][2] == label_name:
                    return self.code[i][0]

    def line_block(self, line_num):
        for i in range(len(self.basic_blocks)):
            block = self.basic_blocks[i]
            if block[0] <= line_num and block[1] >= line_num:
                return i

    def iterate_block(self):
        for i, block in enumerate(self.basic_blocks):
            self.next_use.append([])
            self.block_assign(i)

    def block_assign(self, block_index):
        '''
            read the code in the given block from the last line to first line
            update next use 
        '''

        block = self.basic_blocks[block_index]
        start, end = block
        code = self.code[start-1:end]
        preline = {}

        line = {}
        for i in range(len(code), 0, -1):
            code_line = code[i-1]
            line_num, _, lhs, op1, op2 = code_line

            if type(lhs) == Symbol:
                line[lhs] = float("inf")
            if type(lhs) == Symbol:
                line[op1] = line_num
            if type(lhs) == Symbol:
                line[op2] = line_num
            preline = line.copy()
            self.next_use[block_index].append(preline)

        self.next_use[block_index] = list(reversed(self.next_use[block_index]))
        # print(self.next_use[block_index])

    def get_block_minuse(self, block_index, line_num):
        '''
            return the symbol with min value of next use
        '''
        start = self.basic_blocks[block_index][0]
        next_use_block = self.next_use[block_index][line_num+1-start]
        max_line = 0
        max_sym = ''

        for sym in next_use_block.keys():
            if self.symbol_register[sym] != '' and float(next_use_block[sym]) > max_line:
                max_line = float(next_use_block[sym])
                max_sym = sym

        return max_sym

    def offset(self, op, scope_stack):
        try:
            return self.symtable[scope_stack[-1]].get(op.name).offset, None
        except ValueError:
            code = ['move $t9, $fp']
            scope_index = -1
            while True:
                scope_index -= 1
                scope = self.symtable[scope_stack[scope_index]]
                code.append('lw $t9, 76($t9)')
                try:
                    return scope.get(op.name).offset, code
                except ValueError:
                    pass

    def load_mem(self, op, reg, scope_stack):
        if not op.reference:
            off, code = self.offset(op, scope_stack)
            if code is None:
                return "lw {}, {}($fp)".format(reg, -off)
            else:
                return '\n'.join(code + ["lw {}, {}($t9)".format(reg, -off)])
        else:
            return "lw $t9, {}($fp) \nlw {}, 0($t9)".format(-op.offset, reg)

    def store_mem(self, op, reg, scope_stack):
        if not op.reference:
            off, code = self.offset(op, scope_stack)
            if code is None:
                return "sw {}, {}($fp)".format(reg, -off)
            else:
                return '\n'.join(code + ["sw {}, {}($t9)".format(reg, -off)])
        else:
            return "lw $t9, {}($fp) \nsw {}, 0($t9)".format(-op.offset, reg)

    def getReg(self, op, block_index, line_num, scope_stack):
        '''
            分配寄存器
        '''
        code_line = self.code[line_num]
        start, end = self.basic_blocks[block_index]
        reg = ''
        asmcode = []

        line_num, operation, lhs, op1, op2 = code_line

        if op in self.symbol_register:
            reg = self.symbol_register[op]

        elif len(self.unused_register) > 0:
            reg = self.unused_register[0]
            self.unused_register.remove(reg)
            self.symbol_register[op] = reg

            asmcode.append(self.load_mem(op, reg, scope_stack))

        else:
            var = self.get_block_minuse(block_index, line_num)
            reg = self.symbol_register[var]
            asmcode.append(self.store_mem(var, reg, scope_stack))
            del self.symbol_register[var]

            self.symbol_register[op] = reg

            asmcode.append(self.load_mem(op, reg, scope_stack))

        return reg, asmcode
