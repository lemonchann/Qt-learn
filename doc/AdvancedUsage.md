# 高级应用

## 添加新的配置功能

通过在项目文件当中将功能的名称添加到CONFIG变量的值列表中，你可以创建自己需要的功能。这些功能特性由两部分组成，一是自定义功能，二是定义在.prf文件当中的功能，而这些.prf文件存放于许多标准目录中的一个。这些目录的位置被定义在了许多地方，在查找.prf文件时，qmake将会按照以下顺序进行查找。

1.存放于环境变量QMAKEFEATURES中的目录，不同的目录之间用平台路径分隔符进行分隔。（Unix使用冒号，windows使用分号）

2.存放于属性变量QMAKEFEATURES中的目录，不同目录间同样用平台路劲分隔符分隔。

3.位于mkspecs目录中的功能目录。mkspecs目录可以位于QMAKEPATH环境变量所包含目录的任一目录下。QMAKEPATH包含的目录同样由平台路径分隔符进行分隔。例如:$QMAKEPATH/mkspecs/。

4.QMAKESPEC环境变量提供的目录下的功能目录。例如：$QMAKESPEC\\<features\>。

5.存放在data_install/mkspecs目录下的功能目录。例如：data_install/mkspecs/\<features\>。

6.在作为QMAKESPEC环境变量指定的同级目录的功能目录中。例如：$QMAKESPEC/../\<features\>。

在下面的功能目录中搜索功能文件。

```.pro
1.features/unix, features/win32, or features/macx, 依赖于平台使用。
2.features/
```

例如：考虑下面在一个项目文件中的赋值：

```.pro
CONFIG += myfeatures
```

除了CONFIG变量之外，在解析完项目文件之后，qmake将会搜索上面列出的myfeature.prf文件的位置。在unix系统中，qmake会搜索以下位置。

1.$QMAKEFEATURES/myfeatures.prf (QMAKEFEATURES环境变量中列出的目录)

2.$$QMAKEFEATURES/myfeatures.prf ( QMAKEFEATURES属性变量中列举的目录)

3.myfeatures.prf (项目的根目录)

4.$QMAKEPATH/mkspecs/features/unix/myfeatures.prf 和 $QMAKEPATH/mkspecs/features/myfeatures.prf (QMAKEPATH环境变量中列出的目录)

5.$QMAKESPEC/features/unix/myfeatures.prf 和 $QMAKESPEC/features/myfeatures.prf

6.data_install/mkspecs/features/unix/myfeatures.prf 和 data_install/mkspecs/features/myfeatures.prf

7.$QMAKESPEC/../features/unix/myfeatures.prf 和 $QMAKESPEC/../features/myfeatures.prf

注意：.prf的文件名必须是小写。

## 安装文件

Unix平台下通常使用构建工具来安装应用程序和库。例如：通过调用make工具来安装。因此qmake有一个install集合概念，一个包含了有关安装项目的一部分方式说明的对象。例如，项目的相关文档信息可以用下面方式进行描述。

```.pro
documentation.path = /usr/local/program/doc
documentation.files = docs/*
```

path 成员告知qmake文件应该被安装到 usr/local/program/doc（path成员）。file成员指定将被安装的文件。在这个例子中，docs目录下的所有文档将被复制到usr/local/program/doc目录下。

一旦你完成了对安装集合的充分描述，你就可以使用下面的代码将其添加到安装列表中去。

```.pro
INSTALLS += documentation
```

qmake将会确保指定的文件被复制到安装目录中。如果你想在这个过程中添加更多的控制，你可以定义一个额外的成员对象。例如，下面的一行命令将会告诉qmake为该安装集合执行一系列命令。

```.pro
unix:documentation.extra = create_docs; mv master.doc toc.doc
```

unix作用域将会确保这些特定的命令只有在unix平台下才会被执行。其他平台下与之类似。

在额外成员中指定的命令将会先于其他的对象成员。

如果你将一个内置的安装集合添加到了INSTALLS变量中，但没有指定文件或者额外成员，qmake将会自己决定为你复制那些需要的内容。当前，支持target和dlltarget安装集合，例如：

```.pro
target.path = /usr/local/myprogram
INSTALLS += target
```

在上面的命令中，qmake将知道哪些时需要复制的，将会在安装过程中自动处理这些。

## 添加自定义目标

qmake试图完成一个跨平台构建工具所期望的一切。但，当你真的需要去运行一些特定平台的命令时，常常不尽人意。这可以通过对qmake作指定的不同后台说明来改善这些。

通过一个 object-style API ，就如qmake其它地方使用的一样，来定制Makefile文件的输出。通过指定其成员，对象将会被自动定义。例如：

```.pro
mytarget.target = .buildfile
mytarget.commands = touch $$mytarget.target
mytarget.depends = mytarget2

mytarget2.commands = @echo Building $$mytarget.target
```

上面的定义定义了一个名为mytarget的qmake目标。该目标包含一个名为.buildfile的Makefile目标，其由touch()函数生成。最后，.depends成员指定了mytarget依赖于mytarget2，这是一个之后定义的目标。mytarget2是一个虚拟目标。它仅被定义将一些文本回显到控制台。

最后一步是是通过QMAKE_EXTRA_TARGETS变量来告知qmake对于该对象所需构建的目标。

