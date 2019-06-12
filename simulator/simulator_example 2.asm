# handle_label
ScopeInner:

# handle_binary
addi $t0, $0, 10

# handle_print
li $v0, 1
addi $a0, $t0, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall

# handle_return
addi $sp, $sp, 80
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
Summation:

# handle_binary
addi $t1, $0, 1

# handle_label
_l000000:

# handle_binary
addi $t1, $0, 2

# handle_label
_l000001:

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
addi $fp, $sp, -76
addi $sp, $sp, -96
jal ScopeInner

# handle_return
addi $sp, $sp, 88
addi $fp, $sp, 76
lw $v0, -4($fp)
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
move $t1, $v0
jr $t8

main:
# handle_input
li $v0, 5
syscall
addi $t2, $v0, 0

# handle_binary
addi $t2, $0, 20

# handle_binary
addi $t3, $0, 2

# handle_binary
add $t4, $t2, $t3

# handle_print
li $v0, 1
addi $a0, $t4, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall

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
addi $fp, $sp, -76
addi $sp, $sp, -96
jal ScopeInner

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
addi $fp, $sp, -76
addi $sp, $sp, -96
jal Summation

# handle_binary
add $t6, $t2, $t5

# handle_binary
addi $t2, $t6, 0

# handle_print
li $v0, 1
addi $a0, $t2, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall
li $v0, 10
syscall