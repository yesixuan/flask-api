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