PROGRAM loop;

VAR
	i,j,k,res : integer;

BEGIN
	res := 0;
	i := 0;
	WHILE (i < 10) DO
	BEGIN
		j := 0;
		WHILE (j < 10) DO
		BEGIN
			k := 0;
			WHILE (k < 10) DO
			BEGIN
				res := res + 1;
				k := k + 1;
			END;
			j := j + 1;
		END;
		i := i + 1;
	END;
	write ('res = ');
	writeln (res);
END.