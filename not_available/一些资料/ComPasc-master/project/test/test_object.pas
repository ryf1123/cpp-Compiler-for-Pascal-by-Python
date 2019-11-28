Program TestObjects;

CONSTANT
a = 7;
b = 8;

Type
   DrawingObject = Object
      x, y : INTEGER;
      height, width : INTEGER;       // replaced 'single' by 'integer' for now
   end;
 
Var
  Rectangle : DrawingObject;
   x, y	    :  INTEGER;

FUNCTION MyFunc(o1: DrawingObject; size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc : INTEGER;
   yo  : INTEGER;
BEGIN
   yo := o1.x;
   yo := yo + o1.y;
    // yo should be 11
    WRITELN(yo);
    MyFunc := temp + size - 8; 
END;

begin
 
  Rectangle.x:= 50;  //  the fields specific to the variable "Rectangle"
  Rectangle.y:= 100;
   y := MyFunc(Rectangle, a, b);
   WRITELN(y);
   
end;
