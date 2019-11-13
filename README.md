
这是用于测试gitbook生成的网页推送到github pages的case
https://lemonchann.github.io/Qt-learn/


[参考](http://www.chengweiyang.cn/gitbook/github-pages/README.html)
构建书籍
首先，使用 gitbook build 将书籍内容输出到默认目录，也就是当前目录下的 _book 目录。

$ gitbook build
Starting build ...
Successfully built!

$ ls _book
GLOSSARY.html       chapter1            chapter2            gitbook             glossary_index.json index.html          search_index.json
创建 gh-pages 分支
执行如下命令来创建分支，并且删除不需要的文件：

$ git checkout --orphan gh-pages
$ git rm --cached -r .
$ git clean -df
$ rm -rf *~
现在，目录下应该只剩下 _book 目录了，首先，忽略一些文件：

$ echo "*~" > .gitignore
$ echo "_book" >> .gitignore
$ git add .gitignore
$ git commit -m "Ignore some files"
然后，加入 _book 下的内容到分支中：

$ cp -r _book/* .
$ git add .
$ git commit -m "Publish book"
上传书籍内容到 GitHub
现在，可以将编译好的书籍内容上传到 GitHub 中 test 项目的 gh-pages 分支了，虽然这里还没有创建分支，上传和创建会一步完成！

$ git push -u origin gh-pages
Counting objects: 49, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (45/45), done.
Writing objects: 100% (49/49), 1.34 MiB | 131.00 KiB/s, done.
Total 49 (delta 5), reused 0 (delta 0)
To https://github.com/chengweiv5/test.git
 * [new branch]      gh-pages -> gh-pages
Branch gh-pages set up to track remote branch gh-pages from github.
现在，书籍的内容已经上传到 GitHub 上，所以通过访问 chengweiv5.github.io/test 就可以阅读 test 这本书了！