```.pro
QMAKE_EXTRA_TARGETS += mytarget mytarget2
```

这是你你实际构建自定义目标所需的全部内容。当然你也可以将这些目标中的一个绑定到[qmake build target](http://doc.qt.io/qt-5/qmake-variable-reference.html#target).做到这些你只需要，将你的Makefile目标包含到[PRE_TARGETDEPS](http://doc.qt.io/qt-5/qmake-variable-reference.html#pre-targetdeps)列表中。

自定义目标指定支持如下成员：

|成员|描述|
|-|-|
|commands|用于生成自定义构建目标的命令
|CONFIG|为自定义构建目标指定配置选项。可以在Makefile中指明递归的的规则，该规则用以调用相关目标（存放在子目标指定的Makefile中）。该成员默认为每个子目标创建了一个条目。
|depends|构建自定义目标依赖的已存在的构建目标。
|recurse|用于指定那个子目标将会被使用，当在Makefile创建子目标的调用规则，这些子目标在其指定的Makefile中。该成员只用在CONFIG中设置了recursive（递归）时才会被使用。其典型值为“Debug”和“Release”。
|recurse_target|为Makefile中的规则指定目标，这些目标应该通过子目标的Makefile来构建。这个成员添加了类似于$(MAKE) -f Makefile.[subtarget] [recurse_target]的一些东西。该成员只用在CONFIG中设置了recursive（递归）时才会被使用。
|target|自定义目标的名字|

## 添加编译器

可以通过自定义来让qmake支持新的编译器和预处理器。

```.pro
new_moc.output  = moc_${QMAKE_FILE_BASE}.cpp
new_moc.commands = moc ${QMAKE_FILE_NAME} -o ${QMAKE_FILE_OUT}
new_moc.depend_command = g++ -E -M ${QMAKE_FILE_NAME} | sed "s,^.*: ,,"
new_moc.input = NEW_HEADERS
QMAKE_EXTRA_COMPILERS += new_moc
```

基于上面的定义，你可以使用对moc的直接替换，如果可用的话。该命令将会执行NEW_HEADERS变量（该变量来自于input成员）中所包含的所有参数，并会将执行结果写入到output成员定义的文件当中。该文件将会被添加到项目的其他源文件中。此外，qmake还将执行depend_command以生成依赖信息，并将该信息存放在项目中。

自定义编译器的指定规则将包含以下成员：

|成员|描述|
|-|-|
|commands|从输入到生成输出所需的命令
|CONFIG|指定自定义编译器的配置选项。进一步信息请参阅CONFIG表
|depend_command|指定用于为输出生成依赖列表的的命令。
|dependency_type|指定输出文件的类型。如果是已知类型（例如，TYPE_C,TYPE_UI,TYPE_QRC),则将其作为这些问价类型进行处理。
|input|指定需要被自定义编译器处理的文件的变量。
|name|对于自定义编译器正在作的内容做一个描述。这仅在一些后端使用。
|output|由自定义编译器创建的文件名。
|ouput_functyion|指定一个自定义的qmake函数，该函数通常被用来指定被创建的文件名。
|variables|当在.pro文件中以$(VARNAME)引用时，此处指定的变量将会被替换成$(QMAKE_COMP_VARNAME).
|variable_out|从输出创建的文件应该被添加到变量中。

CONFIG成员支持以下选项：

|选项|描述
|-|-|
|combine|表示所有的输入文件将会被合并为一个输出文件。
|target_predeps|指明输出应该被添加到PRE_TARGETTDEPS列表中。
|explicit_dependencies|输出的依赖只能从depends成员生成，而不能从其他地方。
|no_link|指明叔叔不应该被添加到要被链接的对象列表中。

## 库依赖

通常，在于库进行链接时qmake依赖底层平台去知晓该库链接的其他库，并让平台将它引入。然而在许多案例中，这并不能满足需要。例如，当链接一个静态库时，由于不需要链接其他库，因而就不创建这些库的依赖关系。但是，之后需要链接该库的应用程序需要知道在哪可以发现这些静态库所需的符号。如果你显式的启用了库追踪，在适当的时候，qmake将会尝试追踪库的依赖关系。

第一步是启用库中的依赖关系追踪。要做到这个，你必须告知qmake保存库的相关信息：

```.pro
CONFIG += create_prl
```

该选项只有在lib模板下有效，其他模板下将会被忽略。当启用该选项时，qmake将会创建一个后缀为.prl的文件，该文件保存了库的一些元信息。该元文件，就像一个普通的项目文件，但仅包含了内置变量声明。当安装这个库时，通过指定它作为一个INASTALL目标声明，qmake将会自动的将.prl文件复制到安装目录中。

第二步是在使用静态库的应用程序中启用读取此元信息：

```.pro
CONFIG += link_prl
```

启用此功能后，qmake将会处理应用程序链接的所有库并查找其元信息。qmake将会借此来确定相关的链接信息，特别是将一些值添加到应用程序项目文件的DEFINES 和IBS中。一旦qmake处理完该文件，它将查看LIBS变量中新添加的库，并查找其依赖的.prl文件，知道解决所有的库。此时，Makefile会像往常一样被创建，并显式的将这些库链接到应用程序中。

.prl文件应该只能被qmake创建，不因该在操作系统之间传输，因为它们可能会包含平来依赖信息。