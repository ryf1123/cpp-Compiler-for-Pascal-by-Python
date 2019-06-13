# handle_label
main:
move $fp, $sp

# handle_binary
lw $t0, 0($fp)
addi $t0, $0, 10
sw $t0, 0($fp)

# handle_label
_l000000:

# handle_print
lw $t0, 0($fp)
li $v0, 1
addi $a0, $t0, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall

# handle_binary
lw $t1, -4($fp)
addi $t1, $t0, 1

# handle_binary
addi $t0, $t1, 0

# handle_cmp
lw $t2, -8($fp)
li $t8, 31
seq $t2, $t0, $t8

# handle_jmp
li $t8, 0

sw $t0, 0($fp)
sw $t1, -4($fp)
sw $t2, -8($fp)
beq $t2, $t8, _l000000
li $v0, 10
syscall