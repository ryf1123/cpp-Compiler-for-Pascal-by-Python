One major assumption in Assignment2 : SymbolTable contains entries for temporaries as well

- Misc:
    2. Designator Type Checks while assignment and others operations, like AddOp and MulOp
    3. NOT relational operator not working fine

# Things out of mind

## Classes and objects
- Replicating for classes

## Few things to keep in mind for demo
- Statements in IF-ELSE are always in BEGIN END blocks
- Repeat statement not working, the IR is not correct
- Testing division
- We need to ensure that whilw writing multiplicative expression, we'll write a = b*6; that is constant should be on right.
- Can't send complex expressions(maybe)

## Test cases
- test_arr_ls: loading and storing of arrays [TESTED]
- test_arr_func: sending the array to a function [TESTED]
- test_rec: testing recursion, by computing the sum againn [TESTED]
- test_while_array_simple: assigning array inside a while loop [TESTED]
- test_procedure: procedure,instead of a function
- test_case: switch case testing [TESTED]
- test_object: [TESTED]
- test_arr_rec: checking the effects of recursion on the array 
- test_while_array: Array assignments happening correctly. Issue with nested looping.

