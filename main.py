from flask import Flask, render_template, request, redirect, make_response
from orm import alchemy
import datetime

app = Flask(__name__)
# TODO 上线之后关闭debug
app.debug = True


@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    print(user_id)
    if user_id:
        user = alchemy.select_user(user_id)
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        # 密码加密
        password = alchemy.pwd(password)
        alchemy.add_user(username, password)
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = alchemy.pwd(password)
        num = alchemy.check_user(username, password)
        if num:
            res = make_response(redirect('books'))
            res.set_cookie(key='user_id', value=str(num), expires=datetime.datetime.now() + datetime.timedelta(days=7))
            return res

        else:
            return render_template('login.html', fail=True)


@app.route('/quit')
def quit_page():
    response = make_response(redirect('/'))
    response.delete_cookie('user_id')
    return response


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')

    elif request.method == 'POST':
        admin_name = request.form['admin_name']
        password = request.form['password']
        password = alchemy.pwd(password)

        admin = alchemy.check_admin(admin_name, password)
        if admin:
            print('88888888888888888888888888888888888')
            return redirect('/users')
        else:
            return render_template('admin_login.html', fail=True)


@app.route('/users<deleting_user>')
def delete_user(deleting_user):
    if deleting_user:
        alchemy.delete_user(deleting_user)

    users = alchemy.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users')
def all_user():
    users = alchemy.get_all_users()
    return render_template('users.html', users=users)


@app.route('/books')
def books():
    if request.cookies:
        user_id = request.cookies['user_id']
        book = alchemy.get_user_books(user_id)
        return render_template('books.html', books=book)


@app.route('/detail<int:num>')
def detail(num):
    user_id = request.cookies['user_id']
    result = alchemy.check_book(num, user_id)
    return render_template('detail.html', num=num, book=result)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html')

    elif request.method == 'POST':
        book_name = request.form['book_name']
        book_price = request.form['book_price']
        try:
            book_price = int(book_price)
        except Exception as e:
            print(e)
            return redirect('/add_book')

        user_id = request.cookies['user_id']
        the_book = alchemy.check_book(book_name, user_id)

        if the_book:
            return render_template('add_book.html', exist=True, book=book_name)
        else:
            user_id = request.cookies['user_id']
            alchemy.add_book(book_name=book_name, book_price=book_price, user_id=user_id)
            return redirect('/books')


@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'GET':
        return render_template('delete_book.html')

    elif request.method == 'POST':
        book_name = request.form['book_name']
        user_id = request.cookies['user_id']
        result = alchemy.delete_book(book_name, user_id)
        if result:
            return redirect('/books')
        else:
            pass


@app.route('/books<deleting_book>')
def delete_books(deleting_book):
    if delete_book:
        user_id = request.cookies['user_id']
        alchemy.delete_book(deleting_book, user_id)
        book = alchemy.get_user_books(user_id)
        return render_template('books.html', books=book)


@app.route('/alter_book<book_name>', methods=['GET', 'POST'])
def alter_book(book_name):
    user_id = request.cookies['user_id']
    book = alchemy.check_book(book_name, user_id)
    if request.method == 'GET':
        return render_template('alter_book.html', book=book)

    elif request.method == 'POST':
        new_book_name = request.form['new_book_name']
        new_book_price = request.form['new_book_price']
        alchemy.alter_book(book_name, new_book_name, new_book_price)
        return redirect('/books')


if __name__ == '__main__':
    app.run()
