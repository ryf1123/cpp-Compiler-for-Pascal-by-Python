PROGRAM Greeting;

CONSTANT
x = 5;
y = 1;
z = 7;
   
TYPE
   a1 = ARRAY[y..10] OF INTEGER;

VAR 
a : INTEGER;
a2 : a1;
d : INTEGER;

FUNCTION MyFunc(arr: a1;size: INTEGER;):INTEGER;
VAR
    MyFunc : INTEGER;
    i : INTEGER;
BEGIN
    IF size = 1 THEN
        BEGIN
            MyFunc := 1;
            arr[2] := 10;
        END;
    ELSE
        BEGIN
            i := size - 1;
            MyFunc := MyFunc(arr,i) + size;
            WRITELN(size);
        END;
END;


BEGIN
    a2[2] := 3;
    a := MyFunc(a2,x);
    WRITELN(a);
    d := a2[2]; //should be 10
    WRITELN(d);
END;
