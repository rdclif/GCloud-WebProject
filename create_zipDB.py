#Code Used to Create Zip DB.

from main import db
from main import Zip



if __name__ == '__main__':
    print('Creating all database tables...')


    for obj in r:
        new = Zip(obj['zip'], obj['city'], obj['state'], obj['lat'], obj['lon'])
        db.session.add(new)
    db.session.commit()


    print("all done")