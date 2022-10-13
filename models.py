from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import * 
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.
class User(UserMixin, Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = generate_password_hash(password)

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)


class PTOs(Base):
    __tablename__ = 'PTOs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    type = db.Column(db.String(120))
    startday = db.Column(db.Date)
    endday = db.Column(db.Date)
    days = db.Column(db.Integer)

    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type

# Create tables.
Base.metadata.create_all(bind=engine)
