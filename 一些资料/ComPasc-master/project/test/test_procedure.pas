PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;
z = 7;
   
TYPE
   a1 = ARRAY[x..10,y..10,z..10] OF INTEGER;

VAR 
a	      : INTEGER; 

PROCEDURE MyFunc(size: INTEGER;);
BEGIN
    size := size + 1;
    WRITELN(size);
END;


BEGIN
   MyFunc(x);
END;
