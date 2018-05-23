# 使用预编译头文件

预编译头文件（PCH）是许多编译器所支持的功能，用于编译稳定的代码体，将代码的编译状态保存在二进制文件当中。在之后的编译中，编译器将加载存储的状态，并在这基础上继续编译指定的文件。之后的每次编译都会很快，因为已经编译的代码不需要再次被编译。

qmake在某些平台下的构建构建环境，支持预编译，如下所示：

```.pro
windows:
       >nmake
       >Vistual Studio projects(VS 2008 版本以上)
>macOS,iOS,tvOS,和watchOS
    >Makefile
    >Xcode
>Unix
    >GCC3.4 或更高版本
```

## 在你的项目中添加预编译头文件

预编译头文件所包含的代母必须是项目中稳定且静态的代码。一个典型的预编译头文件应该像下面这样：

```.pro
// Add C includes here

#if defined __cplusplus
// Add C++ includes here
#include <stdlib>
#include <iostream>
#include <vector>
#include <QApplication> // Qt includes
#include <QPushButton>
#include <QLabel>
#include "thirdparty/include/libmain.h"
#include "my_stable_class.h"
...
#endif
```

注意：预编译头文件需要将C语言的包含从C++中分离出来，因为C的预编译头文件也许不包含C++的代码。

要在你的项目中使用预编译头文件，你至于要在你的项目文件中定义PRECOMPILED_HEADER变量。如下所示：

```.pro
PRECOMPILED_HEADER += stable.h
```

qmake将会处理剩下的，以确保预编译头文件被生工的创建和使用。如果你配置支持了预编译头文件，你将不再需要将头文件添加到HEADERS变量中，因为qmake将会自己完成这些。

对于Windows的MSVC和g++规范默认启用precomplie_header.

使用这个选项，你将在使用预编译头文件时触发项目中的条件以便添加一些设置。例如：

```.pro
precompile_header:!isEmpty(PRECOMPILED_HEADER) {
DEFINES += USING_PCH
}
```

为了在MSVC nmake下对C语言文件使用预编译头文件，你需要将precomplie_header选项添加到CONFIG变量中。如果C++也使用该头文件，并且该头文件包含C++的关键词，那么请将相关头文件包含在#ifdef 和__cplusplus之间.

## 对于可能遇到的问题的说明

在某些平台上预编译头文件的后缀可能和其他目标文件相同。例如下面的定义，也许会导致生成两个同名的目标文件。

```.pro
PRECOMPILED_HEADER = window.h
SOURCES            = window.cpp
```

为了避免类似于上面的冲突，你需要给预编译头文件一个特殊的名字。

## 项目案例

你可以在你的QT安装路径下的/example/qmake/precompile目录下找到相关源代码。

下图展示了Qt Creator 设计模式下的mydialog.ui文件，你可以在编辑模式下查看其代码。

图片可以查看[原文](http://doc.qt.io/qt-5/qmake-precompiledheaders.html)