PROGRAM Greeting;

CONSTANT
x = 0;
y = 1;
z = 7;
k = 8;

TYPE
   a1 = ARRAY[x..10] OF INTEGER;

VAR 
a2: a1;
i : INTEGER;
j : INTEGER;
c : INTEGER;

BEGIN
    i := 0;
    c := x+6;
    WHILE i < 10 DO
        BEGIN
            a2[i] := c;
            j := a2[i];
	   WRITELN(a2[i]);
            i := i + 1;
        END;
END;
