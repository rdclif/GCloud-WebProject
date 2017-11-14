
from main import db
from main import Visit
from main import sqlalchemy


if __name__ == '__main__':
    print('Creating all database tables...')
    x = db.create_all()
    print('Done!')