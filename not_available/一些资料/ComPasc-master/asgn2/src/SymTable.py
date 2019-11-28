import pprint


class SymTable (object):
    '''
    SymbolTable built after parsing
    Some changes made keeping in mind the link : https://www.tutorialspoint.com/compiler_design/compiler_design_symbol_table.htm 
    '''

    def __init__(self): # local variables can be inside functions and functions only

        # default values
        self.table = {'Scope' : 'Main',
                        'ParentScope' : 'Main',
                        'Type' : 'function', # This can be function or loop
                        'ReturnType' : 'undefined',
                        'Func' : {},
                        'Ident' : {}
                        }
        self.scopelist = [self.table] 
        # add itself, at least! Index 0 has highest, 1 is inside 0, 2 is inside 1 ...
        # Current scope is always at index [-1]

    def PrintSymTable(self):
        pprint.pprint(self.scopelist)

    def GetCurrentScopeName(self):
        '''
            WARNING: Currently, the Symbol Table has no key with name 'ScopeName'
        '''
        return self.scopelist[-1]['ScopeName'] # even if it contains only one scope, this command helps

    def Check_identifier(self, identifier, index):
        if index == -1 :
            return None # exhausted everything
        t_scope = self.scopelist[index]
        # if t_scope['Ident'].has_key(identifier):
        if identifier in t_scope['Ident']:
            return t_scope['Ident'][identifier]
        else:
            return self.Check_identifier(identifier, index-1) # go one level up

    def AddScope (self, scopeName, Type):
        curr_scope = self.scopelist[-1]
        temp_scope = {
            'Scope' : curr_scope['ScopeName']+ '.'+ scopeName, # main.scope
            'ParentScope' : curr_scope['ScopeName'],
            'Type' : Type, # Type of scope
            'ReturnType' : 'undefined', # default value
            'Func' : {},
            'Ident' : {},
        }
        self.scopelist.append(temp_scope)

    def Define(self, v, typ, varfunc):
        '''
            args:
                symbol: an object of class SymTable entry
        '''
        curr_scope = self.scopelist[-1]
        e = None
        if (varfunc == "var"):
            if (v not in curr_scope['Ident']):
                e = SymTableEntry (v, typ, "var")
                curr_scope['Ident'][v] = e
        else:
            if (v not in curr_scope['Func']):
                e = SymTableEntry (v, typ, "func")
                curr_scope['Func'][v] = e
        # else:
            # print ('Symbol already exists!')
        return e


    def Lookup(self, identifier):
        '''
            Call auxiliary function recursively, i.e. go up the hierarchy
        '''
        return self.Check_identifier(identifier, len(self.scopelist) - 1);

    def Del_scope(self, scopeName):
        del self.scopelist[-1]

class SymTableEntry(object):
    '''
    Create a symbol table entry
    '''
    def __init__(self,name,typ,varfunc = "var", memsize = 4):
        self.name = name
        self.varfunc = varfunc # either var, function, class or object
        self.typ = typ # for var: int, char, double | for function: typ is return type
        self.memsize = memsize # number of elements in the array
