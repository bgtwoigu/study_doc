# LNMP #
##

### 一、LNMP环境搭建 ###
1. 一键安装包网站：http://lnmp.org/   
2. 根据安装指导执行  
    `wget -c http://soft.vpser.net/lnmp/lnmp1.2-full.tar.gz && tar zxf lnmp1.2-full.tar.gz && cd lnmp1.2-full && ./install.sh lnmp`  
    一路使用默认值回车，指导安装完毕。（请记住mysql的root密码，后面很多地方都需要用到）

### 二、Pureftp搭建 ###
1. 参考网页：`http://lnmp.org/faq/ftpserver.html`  
    注意：管理员密码一定要记住，后面修改也比较麻烦
2. 测试是否搭建成功：http://ip/ftp/进入ftp页面  
    注意：这个页面新建账号的密码总是会有问题，导致503授权失败。需要使用lnmp ftp命令增加账号，然后登陆这个网站调整上传下载速度。
3. 新建账号  
    命令`lnmp ftp add`，如：  
<pre>
root@server-145:/home/wwwroot/default/simcard# lnmp ftp add
+-------------------------------------------+
|    Manager for LNMP, Written by Licess    |
+-------------------------------------------+
|              http://lnmp.org              |
+-------------------------------------------+
verify your current MySQL root password: ****
MySQL root password correct.
Enter ftp account name: simcard
Enter password for ftp account simcard: simcard
Enter directory for ftp account simcard: /home/wwwroot/default/simcard
</pre>

   请记住账号密码，记住输入：directory，这个是对应该账号上传目录   
4. ftp登陆日志路径：`/var/log/syslog`，如果登陆有问题，可以查看该处日志看具体原因

### 常见问题 ###
1. 安装失败
    根据安装log到lnmp论坛中查看失败原因，正常情况下不会有任何问题。我遇到了几次Ubuntu系统创建文件失败`File exists`，因为安装包都是sh脚本，可以根据错误找到具体是哪个模块编译出错。  
2. libmcrypt-2.5.8编译出错  
    `checking if g++ supports -c -o file.o... mkdir: cannot create directory `conftest': File exists`  
    参考libmcrypt-2.5.8_configure.patch、libmcrypt-2.5.8_libltdl_configure.patch  
    手动打入patch并编译完后，记得注释掉include/init.sh中对应模块注释掉，如：  
<pre>
Install_Libmcrypt()
{
    Echo_Blue "[+] Installing ${LibMcrypt_Ver}"
    #Tar_Cd ${LibMcrypt_Ver}.tar.gz ${LibMcrypt_Ver}
    #./configure
    #make && make install
    #/sbin/ldconfig
    #cd libltdl/
    #./configure --enable-ltdl-install
    #make && make install
    #ln -s /usr/local/lib/libmcrypt.la /usr/lib/libmcrypt.la
    #ln -s /usr/local/lib/libmcrypt.so /usr/lib/libmcrypt.so
    #ln -s /usr/local/lib/libmcrypt.so.4 /usr/lib/libmcrypt.so.4
    #ln -s /usr/local/lib/libmcrypt.so.4.4.8 /usr/lib/libmcrypt.so.4.4.8
    #ldconfig
}
</pre>
3. Pureftp管理界面502或超时无法登陆  
    在/home/wwwroot/default/.user.ini里设置，将open_basedir注释掉，**过几分钟后生效**  
    修改前需要执行：chattr -i /home/wwwroot/default/.user.ini  
    修改完成后再执行：chattr +i /home/wwwroot/default/.user.ini  
4. Pureftp账号建立后，使用ftp工具连接，提示503授权失败  
    不要通过http://ip/ftp新建账号，使用命令`lnmp ftp add`新建账号可以解决这个问题
