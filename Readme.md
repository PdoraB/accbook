# Account

使用flask 结合peewee 调度数据库 写的一个记账程序

```shell
conda create -p <dir of path>/account python=3
conda activate env_path
```
```shell
pip install -r requirements.txt
```

首页统计
![img_1.png](img_1.png)
输入页面
![img.png](img.png)
数据库查询页面
![img_2.png](img_2.png)

#系统参数配置
```shell
系统参数配置
编辑config.py， 修改SECRET_KEY及MySQL数据库相关参数
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
DB_HOST = '127.0.0.1'
DB_USER = 'foobar'
DB_PASSWD = 'foobar'
DB_DATABASE = 'foobar'

```
```shell
编辑log-app.conf，修改日志路径
args=('/path/to/log/flask-rest-sample.log','a','utf8')
```

