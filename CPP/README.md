# CPP 

运行方式

```shell
pip2.7 install ply
python2.7 myyacc2.py test_div_mod.pas
```

文件内容

```shell
➜  # 请忽略里面的.pyc文件
.
├── README.md
├── mylex.py					词法分析主要函数
├── mylex.pyc #
├── myyacc2.py				语法分析的主要函数
├── parser.out				这个文件很有用，自动生成，里面有所有产生式
├── parsetab.py				没用
├── parsetab.pyc #
├── reserved.py				保留符号写在里面
├── reserved.pyc #
├── test_case.pas 		还没有经过测试的代码
├── test_div_mod.pas 	已经通过测试的代码
├── testcase1.pas			还没有经过测试的代码
├── tree_visual.py 		将分析树可视化的代码
└── tree_visual.pyc # 
```

