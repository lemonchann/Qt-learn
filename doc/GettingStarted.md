# 入门简介

[目录](.\SUMMAY.md)

本教程向你介绍使用qmake的基础部分。本手册中的其他部分将包含有关使用qmake的更多详细信息。

## 从一个简单的例子开始

假设你刚刚实现了应用程序的基本部分，并已成功创建了以下文件：

```.pro
HELLO.CPP
hello.h
main.cpp
```

你可以在你的qt安装目录的examples/qmake/tutorial中找到这些文件。关于应用程序的设置，你唯一知道的是它是用Qt编写的。首先，你可以用你喜欢的文本编辑器在examples/qmake/tutorial目录中创建一个名为hello.pro的文件，并首先在hello.pro文本文档中添加一些内容，以此来告诉qmake该目录下的相关头文件以及源文件是你开发项目中的一部分。

我们将首先将源文件添加到项目文件中。要做到这一点，你需要使用SOURCES变量(关于SOURCES变量的详细信息你可以在[变量](.\Variable.md)这一节中查找)，并在hello.pro文件中添加如下内容：

```.pro
SOURCES + = hello.cpp
SOURCES + = main.cpp
```

如果你更喜欢使用Make-like语法，可以使用转译字符（\），写成下面这样的形式：

```.pro
SOURCES = hello.cpp \
          main.cpp中
```

既然源文件已列在项目文件中，则还要添加头文件。这里我们使用HEADERS变量，其使用形式与SOURCES变量是一样的。

如果你完成了上面这些，你的项目文件(hello.pro)应该包含以下内容：

```.pro
HEADERS + = hello.h
SOURCES + = hello.cpp
SOURCES + = main.cpp
```

生成的目标文件的名称默认是和项目文件名是保持一致的，但对于不同的平台，不同的操作系统，其在形式上会有所不同。比如对于我们这个简单的例子来说，由于项目文件名是hello.pro所以在windows下默认会生成hello.exe,在Unix下会生成hello，如果你想要自定义名称可以在你的项目文件中添加以下内容：

```.pro
TARGET = helloworld
```

现在你可以使用qmake为你的应用程序生成一个Makefile。打开命令行，切换到你的项目目录，并键入以下内容：

```bash
qmake -o Makefile hello.pro
```

然后键入make或nmake,这取决于你使用的编译器。

对于Visual Studio用户，qmake也可以生成Visual Studio项目文件。例如：

```bash
qmake -tp vc hello.pro
```

## 添加调试功能

应用程序的发行版本不包含任何调试符号或其他调试信息。在项目开发过程中，生成带有调试信息的调试版本是非常有用的，而想做到这个，我们只需要将debug添加到CONFIG变量中，即可轻松完成。
例如我们可以在该项目中这样做：

```.pro
CONFIG + =debug
HEADERS + =hello.h
SOURCES + = hello.cpp
SOURCES + = main.cpp
```

完成上面的操作，即可像之前一样使用make生成Makefile，并进而生成可以在调试环境中运行并生成相关调试信息的调试版本。

## 添加不同平台的特定源文件

经过几个小时的代码编写之后，你可能需要在不同的平台下使用不同的源代码来编译你的应用程序。所以我们需要同时将两个不同的源文件添加到项目中，例如在这个例子中我们可能需要添加hellowin.cpp和 hellounix.cpp两个源文件。但我们不能像之前那样直接将两个源文件用SOURCES变量添加到项目中区，因为如果这样两个源文件都会被添加到Makefile当中，导致在任何一个平台，两个源文件都会被直接编译。因此我们可以在项目文件当中，向下面那样为不同的平台添加不同的源文件。

为Windows添加平台相关文件的简单示例：

```.pro
win32 {{
    SOURCES + = hellowin.cpp
}}
```

在为Windows构建时，qmake将添加hellowin.cpp到源文件列表中。在为任何其他平台构建时，qmake会忽略它。使用类似的方法也可以为unix平台添加其使用的源文件。

如果你完成以上所有操作，你的项目文件应该包含如下内容：

```.pro
CONFIG + =debug
HEADERS + = hello.h+ 
SOURCES + = hello.cpp 
SOURCES + = main.cpp
win32 {{
    SOURCES + = hellowin.cpp
}}
unix {{
    SOURCES + = hellounix.cpp
}}
```

像前面一样在运行qmake后就可以重新生成一个Makefile

## 运行qmake时检查文件是否存在

如果某个文件不存在，你可能不想创建Makefile。我们可以通过使用exists（）函数来检查文件是否存在。我们可以通过使用error（）函数来阻止qmake继续运行。这个功能的使用和上面为不同平台添加不同源文件的使用方法类似，例如我们要检查一个名为main.cpp的文件，如下所示：

```.pro
！exists（main.cpp）{
    error("no main.cpp file found")
}
```

感叹号用于否定。也就是说，对于exists( main.cpp )，如果文件存在返回的是True，如果不存在返回的是false。到这一步，我们的项目文件应该包含以下内容：

```.pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
win32 {
    SOURCES += hellowin.cpp
}
unix {
    SOURCES += hellounix.cpp
}
!exists( main.cpp ) {
    error( "No main.cpp file found" )
}
```

像以前一样使用qmake来生成一个makefile。如果你main.cpp暂时重命名，你将看到No main.cpp file found的提示，并且qmake将停止运行，你将无法获得一个新的Makefile。

## 对更多的条件进行检查

假设你使用Windows，想要当你在命令行运行你的应用程序时，通过qDebug()函数看到程序的输出状态。想要做到这样，你必须使用适当的控制台设置来构建你的应用程序。我们可以很容易地把console添加到CONFIG变量中，就可以将相关设置写入到Makefile，从而实现此功能。但是，假设我们只想在windows平台，并且只在debug模式当中启用该功能，这需要使用两个嵌套的作用域。首先创建一个作用域，然后在其中创建另一个作用域。将相关设置放在第二个作用域当中，如下所示：

```.pro
win32 {
    debug {
        CONFIG += console
    }
}
```

嵌套作用域可以使用冒号连接在一起，所以最终的项目文件如下所示：

```.pro
CONFIG += debug
HEADERS += hello.h
SOURCES += hello.cpp
SOURCES += main.cpp
win32 {
    SOURCES += hellowin.cpp
}
unix {
    SOURCES += hellounix.cpp
}
!exists( main.cpp ) {
    error( "No main.cpp file found" )
}
win32:debug {
    CONFIG += console
}
```

ok！你现在已经完成了qmake的入门教程，并准备为你的开发项目编写项目文件。

## 以下内容是我自己补充的内容

1.在安装qt的时候我们就可以选择安装相关的编译工具，既然我们选择了qmake那自然就安装windows下的minGw（该编译器其实就是gcc的windows版本）,或者Linux下的gcc。而qt中是包含相关的编译工具的。qt安装的minGW是包含make工具的，具体如何使用可以自行百度或者谷歌，这里不再具体说明了。

[返回目录](.\SUMMAY.md)