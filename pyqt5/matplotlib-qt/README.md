# 在pyqt5中使用matplotlib

## 前言

虽然，qt中也提供了绘图函数，但对于初学者并不是很容易掌握，众所周知，[matplot](https://matplotlib.org/)提供了简单，易用，强大的绘图函数，结合mumpy基本可以达到matlb中的绘图体验，并且比matlab更加具有扩展性，也更自由。通过matplotlib提供的官方例程的修改，就可以很容易的绘制你想要的图形，真的很强大。（我也是名初学者）

## 代码解析

通过matplotlib.use('Qt5Agg')，这行代码声明matplotlib将要嵌入到pyqt5中，同样通过这句，也可以声明将matplotlib嵌入到其他的，gui界面中去，然后通过继承FigureCanvas类来获得一个即使widget的类也是FigureCanva类的类，然后通过self.fig成员，生成一个绘图类，并由其创建一个绘图布局，返回一个self.axes来管理绘图布局中的内容。坐标轴，标题，标签，图形样式（饼图，柱状图，折线图等）等等的设置都通过self.axes的成员函数来设置完成。刚开始的使用还是比较云里雾里的，现在就差不多了。我对官方例程做了些修改，具体的代码，可以到我的GitHub仓储上查看[Qt-learn-pyqt5-matplotlib](https://github.com/zhangzhen2618/Qt-learn/tree/master/pyqt5/matplotlib-qt)里面也有一些其他的例子，应该还会不定期的更新，有兴趣也可以看看。下面只需要对这几个类进行实例话，开启qt的事件循环就可以看到界面了，具体的可以看我的github代码，这里就不多说了。

## 写在最后

因为自身能力有限，也不是科班出身，都是自学的，目前还是一名学生，所以有未尽之处还请指正，不喜勿喷。谢谢。