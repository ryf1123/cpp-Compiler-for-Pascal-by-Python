PROGRAM incorrect_copy;

VAR 
	i : integer;
	0x123 : integer;
	1e2, 1e2e3, 1.2.3 : real;

BEGIN
	i := 6;
	WHILE ((i <= 8) AND (i < 6.67) AND (i <> 7)) DO
	BEGIN
		IF (i >= 0) THEN;
			writeln('yes')
		ELSE
			writeln('no');
		i := i + 1;
	END;
END.
