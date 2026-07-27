# jiduoduo (Chinese name: 鸡多多)

❗️WAR❗️NING❗.......️ A massive wave of test scripts has been spotted ahead........ and is heading straight for jiduoduo!!!!!!!!

## A Wordy Introduction:

(A gift for all the MJJs in the universe)

An open-source Web-based VPS automated testing platform supporting IPv4 + IPv6, private deployment, and fully automated background operation. Test anytime, anywhere!

Wuhu~ Currently supporting 20+ top-tier test scripts! Including but not limited to: YABS GB5, IP Unlock tests, Three-network Return Path, Fusion Monster...

`Everyone is welcome to participate in the jiduoduo open-source project~ XD`

## Fragments of jiduoduo:

### Homepage Screenshot

![首页截图](https://img.erpweb.eu.org/imgs/2024/07/fd9dc374b31ac895.png)

### Currently supporting 20+ common tests (continuously increasing...)

![新建测试](https://img.erpweb.eu.org/imgs/2024/07/fcd552821dffdeec.png)

### GB5 Test Screenshot

![GB5测试](https://img.erpweb.eu.org/imgs/2024/07/ec18842560908b26.png)

### Fusion Monster Test Screenshot

![融合怪测试截图](https://img.erpweb.eu.org/imgs/2024/07/f49f44c886971261.png)

### IP Quality Health Report Screenshot

![IP质量体检报告](https://img.erpweb.eu.org/imgs/2024/07/69b49875c81716e4.png)

## Disclaimer

This project and related code files are for learning purposes only. They must not be used for commercial purposes or illegal activities; otherwise, the user assumes all responsibility.

## How to get involved in the jiduoduo project?

Code contributions, punctuation corrections, typo fixes, copy optimization, variable renaming, bug reports, improvement suggestions, complaints, and critiques are all welcome...    
`(OMG! I found a typo in the README.md file, submitting it right now!)`

## How to fix typos? How to contribute code? How to make jiduoduo more robust?

Simply initiate a `Pull request` to the `develop` branch. It will be merged after the review is passed. Once merged, the submitted content will immediately appear in the develop branch.  
`(Yay!)`

Before submitting, please review your changes thoroughly to avoid wasting everyone's time.  
`(Alright!)`

## How to deploy locally?

First, ensure that `docker` and `docker-compose` are installed on your machine.

If you don't know how to install them, here is a super useful method!

    First, install 1panel (Go to the link below, find the command line for your current system, and follow the prompts step by step...)
    https://1panel.cn/docs/installation/online_installation/

    After installing 1panel, enter the following command to uninstall 1panel in one click (the 1panel team will be heartbroken)
    1pctl uninstall
    
    This way, you get the latest versions of docker and docker-compose for free! Simple, right!

Pro tip: You can enter the following two commands in the terminal to confirm if docker and docker-compose were installed successfully.

If installed, version information will be output; otherwise, it will report an error.  
`(Ehehe, learned another trick~`

    docker -v

    docker-compose -v

After confirming docker and docker-compose are installed, you can start the service locally.  
(It also works on a VPS, but there is no documentation for that yet...)

Finally, follow these steps and execute the commands in order:

### 1. Pull Docker images

    docker-compose pull 

### 2. Build Docker images (mainly jiduoduo-webserver and jiduoduo-worker)

    docker-compose build

### 3. Kill old Docker containers and start new ones

    docker-compose down && docker-compose up -d

## How to access via browser after local deployment?

### jiduoduo Web Page:

Default address: http://localhost:15000/    
Default Account & Password: Please register manually

### jiduoduo Redis Management Page (Requires starting with docker-compose.all.yaml):

Default address: http://localhost:15011/  
Default Username: jiduoduo  
Default Password: jiduoduo

### jiduoduo SQLite3 Management Page (Requires starting with docker-compose.all.yaml):

Default address: http://localhost:15012/  
Default System: SQLite 3  
Default Username: jiduoduo  
Default Password: jiduoduo  
Default Database: /jiduoduo_data/db.sqlite3

### ⚠️ Note: Please do not modify data randomly without understanding the database structure to avoid making the service unavailable or causing permanent data loss.

## FAQ

### How to backup the database and configuration files?

`Please see the ⚠️ Note below`

### ⚠️ Note: A `jiduoduo_data` folder will be created in the current directory after startup, containing:

1. `db.sqlite3` file (jiduoduo's sqlite3 database, copy it out for backup if needed)
2. `.env` file (Web-related configurations, allowing custom SQL database and Redis configurations. Refer to the `.env.example` file for modifications)
3. Other files

### How to start a specific Docker container individually?

    # Execute the following commands in the terminal:

    # Start webserver individually
    docker-compose down webserver && docker-compose up webserver -d
    
    # Start webserver and worker
    docker-compose down webserver worker && docker-compose up webserver worker -d

    # Start redis and redis-commander (Requires starting with docker-compose.all.yaml)
    docker-compose down redis redis-commander && docker-compose up redis redis-commander -d

### How to see which containers are currently running in Docker?

    # Execute the following command:

    docker ps

### How to see which processes are running inside a Docker container?

    # Execute the following commands:

    # Check processes in webserver container
    docker top jiduoduo-webserver

    # Check processes in worker container
    docker top jiduoduo-worker
    
    # Check processes in redis container
    docker top jiduoduo-redis

    # Check processes in redis-commander container (Requires starting with docker-compose.all.yaml)
    docker top jiduoduo-redis-commander

    # Check processes in adminer container (Requires starting with docker-compose.all.yaml)
    docker top jiduoduo-adminer

### How to enter a running Docker container?

    # Execute the following commands:

    # Enter webserver container
    docker exec -it jiduoduo-webserver bash

    # Enter worker container
    docker exec -it jiduoduo-worker bash

    # Enter redis container
    docker exec -it jiduoduo-redis bash

    # Enter redis-commander container (Note: use sh instead of bash) (Requires starting with docker-compose.all.yaml)
    docker exec -it jiduoduo-redis-commander sh

    # Enter adminer container (Requires starting with docker-compose.all.yaml)
    docker exec -it jiduoduo-adminer bash

## Preparations before coding — Introductory materials

### How to get started with Python3?

    Liao Xuefeng: Python Tutorial
    https://www.liaoxuefeng.com/wiki/1016959663602400

    Python3 Official Documentation
    https://docs.python.org/3/tutorial/index.html

### How to get started with Flask? (Flask is an open-source Python3 Web framework)

    Li Hui: Flask Introductory Tutorial
    https://tutorial.helloflask.com/

### How to get started with Docker?

    Ruan Yifeng: Docker Introductory Tutorial
    https://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html

## How to develop and debug locally?

### 1. Ensure Python3.11 is installed on your machine. To verify, enter the following command; if it returns something like "Python 3.11.9", it is successful:

    python3 -V 

### [Optional] Install a virtual environment and a code editor (Notepad, VS Code, or PyCharm are all fine)

Huh? You still don't know how? Go ask the magical ChatGPT~

### 2. Use the following command to install dependency packages:

    pip3 install -e .

### Wuhu~ Time to start hacking the code!

`(Damn! Why does time fly as fast as money does?`
