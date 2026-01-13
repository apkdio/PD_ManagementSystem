# PD_ManagementSystem

本项目是一个基于 Python Django 框架的信息管理系统demo，采用 MySQL 作为数据库，采用Django MTV + 前后端分离结合的模式开发。主要功能包括：
- 部门管理（增删改查）
- 部门管理员设置
- 员工管理（增删改查）
- 管理员账户管理（增删改查，利用“安全密码和正常安全密码”验证）
- 客户管理（增删改查，负责人设置）
- 日志系统（记录管理员关键操作）
- 数据校验（电话号码、年龄、薪资等）
- 严格的权限控制
- 登录页图片验证码，一言api使用
## 部署
开发环境依赖:
- Python  3.12.4
- Django 5.0.6
- MySQL 8.0.35 MySQL Community Server - GPL

三方库：
1. APScheduler 3.10.4
2. asgiref     3.8.1
3. mysqlclient 2.2.4
4. pillow      10.4.0
5. pip         24.0
6. pytz        2025.2
7. six         1.17.0
8. sqlparse    0.5.3
9. tzlocal     5.3.1
### 部署步骤
部署步骤：
1. 配置好相应环境。
2. 解压PD管理系统.zip 至任意非中文路径文件夹。
3. 进入MySQL数据库创建相应的用户和数据库。
4. 修改example01/setting.py内的数据库连接为本地MySQL数据库连接以及INITIAL_SETTING初始化条件。
5. 进入example01文件夹，打开终端依次运行`python manage.py makemigrations app03`,`python manage.py migrate app03`进行数据库表迁移。（若执行迁移后数据库没有相对应的表，执行`python manage.py migrate --fake app03 zero`重置数据库迁移，然后再次执行上面两条命令）
6. 执行`python manage.py runserver 127.0.0.1:8000`等待系统启动。
7. 进入浏览器使用`127.0.0.1:8000`访问系统。
8. 因各浏览器请求端口不一致，若出现orbidden (Origin checking failed - http://127.0.0.1:xxxxx does not match any trusted origins.)错误，则需要将对应的ip添加到`setting.py`的`CSRF_TRUSTED_ORIGINS`选项中，
如CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:11434"]，具体到端口


默认账户为`setting.py`文件中INITIAL_SETTING 的username和password，具体如下
INITIAL_SETTING = {
    "user": "admin", # 默认用户名
    "password": "admin", # 默认密码
    "depart_id": 1,  # 默认部门id，必须选择大于0的值
    "depart_name": "管理员", # 默认部门名称
    "safe_password": "123456", # 安全密码，用于添加管理员和修改管理员
    "normal_safe_password": "12345" # 用于重置密码的安全密码
}
如需部署到其他URL运行，则需要`setting.py`中CSRF_TRUSTED_ORIGINS和
ALLOWED_HOSTS 存在相应IP或URL
