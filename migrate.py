from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from globals import app, db

migrate_tool = Migrate(app, db)
manager = Manager(app)

if __name__ == "__main__":
    manager.add_command('db', MigrateCommand)
    manager.run()
