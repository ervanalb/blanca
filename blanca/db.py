from sqlalchemy import Column, Integer, Sequence, String, Enum, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import random
import string
import hashlib
from contextlib import contextmanager

Base = declarative_base()
Session = None

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    fullname = Column(String(255), nullable=False)
    password_salt = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, Sequence('list_id_seq'), primary_key=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text(), nullable=False)
    admin_type = Column(Enum("USER", "LIST"), nullable=False)
    admin_id = Column(Integer, nullable=False)

    def __repr__(self):
        return "<List(name='%s')>" % (self.name)

class String(Base):
    __tablename__ = 'strings'
    id = Column(Integer, Sequence('string_id_seq'), primary_key=True)
    string = Column(String(255), nullable=False)

    def __repr__(self):
        return "<String(string='%s')>" % (self.string)

class Membership(Base):
    __tablename__ = 'membership'
    id = Column(Integer, Sequence('membership_id_seq'), primary_key=True)
    list_id = Column(Integer, nullable=False)
    member_type = Column(Enum("USER", "LIST", "STRING"), nullable=False)
    member_id = Column(Integer, index=True, nullable=False)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def is_name_valid(name):
    return (isinstance(name, str)
        and len(name) > 0
        and len(name) <= 255
        and re.match(r"[A-Za-z0-9\!\#\$\%\&'\*\+\-\/\=\?\^\_\`\{\|\}\~]+", name) is not None)

def is_password_valid(password):
    return (isinstance(password, str)
        and len(password) >= 6
        and len(password) <= 255)

def lookup(name, session):
    result = session.query(User).filter(User.name == name).first()
    if result is not None:
        return result
    else:
        result = session.query(List).filter(List.name == name).first()
        return result

def check_password(user, password):
    hash = user.password_hash
    salt = user.password_salt
    return hash == hashlib.sha256(bytes(password + salt, encoding="utf8")).hexdigest()

def create_password(password):
    salt = ''.join(random.choice(string.printable) for _ in range(8))
    hash = hashlib.sha256(bytes(password + salt, encoding="utf8")).hexdigest()
    return (salt, hash)

def create_user(name, password, fullname=""):
    if not is_name_valid(name):
        raise ValueError("Username is not valid.")
    if not is_password_valid(password):
        raise ValueError("Password is not valid.")
    (salt, hash) = create_password(password)
    with session_scope() as session:
        exists = lookup(name, session)
        if exists is not None:
            raise ValueError("User / list already exists: '{}'".format(name))
        new_user = User(name=name, fullname=fullname, password_salt=salt, password_hash=hash)
        session.add(new_user)

def login(name, password):
    with session_scope() as session:
        user = lookup(name, session)
        if not isinstance(user, User):
            return False
        return check_password(user, password)

def create_list(name, admin, description=""):
    if not is_name_valid(name):
        raise ValueError("List name is not valid.")
    with session_scope() as session:
        exists = lookup(name)
        if exists is not None:
            raise ValueError("User / list already exists: '{}'".format(name))
        # TODO handle self-ownership
        admin_row = lookup(admin)
        if admin_row is None:
            raise ValueError("Could not find user / list: '{}'".format(admin))
        new_list = List(name=name, admin=admin, description=description)
        session.add(new_list)

def init(url):
    global Session
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    init('sqlite:///db.sql')
    #create_user("eric", "asdfgh")
    #login("eric", "asdfgh")
    #me = User(name='eric', fullname='Eric VA', password='hunter2')
    #session.add(me)
    #session.commit()

#
#me = User(name='ed', fullname='Ed Jones', password='edspassword')
#session.add(me)
#session.commit()
