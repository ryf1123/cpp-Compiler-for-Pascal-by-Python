
# 0 LABEL go main.go None
go:

# 1 > Symbol(`_t000000`, boolean, var, 20) Symbol(`a`, integer, var, 4) 0
lw $t0, -4($fp)
lw $t1, -20($fp)
li $t8, 0
sgt $t1, $t0, $t8

# 2 BEQ _l000000 Symbol(`_t000000`, boolean, var, 20) False
sw $t0, -4($fp)
sw $t1, -20($fp)
li $t8, 0
beq $t1, $t8, _l000000

# 3 - Symbol(`_t000001`, integer, var, 24) Symbol(`a`, integer, var, 4) 1
lw $t0, -4($fp)
lw $t1, -24($fp)
li $t8, 1
sub $t1, $t0, $t8

# 4 REFER None Symbol(`b`, integer, var, 0, *) None
sw $t0, -4($fp)
sw $t1, -24($fp)
lw $t9, 0($fp) 
lw $t0, 0($t9)

# pass value because it is an address already. 
lw $t9, 0($fp)
sw $t9, -76($sp)
lw $t9, 0($fp) 
sw $t0, 0($t9)

# 5 PARAM None Symbol(`_t000001`, integer, var, 24) None
lw $t0, -24($fp)
sw $t0, -80($sp)

# 6 CALL Symbol(`_t000002`, integer, var, 28) go main
sw $t0, -24($fp)
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
addi $sp $sp -120
jal go
lw $t0, -28($fp)
move, $t0, $v0
sw $t0, -28($fp)

# 7 * Symbol(`_t000003`, integer, var, 32) Symbol(`a`, integer, var, 4) Symbol(`_t000002`, integer, var, 28)
lw $t0, -4($fp)
lw $t1, -28($fp)
lw $t2, -32($fp)
mul $t2, $t0, $t1

# 8 + Symbol(`_return`, integer, var, 8, [('b', 'integer', True), ('a', 'integer', False)]) Symbol(`_t000003`, integer, var, 32) 0
lw $t3, -8($fp)
li $t8, 0
add $t3, $t2, $t8

# 9 JMP _l000001 None None
sw $t0, -4($fp)
sw $t1, -28($fp)
sw $t2, -32($fp)
sw $t3, -8($fp)
j _l000001

# 10 LABEL _l000000 None None
_l000000:

# 11 + Symbol(`_return`, integer, var, 8, [('b', 'integer', True), ('a', 'integer', False)]) 1 0
lw $t0, -8($fp)
addi $t0, $0, 1
sw $t0, -8($fp)

# 12 LABEL _l000001 None None
_l000001:

# 13 + Symbol(`_t000004`, integer, var, 36) Symbol(`b`, integer, var, 0, *) Symbol(`_return`, integer, var, 8, [('b', 'integer', True), ('a', 'integer', False)])
lw $t9, 0($fp) 
lw $t0, 0($t9)
lw $t1, -8($fp)
lw $t2, -36($fp)
add $t2, $t0, $t1
lw $t9, 0($fp) 
sw $t0, 0($t9)
sw $t1, -8($fp)
sw $t2, -36($fp)

# 14 + Symbol(`b`, integer, var, 0, *) Symbol(`_t000004`, integer, var, 36) 0
lw $t0, -36($fp)
lw $t9, 0($fp) 
lw $t1, 0($t9)
li $t8, 0
add $t1, $t0, $t8
sw $t0, -36($fp)
lw $t9, 0($fp) 
sw $t1, 0($t9)

# 15 + Symbol(`_t000005`, integer, var, 40) Symbol(`k`, integer, var, 4) Symbol(`_return`, integer, var, 8, [('b', 'integer', True), ('a', 'integer', False)])
move $t9, $fp
lw $t9, 76($t9)
lw $t0, -4($t9)
lw $t1, -8($fp)
lw $t2, -40($fp)
add $t2, $t0, $t1

# 16 + Symbol(`k`, integer, var, 4) Symbol(`_t000005`, integer, var, 40) 0
li $t8, 0
add $t0, $t2, $t8

# 17 RETURN Symbol(`_return`, integer, var, 8, [('b', 'integer', True), ('a', 'integer', False)]) main.go None
move $t9, $fp
lw $t9, 76($t9)
sw $t0, -4($t9)
sw $t1, -8($fp)
sw $t2, -40($fp)
lw $v0, -8($fp)
addi $sp, $sp, 120
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

# 18 LABEL main None None
main:
move $fp, $sp
addi $sp, $sp, -12

# 19 + Symbol(`k`, integer, var, 4) 0 0
lw $t0, -4($fp)
addi $t0, $0, 0

# 20 REFER None Symbol(`k`, integer, var, 4) None

# pass address.
addi $t8, $fp, -4
sw $t8, -76($sp)

# 21 PARAM None 5 None
li $t8, 5
sw $t8, -80($sp)

# 22 CALL Symbol(`_t000000`, integer, var, 8) go main
sw $t0, -4($fp)
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
addi $sp $sp -120
jal go
lw $t0, -8($fp)
move, $t0, $v0
sw $t0, -8($fp)

# 23 + Symbol(`f`, integer, var, 0) Symbol(`_t000000`, integer, var, 8) 0
lw $t0, -8($fp)
lw $t1, 0($fp)
li $t8, 0
add $t1, $t0, $t8

# 24 PRINT None Symbol(`f`, integer, var, 0) None
li $v0, 1
addi $a0, $t1, 0
syscall

# 25 PRINTLN None None None
li $v0, 11
addi $a0, $0, 10
syscall

# 26 PRINT None Symbol(`k`, integer, var, 4) None
lw $t2, -4($fp)
li $v0, 1
addi $a0, $t2, 0
syscall

# 27 PRINTLN None None None
li $v0, 11
addi $a0, $0, 10
syscall
sw $t0, -8($fp)
sw $t1, 0($fp)
sw $t2, -4($fp)
li $v0, 10
syscall
