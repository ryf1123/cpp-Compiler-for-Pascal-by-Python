program test3; 
var 
	A : integer; 

	procedure ScopeInner; 
	var A : integer; 
		begin
		A := 10; 
		writeln(A) ;
	end; 

	function Summation(num : integer) : integer;
	begin
		if num = 1 then 
			Summation := 1 
		else 
			Summation := 2;
			ScopeInner;
	end; 

begin 
	read(A);
	A := 20000; 
	writeln(A + 1 * 2); 
	ScopeInner;
	A := A + Summation(10);
	writeln(A); 
end.