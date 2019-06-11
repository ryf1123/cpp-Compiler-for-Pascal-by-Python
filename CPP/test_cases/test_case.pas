PROGRAM Greeting;

CONST
x = 4;

var y : integer;
   
BEGIN

   CASE x OF
    1: y := x + 1;
    2: y := x + 2;
    3: y := x + 3;
    END;
    BEGIN
        y := x + 5;
    END;

   WRITELN(y);
END.
