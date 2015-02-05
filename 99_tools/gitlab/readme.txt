一、安装
1. 根据官网步骤下载并安装
    链接：https://about.gitlab.com/downloads/
    所有配置文件地址：/etc/gitlab/gitlab.rb

2. 安装完毕后，配置外部访问地址
    2.1：配置ip地址
    sudo vi /etc/gitlab/gitlab.rb
    修改url为:ip+端口，如：
    external_url 'http://10.1.1.131:1234'    
    2.2：测试
    浏览器访问：http://10.1.1.131:1234，出现gitlab页面
    输入如下默认账号：
    Username: root 
    Password: 5iveL!fe

3. 配置邮箱
    3.1：修改邮箱信息
    sudo vi /etc/gitlab/gitlab.rb
    添加如下配置，并注释掉端口
    gitlab_rails['smtp_enable'] = true
    gitlab_rails['smtp_address'] = "smtp.263.net"
    #gitlab_rails['smtp_port'] = 456
    gitlab_rails['smtp_user_name'] = "xumingtao@hipad.com"
    gitlab_rails['smtp_password'] = "密码"
    gitlab_rails['smtp_domain'] = "263.net"
    gitlab_rails['smtp_authentication'] = "login"
    gitlab_rails['smtp_enable_starttls_auto'] = true
    gitlab_rails['smtp_tls'] = false
    gitlab_rails['smtp_openssl_verify_mode'] = false
    修改如下两项值为邮箱
    gitlab_rails['gitlab_email_from'] = 'xumingtao@hipad.com'
    user['git_user_email'] = "xumingtao@hipad.com"
    3.2：测试
    root账号登陆gitlab页面后，新建账号，默认会给新账号发一份邮件。

4. 修改配置文件后，需要重新配置
    sudo gitlab-ctl reconfigure
二、常见问题
