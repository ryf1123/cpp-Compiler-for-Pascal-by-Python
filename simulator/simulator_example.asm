.data
msg1: .asciiz "hello world"

.text
.globl main
main:

addi $29, $29, -4

li $v0, 6
syscall

mov.s $f12, $f0

li $v0, 2
syscall

li $v0, 10
syscall
