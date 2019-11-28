PROGRAM progf;

VAR 
	i : integer;

BEGIN
	i := 6;
	WHILE ((i <= 8) AND (i >= 6) AND (i <> 7)) DO
	BEGIN
		IF (i >= 0) THEN
			writeln('yes')
		ELSE
			writeln('no');
		i := i + 1;
	END;
END.
