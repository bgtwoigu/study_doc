# SVN常用命令操作 #
##

### 1. 创建仓库 ###
   `sudo svnadmin create /home/svn/test`  

### 2. 修改权限 ###
   `sudo chown -R www-data:www-data /home/svn/test`  

### 3. 添加账号密码 ###
   `-c`表示新建passwd文档  
   `sudo htpasswd -c /home/svn/test/conf/passwd username`  
   `sudo htpasswd /home/svn/test/confpasswd username2`

### 4. 修改apache配置 ###
   `sudo gedit /etc/apache2/mods-available/dav_svn.conf`  
   把新建的仓库，在文件`dav_svn.conf`中增加如下内容，确保可以访问
<pre>
<location test>
DAV svn
SVNPath /home/svn/test
AuthType Basic
AuthName "test project subversion repository"
AuthUserFile /home/svn/test/conf/passwd
 
Require valid-user
</location>
</pre>

### 5. 重启Apache2服务 ###
   `sudo /etc/init.d/apache2 restart`

### 6. 代码导入仓库 ###
<pre>
svn import <b>android/</b> http://10.1.1.144/android/qualcomm/msm8939/vendor/MSM8939.LA2.1_M8939AAAAANLYD2150.1/<b>android</b> -m "init import M8939AAAAANLYD2150.1,android" --no-ignore

svn import <b>modem/</b> http://10.1.1.144/android/qualcomm/msm8939/vendor/MSM8939.LA2.1_M8939AAAAANLYD2150.1/<b>modem</b> -m "init import M8939AAAAANLYD2150.1,modem" --no-ignore
</pre>


 