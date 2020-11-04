from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from chengse_project import create_app, db

app = create_app("product")
# app.host = "0.0.0.0"
manager = Manager(app)

# manager = Manager(app)

# 创建数据库迁移工具对象
Migrate(app=app, db=db)

# 向manager对象中添加数据库操作命令
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    # print(app.url_map)
    manager.run()

