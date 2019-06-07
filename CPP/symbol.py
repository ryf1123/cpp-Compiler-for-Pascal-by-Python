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

    def _get_size(self):
        '''计算一个符号的大小

        # TODO 自动计算大小，需要确定 object 的数据结构
        # TODO 函数的 size 是不是 0？
        '''

        size = {
            'integer': 4,
            'real': 8,
            'char': 1
        }

        if self.var_function in ('var', 'const'):
            return size[self.type]

        elif self.var_function == 'object':
            # TODO 明确 object 和 type 的定义
            return 0

        elif self.var_function == 'array':
            size = size[self.type]
            for (start, end) in self.params:
                size *= end - start + 1

            return size

        elif self.var_function == 'function':
            return 0

        else:  # type
            symbol = Table().get_identifier(self.type)
            if symbol.type != 'object':
                sys.exit('`%s` is not a type. ' % self.type)

            size = 0
            for (name, type) in symbol.params:
                size += Symbol(name, type)._get_size()

            return size

    def __init__(self, name, type, var_function="var", offset=0, params=None, scope=None):
        '''初始化一个符号

        name:           符号名

        type:           one of 'integer', 'real', 'char'
                        如果是函数，那么该字段表示它的返回值类型

        var_function:   one of 'var', 'const', 'array', 'object', 'function'
                        # array 只支持基础类型
                        # function 返回值只支持基础类型
                        # object 需要支持嵌套

        offset:         该符号位于对应的作用域中的偏移量

        params:         函数参数列表 # TODO
                        如果是 array，那么 params 依照 [(0, 10), (0, 100)] 的结构依次记录起始索引和结束索引
                        如果是 object 那么 params 依照 [(name, type), ...] 的结构依次记录。其中 type 可能是复杂类型
        '''

        self.name = name
        self.type = type
        self.var_function = var_function
        self.offset = offset
        self.params = params
        self.scope = scope
        self.size = self._get_size()

    def __str__(self):
        return 'Symbol(`%s`, %s, %s)' % (
            str(self.name),
            str(self.type),
            str(self.var_function))


class Scope:
    '''作用域类'''

    def __init__(self, name=None, parent_scope=None, type=None, return_type=None, width=0):
        self.name = name
        self.parent_scope = parent_scope
        self.type = type
        self.return_type = return_type
        self.width = width

        self.symbols = {}

    def __str__(self):
        return 'Scope(`%s`, symbols=%s)' % (
            str(self.name),
            list_format(list(self.symbols.values())),
        )

    def define(self, name, type, var_function='var', params=None):
        if name in self.symbols:
            sys.exit('Name `%s` is already defined. ' % name)

        symbol = Symbol(name, type, var_function,
                        offset=self.width, params=params)
        self.symbols[name] = symbol
        self.width += symbol.size

        return symbol


class Table:
    '''符号表类'''

    def __new__(cls, *args, **kwargs):
        '''单例模式，使得任何地方的符号表都是同一个'''
        if not hasattr(Table, "_instance"):
            Table._instance = object.__new__(cls)
        return Table._instance

    def __init__(self):
        '''符号表用一个栈表示，其中每一个为一层 scope。

        初始只有一层 main。
        临时变量全部放在 temp 中。
        '''
        self.table = [Scope('main', type='function')]
        self.temp = Scope('temp', type='function')

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
        if name in scope.symbols:
            return scope.symbols[name]
        else:
            return self.get_identifier(name, index - 1)

    def set_identifier(self, name, type, var_function, params=None):
        '''定义一个新名字'''
        return self.table[-1].define(name, type, var_function, params)

    define = set_identifier

    def new_temp(self, type):
        name = '_t%06d' % len(self.temp.symbols)
        symbol = self.temp.define(name, type)
        return symbol

    define_temp = new_temp

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
    t.set_identifier('i', 'integer', 'var')
    t.set_identifier('j', 'integer', 'var')
    t.add_scope('f', 'function', None)
    t.set_identifier('j', 'integer', 'var')
    print(t)
    print(t.get_identifier('i'))

    print()

    symbol = t.new_temp('integer')
    print(symbol)
    symbol = t.new_temp('integer')
    print(symbol)
