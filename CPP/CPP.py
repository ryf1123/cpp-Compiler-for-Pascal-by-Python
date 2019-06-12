from CPP_yacc import *

if __name__ == '__main__':
    print("--------- Wellcome to CPP: Compiler for Pascal in Python ---------")
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
        print("[info] source code loaded")
        result = parser.parse(data, debug=0)
        print("[info] parser done")
        tac.addLinenum()
        tac.display()
        allocReg = AllocateRegister.AllocteRegister(table, tac)
        print("[info] register allocation done")
        codegen = CodeGen.CodeGen(table, tac, allocReg)
        print("[info] code generation done")
        print("--------- This is the end of this program ---------")

    else:
        while True:
            try:
                data = input('Type here > ')
            except EOFError:
                break
            if data == "q" or data == "quit":
                break
            if not data:
                continue

            result = parser.parse(data, debug=1)
            print(result)