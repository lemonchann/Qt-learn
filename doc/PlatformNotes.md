# 平台笔记

许多跨平台的项目可以通过基本的qmake配置来处理。然而，在一些平台上利用一些特定于平台的功能，是有效的，甚至是必要的。qmake可以通过一些特定的变量来访问这些功能，这些变量只对特定的平台生效。

## macOS，iOS，tvOS，和watchOS

特定于这些平台的功能包括支持创建通用二进制文件，框架和软件包。

### 源码和二进制包

源代码中使用的qmake和二进制包中的稍有不同，因为它们使用不同的功能规格（译者自注：qt的安装包有源码版本和二进制版）。源代码包中通常使用macx-g++规范，而二进制版本则使用macx-xcode规范。

每个包的使用者都可以通过在调用qmake的时候添加-spec选项来覆盖相关配置（更详细的信息请参阅[运行qmake](RunningQmake.md)）。例如：你可以在命令行中调用下面的命令来通过二进制版本的qmake在项目路径当中生成项目的Makefile。

```.pro
qmake -spec macx-g++
```

### 使用框架

qmake可以自动生成构建规则，以便存放于/Library/Frameworks/下的macOS上的标准框架目录中的框架进行链接。

要将标准框架目录指以外的目录添加到构建系统当中，可以通过LIBS变量添加链接选项。例如：

```.pro
LIBS += -F/path/to/framework/directory/
```

框架本身通过在LIBS变量中附加-framework选项和框架名来链接：

```.pro
LIBS += -framework TheFramework
```

### 创建框架

可以对任何给定的库项目进行配置，以便将生成的库文件放入到框架当中，以备部署。因此我们要将项目设置成lib模板，并将lib_bundle选项添加到CONFIG变量当中。

```.pro
TEMPLATE += lib
CONFIG += lib_bundle
```

通过使用QMAKE_BUNDLE_DATA绑定和库相关的数据。这些数据和库绑定的通常用于指定相关的头文件，正如下面所示：

```.pro
FRAMEWORK_HEADERS.version = Versions
FRAMEWORK_HEADERS.files = path/to/header_one.h path/to/header_two.h
FRAMEWORK_HEADERS.path = Headers
QMAKE_BUNDLE_DATA += FRAMEWORK_HEADERS
```

通过使用FRAMEWORK_HEADERS变量需要的头文件，尤其是框架需要的。将它附加到QMAKE_BUNDLE_DATA变量中可以确保头文件相关的信息可以被添加到库安装包资源的集合当中。框架的名字和版本信息也可以使用，QMAKE_FRAMEWORK_BUNDLE_NAME和QMAKE_FRAMEWORK_VERSION变量所指定，当然默认情况下，其值是由TARGET和VRRSION变量所指定的。

