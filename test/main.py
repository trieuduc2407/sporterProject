import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'e6008a019495ffa0b29f43ad'
sqldbname = 'database.db'


def carousel():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products ORDER BY RANDOM() LIMIT 5")
    products = c.fetchall()
    result = []
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        img = c.fetchone()
        dict = {"productName": product[1], "productPrice": product[2], "productImg": img[0]}
        result.append(dict)
    conn.close()
    return result


def teams():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM teams')
    result = c.fetchall()
    conn.close()
    return result


def result_dict(products):
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        img = c.fetchone()[0]
        dict = {"productId": product[0], "productName": product[1], "productPrice": product[2], "productImg": img}
        result.append(dict)
    conn.close()
    return result


def get_max_user_id():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT MAX(userId) FROM users')
    max_id = c.fetchone()[0]
    if max_id > 0:
        max_id = max_id+1
    else:
        max_id = 1
    return max_id


def get_max_cart_id():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT MAX(cartId) FROM cart')
    max_id = c.fetchone()[0]
    if max_id:
        max_id = max_id+1
    else:
        max_id = 1
    return max_id


def get_cart(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, productName, productPrice, quantity FROM cart WHERE userId = ?', (id,))
    products = c.fetchall()
    result = []
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        img = c.fetchone()[0]
        dict = {
            "productId": product[0], "productName": product[1], "productPrice": product[2], "productImg": img,
            "quantity": product[3]
        }
        result.append(dict)
    conn.close()
    return result


# Dinh tuyen ham index cho url '/'
@app.route('/', methods=['GET'])
def index():
    if 'logged_in' in session:
        # Kiem tra neu ton tai gia tri 'logged_in' trong session (User da dang nhap)
        # Render file index.html, truyen vao gia tri:
        # user=session['lname']: Gia tri cua lname trong table users
        return render_template('index.html', user=session['lname'], teams=teams(), carousel=carousel())
    # Neu khong ton tai gia tri ['logged_in'] trong session (User chua dang nhap)
    # Render file index.html va khong truyen vao tham so
    return render_template('index.html', teams=teams(), carousel=carousel())


# Dinh tuyen ham team cho url '/team'
@app.route('/team', methods=['GET'])
def team():
    # Render file displayTeam.html va truyen vao gia tri cua bien result
    return render_template('displayTeam.html', teams=teams())


# Dinh tuyen ham get_team cho url '/team/ten doi bong' vd: '/team/manu'
@app.route('/team/<fteam>', methods=['GET'])
def get_team(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE team = ?', (fteam,))
    # Tim kiem cac san pham la ao dau cua manu va luu vao products
    products = c.fetchall()
    # Render file team.html va truyen vao gia tri cua bien products
    return render_template('team.html', items=result_dict(products))


# Dinh tuyen ham nation cho url '/nations'
@app.route('/nations', methods=['GET'])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE nation NOTNULL')
    # Tim kiem cac ban ghi co gia tri nation NOTNULL va luu vao products
    products = c.fetchall()
    # Render file nation.html va truyen vao gia tri cua bien products
    return render_template('nation.html', items=result_dict(products))


# Dinh tuyen ham search cho url '/search'
@app.route('/search', methods=['POST'])
def search():
    search_text = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products WHERE name LIKE '%"+search_text+"%'")
    # Tim cac san pham co ten gan dung voi search_text va luu vao bien products
    products = c.fetchall()
    return render_template('search.html', items=result_dict(products))


@app.route('/product/<id>', methods=['GET'])
def product(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        'SELECT name, price, sizeTitle, sizeText, infoTitle1, infoText1, infoTitle2, infoText2 FROM products WHERE productId = ?',
        (id,)
    )
    product = c.fetchone()
    c.execute("SELECT * FROM images WHERE productId = ?", (id,))
    img = c.fetchone()
    conn.close()
    result = {
        "productName": product[0], "productPrice": product[1], "sizeTitle": product[2], "sizeText": product[3],
        "infoTitle1": product[4], "infoText1": product[5], "infoTitle2": product[6], "infoText2": product[7],
        "sizeImg1": img[2], "sizeImg2": img[3], "img1": img[4], "img2": img[5], "img3": img[6], "img4": img[7],
    }
    return render_template('product.html', item=result)


# Dinh tuyen ham login cho url '/login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lay gia tri username va password tu html form
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        # Tim kiem ban ghi thoa man username va password luu vao bien user
        user = c.fetchone()
        if user:
            # Neu ton tai user
            session['logged_in'] = True
            session['username'] = username
            session['id'] = user[0]
            session['lname'] = user[5]
            cart = get_cart(user[0])
            session['cart'] = cart
            # Tao session moi voi cac gia tri username, logged_in, lname, cart va redirect ve index
            return redirect(url_for('index'))
        else:
            # Neu khong ton tai user, hien thong bao va yeu cau nhap lai
            return render_template('login-form.html', error='Invalid username or password')
    return render_template('login-form.html')


# Dinh tuyen ham logout cho url '/logout'
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
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
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email,))
        # Tim kiem ban ghi thoa man username hoac email va luu vao bien check
        check = c.fetchone()
        if not check:
            max_id = get_max_user_id()
            c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', (max_id, username, password, email, fname, lname))
            conn.commit()
            # Chen ban ghi moi vao table users va redirect ve login
            return redirect(url_for('login'))
        else:
            # Neu ton tai check (Da co ban ghi thoa man username hoac email)
            # Render register.html, truyen vao thong bao loi
            return render_template('register.html', error='Username or email already registered')
    else:
        return render_template('register.html')


