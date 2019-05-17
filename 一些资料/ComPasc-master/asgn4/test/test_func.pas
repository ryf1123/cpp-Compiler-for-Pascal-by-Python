PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;
z = 7;
   
TYPE
   a1 = ARRAY[x..10,y..10,z..10] OF INTEGER;

VAR 
a	      : INTEGER; 
height, width : INTEGER; 
c	      : CHAR;
   a2	      : a1;

PROCEDURE MyFunc(size: INTEGER;);
BEGIN
    size := size + 1;
END;


BEGIN

   MyFunc(x);

END;
