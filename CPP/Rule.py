# x86汇编rule定义

register_list = ['eax', 'ebx', 'ecx', 'edx']
op32_dict = {
    '+':'addl',
    '-':'subl',
    '*':'imull',
    '/':'idivl',
    'AND':'and',
    'OR':'or',
    'MOD':'mod',
    'CMP':'cmp',
    'SHL':'shll',
    'SHR':'shrl',
}

jump_list = ['JMP', 'JL', 'JLE', 'JG', 'JGE', 'JNE', 'JE', 'JZ']
binary_list = ['+', '-', '*', '/', 'AND', 'OR', 'MOD', 'CMP', 'SHL', 'SHR']
operatore_list = ['UNARY', '=', 'LOADREF', 'STOREREF', 'CALL', 'LABEL', 'PARAM', 'RETURN', 'RETURNVAL', 'PRINT', 'SCAN']

