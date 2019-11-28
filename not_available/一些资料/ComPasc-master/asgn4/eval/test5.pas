PROGRAM Greeting;


VAR 
c    : INTEGER; 
d    : INTEGER; 
e    : INTEGER; 

BEGIN
    IF c=1 THEN
        BEGIN
            IF d=1 THEN
                BEGIN
                    d := d + 1;
                END;
            ELSE
                BEGIN
                    IF d AND e = 1 THEN
                        BEGIN
                            e := e + 1;
                        END;
                    ELSE
                        BEGIN
                            d := d - 1;
                        END;
                END;
        END;
    ELSE
        BEGIN
            IF d AND e = 1 THEN
                BEGIN
                    e := e + 1;
                END;
            ELSE
                BEGIN
                    d := d - 1;
                END;
        END;
END;
