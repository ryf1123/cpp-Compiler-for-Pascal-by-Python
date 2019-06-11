# x86汇编rule定义

register_list = [
    '$zero',
    '$at',
    '$v0',
    '$v1',
    '$a0',
    '$a1',
    '$a2',
    '$a3',
    '$t0',
    '$t1',
    '$t2',
    '$t3',
    '$t4',
    '$t5',
    '$t6',
    '$t7',
    '$s0',
    '$s1',
    '$s2',
    '$s3',
    '$s4',
    '$s5',
    '$s6',
    '$s7',
    '$t8',
    '$t9',
    '$k0',
    '$k1',
    '$gp',
    '$sp',
    '$fp',
    '$ra'
]

unused_register_list = [
    '$t0',
    '$t1',
    '$t2',
    '$t3',
    '$t4',
    '$t5',
    '$t6',
    '$t7',
    '$s0',
    '$s1',
    '$s2',
    '$s3',
    '$s4',
    '$s5',
    '$s6',
    '$s7',
    '$t8',
    '$t9'
]

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

