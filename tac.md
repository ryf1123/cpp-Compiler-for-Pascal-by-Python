| Operation 操作符 | lhs结果 | op1       | Op2     |
| ---------------- | ------- | --------- | ------- |
| +\-\*\/          | 结果    | 操作数1   | 操作数2 |
| PRINT            |         | 参数      |         |
| PARAM            |         | 参数      |         |
| CALL(返回赋值)   | 结果    | 调用label |         |
| CALL(返回不赋值) |         | 调用label |         |
| LOADREF          | 结果    | 符号      | index   |
| STOREREF         | 值      | 符号      | index   |
| SLT              | 结果     | 操作数1   | 操作数2 |
| BNE              | 比较1        | 比较2     | label        |
| BEQ              | 比较1        | 比较2     | label        |
| JMP              |         | Label     |         |
| LABEL            |         | Label     |         |
| SCAN             |         | 参数      |         |
| RETURN           |         | 参数      |         |
| NOT              | 结果    | 操作数    |         |
| MOD              |         |           |         |