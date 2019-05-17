PROGRAM Greeting;

CONSTANT
x = 3;

VAR 
a    : INTEGER; 

FUNCTION foo(x: INTEGER;):INTEGER;
VAR
    foo: INTEGER;
BEGIN
    foo := 3;
END;


BEGIN
    a := foo(x);
END;
