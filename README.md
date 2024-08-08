# jiduoduo（中文名：鸡多多）

❗️警❗️告❗.......️前方发现一大波测试脚本........正在向鸡多多袭来！！！！！！！！！

## 废话连篇的介绍：

（送给全宇宙 MJJ 的礼物）

基于 Web 的开源 VPS 自动化测试平台，支持IPv4 + IPv6，私有化部署，全自动后台运行，随时随地测！

芜湖～ 目前已支持 20+ 种顶级测试脚本！包括但不限于：YABS GB5、IP解锁测试、三网回程、融合怪...

`也欢迎各位小伙伴参与 jiduoduo 开源项目中来～ XD `

## 下面是 jiduoduo 的部分碎片：

### 首页截图

![首页截图](https://img.erpweb.eu.org/imgs/2024/07/fd9dc374b31ac895.png)

### 目前支持 20+ 种常见测试（正在陆续增加中...）

![新建测试](https://img.erpweb.eu.org/imgs/2024/07/fcd552821dffdeec.png)

### GB5测试截图

![GB5测试](https://img.erpweb.eu.org/imgs/2024/07/ec18842560908b26.png)

### 融合怪测试截图

![融合怪测试截图](https://img.erpweb.eu.org/imgs/2024/07/f49f44c886971261.png)

### IP质量体检报告截图

![IP质量体检报告](https://img.erpweb.eu.org/imgs/2024/07/69b49875c81716e4.png)

## 免责声明

本项目及相关代码文件，仅限于学习用途，不可用于商业，不可用于违法犯罪，否则后果自负。

## 如何参与到 jiduoduo 项目中？

欢迎贡献代码，欢迎标点符号修改，欢迎错别字修改，欢迎文本文案优化，欢迎变量命名修改，欢迎反馈BUG，欢迎提出改进建议，欢迎吐槽，欢迎拍砖...    
`（超！发现README.md文件存在错别字，窝立刻提交！）`

## 如何帮助修改错字？如何贡献代码？如何让 jiduoduo 变得更加健壮？

向 `develop` 分支发起 `Pull requests` 就可以啦。Review 通过后会进行合并。合并后，提交的内容立刻就会出现在 develop 分支了。  
`（好耶！）`

提交前，请先让自己疯狂Review一下正在提交的内容，以免造成大家时间流失。  
`（好哦！）`

## 如何在本机部署？

首先，确保本机已经安装 docker 和 docker-compose 软件

如果不会安装，这里推荐推荐一个炒鸡好用的办法！

    先安装 1panel（到下面的链接，找到你当前系统对应的命令行，跟着提示下一步下一步下一步...）
    https://1panel.cn/docs/installation/online_installation/

    安装好 1panel后，输入下面的命令，一键卸载 1panel（1panel团队当场拍断大腿）
    1pctl uninstall
    
    这样就免费得到最新版本的docker 和 docker-compose了！是不是很简单！

小技巧：可在命令行输入下面的两条命令，来确认 docker 和 docker-compose 是否已经安装成功）

如果已安装，则会输出版本信息；否则会报错  
`（诶嘿嘿，又学到一招～`

    docker -v

    docker-compose -v

确认已安装过 docker 和 docker-compose 后，可在本机启动服务  
（在VPS上也行，只不过目前没文档。。。）

最后，按照下面的步骤，依次执行命令：

### 1. 拉 Docker 镜像

    docker-compose pull 

### 2. 构建 Docker 镜像（主要是 jiduoduo-webserver 和 jiduoduo-worker）

    docker-compose build

### 3. 干掉旧的 Docker 容器，启动新的 Docker 容器

    docker-compose down && docker-compose up -d

## 本机部署后，如何浏览器访问？

### jiduoduo Web 页面：

默认地址：http://localhost:15000/    
默认账户 & 密码：请手动注册

### jiduoduo Redis 管理页面（需要用docker-compose.all.yaml启动才行）：

默认地址：http://localhost:15011/  
默认Username：jiduoduo  
默认Password：jiduoduo

### jiduoduo SQLite3 管理页面（需要用docker-compose.all.yaml启动才行）：

默认地址：http://localhost:15012/  
默认System：SQLite 3  
默认Username：jiduoduo  
默认Password：jiduoduo  
默认Database：/jiduoduo_data/db.sqlite3

### ⚠️注意：不了解数据库结构的情况下，请勿随意修改数据，以免导致服务不可用，或数据永久丢失

## FAQ

### 如何备份 数据库 和 配置文件？

`请看下面的 ⚠️注意`

### ⚠️注意：启动后会在当前目录新建 jiduoduo_data 文件夹，内容如下：

1. db.sqlite3 文件（jiduoduo的sqlite3数据库，有需要可以拷贝出去备份）
2. .env 文件（Web相关的配置，能够自定义配置 SQL数据库 和 Redis。可参照.env.example文件修改）
3. 其他文件

### 如何单独启动某个 Docker 容器？

    # 命令行执行下面的命令：

    # 单独启动 webserver
    docker-compose down webserver && docker-compose up webserver -d
    
    # 启动 webserver 和 worker
    docker-compose down webserver worker && docker-compose up webserver worker -d

    # 启动 redis 和 redis-commander（需要用docker-compose.all.yaml启动才行）
    docker-compose down redis redis-commander && docker-compose up redis redis-commander -d

### 如何查看当前 Docker 运行了哪些容器？

    # 命令行执行下面的命令：

    docker ps

### 如何查看 Docker 容器里，正在运行的进程有哪些？

    # 命令行执行下面的命令：

    # 查看 webserver 容器里运行了哪些进程
    docker top jiduoduo-webserver

    # 查看 worker 容器里运行了哪些进程
    docker top jiduoduo-worker
    
    # 查看 redis 容器里运行了哪些进程
    docker top jiduoduo-redis

    # 查看 redis-commander 容器里运行了哪些进程（需要用docker-compose.all.yaml启动才行）
    docker top jiduoduo-redis-commander

    # 查看 adminer 容器里运行了哪些进程（需要用docker-compose.all.yaml启动才行）
    docker top jiduoduo-adminer

### 如何进入到某个正在运行的 Docker 容器里？

    # 命令行执行下面的命令：

    # 进入 webserver 容器
    docker exec -it jiduoduo-webserver bash

    # 进入 worker 容器
    docker exec -it jiduoduo-worker bash

    # 进入 redis 容器
    docker exec -it jiduoduo-redis bash

    # 进入 redis-commander 容器（注意这里不是 bash 而是 sh）（需要用docker-compose.all.yaml启动才行）
    docker exec -it jiduoduo-redis-commander sh

    # 进入 adminer 容器（需要用docker-compose.all.yaml启动才行）
    docker exec -it jiduoduo-adminer bash

## 写代码前的准备——入门资料

### 如何 Python3 入门？

    廖雪峰：Python 教程
    https://www.liaoxuefeng.com/wiki/1016959663602400

    Python3 官方文档
    https://docs.python.org/zh-cn/3/tutorial/index.html

### 如何 Flask 入门？（Flask 是开源的 Python3 Web 框架）

    李辉：Flask 入门教程
    https://tutorial.helloflask.com/

### 如何 Docker 入门？

    阮一峰：Docker 入门教程
    https://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html

## 如何本地开发和调试？

### 1. 确保本机安装了Python3.11，如何确定已经安装？输入下面命令，返回类似 “Python 3.11.9” 则表示成功

    python3 -V 

### 【可选】安装虚拟环境，安装代码编辑工具（notepad 或者 vscode 或者 pycharm 都可以）

啊？这个还不太会？快去问问神奇的ChatGPT叭～

### 2. 使用下面命令安装依赖包

    pip3 install -e .

### 芜湖～ 开始魔改代码吧！

`（淦！时间怎么过得就像花钱一样快啊？`
 

