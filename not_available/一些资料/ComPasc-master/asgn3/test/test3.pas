program exObjects;
type 
   Rectangle = object  
   public
      length, width: integer; 
      
      constructor init(l, w: integer);
      
      procedure setlength(l: integer);
      function getlength(): integer;  
      
      procedure setwidth(w: integer);  
      function getwidth(): integer;  
      
      procedure draw;
end;

   Square = object  
   public
      length, width: integer; 
      
      constructor init(l, w: integer);
      
      procedure setlength(l: integer);
      function getlength(): integer;  
      
      procedure setwidth(w: integer);  
      function getwidth(): integer;  
      
      procedure draw;
end;

type
   
var
   r1: Rectangle;
   pr1: ^Rectangle;

constructor Rectangle.init(l, w: integer);
begin
   length := l;
   width := w;
end;

procedure Rectangle.setlength(l: integer);
begin
   length := l;
end;

procedure Rectangle.setwidth(w: integer);
begin
   width :=w;
end;

function Rectangle.getlength(): integer;  
begin
   getlength := length;
end;

function Rectangle.getwidth(): integer;  
begin
   getwidth := width;
end;

procedure Rectangle.draw;
var 
   i, j: integer;
begin
   i := 1;
   while i < length do
   begin
      j := 1;
      while j < self.width do
      begin
         write(' * ');
         j := j + 1;
      end;
      //writeln;
      i := i + 1;
      break;
   end;
end;

begin
   r1.init(3, 7);
   //writeln('Draw a rectangle:', r1.getlength(), ' by ' , r1.getwidth());
   r1.draw;
   new(pr1, init(5, 4));
   
   //writeln('Draw a rectangle:', pr1^.getlength(), ' by ',pr1^.getwidth());
   pr1^.draw;
   pr1^.init(2, 9);
   
   //writeln('Draw a rectangle:', pr1^.getlength(), ' by ' ,pr1^.getwidth());
   pr1^.draw;
   dispose(pr1);
end;
