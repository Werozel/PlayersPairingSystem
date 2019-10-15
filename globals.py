import sqlalchemy as db
from config import db_user, db_psw


engine = db.create_engine('postgresql://{0}:{1}@localhost:5432/sport'.format(db_user, db_psw))
print(engine.connect())
