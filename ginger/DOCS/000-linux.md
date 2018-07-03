### Linux 常用目录

1. dev: 抽象硬件（网卡、硬盘）  
2. bin: 二进制文件（可执行命令）
3. usr: 安装程序（软件默认目录）
4. var: 经常变化的文件
5. mnt: 文件挂载（U盘、光驱）
6. home: 普通用户目录
7. root: 超级管理员目录
8. etc: 配置文件目录

### 目录与文件管理

1. echo Thanks > hello.txt （将 Thanks 写入 hello.txt）
2. cat hello.txt （查看）
3. 命令行中的 `~` 代表的是当前登录用户的目录
4. `/` 根目录
5. vi 退出编辑：esc  保存 :w  退出 :q
6. cp hello.txt new.txt 复制文件 （参数 `-r` 可以复制文件夹，表示递归复制目录内容）
7. rm -rf 目录 删除文件夹
8. mv -f dir1 /dir2 移动 dir1 目录到 home/dir2 下，强制覆盖已存在的目录或文件
9. ls -l 查看文件或文件夹的属性信息
10. chmod 761 文件或文件夹 （4 2 1 读 写 执行）

### 防火墙

查看、启动、关闭、重启
firewall-cmd --state （如果结果是 running 则说明防火墙正在运行） 
service firewall start/stop/restart  

端口管理  
firewall-cmd --permanent --add-port=8080-8085/tcp（也可以只开放一个端口）  
firewall-cmd --reload （开放防火墙之后要 reload 才能生效）  
firewall-cmd --permanent --remove-port=8080-8085/tcp  

查看开启的端口和服务  
firewall-cmd --permanent --list-ports  
firewall-cmd --permanent --list-services（哪些程序正在使用互联网）  

### docker 虚拟机

安装 docker 虚拟机  
yum -y update（首先更新 yum）  
yum install -y docker （-y 代表选择程序安装中的 yes 选项）  

启动、关闭、重启  
service docker start/stop/restart  

启动 docker 时遇到问题？  
在 `/etc/docker/daemon.json` 下（没有就创建）写入 `{ "storage-driver": "devicemapper" }`

### docker 相关

`curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://ef017c13.m.daocloud.io
`（配置镜像加速）
docker search java  
docker pull java

镜像操作  
docker save java > /home/java.tar.gz（将 java 镜像变成压缩包存储）  
docker load < /home/java.tar.gz（从压缩文件中导入镜像）  
docker iamges  
docker rmi java  

启动容器  
docker run -it --name myjava java bash（-it 是进入容器的交互命令， --name 是给容器命名）  
docker run -it --name myjava  -p 9000:8080 -p 9001:8085 java bash（将容器的8080映射到宿主机的9000...）  
docker run -it --name myjava -v /home/project:/soft --privileged java bash（将容器的 /soft 目录映射到宿主机的 /home/project）  
exit（退出容器命令行，并且停止运行容器）  

管理容器状态  
docker pause/unpause myjava  
docker stop myjava  
docker start -i myjava（在 exit 之后需要这般启动容器，顺便进入容器命令行）  
docker rm myjava（删除容器，必须在彻底停止容器之后） 

### mysql 集群

安装 PXC 镜像  
docker pull percona/percona-xtradb-cluster  
docker load < /home/soft/pxc.tar.gz（前提是本地有）   
docker tag percona/percona-xtradb-cluster pxc（复制镜像并给它取名，原来的镜像可以删除）  

创建 docker 内部网络  
docker network create net1  
docker network create --subnet=172.18.0.0/24 net1（指定IP地址）  
docker network inspect net1  
docker network rm net1  

创建 docker 卷（业务数据要存储在宿主机目录上，这个卷在宿主机和容器中都能看到）  
docker volume create --name v1  
docker inspect v1（查看这个卷在宿主机的那个目录，将来要将容器映射到这个目录）  
docker volume rm v1  

创建 PXC 容器  
docker run -d -p 3306:3306 -v v1:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 --privileged --name-node1 --net=net1 --ip 172.18.0.2 pxc  
（后台创建并启动容器、将v1数据卷映射到容器中mysql的安装目录、给这个mysql实例设置密码、指定pxc集群的名字、数据库节点之间同步用到的密码、给它最高权限、给容器取名、这个容器分配的网段）  

创建集群  
docker volume create --name v1 ~ v5  

docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 -v v1:/var/lib/mysql --privileged --name=node1 --net=net1 --ip 172.18.0.2 pxc  
docker run -d -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 -e CLUSTER_JOIN=node1 -v v2:/var/lib/mysql --privileged --name=node2 --net=net1 --ip 172.18.0.3 pxc  
docker run -d -p 3308:3306 -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 -e CLUSTER_JOIN=node1 -v v3:/var/lib/mysql --privileged --name=node3 --net=net1 --ip 172.18.0.4 pxc  
docker run -d -p 3309:3306 -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 -e CLUSTER_JOIN=node1 -v v4:/var/lib/mysql --privileged --name=node4 --net=net1 --ip 172.18.0.5 pxc  
docker run -d -p 3310:3306 -e MYSQL_ROOT_PASSWORD=123456 -e CLUSTER_NAME=PXC -e XTRABACKUP_PASSWORD=123456 -e CLUSTER_JOIN=node1 -v v5:/var/lib/mysql --privileged --name=node5 --net=net1 --ip 172.18.0.6 pxc  


  

  
  