更多请参阅[QT for macOS-Deployment](http://doc.qt.io/qt-5/osx-deployment.html)中关于应用和库开发的相关信息。

### 创建和移植Xcode项目

macOS下的开发者可以根据[QT for maxOS](http://doc.qt.io/qt-5/osx.html#additional-command-line-options)文档中描述的利用qmake对Xcode项目文件的支持通过运行qmake将qmake项目文件移植成Xcode项目文件。例如：

```.pro
qmake -spec macx-xcode project.pro
```

注意：如果一个项目的的存储位置发生了改变，则必须重新运行qmake对项目文件进行处理并生成一个新的Xcode项目文件。

### 支持同时构建两个目标文件

同时构建两个目标文件在当前是不可行的，因为Xcode的项目构建概念是不同于qmake构建目标文件的概念的。

Xcode动态构建配置设置是基于修改Xcode配置，编译器标识以及其他相似的构建选项。不像visual studio，Xcode不容许根据是否选择debug或release版本来指定不同的库文件。qmake通过控制不同的库文件链接到不同的可执行文件来区别debug和release。

目前无法在qmake生成的Xcode项目文件当中设置Xcode配置当中需要设置的文件。在库和框架中链接其他库的方法依然是选择Xcode的构建系统。

此外，选定的活动配置信息存储在.pbxuser文件当中，该文件有Xcode第一次加载项目文件时生成而不是由qmake生成。

## Windows

特定于此平台的功能包括对windows资源文件（包括被提供的或者自动生成的）的支持，创建visual studio项目文件以及部署使用visual studio 2005或更高版本开发QT应用时所需处理的清单文件。

### windows资源文件

这一节将描述如何处理windows的资源文件并将其链接到应用程序的可执行文件(EXE)或者动态链接文件（DLL）。qmake能够选择性的自动生成一个适合的可填充的windows资源文件。

一个被链接的windows资源文件可能包含许多可以被相应的EXE或DLL文件访问的元素。QT的资源系统应该以独立于平台的方法来访问链接资源。然而，一些被windos资源文件链接的标注元素被windows自身所访问。例如：在windows资源管理器当中文件属性的版本选项由资源元素填充，此外EXE文件的程序图标也是从这些元素中读取。因此，对于QT创建的EXE或DLL同时使用两种资源管理技术是比较好的做法，即使用QT的资源系统有使用windows自身的资源管理系统。

通常，资源定义脚本（.rc文件）被编译为windows资源文件。在Microsoft工具链中，RC工具将生成一个.res文件，该文件可以被Microsoft链接器链接到EXE或DLL。MinGW工具链则使用winres工具生成一个.o文件，并使用MinGW链接器链接到EXE或DLL。

通过对VERSION和RC_ICONS系统变量中的至少一个进行设置qmake就可以选择性的自动生成一个合适的用于填充的.rc文件。生成的.rc文件可以自动编译和链接。被添加到.rc文件中的元素可以由以下系统变量定义： QMAKE_TARGET_COMPANY, QMAKE_TARGET_DESCRIPTION, QMAKE_TARGET_COPYRIGHT, QMAKE_TARGET_PRODUCT, RC_CODEPAGE, RC_ICONS, RC_LANG,和 VERSION。

如果这些元素包含的信息不够充分，qmake还有RC_FILE和RES_FILE两个系统变量用于直接创建一个外部的.rc或.res文件。通过设置其中的一个变量，能够使指定的文件链接到EXE或DLL。

注意：如果设置了RC_FILE或RES_FILE，qmake生成的.rc文件将会被阻断。qmake将不能进一步对生成的.rc文件进行修改，其他和.rc文件相关的变量也将失效。

### 创建Visual Studio项目文件

这一节将描述如何将qmake项目移植到Visual Studio中。qmake能够根据项目文件创建一个Visual Studio项目，该VS项目包含开发环境要求的所有必要信息。这些可以通过将项目模板设置成vcapp（应用程序项目）或vclib（库项目）来获得。当然我们也可以使用命令行来达到相同的效果，例如：

```.pro
qmake -tp vc
```

通过下面的命令可以递归的在子目录下生成一个.vcproj文件和在主目录下生成.sln文件。

```.pro
qmake -tp vc -r
```

你每次更新项目文件后，需要重新运行qmake来更新对应的Visual Studio项目文件。

注意：如果你使用Visual Studio Add-in工具，可以选择QT->Import from .pro file菜单导入.pro项目文件。

### Visual Studio 清单文件

在使用Visual Studio 2005或者更高版本构建QT应用程序的时候，请确保应用程序被链接时创建的清单文件能够被正确处理。这是为生成DLL的工程自动处理的。

删除应用程序的可执行文件的清单嵌入可以通过以下命令完成：

```.pro
CONFIG += embed_manifest_exe
```

同样可以使用下面的命令来删除DLL的清单嵌入式

```.pro
CONFIG -= embed_manifest_dll
```

更多的详细信息请参阅[deployment guide for Windows](http://doc.qt.io/qt-5/windows-deployment.html#manifest-files).