program exObjects;
type 
   Rectangle = object  
   private  
      length, width: integer; 
   public  
      constructor init(l, w: integer);
      destructor done;
      
      procedure setlength(l: integer);
      function getlength(): integer;  
      
      procedure setwidth(w: integer);  
      function getwidth(): integer;  
      
      procedure draw;
      { so you should die }
end;

var
   r1: Rectangle;
   pr1: ^Rectangle;

constructor Rectangle.init(l, w: integer);
begin
   length := l;
   width := w;
end;

destructor Rectangle.done;
begin
   writeln(' *** Desctructor Called');
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
   for i:= 1 to length do
   begin
      for j:= 1 to width do
         write(' * ');
      writeln;
   end;
end;

begin
   r1.init(3, 7);
   writeln('Draw a rectangle:', r1.getlength(), ' by ' , r1.getwidth());
   r1.draw;
   new(pr1, init(5, 4));
   
   writeln('Draw a rectangle:', pr1^.getlength(), ' by ',pr1^.getwidth());
   pr1^.draw;
   pr1^.init(2., 9);
   
   writeln('Draw a rectangle:', pr1^.getlength(), ' by ' ,pr1^.getwidth());
   pr1^.draw;
   dispose(pr1);
   r1.done;
end.