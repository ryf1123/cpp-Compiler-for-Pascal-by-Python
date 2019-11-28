PROGRAM exObjects;

CONSTANT
a = 4;
b = 7;

TYPE 
   Rectangle = OBJECT  
   PUBLIC
      length, width: INTEGER; 

      CONSTRUCTOR init(l, w: INTEGER);
      { procedure setlength(l: integer); }
      { function getlength(): integer;   }
      
      { procedure setwidth(w: integer);   }
      { function getwidth(): integer;   }
      
      { procedure draw; }
END;

VAR
   r1: Rectangle;
   
CONSTRUCTOR Rectangle.init(l, w: INTEGER);
BEGIN
   length := l;
   width := w;
END;

{ procedure Rectangle.setlength(l: integer); }
{ begin }
{    length := l; }
{ end; }

{ procedure Rectangle.setwidth(w: integer); }
{ begin }
{    width :=w; }
{ end; }

{ function Rectangle.getlength(): integer;   }
{ begin }
{    getlength := length; }
{ end; }

{ function Rectangle.getwidth(): integer;   }
{ begin }
{    getwidth := width; }
{ end; }

BEGIN
   r1.init(a, b);
   WRITELN(r1.length);
END;
