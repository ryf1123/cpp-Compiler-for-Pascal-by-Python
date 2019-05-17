PROGRAM Greeting;


CONSTANT
x = 5;
y = 6;
z = 7;
   
VAR
   a : INTEGER;
   b : INTEGER;

FUNCTION MyFunc(size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc : INTEGER;
   yo  : INTEGER;
BEGIN
    yo := size + 1; // yo = 12
    MyFunc := yo*temp + size - 8; // MyFunc = 72 + 11 - 8
END;


BEGIN
   a := x + y; //a = 11
   b := MyFunc(a,y); //b should be 75 here
   WRITELN(b);
END;
