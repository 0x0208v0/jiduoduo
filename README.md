# jiduoduo

项目中文名：鸡多多

## 如何在本机部署？

确保本机已经安装 docker 和 docker-compose。
可用下面两条命令行，确认是否已经安装。
如果已安装，则会输出版本信息；否则会报错。

    docker -v

    docker-compose -v

确认已经安装了 docker 和 docker-compose 后，可在本机启动服务。
按照下面的步骤，依次执行命令：

### 1. 拉镜像

    docker-compose pull 

### 2. 构建镜像（主要是 jiduoduo-webserver和 jiduoduo-worker）

    docker-compose build

### 3. 销毁旧镜像，启动新镜像

    ocker-compose down && docker-compose up -d

### ⚠️注意：启动后会在当前目录新建 jiduoduo_data文件夹，内容如下：

1. db.sqlite3 文件（jiduoduo的数据库，需要的话可以定时备份）
2. .env 文件（Web相关的配置，能够自定义配置 SQL数据库 和 Redis。可参照.env.example文件修改）
3. 其他文件

## 本机部署后，如何浏览器访问？

### jiduoduo Web页面：

默认地址：http://localhost:15000/    
默认账户 & 密码：需手动注册

### jiduoduo Redis管理页面：

默认地址：http://localhost:15011/  
默认账户：jiduoduo  
默认密码：jiduoduo

### jiduoduo SQLite3管理页面：

默认地址：http://localhost:15012/  
默认System: SQLite 3  
默认Username: jiduoduo  
默认Password: jiduoduo  
默认Database: /jiduoduo_data/db.sqlite3

### ⚠️注意：在不了解数据库结构的情况下，请不要随意修改数据，以免造成服务不可用，或数据丢失

## 如何在VPS上部署？

待补充

## 如何本地开发和调试？

### 1. 确保本机安装了Python3.11，如何确定已经安装？输入下面命令，返回类似 “Python 3.11.9” 则表示成功

    python3 -V 

### 2. （可选）生成虚拟环境

请自行到互联网搜索教程学习并实践

### 3. 使用下面命令安装依赖包

    pip install -e .

### 然后就可以开始魔改代码了！

