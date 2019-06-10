program if_statement;
var x, y: integer;
begin
	x := 2;
    y := 15;

	if ( x > y ) then
		x := 3
	else y := 3;

	x := 1000;

	if ( (x < y) and (x > y - 3) or (x - y >= 5)) then
		if (true) then
			x := x - 1
		else
			x := x;
end.