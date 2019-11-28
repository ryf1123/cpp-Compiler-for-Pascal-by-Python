PROGRAM switch;

VAR
	wflg, tflg, dflg, na, Code : integer;
	c : char;
	argv : string;

BEGIN
	wflg := 0;
	tflg := 0;
	dflg := 0;
	Val(ParamStr(1), na, Code);
	argv := ParamStr(2);
	CASE c of
		'w', 'W' : wflg := 1;
		't', 'T' : tflg := 1;
		'd' : dflg := 1;
	END;
END.