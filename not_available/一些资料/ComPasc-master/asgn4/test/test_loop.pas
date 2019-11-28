PROGRAM Greeting;

VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;

CONSTANT
z = 7;

BEGIN

   x := 3;
   y := 6;
   REPEAT
      x := x - 1;
   UNTIL x<5;
    WHILE x < 5 DO
    BEGIN
       x := x + 1;
       WHILE y < 5 DO
       BEGIN
   	  y := y + 1;
   	  IF y=4 THEN
   	     BEGIN
   		BREAK;
   	     END;
       END;
       IF x=3 THEN
       BEGIN
   	  CONTINUE;
       END;
    END;
   REPEAT
        x := x + 1;
    UNTIL x<9;

END;
