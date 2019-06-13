# Report 编译原理项目报告

# CPP: Compile for Pascal by Python 

| 邱兆林 | 刘洪甫 | 任宇凡     |
| ------ | ------ | ---------- |
|        |        | 3160104704 |

## 总体架构

![image-20190613194718564](assets/image-20190613194718564.png)

如上图所示，在CPP(Compiler for Pascal in Python)中，我们实现了从pascal代码到最终可执行的MIPS代码之间的编译过程。最终获得的MIPS代码可以在Mips模拟器上直接运行并且获得Pascal代码想要的结果。

在处理的过程中首先是通过词法和语法分析，从pascal代码构建抽象语法树，在这个过程中也完成了符号表的构建和中间代码的生成。在中间代码的生成过程中进行了类型检查。当完成了中间代码的生成和符号表的构建之后开始目标代码的生成。

和一般使用的通过LLVM的方式实现中间代码的生成到目标代码的生成的方法不同，在我们的工程中我们自己实现了中间代码的生成到目标代码的生成工作。这也就意味着我们需要自己维护运行时环境，这包括了跳转到函数过程中访问链和控制链的维护，也包括了栈内存的分配，返回地址的保护，也包括从函数返回过程中，恢复现场(恢复寄存器)，和保存返回值的工作。

最终我们将生成的MIPS代码放在MIPS模拟器上直接运行，然后得到了正确的结果。

在本报告的倒数第二个章节，我们对老师提供的测试样例，以及我们自己编写的一些测试样例进行了测试，均得到了正确的结果。我们还会对这样的结果进行分析。在最后一个章节我们会对我们的编译器提出可能的优化与展望。

## 词法分析

词法分析部分部分的主要功能是将输入分析的pascal文本处理成一个一个的token。这是编译器处理的第一个环节，通过词法分析后续过程就不需要再面对原始文本，而是一个一个有名字，有类型的token，这位后续的分析提供了很大的便利性。

举个例子，对于普通的变量名NAME，我们可以如下地通过ply.lex库对其通过正则表达式进行定义，这个正则表达式描述了一个以字母开头，后面有字母也可能有数字的一个token，这也就是NAME。

![image-20190613201105342](assets/image-20190613201105342.png)

下面这个例子是实数的，实数的重要组成是中间的小数点，前面的d表示的是数字。

![image-20190613201231473](assets/image-20190613201231473.png)

### 优先级问题

关于优先级问题ply.lex的处理方法和LEX的方法是类似的，都是通过定义的顺序来决定优先级，并且在实际匹配中采用最长匹配原则。

### ply.lex

ply.lex是一个完全通过Python实现的词法分析库，可以通过Python语言，像C语言使用LEX一样使用词法分析功能。

![image-20190613200823613](assets/image-20190613200823613.png)

### lex测试

```pascal
program test3; 
var 
    A : integer; 

    procedure ScopeInner; 
    var A : integer; 
        begin
        A := 10; 
……
```

上面是一段pascal代码，这是不完整的，但是可以用于说明。

```
LexToken(PROGRAM,'program',1,0)
LexToken(NAME,'test3',1,8)
LexToken(SEMI,';',1,13)
LexToken(VAR,'var',2,16)
LexToken(NAME,'A',3,22)
LexToken(COLON,':',3,24)
LexToken(SYS_TYPE,'integer',3,26)
LexToken(SEMI,';',3,33)
LexToken(PROCEDURE,'procedure',5,38)
LexToken(NAME,'ScopeInner',5,48)
LexToken(SEMI,';',5,58)
LexToken(VAR,'var',6,62)
LexToken(NAME,'A',6,66)
LexToken(COLON,’:’,6,68)
```

上面这些Token就是从上面的pascal代码生成的。

## 语法分析

语法分析过程主要有自顶向下和自底向上两种类型。自顶向下方法以LL(1)分析为代表；自底向上分析方法以LR(1)，SLR(1), LALR(1)分析为代表。其中，既有足够强大的表达能力，又足够简单的是LALR(1)分析。在LALR(1)分析中向前展望一个符号。而由于有了YACC语法分析工具这样的部件可以使用，编程者不再需要自己去处理语法分析，而是传入文法的产生式，然后自动生成语法分析的结果：抽象语法树。

