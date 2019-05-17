PROGRAM Greeting;

VAR 
y, z, a: INTEGER; 

CONSTANT
x = 4;
   
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
