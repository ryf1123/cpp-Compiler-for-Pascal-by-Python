

class ThreeAC(object):
    '''
        contains three address code and link to symble table
    '''
    def __init__(self, symtable):
        self.code = []
        self.symtable = symtable
        self.tmpoffset = {}
    
    def map(self):
        for scope in self.symtable.table:
            offset = 0
            scope_name = scope.name
            width = 0
            self.tmpoffset[scope_name] = {}
            mapoff = self.tmpoffset[scope_name]

            for var in scope.symbols.keys():
                var_entry = self.symtable.get_identifier(var)
                if scope != 'main':
                    if var_entry.params != None:
                        mapoff[var] = offset
                        offset -= var_entry.size
            
            for tmp in scope.temp.keys():
                temp_var = scope.temp[tmp]
                mapoff[tmp] = tmp_var.size


    def emit(self, op, lhs, op1, op2):
        self.code.append([op,lhs,op1,op2])


    def addLinenum(self):
        for i, code in enumerate(self.code):
            self.code[i] = [str(i+1)] + code


    def display(self):
        for i, code in enumerate(self.code):
            linenum, op, lhs, op1, op2 = code
            # ++++++
            print("#"+linenum+","+op+","+lhs+","+op1+","+op2)