# Dinh tuyen ham add_to_cart cho url '/cart/add'
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    # Lay cac gia tri product_id, quantity tu html form
    product_id = int(request.form['productId'])
    quantity = int(request.form['quantity'])
    # Cap nhat cart
    cart = session.get('cart', [])
    check = False
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in cart:
        # Kiem tra neu item da co trong cart thi tang quantity
        if item['productId'] == product_id:
            item['quantity'] += quantity
            check = True
            c.execute("UPDATE cart SET quantity = ? WHERE productId = ?", (item['quantity'], item['productId']))
            conn.commit()
            break
    if not check:
        # Neu item chua co trong cart thi them moi item vao table cart
        max_id = get_max_cart_id()
        c.execute('SELECT name, price FROM products WHERE productId = ?', (product_id,))
        result = c.fetchone()
        c.execute(
            'INSERT INTO cart VALUES (?,?,?,?,?,?)', (max_id, session['id'], product_id, result[0], result[1], quantity)
        )
        conn.commit()
        conn.close()
    # Cap nhat lai cart
    session['cart'] = get_cart(session['id'])
    msg = 'added'
    return msg


@app.route('/update', methods=['POST'])
def update_cart():
    product_id = request.form['productId']
    quantity = request.form['quantity']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("UPDATE cart SET quantity = ? WHERE productId = ?", (quantity, product_id))
    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/delete', methods=['POST'])
def delete_cart():
    product_id = request.form['productId']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE productId = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


# Dinh tuyen ham cart cho url '/cart'
@app.route('/cart', methods=['GET'])
def view_cart():
    if 'logged_in' in session:
        # Kiem tra neu ton tai gia tri 'logged_in' trong session (User da dang nhap) thi goi ham getCart()
        session['cart'] = get_cart(session['id'])
        cart = session.get('cart', [])
        # Render file cart.html, truyen vao gia tri bien cart
        return render_template('cart.html', items=cart)
    else:
        # Neu khong ton tai gia tri 'logged_in' trong session (User chua dang nhap)
        # Redirect ve trang login va hien thong bao yeu cau dang nhap de xem gio hang
        return render_template('login-form.html', cartError=True)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
