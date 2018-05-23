# 构建通用项目类型

本章将介绍如何编写基于QT的三种项目类型（应用程序，库文件和插件）的项目文件。虽然所有的项目类型都使用许多相同的变量，但每个项目类型都有其特定的项目变量来定义项目输出文件。

这里将不对特定平台的变量做介绍，对此的详细说明请参阅，[QT for Windows-Deployment](http://doc.qt.io/qt-5/windows-deployment.html)和[QT for macOS](http://doc.qt.io/qt-5/osx.html)

## 构建一个应用程序

当选择app模板时qmake会生成一个可以构建应用程序的Makefile。当选择app模板的时候我们可以通过对CONFIG变量赋予下面的选项来指定应用程序的类型。

|Option|Description
|-|-|
|windows|这是一个windows GUI应用程序
|console|该选项只有app模板可以使用，这是一个windows控制台应用程序
|testcase|这是一个 automated test 应用程序

当使用app模板你应该了解以下qmake系统变量，使用这些变量来在你的.pro项目文件当中指定一些你应用程序的信息。对于依赖于平台的系统变量，可以参阅[平台注释](PlatformNotes.md)

```.pro
>HEADERS - 项目中需要使用的头文件列表
>SOURCES - 项目中需要使用的源文件列表
>FORMS - 项目中需要使用的UI文件列表（由Qt Designer 创建）
>LEXSOURCES - 项目中需要使用的lex源文件列表(what is lex and yacc ,i don't know.)
>YACCSOURCES - 项目中要使用的yacc源文件列表
>TARGET - 用于指定应用程序的可执行文件的文件名，默认是项目文件的文件名，如果该文件有扩展名的话会自动添加
>DESTDIR - 用于指定项目生成的目标执行文件的存储目录
>DEFINES - 应用程序当中需要的附加预处理的定义列表
>INCLUDEPATH - 项目中需要附加的包含目录列表
>DEPENDPATH - 应用程序依赖关系的搜索路径
>VPTH - 支持文件的搜索路径
>DEF_FILE - 仅在windows平台下使用：一个链接应用程序.def文件
```

你只需要对你需要用到的系统变量赋值。例如，如果你不需要使用额外的包含路径，你就不需要对INCLUDEPATH变量指定任何内容。qmake会对这些变量添加必要的默认值。一个项目文件的的示例也许会像下面这样：

```.pro
TEMPLATE = app
DESTDIR  = c:/helloapp
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
DEFINES += USE_MY_STUFF
CONFIG  += release
```

对于只包含一个值的变量的赋值我们使用“=”操作符，例如TEMPLATE和DESTDIR变量。对于包含多个值的变量我们一般使用"+="操作符将新值添加到现有的变量当中。这里我们要区别一下”=“，”+=“操作符的不同，”=“会将新值添加到我们要添加的变量当中，并删除变量之前所拥有的所有值，”+=“则只会将新值添加到变量当中，而不对变量中已有的其他值作操作。

## 构建一个Testcase项目

testcase项目是用来作自动化测试的应用程序项目。任何选用了app模板的的项目都可以通过将testcase赋值给CONFIG变量来将其标记为testcase项目。

对于testcase项目，qmake在生成其Makefile文件的时候会插入一个检查目标进去。该检查目标会运行应用程序。如果应用程序以退出码为零运行结束，则认为测试通过。

检查目标可以通过SUBDIRS项目自动递归。这意味着可以从SUBDIRS项目中发出make check 命令来运行整个测试套件。

检查目标可以由一些Makefile变量所指定。这些变量如下所示：

|变量|描述
|-|-|
|TESTRUNNER|每个测试命令都有一个命令或者shell脚本,示例使用的是一个超时脚本，如果在规定时间内没有通过测试，它将会终止测试程序。
|TESTARGS|对于每个测试命令添加附加参数。例如传递参数来设置测试的输出文件和格式，这可能是有效的（例如QTestLib支持的 -o filename format）

注意：必须在调用make工具时设置相关变量，而不是在.pro项目文件当中。大多数make工具搜支持直接在命令行上设置Makefile变量。如下所示：

```.pro
#通过test-wrapper并使用xunitxml个输出格式来运行测试
# 在这个测试样例中。test-wrapper是一个终止的虚拟包装脚本
# 如果不能在”--timeout“选项设置的时间内完成，则测试将不会完成.
#  "-o result.xml,xunitxml" 选项将会被QTestLib所打断.
make check TESTRUNNER="test-wrapper --timeout 120" TESTARGS="-o result.xml,xunitxml"
```

testcase项目可以使用CONFIG选项进行进一步的配置
|选项|描述|
|-|-|
|insignificant_test|测试的退出代码将会被make check忽略

testcase 通常使用[QTest](http://doc.qt.io/qt-5/qtest.html)和[TestCase](http://doc.qt.io/qt-5/qml-qttest-testcase.html)编写，但一般不需要使用CONFIG+=testcase和make check。唯一的重要要求是测试程序成功运行时退出码为零，否则为非零。

## 构建一个库文件项目

选择lib模板qmake会生成一个能够可以构建库文件的Makefile。当我们使用这个模板的时候，app模板支持的变量以及VERSION变量时被支持的。你可以使用这些变量在.pro文件当中配置库文件的相关信息。

在使用lib模板的时候下面的一些选项能够被添加到CONFIG变量中，以此来确定将要被构建的是那种类型的库文件。

|选项|描述|
|-|-|
|dll|这是一个被分享的库文件（dll）
|staticlib|这是一个静态库
|plugin|该库文件是一个插件

以下的选项也能够添加库的一些附加信息

>VERSION - 库文件的版本号

库文件的目标文件名是依赖于平台的。例如在X11，macOS，以及IOS，库文件名以lib为前缀，在windows平台下则没有前缀。

## 构建一个插件

插件（plugin）使用lib模板构建，其使用方法如上一节所示。选用这个模板qmake将会生成一个Makefile文件，该Makefile将以合适的形式为 不同的平台构建一个插件，通常是库文件的形式。和普通的库文件一样，VERSON变量也可以用于指定插件的相关信息。

### 构建一个QT Designer插件

QT Designer插件是使用一组特定的配置设置构建的，这些配置取决于QT为你的系统的配置的方式。简便起见，可以向QT变量添加designer选项来启用这些设置。例如：

```.pro
QT +=widgets designer
```

查询更多基于插件的例程，请参阅[QT Designer例程](http://doc.qt.io/qt-5/examples-designer.html)

## 在Debug和Release模式下构建和安装

许多时候，同时在Debug和Release模式下构建一个工程是必要的。虽然CONFIG变量包含debug和release两个选项，但在使用的时候只会应用最后一个被指定的选项。

### 在两种模式下同时构建

为了项目能够同时在两种模式下构建，你必须在CONFIG变量中添加debug_and_release选项。添加方式如下：

```.pro
CONFIG += debug_and_release

CONFIG(debug, debug|release) {
    TARGET = debug_binary
} else {
    TARGET = release_binary
}
```

上面的代码段确保了在不同的模式下生成的目标文件名不同。采用不同的目标文件名是为了它们彼此不会覆盖彼此。

当对这个项目文件运行qmake的时候，它会生成一个Makefile文件，该Makefile文件中所包含的内容能够同时在两种不同的模式下同时构建。当你运行以下命令的时候可以被调用。

```.pro
make all
```

当将build_all选项添加到CONFIG变量中的时候，将会默认同时在两种模式下构建。

```.pro
CONFIG +=build_all
```

运行以下命令Makefile将会在默认规则下被处理:

```.pro
make
```

### 在两种模式下安装

build_all选项也确保你在调用安装的时候默认同时安装两个版本：

```.pro
make install
```

可以根据不同的平台（platform）以不同目标文件名来构建项目。例如，一个在Unix平台上使用的库或插件，可以在windows下使用不同惯例来命名。

```.pro
CONFIG(debug, debug|release) {
    mac: TARGET = $$join(TARGET,,,_debug)
    win32: TARGET = $$join(TARGET,,d)
}
```

上述代码片段是在调试模式下更改构建目标的名称的，可以通过添加else，来添加release模式下的类似操作。
