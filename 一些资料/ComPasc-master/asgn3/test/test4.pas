PROGRAM Sort (input, output);

CONST
	MaxElts = 50;
TYPE 
	IntArrType = ARRAY [1..MaxElts] OF Integer;

VAR
	i, j, tmp, size: integer;
	arr: IntArrType;

PROCEDURE ReadArr(size: Integer; a: IntArrType);
BEGIN
    size := 1;
    WHILE NOT eof DO 
    BEGIN
		readln(a[size]);
	END;
	IF NOT eof THEN
	BEGIN
	    size := size + 1;
    END;
END;

BEGIN
	ReadArr(size, arr);
	i := size - 1;
	WHILE i > 1 DO
	BEGIN
		j := 1;
		WHILE j < i DO 
	    BEGIN
			IF arr[j] > arr[j + 1] THEN
			BEGIN
		    	tmp := arr[j];
		    	arr[j] := arr[j + 1];
		    	arr[j + 1] := tmp;
			END;
			j := j + 1;
		END;
		i := i - 1;
	END;

	i := 1;
	WHILE i < size DO
	BEGIN
	    writeln(arr[i]);
	    i := i + 1;
    END;
END;
	    
