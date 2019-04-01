"""
ORM:TODO 编写文档
"""
from sqlalchemy import create_engine, Column, Integer, String, or_, and_, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashlib import sha1

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb", encoding='utf8', echo=True)
Base = declarative_base(bind=engine)
session = sessionmaker(bind=engine)()


class User(Base):
    """ table of mysql """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)


class Admin(Base):
    """ table of mysql """
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False)
    password = Column(String(50), nullable=True)


class Book(Base):
    """ table of mysql """
    __tablename__ = 'book'
    num = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id = Column(Integer, autoincrement=True, nullable=False)
    book_name = Column(String(20), nullable=False)
    book_price = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


def check_user(username, password):
    """ check the user'infomation whether in the user table """
    user = session.query(User).filter(User.username == username).filter(User.password == password).first()
    if user:
        return user.id


def add_user(username, password):
    """ add a user to the user table  """
    user = User(id=0, username=username, password=password)
    session.add(user)
    session.commit()


def delete_user(username):
    """ delete a user from the user table """
    user = session.query(User).filter(User.username == username).first()
    if user:
        session.delete(user)
        return True


def select_user(user_id):
    """  select a user by id """
    return session.query(User).filter(User.id == user_id).first()


def get_all_users():
    """ return all users in the table of user """
    return session.query(User).all()


def check_admin(name, password):
    """ check the admin info whether in the admin table """
    admin = session.query(Admin).filter(and_(Admin.name == name, Admin.password == password)).first()
    if admin:
        return admin


def check_book(book_info, user_id):
    """ check the book whether in the book table """
    book = session.query(Book).filter(or_(Book.id == book_info,
                                          Book.book_name == book_info)).filter(Book.user_id == user_id).first()
    if book:
        return book


def add_book(book_name: str, book_price: int, user_id: int):
    """ add a book to the book table """
    book = Book(num=0, id=0, book_name=book_name, book_price=book_price, user_id=user_id)
    session.add(book)
    # auto increment id from 1
    books = get_user_books(user_id)

    auto_increment(books)
    print(books)
    session.commit()


def delete_book(book_name, user_id):
    """ delete a book from the table of book """
    book = session.query(Book).filter(Book.book_name == book_name).first()
    if book:
        session.delete(book)
        # auto increment id from 1
        books = get_user_books(user_id)
        auto_increment(books)
        session.commit()
        return True


def alter_book(old_name, new_name, book_price):
    """ alter the book info """
    book = session.query(Book).filter(Book.book_name == old_name).first()
    if book:
        book.book_name = new_name
        book.book_price = book_price
        return True


def get_user_books(user_id):
    """ return all books in the table of book """
    return session.query(Book).filter(Book.user_id == user_id).all()


def auto_increment(table):
    """ auto increment id from 1 """
    print(table)
    i = 1
    for row in table:
        row.id = i
        i = i + 1


def pwd(password: str):
    """ use sha1 to let the password more secure """
    password = password.encode('utf8')
    s = sha1()
    s.update(password)
    return s.hexdigest()


if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all(engine)
    print(pwd('123456'))
