
###快速启动-android稳定性测试

----
- 前置条件：需安装`adb`环境、需安装`adb`环境、需安装`adb`环境，重要事情说三遍
-----
- 简介： 
结合字节跳动提供的开源工具`Fastbot_android`, 进行封装了基础版的稳定性测试，
只需要数据线连接电脑，并确定在`cmd`中输入`adb devices`，看到了手机设备号，即可运行命令。
------
- 命令参数
```commandline
必选参数:
  packages              包名-必传参数

可选参数:
  -h, --help            显示命令帮助信息
  -m MINUTE, --minute MINUTE
                        设置分钟-可选参数 固定值 [10, 15, 20, 25, 30]
```
-----
- 基础教程
1. 新建一个工程目录`test_project`
2. 在工程目录中新建一个`test.py`(自定义)文件
3. 在文件中导入`fastrun`，并调用函数`fastrun.running()`
```python
# test_project/test.py

import fastrun

fastrun.running()
```
4. 编辑器中进入`Terminal`命令行，输入如下命令即可运行
```commandline
默认运行5分钟

PS E:\test_project> python test.py "包名(问开发要)" 
```
```commandline
指定运行10分钟

PS E:\test_project> python test.py "包名(问开发要)" -m 10 
```
```commandline
指定运行15分钟

PS E:\test_project> python test.py "包名(问开发要)" -m 15 
```
```commandline
指定运行20分钟

PS E:\test_project> python test.py "包名(问开发要)" -m 20
```
```commandline
指定运行25分钟

PS E:\test_project> python test.py "包名(问开发要)" -m 25
```
```commandline
指定运行30分钟

PS E:\test_project> python test.py "包名(问开发要)" -m 30
```
-----
-----
###严正声明

- 作者只提供工具使用，当用户使用其他用途时，对用户或者他人造成任何形式的损失和伤害，该工具不承担任何责任。

- 本协议的一切解释权与修改权归本工具所有。