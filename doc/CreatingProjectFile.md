# 创建项目文件

项目文件（.pro文件）包含qmake构建应用程序，库库文件或插件所需的所有信息。通常，你使用一系列声明来指定项目中的资源，但支持简单的编程结构使你能够为不同的平台和环境描述不同的构建过程。

## 项目文件元素

qmake使用的项目文件格式可以用来支持简单和相当复杂的构建系统。简单的项目文件使用简单的声明式样式，定义标准变量以指示项目中使用的源文件和头文件。复杂的项目可能会使用控制流结构来优化构建过程。

以下各节介绍项目文件中使用的不同类型的元素。

### 变量

在项目文件中，变量用于保存字符串列表。在简单的项目中，qmake通过这些变量来获得项目配置，以及项目构建过程中所涉及的文件名和路径。

qmake通过项目中某些变量所包含的信息来决定要写入到Makefile中的内容。例如，HEADERS和SOURCES变量所包含的内容，用于告知qmake与项目文件位于同一目录中的头文件和源文件。

变量也可以在内部用于存储临时值列表，现有的值列表可以用新值覆盖或扩展。

以下片段说明如何将值列表赋值给变量：

```.pro
HEADERS = mainwindow.h paintwidget.h
```

变量中的值列表按以下方式扩展：

```.pro
SOURCES = main.cpp mainwindow.cpp \
          paintwidget.cpp
CONFIG + =console
```

注：第一个赋值仅包含与HEADERS变量在同一行中指定的值。第二个赋值SOURCES通过使用反斜线（\）分隔变量中的值。

在CONFIG变量是qmake的生成生成文件时使用另一个特殊的变量。它在“ 常规配置”中讨论。在上面的代码片段中，将console添加到包含的现有值列表中CONFIG。

下表列出了一些常用的变量并描述了它们的内容。有关变量及其说明的完整列表，请参阅[变量](Variables.md)。

|变量 | 内容
|- |:-|
|CONFIG| 一般项目配置选项.
|DESTDIR| 将放置可执行文件或二进制文件的目录.
|FORMS|  用户界面编译器（uic）处理的UI文件列表.
|HEADERS| 构建项目时使用的头文件（.h）文件的列表.
|QT|  项目中使用的Qt模块列表.
|RESOURCES|  最终项目中包含的资源（.qrc）文件列表有关这些文件的更多信息，请参阅Qt资源系统.
|SOURCES|  构建项目时要使用的源代码文件列表.
|TEMPLATE|  用于该项目的模板这决定了构建过程的输出是应用程序，库还是插件.

变量的内容可以通过将变量名加上前缀来读取$$。这可以用来将一个变量的内容分配给另一个变量

```.pro
TEMP_SOURCES = $$ SOURCES
```

该$$运算符广泛地用于对字符串和值列表进行操作的内置函数。有关更多信息，请参阅[qmake语言](qmakeLanguage.md)。

## 空格

空格通常用来在变量赋值中作为分隔符使用，如下所示要想将"Progrom File"这样包含空格的值赋值给变量，则必须像下面这样使用双引号（注意这里的双引号是在英文状态下输入的）：

```.pro
DEST = "Program File"
```

引用的文本被作为变量包含值列表中的一个单独的项目，相似的方法也被用于处理包含空格的文件路径当中，尤其是对于定义windows平台下INCLUDEPATH和LIBS变量：

```.pro
win32:INCLUDEPATH+="c:/mylibs/extra headers"
uinx:INCLUDEPATH+="/home/user/extra headers"
```

## 注释

你可以在项目文件中添加一些必要的注释内容，注释以'#'开始并持续一行的末尾（和c++中的单行注释基本一致），如下所示：

```.pro
＃评论通常从一行开始，但是他们
＃也可以跟随同一行上的其他内容。
```

要想将包含‘#’的值赋值给变量，则必须使用内置的LITERAL_HASH变量。

## 内置函数和控制流

qmake提供了许多内置的函数来处理变量包含的内容。简单项目中最常使用的是include()函数，include()函数的传入参数是文件名。给定文件的内容包含在include()函数使用的地方的项目文件中。include()函数最常使用于包含其他项目文件，例如：

```.pro
include(other.pro)
```

对条件结构的支持,可通过在编程语言中表现如同语句的范围来提供if：

```.pro
win32 {
    SOURCES + = paintwidget_win.cpp
}
```

和c++语言条件运行一样，只有大括号外的条件为真大括号内的内容才会运行。在这种情况下，入宫win32 CONFIG被设置，当你在windos平台下构建项目的时候，便会自动触发这些配置。如果不使用大括号的形式，而使用开放式则必须保证内容都写在一行。

对变量更加复杂的操作，通常抱含循环，可由诸如find(),unique()以及count等内置函数实现。这些函数以及许多其他函数提供了字符串和路径操纵，支持用户输入以及调用外部工具。有关函数使用的更多信息，请参阅[qmake语言](.\QmakeLanguage.md)。对于更多的函数的使用的详细信息，请参阅[替代函数](.\ReplaceFunction.md)和[测试函数](TesstFunction.md)。

## 项目模板

TEMPLATE变量用于定义项目的构建类型，如果项目文件当中没有定义，则qmake会默认构建一个应用程序，当运行qmake时则会生成相应的Makefile，或其他等价的文件。

下表总结了可用项目的类型，并描述了qmake为其生成的相应文件：

