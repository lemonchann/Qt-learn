# qmake语言

许多qmake项目文件简单的运用一些name = value和name += value的形式来描述源文件和头文件。qmake还提供了其他操作符，函数和作用域来处理变量声明中提供的信息。这些高级功能容许qmake通过一个单一文件生成多个平台的Makefile。

## 操作符

在许多项目文件中，赋值操作符（=）和附加操作符（+=）能够包含一个项目的所有信息。典型的使用时为一个变量添加一些值和根据限额是结果附加更多的值。因为qmake在定义一些变量时赋予了其一些默认值，所以许多时候需要使用-=操作符将一些不必要的值从变量中剔除。下面的几节将介绍如何使用这些操作符来编辑这些变量。

### 赋值

使用=操作符将值赋值给相应的变量

```.pro
TARGET = myapp
```

上面命令将myapp赋值给了TATGET变量，myapp这个值将会覆盖TARGET变量之前包含的值。

### 添加附加值

使用+=操作符将一个新值添加到已经包含其他值的变量当中。

```.pro
DEFINES += USE_MY_STUFF
```

上面的变量将会将USE_MY_STUFF附加到预处理定义列表中，并将更改添加到生成的Makefile文件中。

### 移除已有的值

使用-=操作符能够将变量中已经包含的值剔除。

```.pro
DEFINES -= USE_MY_STUFF
```

上面的命令将会将USE_MY_STUFF从预处理定义列表中移除，并且会将更改添加到生成的Makefile文件中。

### 添加唯一的值

使用*=操作符可以将一个值添加到变量的值列表中，但仅在当前值不包含在该变量中时。这可以避免同一个值被多次添加到同一个变量当中。例如：

```.pro
DEFINES *= USE_MY_STUFF
```

上面的命令会将USE_MY_STUFF添加到预处理定义列表中，但仅当其尚未定义时。注意：unique()函数也可以确保变量中仅包含每个值的一个示例。

### 替代一个值

使用~=操作符可以用一个指定的值替换与正则表达式相匹配的任何值：

```.pro
DEFINES ~= s/QT_[DT].+/QT
```

在上面的命令中，可以使用QT替代变量值列表中中任何以QT_D或QT_T开始的值。

### 变量扩展

$$操作符用于提取变量的值，因此其可用于在不同变量之间进行值的传递，以及将变量的值传递给函数。

```.pro
EVERYTHING = $$SOURCES $$HEADERS
message("The project contains the following files:")
message($$EVERYTHING)
```

变量能够存放环境变量的内容。这些可以在运行qmake或者使用生成的Makefile构建项目时得到应用。

使用$$(...)操作可以在运行qmake时获取环境变量的值。

```.pro
DESTDIR = $$(PWD)
message(The project will be installed in $$DESTDIR)
```

上述操作中当项目文件被处理时环境变量PWD的值将会被读取。

如果想要在生成的Makefile被处理时获取环境变量的值可以使用$(...)操作。

```.pro
DESTDIR = $$(PWD)
message(The project will be installed in $$DESTDIR)

DESTDIR = $(PWD)
message(The project will be installed in the value of PWD)
message(when the Makefile is processed.)
```

在上述命令中，在使用qmake处理项目文件时将立即读取PWD的值，但在生成Makefile时才将$(PWD)赋值给DESTDIR。这将使构建过程更加灵活，只要在处理Makefile时正确处理了环境变量即可。

### 访问qmake属性

可以使用$$[...]特殊操作来访问qmake属性。

```.pro
message(Qt version: $$[QT_VERSION])
message(Qt is installed in $$[QT_INSTALL_PREFIX])
message(Qt resources can be found in the following locations:)
message(Documentation: $$[QT_INSTALL_DOCS])
message(Header files: $$[QT_INSTALL_HEADERS])
message(Libraries: $$[QT_INSTALL_LIBS])
message(Binary files (executables): $$[QT_INSTALL_BINS])
message(Plugins: $$[QT_INSTALL_PLUGINS])
message(Data files: $$[QT_INSTALL_DATA])
message(Translation files: $$[QT_INSTALL_TRANSLATIONS])
message(Settings: $$[QT_INSTALL_CONFIGURATION])
message(Examples: $$[QT_INSTALL_EXAMPLES])
```

更多信息请参阅[配置qmake](./ConfiguringQmake.md)\

使用这种操作获取qmake的属性通常用于使第三方插件和组建能够集成到QT中。例如，如果在项目文件中做了如下声明，则一个QT Designer插件就能和QT Designer的内置插件一起安装。

```.pro
target.path = $$[QT_INSTALL_PLUGINS]/designer
INSTALLS += target
```

## 作用域

作用域和编程语言中的流程控制语句if类似。如果某个条件为真则执行作用域中所包含的声明。

### 作用域语法

作用域由一个条件和一个左大括号（在同一行）开始，结束于一个右大括号，中间包含这一些命令和声明。

```.pro
<condition> {
    <command or definition>
    ...
}
```

左括号一定要与条件写在同一行。一个作用域可能包含多个条件，其如何描述书写将在下面的几节来描述。

### 作用域和条件

一个条件和一个包含着许多命令和声明的大括号组成了作用域。例如：

```.pro
win32 {
    SOURCES += paintwidget_win.cpp
}
```

上述代码在为windows平台构建时会将paintwidget_win.cpp文件添加到生成的Makefile源代码列表中。在为其他平台构建时相关定义会被忽略。

作用域外的条件判断也可使用!进行否定，这样只有当原条件为假时才会执行作用域内的内容。例如下面的例子，可以为除了windows平台以外的内容进行构建相关内容。

