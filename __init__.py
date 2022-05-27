#1、包含应用工厂，二是告诉python flask 文件夹应当视为一个包
import os.path

from  flask import Flask

def create_app(test_config=None):
    #创建和配置APP
    app = Flask(__name__,instance_relative_config=True) #创建Flask实例。__name__是当前python的模块名称。应用需要知道在哪里设置路径。后面是告诉配置应用文件是相对路径，用于存放本地数据
    app.config.from_mapping(
        SECRET_KEY='dev',   #SECRET_KEY是用于保证数据安全的。开发过程中为了方便设置为dev
        DATABASE='flaskr.sqlite'
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)  #...pyfile，使用config.py来重载默认配置，如果config存在，当正式部署,用于设置正式的SECRET_KEY
    else:
        app.config.from_mapping(test_config)  #替代实例配置，实现测试和开发分离
    try:
        os.makedirs(app.instance_path) #确保path存在。sqllite文件保存的位置
    except OSError:
        pass

    # 引入db模块
    import db
    db.init_app(app)

    # 引入认证蓝图模块
    import auth
    app.register_blueprint(auth.bp)

    # 引入博客蓝图模块
    import blog
    app.register_blueprint(blog.bp)
    # 与验证蓝图不同，博客蓝图没有 url_prefix 。因此 index 视图会用于 / ，create 会用于 /create ，以
    # 此类推。博客是 Flaskr 的主要功能，因此把博客索引作为主索引是合理的。
    app.add_url_rule('/', endpoint='index')

    @app.route('/hello')   #创建一个简单的路由，创建了url/hello和一个函数之间的关联
    def hello():
        return 'Hello World!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()