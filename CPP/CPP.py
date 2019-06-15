from CPP_yacc import *
import tree_visual

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

        tree_visual.drawTree(result)
        print("[info] draw tree done")

        scopes['main'] = table.scope()

        tac.addLinenum()
        tac.display()
        allocReg = AllocateRegister.AllocteRegister(scopes, tac)
        print("[info] register allocation done")
        codegen = CodeGen.CodeGen(scopes, tac, allocReg)

        print("[info] code generation done")
        print("---------         This is the end of this program       ---------")
    else:
        print("[error] error in paramater's number")
