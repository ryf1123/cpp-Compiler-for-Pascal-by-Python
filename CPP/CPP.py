from CPP_yacc import *

if __name__ == '__main__':
    print("\n\n\n\n\n")
    print("--------- Wellcome to CPP: Compiler for Pascal in Python ---------")
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
        
        print("[info] source code loaded")
        print("\n\n\n")
        result = parser.parse(data, debug=0)
        
        print("[info] parser done")
        print("\n\n\n")

        tac.addLinenum()
        tac.display()
        allocReg = AllocateRegister.AllocteRegister(table, tac)
        
        print("[info] register allocation done")
        print("\n\n\n")
            
        codegen = CodeGen.CodeGen(table, tac, allocReg)
        print("\n\n\n")
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