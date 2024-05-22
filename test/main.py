from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
sqldbname = 'database.db'
app.secret_key = 'test'


# Dinh tuyen ham index cho url mac dinh
@app.route('/', methods=['get'])
def index():
    # Render file index.html khi trinh duyet tro den url '/' (url mac dinh)
    return render_template('index.html')


# Dinh tuyen ham team cho url '/team/ten doi bong' vd: '/team/manu'
@app.route('/team/<fteam>', methods=['get'])
def team(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE team = ?', (fteam,))
    # Tim kiem cac san pham la ao dau cua manu va luu vao products
    products = c.fetchall()
    conn.close()
    # Render file team.html va truyen vao gia tri cua bien products
    return render_template('team.html', products=products)


# Dinh tuyen ham nation cho url '/nations'
@app.route('/nations', methods=['get'])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE nation <> 0')
    # Tim kiem cac ban ghi co gia tri nation != 0 va luu vao products
    products = c.fetchall()
    conn.close()
    # Render file nation.html va truyen vao gia tri cua bien products
    return render_template('nation.html', products=products)


# Dinh tuyen ham login cho url '/login'
@app.route('/login', methods=['get', 'post'])
def login():
    # Neu method la post thi lay data tu form
    if request.method == 'post':
        username = request.form.get('username')
        password = request.form.get('password')
        # Tao bien check
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        # Tim kiem user va password trong table users
        c.execute('SELECT * FROM "users " WHERE username = ? AND password = ?', (username, password))
        # Luu ket qua tim kiem dau tien vao bien user
        user = c.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            session['id'] = user[0]
            return render_template(url_for('index'))
    elif request.method == 'get':
        return render_template('login.html')


# Dinh tuyen ham logout cho url '/logout'
@app.route('/logout')
def logout():
    # Xoa session username va chuyen huong den trang index
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
