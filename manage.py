import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app import models

app = create_app(os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
	return dict(app=app, db=db, User=models.User, Events=models.Events)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()