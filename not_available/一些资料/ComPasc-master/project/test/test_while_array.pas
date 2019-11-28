PROGRAM Greeting;

CONSTANT
x = 1;
y = 1;
z = 7;
k = 8;

TYPE
   a1 = ARRAY[x..10,y..10] OF INTEGER;

VAR 
a2: a1;
i : INTEGER;
j : INTEGER;
c : INTEGER;

BEGIN
    i := 1;
    j := 1;
    c := x+y;
    WHILE i < 10 DO
        BEGIN
            WHILE j < 10 DO
                BEGIN
                    a2[i,j] := c;
                    WRITELN(a2[i,j]);
                    j := j + 1;
                END;
            i := i + 1;
        END;
END;
