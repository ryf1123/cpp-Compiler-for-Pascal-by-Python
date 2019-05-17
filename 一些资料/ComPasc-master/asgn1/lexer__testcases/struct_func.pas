Program struct_func;

TYPE
   T = OBJECT
      b,d : integer;
      a,c,f : char;
      e : real;
      namez : string;
   END;

PROCEDURE f (x : T);
	BEGIN
		x.a := 'a';
		x.b := 47114711;
		x.c := 'c';
	  	x.d := 1234;
		x.e := 3.141592897932;
		x.f := '*';
		x.namez := 'abc';
	END;

VAR
  k : T;

BEGIN
	f(k);
END.
