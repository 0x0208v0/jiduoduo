# jiduoduo（中文名：鸡多多）

## 一句话介绍：

基于 Web 的 开源的 VPS 自动测试平台

`欢迎全宇宙的小伙伴们参与贡献 jiduoduo 开源项目 `  
`（此处有眼神暗示全场MJJ）`

## 免责声明

本项目及相关代码文件，仅限于学习用途，不可用于商业，不可用于违法犯罪，否则后果自负。

## 如何参与到 jiduoduo 项目中？

欢迎贡献代码，欢迎标点符号修改，欢迎错别字修改，欢迎文本文案优化，欢迎变量命名修改，欢迎反馈BUG，欢迎提出改进建议，欢迎吐槽，欢迎拍砖...    
`（超！窝发现README.md文件存在错别字，劳资立刻提交！）`

## 如何贡献代码？如何帮助修改错字？

向 `develop` 分支提交 `Pull requests` 即可，Review 通过后，会立刻合并。  
`（好耶！）`

提交前，请先自己疯狂Review一下自己提交的内容。  
`（好的！）`

## 如何在本机部署？

首先，要确保本机已经安装 docker 和 docker-compose 软件

小技巧：可在命令行输入下面的两条命令，来确认是否已经安装过）

如果已安装，则会输出版本信息；否则会报错  
`（诶嘿嘿，又学到一招～`

    docker -v

    docker-compose -v

确认已安装过 docker 和 docker-compose 后，可在本机启动服务  
（在VPS上也行，只不过目前没文档。。。）

最后，按照下面的步骤，依次执行命令：

### 1. 拉镜像

    docker-compose pull 

### 2. 构建镜像（主要是 jiduoduo-webserver和 jiduoduo-worker）

    docker-compose build

### 3. 销毁旧镜像，启动新镜像

    docker-compose down && docker-compose up -d

## 写代码前的准备——入门资料

### 如何 Python3 入门？

    廖雪峰：Python教程
    https://www.liaoxuefeng.com/wiki/1016959663602400

    Python3 官方文档
    https://docs.python.org/zh-cn/3/tutorial/index.html

### 如何 Flask 入门？（Flask 是开源的 Python3 Web 框架）

    李辉：Flask 入门教程
    https://tutorial.helloflask.com/

### 如何 Docker 入门？

    阮一峰：Docker 入门教程
    https://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html

## FAQ

### 如何单独启动某个 Docker 容器？

    # 命令行执行下面的命令：

    # 单独启动 webserver
    docker-compose down webserver && docker-compose up webserver -d
    
    # 启动 webserver 和 worker
    docker-compose down webserver worker && docker-compose up webserver worker -d

    # 启动 redis 和 redis-commander
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

    # 查看 redis-commander 容器里运行了哪些进程
    docker top jiduoduo-redis-commander

    # 查看 adminer 容器里运行了哪些进程
    docker top jiduoduo-adminer

### 如何进入到某个正在运行的 Docker 容器里？

    # 命令行执行下面的命令：

    # 进入 webserver 容器
    docker exec --rm -it jiduoduo-webserver bash

    # 进入 worker 容器
    docker exec --rm -it jiduoduo-worker bash

    # 进入 redis 容器
    docker exec --rm -it jiduoduo-redis bash

    # 进入 redis-commander 容器（注意这里不是 bash 而是 sh）
    docker exec --rm -it jiduoduo-redis-commander sh

    # 进入 adminer 容器
    docker exec --rm -it jiduoduo-adminer sh

### 如何备份数据库和配置文件？

`请看下面的 ⚠️注意`

### ⚠️注意：启动后会在当前目录新建 jiduoduo_data 文件夹，内容如下：

1. db.sqlite3 文件（jiduoduo的sqlite3数据库，有需要可以拷贝出去备份）
2. .env 文件（Web相关的配置，能够自定义配置 SQL数据库 和 Redis。可参照.env.example文件修改）
3. 其他文件

## 本机部署后，如何浏览器访问？

### jiduoduo Web 页面：

默认地址：http://localhost:15000/    
默认账户 & 密码：请手动注册

### jiduoduo Redis 管理页面：

默认地址：http://localhost:15011/  
默认Username：jiduoduo  
默认Password：jiduoduo

### jiduoduo SQLite3 管理页面：

默认地址：http://localhost:15012/  
默认System：SQLite 3  
默认Username：jiduoduo  
默认Password：jiduoduo  
默认Database：/jiduoduo_data/db.sqlite3

### ⚠️注意：在不了解数据库结构的情况下，请不要随意修改数据，以免导致服务不可用，或数据永久丢失

## 如何本地开发和调试？

### 1. 确保本机安装了Python3.11，如何确定已经安装？输入下面命令，返回类似 “Python 3.11.9” 则表示成功

    python3 -V 

### 【可选】安装虚拟环境，安装代码编辑工具（notepad 或者 vscode 或者 pycharm 都可以）

啊？这个还不太会？快去问问神奇的ChatGPT叭～

### 2. 使用下面命令安装依赖包

    pip3 install -e .

### 芜湖～开始魔改代码吧！

`（靠！时间怎么流逝得就像花钱一样快？`
 

