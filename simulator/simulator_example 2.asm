# handle_label

main:
move $sp $gp
# handle_binary
lw $t0, 0($fp)
addi $t0, $0, 3

# handle_binary
lw $t1, -4($fp)
addi $t1, $t0, 1

# handle_binary
addi $t0, $t1, 0

# handle_print
li $v0, 1
addi $a0, $t0, 0
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall

# handle_print
li $v0, 1
addi $a0, $0, 1
syscall

# handle_print
li $v0, 11
addi $a0, $0, 32
syscall
li $v0, 10
syscall