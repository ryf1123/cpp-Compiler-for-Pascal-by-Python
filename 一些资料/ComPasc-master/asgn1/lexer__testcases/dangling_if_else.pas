PROGRAM dangling_if_else;

VAR 
	i : integer;
	a : array [0..2] of integer = (1,2,3);

BEGIN
	i := 0;
	IF (i <= 3) THEN
		a[i] := a[i] + 1;
	IF (i >= 2) THEN
		a[i] := a[i] - 1
	ELSE
		a[i] := 4;
END.
