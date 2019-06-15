
# 0 LABEL go main.go None
go:

# 1 = Symbol(`_t000000`, boolean, var, 8) Symbol(`a`, integer, var, 0) 1
lw $t0, 0($fp)
lw $t1, -8($fp)
li $t8, 1
seq $t1, $t0, $t8

# 2 BEQ _l000000 Symbol(`_t000000`, boolean, var, 8) False
sw $t0, 0($fp)
sw $t1, -8($fp)
li $t8, 0
beq $t1, $t8, _l000000

# 3 + Symbol(`_return`, integer, var, 4, [('a', 'integer', False)]) 1 0
lw $t0, -4($fp)
addi $t0, $0, 1

# 4 JMP _l000001 None None
sw $t0, -4($fp)
j _l000001

# 5 LABEL _l000000 None None
_l000000:

# 6 = Symbol(`_t000001`, boolean, var, 12) Symbol(`a`, integer, var, 0) 2
lw $t0, 0($fp)
lw $t1, -12($fp)
li $t8, 2
seq $t1, $t0, $t8

# 7 BEQ _l000002 Symbol(`_t000001`, boolean, var, 12) False
sw $t0, 0($fp)
sw $t1, -12($fp)
li $t8, 0
beq $t1, $t8, _l000002

# 8 + Symbol(`_return`, integer, var, 4, [('a', 'integer', False)]) 1 0
lw $t0, -4($fp)
addi $t0, $0, 1

# 9 JMP _l000003 None None
sw $t0, -4($fp)
j _l000003

# 10 LABEL _l000002 None None
_l000002:

# 11 - Symbol(`_t000002`, integer, var, 16) Symbol(`a`, integer, var, 0) 1
lw $t0, 0($fp)
lw $t1, -16($fp)
li $t8, 1
sub $t1, $t0, $t8

# 12 PARAM None Symbol(`_t000002`, integer, var, 16) None
sw $t1, -76($sp)

# 13 CALL Symbol(`_t000003`, integer, var, 20) go main
sw $t0, 0($fp)
sw $t1, -16($fp)
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
addi $sp $sp -112
jal go
lw $t0, -20($fp)
move, $t0, $v0
sw $t0, -20($fp)

# 14 - Symbol(`_t000004`, integer, var, 24) Symbol(`a`, integer, var, 0) 2
lw $t0, 0($fp)
lw $t1, -24($fp)
li $t8, 2
sub $t1, $t0, $t8

# 15 PARAM None Symbol(`_t000004`, integer, var, 24) None
sw $t1, -76($sp)

# 16 CALL Symbol(`_t000005`, integer, var, 28) go main
sw $t0, 0($fp)
sw $t1, -24($fp)
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
addi $sp $sp -112
jal go
lw $t0, -28($fp)
move, $t0, $v0
sw $t0, -28($fp)

# 17 + Symbol(`_t000006`, integer, var, 32) Symbol(`_t000003`, integer, var, 20) Symbol(`_t000005`, integer, var, 28)
lw $t0, -20($fp)
lw $t1, -28($fp)
lw $t2, -32($fp)
add $t2, $t0, $t1

# 18 + Symbol(`_return`, integer, var, 4, [('a', 'integer', False)]) Symbol(`_t000006`, integer, var, 32) 0
lw $t3, -4($fp)
li $t8, 0
add $t3, $t2, $t8
sw $t0, -20($fp)
sw $t1, -28($fp)
sw $t2, -32($fp)
sw $t3, -4($fp)

# 19 LABEL _l000003 None None
_l000003:

# 20 LABEL _l000001 None None
_l000001:

# 21 RETURN Symbol(`_return`, integer, var, 4, [('a', 'integer', False)]) main.go None
lw $v0, -4($fp)
addi $sp, $sp, 112
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

# 22 LABEL main None None
main:
move $fp, $sp
addi $sp, $sp, -8

# 23 PARAM None 12 None
li $t8, 12
sw $t8, -76($sp)

# 24 CALL Symbol(`_t000000`, integer, var, 4) go main
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
addi $sp $sp -112
jal go
lw $t0, -4($fp)
move, $t0, $v0
sw $t0, -4($fp)

# 25 + Symbol(`i`, integer, var, 0) Symbol(`_t000000`, integer, var, 4) 0
lw $t0, -4($fp)
lw $t1, 0($fp)
li $t8, 0
add $t1, $t0, $t8

# 26 PRINT None Symbol(`i`, integer, var, 0) None
li $v0, 1
addi $a0, $t1, 0
syscall

# 27 PRINTLN None None None
li $v0, 11
addi $a0, $0, 10
syscall
sw $t0, -4($fp)
sw $t1, 0($fp)
li $v0, 10
syscall
