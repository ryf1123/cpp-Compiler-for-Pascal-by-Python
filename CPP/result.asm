
# 0 LABEL gcd main.gcd None
gcd:

# 1 = Symbol(`_t000000`, boolean, var, 12) Symbol(`b`, integer, var, 4) 0
lw $t0, -4($fp)
lw $t1, -12($fp)
li $t8, 0
seq $t1, $t0, $t8

# 2 BEQ _l000000 Symbol(`_t000000`, boolean, var, 12) False
sw $t0, -4($fp)
sw $t1, -12($fp)
li $t8, 0
beq $t1, $t8, _l000000

# 3 + Symbol(`_return`, integer, var, 8, [('a', 'integer', False), ('b', 'integer', False)]) Symbol(`a`, integer, var, 0) 0
lw $t0, 0($fp)
lw $t1, -8($fp)
li $t8, 0
add $t1, $t0, $t8

# 4 JMP _l000001 None None
sw $t0, 0($fp)
sw $t1, -8($fp)
j _l000001

# 5 LABEL _l000000 None None
_l000000:

# 6 MOD Symbol(`_t000001`, integer, var, 16) Symbol(`a`, integer, var, 0) Symbol(`b`, integer, var, 4)
lw $t0, 0($fp)
lw $t1, -4($fp)
lw $t2, -16($fp)
div $t0, $t1
mfhi $t2

# 7 PARAM None Symbol(`b`, integer, var, 4) None
sw $t1, -76($sp)

# 8 PARAM None Symbol(`_t000001`, integer, var, 16) None
sw $t2, -80($sp)

# 9 CALL Symbol(`_t000002`, integer, var, 20) gcd main
sw $t0, 0($fp)
sw $t1, -4($fp)
sw $t2, -16($fp)
# = parent's
lw $t8, 76($fp)
sw $t8, 0($sp)
sw $fp, -4($sp)
sw $ra, -8($sp)
sw $8, -12($sp)
sw $9, -16($sp)
sw $10, -20($sp)
sw $11, -24($sp)
sw $12, -28($sp)
sw $13, -32($sp)
sw $14, -36($sp)
sw $15, -40($sp)
sw $16, -44($sp)
sw $17, -48($sp)
sw $18, -52($sp)
sw $19, -56($sp)
sw $20, -60($sp)
sw $21, -64($sp)
sw $22, -68($sp)
sw $23, -72($sp)
addi $fp $sp -76
addi $sp $sp -100
jal gcd
lw $t0, -20($fp)
move, $t0, $v0
sw $t0, -20($fp)

# 10 + Symbol(`_return`, integer, var, 8, [('a', 'integer', False), ('b', 'integer', False)]) Symbol(`_t000002`, integer, var, 20) 0
lw $t0, -20($fp)
lw $t1, -8($fp)
li $t8, 0
add $t1, $t0, $t8
sw $t0, -20($fp)
sw $t1, -8($fp)

# 11 LABEL _l000001 None None
_l000001:

# 12 RETURN Symbol(`_return`, integer, var, 8, [('a', 'integer', False), ('b', 'integer', False)]) main.gcd None
lw $v0, -8($fp)
addi $sp, $sp, 100
lw $fp, 72($fp)
lw $8, -12($sp)
lw $9, -16($sp)
lw $10, -20($sp)
lw $11, -24($sp)
lw $12, -28($sp)
lw $13, -32($sp)
lw $14, -36($sp)
lw $15, -40($sp)
lw $16, -44($sp)
lw $17, -48($sp)
lw $18, -52($sp)
lw $19, -56($sp)
lw $20, -60($sp)
lw $21, -64($sp)
lw $22, -68($sp)
lw $23, -72($sp)
move $t8, $ra
lw $ra, -8($sp)
jr $t8

# 13 LABEL main None None
main:
move $fp, $sp
addi $sp, $sp, -16

# 14 PARAM None 9 None
li $t8, 9
sw $t8, -76($sp)

# 15 PARAM None 36 None
li $t8, 36
sw $t8, -80($sp)

# 16 CALL Symbol(`_t000000`, integer, var, 4) gcd main
# = fp
sw $fp, 0($sp)
sw $fp, -4($sp)
sw $ra, -8($sp)
sw $8, -12($sp)
sw $9, -16($sp)
sw $10, -20($sp)
sw $11, -24($sp)
sw $12, -28($sp)
sw $13, -32($sp)
sw $14, -36($sp)
sw $15, -40($sp)
sw $16, -44($sp)
sw $17, -48($sp)
sw $18, -52($sp)
sw $19, -56($sp)
sw $20, -60($sp)
sw $21, -64($sp)
sw $22, -68($sp)
sw $23, -72($sp)
addi $fp $sp -76
addi $sp $sp -100
jal gcd
lw $t0, -4($fp)
move, $t0, $v0
sw $t0, -4($fp)

# 17 PARAM None 3 None
li $t8, 3
sw $t8, -76($sp)

# 18 PARAM None 6 None
li $t8, 6
sw $t8, -80($sp)

# 19 CALL Symbol(`_t000001`, integer, var, 8) gcd main
# = fp
sw $fp, 0($sp)
sw $fp, -4($sp)
sw $ra, -8($sp)
sw $8, -12($sp)
sw $9, -16($sp)
sw $10, -20($sp)
sw $11, -24($sp)
sw $12, -28($sp)
sw $13, -32($sp)
sw $14, -36($sp)
sw $15, -40($sp)
sw $16, -44($sp)
sw $17, -48($sp)
sw $18, -52($sp)
sw $19, -56($sp)
sw $20, -60($sp)
sw $21, -64($sp)
sw $22, -68($sp)
sw $23, -72($sp)
addi $fp $sp -76
addi $sp $sp -100
jal gcd
lw $t0, -8($fp)
move, $t0, $v0
sw $t0, -8($fp)

# 20 * Symbol(`_t000002`, integer, var, 12) Symbol(`_t000000`, integer, var, 4) Symbol(`_t000001`, integer, var, 8)
lw $t0, -4($fp)
lw $t1, -8($fp)
lw $t2, -12($fp)
mul $t2, $t0, $t1

# 21 + Symbol(`ans`, integer, var, 0) Symbol(`_t000002`, integer, var, 12) 0
lw $t3, 0($fp)
li $t8, 0
add $t3, $t2, $t8

# 22 PRINT None Symbol(`ans`, integer, var, 0) None
li $v0, 1
addi $a0, $t3, 0
syscall

# 23 PRINTLN None None None
li $v0, 11
addi $a0, $0, 32
syscall
sw $t0, -4($fp)
sw $t1, -8($fp)
sw $t2, -12($fp)
sw $t3, 0($fp)
li $v0, 10
syscall
