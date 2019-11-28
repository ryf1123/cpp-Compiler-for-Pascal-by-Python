PROGRAM Greeting;


VAR 
c    : INTEGER; 
d    : INTEGER; 

BEGIN
    c := 1;
    d := 1;
    IF c=1 THEN
        BEGIN
            IF d=1 THEN
                BEGIN
                    d := d + 1;
                END;
            ELSE
                BEGIN
                    d := d - 1;
                END;
        END;
END;