|模板|  qmake输出
|-|-|
|app(default)| 一个用于构建应用程序的Makefile。
|lib |一个用于构建库文件的Makefile。
|aux| 生成一个不构建任何内容的Makefile。如果你不准备使用编译器区构建目标项目，那么可以使用它。比如你的项目时使用解释型语言编写的。(注意：该选项只适用于生成Makefile文件，其并不适用于生成vcxproj和Xcode项目文件)
|subdirs|生成一个包含子目录规则的Makefile，特别是使用SUBDIRS变量的。每个子目录必须包含其自己的项目文件。
|vcapp  | 生成一个用于生成应用程序的Visual Studio项目文件
|vclib  | 生成一个用于构建库文件的Visual Studio项目文件。
|vcsubdirs  | 在子文件夹中构建项目的Visual Studio解决方案。

有关TEMPLATE变量使用lib和app选项编写项目文件的进一步信息，请参阅[构建常用项目类型](.\BuildingCommonProjectTypes.md)。

在TEMPLATE变量使用subdirs选项时，qmake会生成一个Makefile，用于检查每个指定子文件夹，并运行相应平台下的make工具，通过生成的Makefile来处理这些子文件夹下所包含的所有项目文件。所用需要被处理的子文件夹列表都保存在SUBDIRS变量当中。 

## 一般配置

通过CONFIG变量可以指定项目中需要配置的选项和功能。

项目可以在release，debug以及debug_and_release三种模式下构建。如果同时指定了debug和release两种模式，则只有release模式会生效。如果使用了debug_and_release模式，则qmake生成的Makefile则会同时包含debug和release两个版本的生成信息，并通过以下命令生成：

```.pro
make all
```

将build_all添加到变量CONFIG中可以使在构建项目时默认生成release和debug两个版本。

注意：在使用CONFIG变量时也可以使用条件判定，使用内置的CONFIG()函数可以判定某些配置在当前是否可用。例如，可以用下面的代码来测试opengl选项是否可用：

```.pro
CONFIG(opengl) {
    message(Building with OpenGL support.)
} else {
    message(OpenGL support is not available.)
}
```

使用不同的配置可以分别对应release和debug的构建，关于这个的详细信息，可以参阅[qmake语言](.\qmakeLanguage.md)中的Using Scopes部分。

以下选项定义了要构建的项目类型。

注意：其中一些选项仅在相关平台上使用时才生效。

|Option| Description
|-|-|
|QT  |该项目是一个Qt应用程序，应该链接到Qt库。你可以使用该QT变量来控制应用程序所需的任何其他Qt模块。qt这个值是默认添加到你的项目当中的，当然你可以将它。删除对非qt项目使用qmake。
|X11| 该项目是一个X11应用程序或库。如果目标使用Qt，则不需要此值。

该应用程序和库项目模板为你提供更专业的配置选项微调构建过程。这些选项在[构建常用项目文件](.\BuildingCommonProjectTypes.md)中详细介绍。

例如，如果你的应用程序使用Qt库并且你想以debug模式构建它，那么你的项目文件将包含以下内容：

```.pro
CONFIG+=qt debug
```

注意：你必须使用“+ =”，而不是“=”，否则qmake将无法使用Qt的配置来确定项目所需的设置。

## 在项目中添加qt库

如果qt这个值被赋值给了CONFIG变量，则qmake会启用对qt应用程序的支持。这可以让我们方便准确的添加我们应用程序中所需要使用的qt模块。我们可以通过QT变量来声明我们要使用的扩展模块。例如，我们可以通过下面的方法添加XML和network模块：

```.pro
QT+=network xml
```

注意：QT变量是默认包含core和gui模块的，所以像上面那样是可以将network和xml模块添加到默认列表当中的，即此时的QT包含core，gui，network和xml四个模块。如果使用下面的赋值语句则会将默认的core和gui模块排除在外，但如果这样当你在编译源代码的时候会导致一些错误。

```.pro
QT=network xml#Thid will omit the core and gui modules
```

如果你想构建一个不包含gui模块的项目，你可以使用“-=”操作符将gui模块排除在项目之外。默认情况下QT会包含core和gui模块，所以你使用下面的命令就可以创建一个最小QT项目（不包含gui）：

```.pro
QT -= gui #only the core module is used.
```

有关QT可以添加的模块列表，可以查阅[变量](.\Variables.md)中介绍的QT变量。

## 配置相关特性

可以使用一些包含指定特性的文件来设置一些qmake的额外特性。这些额外的特性通常为构建过程中使用的自定义工具提供支持。要在构建过程中添加某个特性，需要将特性的名（特性文件名的主干）添加到CONFIG变量当中。

例如，qmake能够利用[pkg-config](http://www.freedesktop.org/wiki/Software/pkg-config)所支持的外部库文件来配置构建过程，比如下面使用的D-Bus 和ogg库：

```.pro
CONFIG += link_pkgconfig
PKGCONFIG += ogg dbus-1
```

有关添加特性的更多信息，请参阅添加[高级使用](AdvancedUsage.md)中的添加一个新的特性。

## 使用其他库文件

如果你要在项目中使用除了qt库之外的库文件的话，你需要在你的项目文件当中指明它。

qmake搜索库的路径以及要链接的特定库的路径，可以添加到LIBS变量中的值列表中。你可以指定库的路径或使用Unix风格的表示法来指定库和路径。

例如，以下几行显示了如何指定一个库：

```.pro
LIBS += -L/usr/local/lib -lmath
```

包含头文件的路径也可以使用INCLUDEPATH变量以类似的方式指定。

例如，要添加多个要搜索头文件的路径：

```.pro
INCLUDEPATH = c:/msdev/include d:/stl/include
```
