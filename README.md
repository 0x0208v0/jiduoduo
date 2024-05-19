# jiduoduo（中文名：鸡多多的）

一句话项目简介：基于 Web 的 开源的 VPS 自动测试平台

欢迎全宇宙的小伙伴们参与贡献该开源项目 :)  
（超！Review 很严格的

## 免责声明

本项目及相关代码文件，仅限于学习用途，不可用于商业，不可用于违法犯罪，否则后果自负。

## 如何参与到jiduoduo项目中？

欢迎任何PR，欢迎贡献代码，欢迎错字修改，欢迎文案修改，欢迎变量命名修改，欢迎反馈BUG，欢迎提出改进建议，欢迎吐槽，欢迎拍砖...    
（妈耶，发现README.md文件存在错别字，窝立刻提交！）

## 如何贡献代码？如何帮助修改错字？

向 develo p分支提交 PR 即可，Review 通过立刻合并（好耶！）  
（提交前，请先自己疯狂Review一下自己提交的内容（好的！）

## 如何在本机部署？

首先，要确保本机已经安装 docker 和 docker-compose 软件

小技巧：可在命令行输入下面的两条命令，来确认是否已经安装过）

如果已安装，则会输出版本信息；否则会报错`（靠！又学到一招`

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

### 【其他】 如何启动单个服务？（以webserver为例）

    docker-compose down webserver && docker-compose up webserver -d

### 【其他】 如何备份数据库和配置文件？

`请看下面的 ⚠️注意`

### ⚠️注意：启动后会在当前目录新建 jiduoduo_data 文件夹，内容如下：

1. db.sqlite3 文件（jiduoduo的sqlite3数据库，有需要可以拷贝出去备份）
2. .env 文件（Web相关的配置，能够自定义配置 SQL数据库 和 Redis。可参照.env.example文件修改）
3. 其他文件

## 本机部署后，如何浏览器访问？

### jiduoduo Web页面：

默认地址：http://localhost:15000/    
默认账户 & 密码：请手动注册

### jiduoduo Redis管理页面：

默认地址：http://localhost:15011/  
默认Username：jiduoduo  
默认Password：jiduoduo

### jiduoduo SQLite3管理页面：

默认地址：http://localhost:15012/  
默认System：SQLite 3  
默认Username：jiduoduo  
默认Password：jiduoduo  
默认Database：/jiduoduo_data/db.sqlite3

### ⚠️注意：在不了解数据库结构的情况下，请不要随意修改数据，以免造成服务不可用，或数据丢失

## 如何在VPS上部署？

待补充

## 如何本地开发和调试？

### 1. 确保本机安装了Python3.11，如何确定已经安装？输入下面命令，返回类似 “Python 3.11.9” 则表示成功

    python3 -V 

### 【可选】生成虚拟环境

请自行到互联网搜索教程学习并实践

### 2. 使用下面命令安装依赖包

    pip install -e .

### 然后就可以开始魔改代码了！（啊？我的时间流失速度怎么和花钱一样快？
 

