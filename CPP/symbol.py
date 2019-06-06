import sys
import json


def list_format(list, indent=4):
    return '[%s%s%s]' % (
        '\n' + ' '*indent if len(list) else '',
        (',' + '\n' + ' '*indent).join(
            str(item).replace('\n', '\n' + ' ' * indent)
            for item in list),
        '\n' if len(list) else ''
    )


class Symbol:
    '''符号类'''

    def __init__(self, name, type, var_function="var", memory_size=4, params=[]):
        self.name = name
        self.type = type
        self.var_function = var_function
        self.memory_size = memory_size
        # +++++
        self.params = params

    def __str__(self):
        return 'Symbol(`%s`, %s, %s, memory_size=%s)' % (
            str(self.name),
            str(self.type),
            str(self.var_function),
            str(self.memory_size))


class Scope:
    '''作用域类'''

    def __init__(self, name=None, parent_scope=None, type=None, return_type=None, width=0):
        self.name = name
        self.parent_scope = parent_scope
        self.type = type
        self.return_type = return_type
        # +++++
        self.width = width

        self.function = {}
        self.var = {}

    def __str__(self):
        return 'Scope(`%s`, function=%s, var=%s)' % (
            str(self.name),
            list_format(list(self.function.values())),
            list_format(list(self.var.values()))
        )


class Table:
    '''符号表类'''

    def __init__(self):
        '''符号表用一个 list 表示，其中每一个为一层 scope。初始只有一层 main。'''
        self.table = [Scope('main', type='function')]
        # +++++
        self.tmp_vals = {}

    def __str__(self):
        return 'Table(%s)' % list_format(self.table)

    def get_current_scope_name(self):
        '''获得当前作用域名'''
        return self.table[-1].name

    def get_identifier(self, name, index=None):
        '''按照作用域依次查找一个名字'''

        if index is None:
            index = len(self.table) - 1
        if index == -1:
            return None

        scope = self.table[index]
        if name in scope.var:
            return scope.var[name]
        else:
            return self.get_identifier(name, index - 1)

    def set_identifier(self, name, type, var_function):
        '''定义一个新名字'''
        scope = self.table[-1]

        if name in scope.__getattribute__(var_function):
            sys.exit('Name `%s` is already defined. ' % name)

        else:
            symbol = Symbol(name, type, var_function)
            scope.__getattribute__(var_function)[name] = symbol
            return symbol

    def add_scope(self, name, type, return_type):
        '''增加一层作用域'''
        scope = self.table[-1]
        self.table.append(Scope(
            name='%s.%s' % (scope.name, name),
            parent_scope=scope.name,
            type=type,
            return_type=return_type))

    def del_scope(self):
        '''删除一层作用域'''
        return self.table.pop()


if __name__ == '__main__':
    t = Table()
    t.set_identifier('i', 'int', 'var')
    t.set_identifier('j', 'int', 'var')
    t.add_scope('f', 'function', None)
    t.set_identifier('j', 'int', 'var')
    print(t)
    print(t.get_identifier('i'))
