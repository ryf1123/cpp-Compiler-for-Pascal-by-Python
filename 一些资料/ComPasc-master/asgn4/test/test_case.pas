PROGRAM Greeting;

VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;

CONSTANT
x = 1;
   
BEGIN

   CASE x OF
    1: y := x + 1;
    2: y := x + 2;
    3: y := x + 3;
    ELSE
    BEGIN
        y := x + 5;
    END;
   END;
   WRITELN(y);
END;
