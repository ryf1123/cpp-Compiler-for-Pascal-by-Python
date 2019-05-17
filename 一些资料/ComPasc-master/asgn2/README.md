# Intro
Would essentially use Quadruple 3 AC structure
The precise 3AC Structure and Syntax is available [here](./3AC_Complete.md)

# Build and Folder Details

## Folder Details
- main.py: program starts executing from here
- SymTable.py: symboltable and symboltable entry classes
- varAllocateRegister.py: basic blocks, nextuse and all such things
- ThreeAddrCode.py: structure and helpers for 3AC
- codegen.py: This is the heart of assignment. Assembly code is generated here

## To Build
```
cd asgn2
make
bin/codegen test/test1.ir
```

## data types
- int:
- string:
- char:
- array: 

## instructions and their types

- Unary: op = unary, lhs = variable to store into, op1 = '+,-, Nothing', op2 = variable with which you want to do things

- Binary: lineno,op,lhs,op1,op2
    - + : op = add
    - - : op  = sub
    - * : op = mul
    - \ : op = div
    - SHL: op = shl
    - SHR: op = shr
    - MOD: op = mod
    - OR: op = or
    - AND: op = and

- Array reference:

- If statement:
    - our IR won't have if statement. We will simply have (un)conditional jump

- Goto Statement:
    - (un)conditional jumps here

# Validity checking with our IR set

## Arithmetic
- Easy

## Labels
- Conversion of labels to line numbers. Any potential pit falls
- [Meeting] Assembly supports labels, no change required.

## if-else
- Can be modelled easily using if-goto

## while, repeat
- Have a loop condition, followed by jump stmt out of the loop, body, and update and jump back to check condition

## function calls
- Replace with a label
- Ask Sir about how we can look for arguments. Other than that can be essentially modelled as a program
- [Meeting] Give labels to functions, and the standard way for function argument IR is shown below: 
    ```
    param a
    param b
    param c
    call foo
    ```

## lambda call
- Maybe convert it to a simple function call in the IR?
- [Meeting] Yes, May have to keep a dict while converting to function to account for environ variables.

## Input-Output
- Direct interfacing by calling C calls in x86

## Classes and Objects
- Ask Sir about inheritance
- [Meeting] Classes boiled down to IR and details already exisiting in SymTable

