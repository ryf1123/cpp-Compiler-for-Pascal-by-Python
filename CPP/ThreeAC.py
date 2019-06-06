

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
                    if len(var_entry.params) != 0:
                        mapoff[var] = offset
                        offset -= var_entry.size
                                          
            # TODO 临时变量的偏移量计算
            # for local in self.symtable.localVals[scope_name]:
            #     objectVar = local.split('_')

            #     if len(objectVar) == 2:
            #         objName = objectVar[0]
            #         varName = objectVar[1]
            #         objEntry = self.symtable.Lookup(scope_name+"_"+objName, 'Ident')
            #         objoffset = objEntry.offset
            #         for param in objEntry.params:
            #             if param[0] == varName:
            #                 offset = objoffset+param[3]
            #                 mapdic[local] = offset
            #                 break
            #         offset = objoffset
            #         continue

            #     offset -= 4
            #     mapdic[local] = offset
            #     width += 4
 


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