这部分的代码在`CPP_yacc.py`中，

如下例中，我们希望写出从routine头，主标签，以及routine内容到routine的规约。于是我们的书写过程如下所示。这个里面值得关注的一点是和一般的Python代码逻辑不通，这里中间的注释内容才是需要的。(Python中三个连续的引号是注释)

![image-20190613202930965](assets/image-20190613202930965.png)

在下面一个例子中我们希望写出程序头的产生式。而这一个产生式也是在下面介绍ply.yacc的过程中使用到的例子。

![image-20190613203522531](assets/image-20190613203522531.png)

### ply.yacc

ply.yacc方法是对于Python支持的语法分析库，通过ply.yacc我们可以通过Python语言像C语言使用YACC工具一样简单地使用语法分析功能。

而ply.yacc比较出色的一点在于其更加强大的debug能力。

首先ply.yacc可以生成文法的所有的产生式，如下图所示(这一步基本上是对于我们提供的产生式的优化)

![image-20190613201934069](assets/image-20190613201934069.png)

第二是通过开启debug模式我们可以在处理的过程中看到语法分析的全过程。这包括在处理的过程中栈是怎么变化的，采用了什么样的规约，或者移进操作。

![image-20190613202309303](assets/image-20190613202309303.png)

在上图中我们可以看到语法分析在处理一个pascal程序最开始的时候。首先遇到了PROGRAM这个保留字（注意其中的点号，这个点号和我们在编译原理课程中学到的分割输入和栈的点号意义完全相同），然后采取了移进操作。然后获取到了一个名为`repeatLoop`的名字，这个名字显然就是函数名了。然后接着又得到了一个分号，得到分号之后通过规约操作`[program_head -> PROGRAM NAME SEMI] with ['program','repeatLoop',';']`将刚刚收到的所有内容规约成一个`program_head`。这样就完成了函数头部的处理，往往一个稍微长的pascal代码的处理过程，操作数目非常巨大，但是不可否认这样的直观的栈和输入流，可以给代码的编写带来便利。

### yacc测试

```
A := 20000; 
```

上面是一条pascal的语句，其中完成了对A变量的赋值操作。而下面是当栈顶是赋值符号，然后输入一个20000的语法分析过程。可以看出这个20000在词法分析的过程中已经被处理成了一个整数Integer。然后程序采用的是移进，将integer读入到栈顶，然后展望到分号。

当看到分号之后程序采用了将integer规约成const_value的规约操作，然后将这个const_value进一步变成factor。这和我们的预想是完全一样的。

```
State  : 61
Stack  : program_head routine_head BEGIN stmt_list NAME ASSIGN . LexToken(INTEGER,20000,23,287)
Action : Shift and goto state 77

State  : 77
Stack  : program_head routine_head BEGIN stmt_list NAME ASSIGN INTEGER . LexToken(SEMI,';',23,292)
Action : Reduce rule [const_value -> INTEGER] with [20000] and goto state 76
Result : <Node @ 0x10a5a8a20> (<tree_visual.Node object at 0x10a5a8a20>)

State  : 76
Stack  : program_head routine_head BEGIN stmt_list NAME ASSIGN const_value . LexToken(SEMI,';',23,292)
Action : Reduce rule [factor -> const_value] with [<Node @ 0x10a5a8a20>] and goto state 71
Result : <Node @ 0x10a5d3b38> (<tree_visual.Node object at 0x10a5d3b38>)

State  : 71
Stack  : program_head routine_head BEGIN stmt_list NAME ASSIGN factor . LexToken(SEMI,';',23,292)
Action : Reduce rule [term -> factor] with [<Node @ 0x10a5d3b38>] and goto state 69
Result : <Node @ 0x10a5d3b00> (<tree_visual.Node object at 0x10a5d3b00>)
```

## 抽象语法树的生成

抽象语法树的生成过程应该是在语法分析的过程中完成的。



## 语义分析(这个如果没有的话就写一下类型检查吧)



## 符号表

![image-20190613195223079](assets/image-20190613195223079.png)



## 中间代码生成



## 代码生成

![image-20190613195205142](assets/image-20190613195205142.png)

## 测试样例





## 优化与展望





## 附1： 分工



## 附2：测试样例与工程代码