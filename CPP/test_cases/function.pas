program test3; 
var 
	A,B : integer; 

	function g(var x: integer): integer;
	begin
		x := 4;
	end;

	function f(var x : integer): integer;
	begin
		f := g(x);
	end; 

begin 
	A := 5;
	B := f(A);
	writeln(A);
end.