```.pro
!win32 {
    SOURCES -= paintwidget_win.cpp
}
```

作用域可以多层嵌套以进行多个条件判定。例如，如果你要为指定平台添加特定的文件，并且只在debug模式下起作用。要编写的内容如下：

```.pro
macx{
    CONFIG(debug,debug|release){
        HEADERS += debugging.h
    }
}
```

为了简化多层嵌套作用域的编写，可以使用":"操作符。这样，上面的例子也可以写成下面的形式：

```.pro
macx:CONFIG(debug,debug|release){
    HEADERS += debugging.h
}
```

你也可以使用":"操作符，编写单行条件赋值语句。如下：

```.pro
win32:DEFINES += USE_MY_STUFF
```

上面的命令会仅在为windows平台构建时，将USE_MY_STUFF添加到DEFINES变量中。通常":"运算符类似于逻辑与操作，它会将一系列条件结合起来，并且当所有条件为真时才为真。

同样的也可以使用"|"操作符实现逻辑或操作。将一系列条件结合起来，只要有一个条件为真结果就为真。

```.pro
win32|macx{
    HEADERS += debugging.h
}
```

你还可以使用else作用域来提供替代选项。每个else作用域只有当提供的条件为false时才被处理。这可以让你编写复杂的测试，使用更多的选项。例如：

```.pro
win32:xml{
    message(building for windows)
    SOURCES += xmlhandler_win.cpp
}else:xml{
    SOURCES += xmlhandler.xpp
}else{
    message("Unknow configuration")
}
```

### 配置和作用域

CONFIG变量中存储的值将会被qmake特殊处理。每个可能的值都可以作为一个作用域的条件。例如：可以通过opengl值扩展CONFIG变量的值列表。

```.pro
CONFIG += opengl
```

上面命令的结果是。opengl的任何测试域都将被执行。我们可以使用这个特性，给最后的可执行文档一个适用的名称。

```.pro
opengl {
    TARGET = application-gl
} else {
    TARGET = application
}
```

使用这个功能我们能方便的修改项目的配置而不改变原有的设置。在上面的代码中如果指定了opengl则会生成一个名为application-gl的应用程序，反之则会生成一个名为application的应用程序。

由于我们可以方便的修改CONFIG的值，借助这个我们可以方便的自定义项目的设置来微调生成的Makefile。

### 平台作用域限定值

除了在许多条件作用域中使用的win32，macx和unix限定值，还可以使用其他的诸如一些平台内置工具，特定的编译器等。这些都基于QT mkspecs中提供的平台规范。例如，下面的几行命令将显示项目当前使用的规范，以及在项目中测试linux-g++规范。

```.pro
message($$QMAKESPEC)

linux-g++ {
    message(Linux)
}
```

你可以测试任何其他平台的编译器组合，只要其存在于 mkspecs目录中即可。

## 变量

项目文件中使用的文档都是qmake在生成Makefile时使用的特殊变量，例如DEFINES,SOURCES 和HEADERS。此外你还可以定义自己的变量，其创建方法时在第一次赋值的时候即是创建了变量（译者注：和python类似）。

```.pro
MY_VARIABLE = value
```

对自己定义的变量的操作是没有限制的，因为qmake会默认忽略它，除非在处理作用域内要对他进行评估。

你也可以将当前的一个变量的值赋值给另一个变量，通过$$前置字符。例如：

```.pro
MY_DEFINES = $$DEFINES
```

现在My_DEFINES变量中已经包含了DEFINES变量的值，这也等价于：

```.pro
MY_DEFINES = $${DEFINES}
```

第二种方法容许你将变量的内容附加到另一个变量而不用使用一个空格将其分隔成两部分。例如，下面的命令将确保最后的可执行文件的文件名包含项目模板的名称。

```.pro
TARGET = myproject_$${TEMPLATE}
```

## 替代函数

qmake提供了一系列的内置函数来处理变量的内容。这戏函数以变量为参数并返回一个或多个变量的值。使用$$操作符可以将这些函数的返回值赋值给另一个变量，这个和将一个变量的值赋值给另一个变量是一样的。

```.pro
HEADERS = model.h
HEADERS += $$OTHER_HEADERS
HEADERS = $$unique(HEADERS)
```

这类函数应用在赋值的右边（即作为操作数）。

你也可以定义自己的函数来处理变量的内容。

```.pro
defineReplace(functionName){
    #function code
}
```

下面的示例函数演示了，将变量名作为唯一的参数，使用内置函数eval()来提取变量的值列表，并编译文件列表。

```.pro
defineReplace(headersAndSources) {
    variable = $$1
    names = $$eval($$variable)
    headers =
    sources =

    for(name, names) {
        header = $${name}.h
        exists($$header) {
            headers += $$header
        }
        source = $${name}.cpp
        exists($$source) {
            sources += $$source
        }
    }
    return($$headers $$sources)
}
```

## 测试函数

qmake提供了一些内置函数可以用来在写作用域的时候用作条件，这些函数将不会返回一个值，而是判断测试时成功还是失败。

```.pro
count(options, 2) {
    message(Both release and debug specified.)
}
```

这种类型的函数智能用于条件表达式。

你也可以自定义这样的函数。下面的例子将演示，如何判断文件列表中的每个文件是否存在。
如果所有文件都存在则返回true反之则返回false。

```.pro
defineTest(allFiles) {
    files = $$ARGS

    for(file, files) {
        !exists($$file) {
            return(false)
        }
    }
    return(true)
}
```