## db
1. sqlite3介绍
http://192.168.0.170:4999/web/#/10?page_id=924

2. 连接sqlite
```
touch flaskr.sqlite
sqlite3 flaskr.sqlite
```

3. 初始化db
直接在sqlite3命令行中执行 schema.sql 

## 运行
直接运行 __init__.py

访问
测试
http://127.0.0.1:5000/hello
注册
http://127.0.0.1:5000/auth/register
登录
http://127.0.0.1:5000/auth/login