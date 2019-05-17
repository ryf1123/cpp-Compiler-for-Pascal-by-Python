PROGRAM Greeting;

//Just testing the sending of array base pointer

CONSTANT
x = 5;
y = 6;
z = 7;
   
TYPE
    a1 = ARRAY[x..10,y..10] OF INTEGER;

VAR
   a : INTEGER;
   b : INTEGER;
   a2: a1;

FUNCTION MyFunc(arr: a1;size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc : INTEGER;
   yo  : INTEGER;
BEGIN
    yo := arr[7,8];
    // yo should be 11
    WRITELN(yo);
    {yo := 99;}
    {arr[7,8] := 99;}
    MyFunc := temp + size - 8; 
END;


BEGIN
   a := x + y;  
   WRITELN(a);

   a2[7,8] := a;

   b := MyFunc(a2,x,y); 
   WRITELN(b);

   b := a2[7,8]; 
   WRITELN(b);

END;
