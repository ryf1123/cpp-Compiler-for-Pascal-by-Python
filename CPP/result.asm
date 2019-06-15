
# 0 + Symbol(`a`, integer, const, 0, 2) 2 0
lw $t0, 0($fp)
addi $t0, $0, 2

# 1 + Symbol(`flag`, boolean, const, 4, True) True 0
lw $t1, -4($fp)
addi $t1, $0, 1
sw $t0, 0($fp)
sw $t1, -4($fp)

# 2 LABEL main None None
main:
move $fp, $sp
addi $sp, $sp, -112

# 3 + Symbol(`y`, integer, var, 12) 2 0
lw $t0, -12($fp)
addi $t0, $0, 2

# 4 = Symbol(`_t000002`, boolean, var, 52) 1 1
lw $t1, -52($fp)
addi $t1, $0, 1

# 5 + Symbol(`x`, boolean, var, 8) Symbol(`_t000002`, boolean, var, 52) 0
lw $t2, -8($fp)
li $t8, 0
add $t2, $t1, $t8

# 6 AND Symbol(`_t000003`, boolean, var, 56) True True
lw $t3, -56($fp)
addi $t3, $0, 1

# 7 AND Symbol(`_t000004`, boolean, var, 60) Symbol(`_t000003`, boolean, var, 56) True
lw $t4, -60($fp)
li $t8, 1
and $t4, $t3, $t8

# 8 NOT Symbol(`_t000005`, boolean, var, 64) Symbol(`flag`, boolean, const, 4, True) None
lw $t5, -4($fp)
lw $t6, -64($fp)
not $t6, $t5

# 9 AND Symbol(`_t000006`, boolean, var, 68) Symbol(`_t000004`, boolean, var, 60) Symbol(`_t000005`, boolean, var, 64)
lw $t7, -68($fp)
and $t7, $t4, $t6

# 10 + Symbol(`q`, boolean, var, 16) Symbol(`_t000006`, boolean, var, 68) 0
lw $s0, -16($fp)
li $t8, 0
add $s0, $t7, $t8

# 11 + Symbol(`_t000007`, integer, var, 72) Symbol(`a`, integer, const, 0, 2) 13
lw $s1, 0($fp)
lw $s2, -72($fp)
li $t8, 13
add $s2, $s1, $t8

# 12 DIV Symbol(`_t000008`, integer, var, 76) Symbol(`_t000007`, integer, var, 72) 5

# 13 MOD Symbol(`_t000009`, integer, var, 80) Symbol(`_t000008`, integer, var, 76) 1
lw $s3, -76($fp)
lw $s4, -80($fp)
li $t8, 1
div $s3, $t8
mfhi $s4

# 14 + Symbol(`x`, boolean, var, 8) Symbol(`_t000009`, integer, var, 80) 0
li $t8, 0
add $t2, $s4, $t8

# 15 STOREREF 1 peoples Symbol(`x`, boolean, var, 8)

# 16 LOADREF Symbol(`_t000010`, people_arr, var, 84) peoples 0

# 17 + Symbol(`x`, boolean, var, 8) Symbol(`_t000010`, people_arr, var, 84) 0
lw $s5, -84($fp)
li $t8, 0
add $t2, $s5, $t8

# 18 STOREREF 1 newton score

# 19 LOADREF Symbol(`_t000011`, integer, var, 108) newton score

# 20 + Symbol(`x`, boolean, var, 8) Symbol(`_t000011`, integer, var, 108) 0
lw $s6, -108($fp)
li $t8, 0
add $t2, $s6, $t8
sw $t0, -12($fp)
sw $t1, -52($fp)
sw $t2, -8($fp)
sw $t3, -56($fp)
sw $t4, -60($fp)
sw $t5, -4($fp)
sw $t6, -64($fp)
sw $t7, -68($fp)
sw $s0, -16($fp)
sw $s1, 0($fp)
sw $s2, -72($fp)
sw $s3, -76($fp)
sw $s4, -80($fp)
sw $s5, -84($fp)
sw $s6, -108($fp)
li $v0, 10
syscall
