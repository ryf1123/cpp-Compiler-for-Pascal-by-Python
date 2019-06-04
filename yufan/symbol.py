import sys


class Symbol:
    def __init__(self, name, type, var_function="var", memory_size=4):
        self.name = name
        self.type = type
        self.var_function = var_function
        self.memory_size = memory_size

    def __str__(self):
        return 'Symbol(name=%s, type=%s, var_function=%s, memory_size=%s)' % (
            str(self.name),
            str(self.type),
            str(self.var_function),
            str(self.memory_size)
        )


class Table:
    def __init__(self):
        '''符号表用一个 list 表示，其中每一个为一层 scope。初始只有一层 main。'''
        self.tables = [{
            'scope': 'main',
            'parent_scope': None,
            'type': 'function',
            'return_type': 'void',
            'functions': {},
            'vars': {},
        }]

    def __str__(self):
        return 'Table()'

    def get_current_scope_name(self):
        '''获得当前作用域名'''
        return self.tables[-1]['scope']

    def get_identifier(self, identifier, index=None):
        '''按照作用域依次查找一个名字'''
        if index is None:
            index = len(self.tables) - 1
        if index == -1:
            return None
        if identifier in self.tables[index]['vars']:
            return self.tables[index]['vars'][identifier]
        else:
            return self.get_identifier(identifier, index - 1)

    def set_identifier(self, name, type, var_function):
        '''定义一个新名字'''
        scope = self.tables[-1]
        var_function = var_function + 's'

        if name in scope[var_function]:
            sys.exit('Name `%s` is already defined. ')

        else:
            symbol = Symbol(name, type, var_function)
            scope[var_function] = symbol
            return symbol

    def add_scope(self, name, type, return_type):
        '''增加一层作用域'''
        scope = self.tables[-1]
        self.tables.append({
            'scope': '%s.%s' % (scope['scope'], name),
            'parent_scope': scope['scope'],
            'type': type,
            'return_type': return_type,
            'functions': {},
            'vars': {},
        })

    def del_scope(self):
        '''删除一层作用域'''
        return self.tables.pop()
