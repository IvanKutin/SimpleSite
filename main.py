from flask import Flask, render_template, request, redirect, make_response, url_for
from database import *
import hashlib

# create the app
app = Flask(__name__)

user = ''
basket=[]

@app.route('/',methods=['GET', 'POST'])
def index():
    global user
    search = request.args.get('search')
    db = Database()
    purchases = db.all_purchase()
    if search != None:
        i=0
        j=0
        k=len(purchases)
        while j<k:
            print(purchases[i])
            if purchases[i][0]!=search:
                purchases.remove(purchases[i])
            else:
                i=i+1
            j=j+1
    else:
        search=''
    context = {'user': user, 'purchases': purchases,'search':search}
    return render_template("main_page.html", **context)


@app.route('/<int:id>')
def purchase(id):
    global user
    db = Database()
    purchases = db.all_purchase()
    for i in purchases:
        if id == i[5]:
            purchase = i
    context = {'user': user, 'purchase': purchase}
    return render_template("purchase.html", **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global user
    reg = ''
    mistake = ''
    mistake1 = ''
    mistake2 = ''
    mistake3 = ''
    user = ''
    context = {'user': user}
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if login == '':
            mistake1 = 'Введите имя пользователя'
        if password == '':
            mistake2 = 'Введите пароль'
        if password2 != password:
            mistake3 = 'Введенные пароли не сопадают'
        if mistake1 == '' and mistake2 == '' and mistake3 == '':
            db = Database()
            users = db.all()
            for i in users:
                if i[0] == login:
                    mistake = 'Данный пользователь уже зарегестрирован!'
            if not mistake:
                reg = '1'
                hash = hashlib.sha256(password.encode()).hexdigest()
                db.register(login, hash)
                user = User(login, hash)
        context = {'login': login, 'mistake': mistake, 'mistake1': mistake1, 'mistake2': mistake2,
                   'mistake3': mistake3,
                   'reg': reg, 'user': user, 'password': password, 'password2': password2}
        return render_template('register.html', **context)
    else:
        return render_template("register.html", **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    reg = ''
    if request.method == 'POST':

        login = request.form.get('login')
        password = request.form.get('password')
        if password is not None:
            hash = hashlib.sha256(password.encode()).hexdigest()
        mistake = 'В ваших данных ошибка,попробуйте снова'
        db = Database()
        users = db.all()
        for i in users:
            if i[0] == login and i[1] == hash:
                mistake = ''
                user = User(login, hash)
                reg = 1
        context = {'user': user, 'mistake': mistake, 'reg': reg, 'auto': 1, 'login': login, 'password': password}
        return render_template('login.html', **context)
    else:
        context = {'user': user}
        return render_template("login.html", **context)


@app.route('/my_basket')
def my_basket():
    search=''
    global user
    global basket
    search = request.args.get('search')
    basket1=[]
    for i in basket:
        basket1.append(i)
    if search != None:
        i = 0
        j = 0
        k = len(basket1)
        while j < k:
            print(basket1[i])
            if basket1[i][0] != search:
                basket1.remove(basket1[i])
            else:
                i = i + 1
            j = j + 1
    else:
        search=''
    context = {'user': user, 'purchases':basket1,'search':search}
    return render_template("my_basket.html", **context)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global user
    hash = ''
    if request.method == 'POST':
        reg = ''
        mistake1 = ''
        mistake2 = ''
        mistake3 = ''
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == '':
            mistake2 = 'Введите пароль'
        if password2 != password1:
            mistake3 = 'Введенные пароли не сопадают'
        if password is not None:
            hash = hashlib.sha256(password.encode()).hexdigest()
        if user.hash != hash:
            mistake1 = 'Вы ввели не свой пароль'
        if mistake1 == '' and mistake2 == '' and mistake3 == '':
            reg = 1
            db = Database()
            db.update(user.login, hashlib.sha256(password1.encode()).hexdigest())
        context = {'login': login, 'mistake1': mistake1, 'mistake2': mistake2,
                   'mistake3': mistake3,
                   'reg': reg, 'user': user, 'password': password, 'password2': password2, 'password1': password1}
        return render_template('profile.html', **context)
    else:
        if user != '':
            context = {'user': user}
            return render_template("profile.html", **context)
        else:
            return ('NOT_FOUND')


@app.route('/change_password')
def change_password():
    global user
    context = {'user': user}
    return render_template("change_password.html", **context)


@app.route('/delete')
def delete():
    global user
    global basket
    user = ''
    basket = []
    return redirect('/')

@app.route('/append<int:id>')
def append(id):
    global user
    global basket
    db = Database()
    purchases = db.all_purchase()
    for i in purchases:
        if id == i[5]:
            purchase = i
    basket.append(purchase)
    return redirect('/my_basket')


@app.route('/buy<int:id>')
def buy(id):
    global user
    db = Database()
    purchases = db.all_purchase()
    for i in purchases:
        if id == i[5]:
            purchase = i
    m=1
    context = {'user': user, 'purchase': purchase,'m':m}
    return render_template("purchase.html", **context)

@app.route('/success_buy<int:id>')
def success_buy(id):
    global user
    global basket
    for i in basket:
        if i[5]==id:
            basket.remove(i)
    context = {'user': user, 'buy':1}
    return render_template("purchase.html", **context)

app.run()
