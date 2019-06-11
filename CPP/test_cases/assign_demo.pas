program Arithmetic;
const a = 2; flag=true;
type
    int1=integer;
    people=record
        score: integer;
        sex: char;
    end;
    people_arr=array [1..3] of people;
var x: boolean; q:boolean; newton: people; peoples: people_arr;
begin
    q := true and true and true and not flag;
    x := (a + 13) DIV 5 mod 1;
    peoples[x] := 1;
    x := peoples[0];

    newton.score := 1;
    x :=newton.score;


end.