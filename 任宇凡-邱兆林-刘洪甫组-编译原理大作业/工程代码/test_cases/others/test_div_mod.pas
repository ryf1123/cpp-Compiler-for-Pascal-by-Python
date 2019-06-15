PROGRAM Greeting;

CONST
b = 5;
c = 6;
d = 7;
e = 8; 


VAR 
a    : INTEGER; 

BEGIN
    a := b + c - d/e*b MOD 10;
    WRITELN(a);
END.
