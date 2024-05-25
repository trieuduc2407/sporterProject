from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'e6008a019495ffa0b29f43ad'
sqldbname = 'database.db'


# Dinh tuyen ham index cho url '/'
@app.route('/', methods=['GET'])
def index():
    if 'logged_in' in session:
        # Kiem tra neu ton tai gia tri 'logged_in' trong session (User da dang nhap)
        # Render file index.html, truyen vao gia tri:
        # user=session['lname']: Gia tri cua lname trong table users
        return render_template('index.html', user=session['lname'], teams=teams())
    # Neu khong ton tai gia tri ['logged_in'] trong session (User chua dang nhap)
    # Render file index.html va khong truyen vao tham so
    return render_template('index.html')


# Dinh tuyen ham team cho url '/team'
@app.route('/team', methods=['GET'])
def team():
    # Render file displayTeam.html va truyen vao gia tri cua bien result
    return render_template('displayTeam.html', imgs=teams())


def teams():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM team')
    result = c.fetchall()
    conn.close()
    return result


# Dinh tuyen ham getTeam cho url '/team/ten doi bong' vd: '/team/manu'
@app.route('/team/<fteam>', methods=['GET'])
def getTeam(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE team = ?', (fteam,))
    # Tim kiem cac san pham la ao dau cua manu va luu vao products
    products = c.fetchall()
    conn.close()
    # Render file team.html va truyen vao gia tri cua bien products
    return render_template('team.html', products=products)


# Dinh tuyen ham nation cho url '/nations'
@app.route('/nations', methods=['GET'])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE nation NOTNULL')
    # Tim kiem cac ban ghi co gia tri nation NOTNULL va luu vao products
    products = c.fetchall()
    conn.close()
    # Render file nation.html va truyen vao gia tri cua bien products
    return render_template('nation.html', products=products)


# Dinh tuyen ham search cho url '/search'
@app.route('/search', methods=['POST'])
def search():
    searchText = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE name LIKE '%"+searchText+"%'")
    products = c.fetchall()
    conn.close()
    return render_template('search.html', products=products)


# Dinh tuyen ham login cho url '/login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lay gia tri username va password tu html form
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute('SELECT * FROM "users " WHERE username = ? AND password = ?', (username, password))
        # Tim kiem ban ghi thoa man username va password luu vao bien user
        user = c.fetchone()
        if user:
            # Neu ton tai user
            session['username'] = username
            session['logged_in'] = True
            session['lname'] = user[5]
            # Tao session moi voi cac gia tri username, logged_in, lname va redirect ve index
            return redirect(url_for('index'))
        else:
            # Neu khong ton tai user, hien thong bao va yeu cau nhap lai
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


# Dinh tuyen ham logout cho url '/logout'
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('lname', None)
    # Xoa cac gia tri session va redirect ve index
    return redirect(url_for('index'))


# Dinh tuyen ham register cho url '/register'
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lay cac gia tri username, password, email, fname, lname tu html form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute('SELECT * FROM "users " WHERE username = ? OR email = ?', (username, email,))
        # Tim kiem ban ghi thoa man username hoac email va luu vao bien check
        check = c.fetchone()
        if not check:
            c.execute('SELECT MAX(id) FROM "users "')
            # Neu khong ton tai check, tim kiem ban ghi co id lon nhat va luu vao max_id
            max_id = c.fetchone()[0]
            if max_id > 0:
                max_id = max_id+1
            else:
                max_id = 1
            c.execute('INSERT INTO "users " VALUES (?,?,?,?,?,?)', (max_id, username, password, email, fname, lname))
            conn.commit()
            # Chen ban ghi moi vao table users va redirect ve login
            return redirect(url_for('login'))
        else:
            # Neu ton tai check (Da co ban ghi thoa man username hoac email)
            # Render register.html, truyen vao thong bao loi
            return render_template('register.html', error='Username or email already registered')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, port=5005)
