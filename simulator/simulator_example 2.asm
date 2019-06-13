# handle_label
go:

# handle_cmp
lw $t0, 0($fp)
lw $t1, -8($fp)
li $t8, 1
seq $t1, $t0, $t8
sw $t0, 0($fp)
sw $t1, -8($fp)

# handle_jmp
li $t8, 0
beq $t1, $t8, _l000000

# handle_binary
lw $t0, -4($fp)
addi $t0, $0, 1
sw $t0, -4($fp)

# handle_jmp
j _l000001

# handle_label
_l000000:

# handle_cmp
lw $t0, 0($fp)
lw $t1, -12($fp)
li $t8, 2
seq $t1, $t0, $t8
sw $t0, 0($fp)
sw $t1, -12($fp)

# handle_jmp
li $t8, 0
beq $t1, $t8, _l000002

# handle_binary
lw $t0, -4($fp)
addi $t0, $0, 1
sw $t0, -4($fp)

# handle_jmp
j _l000003

# handle_label
_l000002:

# handle_binary
lw $t0, 0($fp)
lw $t1, -16($fp)
subi $t1, $t0, 1

# handle_params
sw $t1, -76($sp)
sw $t0, 0($fp)
sw $t1, -16($fp)

# handle_call
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

# handle_binary
lw $t0, 0($fp)
lw $t1, -24($fp)
subi $t1, $t0, 2

# handle_params
sw $t1, -76($sp)
sw $t0, 0($fp)
sw $t1, -24($fp)

# handle_call
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

# handle_binary
lw $t0, -20($fp)
lw $t1, -28($fp)
lw $t2, -32($fp)
add $t2, $t0, $t1

# handle_binary
lw $t3, -4($fp)
addi $t3, $t2, 0
sw $t0, -20($fp)
sw $t1, -28($fp)
sw $t2, -32($fp)
sw $t3, -4($fp)

# handle_label
_l000003:

# handle_label
_l000001:

# handle_return
lw $v0, -4($fp)
addi $sp, $sp, 112
addi $fp, $sp, 76
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

# handle_label
main:
move $fp, $sp

# handle_params
li $t8, 10
sw $t8, -76($sp)

# handle_call
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

# handle_binary
lw $t0, -4($fp)
lw $t1, 0($fp)
addi $t1, $t0, 0

# handle_print
li $v0, 1
addi $a0, $t1, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall
sw $t0, -4($fp)
sw $t1, 0($fp)
li $v0, 10
syscall