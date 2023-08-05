# KenkoAdvance

一些方便自己的自定义小功能

作者：AkagiYui

Work In Progress:
- [ ] AyBase64
- [ ] AyAdb

## `类` GocqConnection

描述：go-cqhttp连接类

需要的包：websocket-client requests

`from KenkoAdvance.GocqConnection import GocqConnection`

## `类` TextToMidi

描述：文本转Midi

作者：Scarlett凛子 `QQ: 1587524`

需要的包：mido

`from KenkoAdvance.TextToMidi import TextToMidi`


## `类` HiddenPrints

描述：暂时全局关闭标准输出

收录自：https://zhuanlan.zhihu.com/p/360137954


## `类` AyStr

描述：自定义字符串类

> 自定义字符串类 
> 
> 重写in支持判断列表或元组成员是否出现在字符串里 
> 
> 重写find()支持查找子串列表或元组


## `类` AyDict

描述：自定义字典类

> 键用半角实心点.做下级入口
> 
> 例 dict['web']['port'] == AyDict['web.port']


## `函数` get_file_format

描述：用文件头判断文件格式

收录自：https://blog.csdn.net/privateobject/article/details/78069500


## `函数` int_to_chinese

描述：数字转汉字

收录自：https://blog.csdn.net/PlusChang/article/details/72991191


## `函数` get_self_uptime

描述：获取自身运行时长

需要的包：psutil

## `函数` get_machine_uptime

描述：获取开机时长

需要的包：psutil

## `函数` get_self_ip

描述：获取自身IP

收录自：https://www.zhihu.com/question/49036683/answer/1243217025

## `函数` chinese_to_int

描述：汉字转数字

收录自：https://www.iplaypy.com/code/base/b2600.html

## `函数` chinese_to_int_e

描述：汉字转数字

收录自：https://www.jb51.net/article/114789.htm