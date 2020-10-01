from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from server import app, db

# database migration tool for sqlachemy
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# run the server
if __name__ == '__main__':
    manager.run()

