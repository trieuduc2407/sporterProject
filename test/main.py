import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'e6008a019495ffa0b29f43ad'
sqldbname = 'database.db'


# Ham result_to_dict dung de chuyen products tu list ve dictionary
def result_to_dict(products):
    # Tao bien result la 1 empty list
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        dict = {"productId": product[0], "productName": product[1], "productPrice": product[2], "productImg": img}
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(dict)
    conn.close()
    # Tra ve bien result
    return result


# Ham get_max_id su dung de lay ra maxId tu mot table
def get_max_id(table_name):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    if table_name == 'users':
        c.execute('SELECT MAX(userId) FROM users')
        # Tim kiem userId lon nhat trong table cart va luu vao max_id
        max_id = c.fetchone()[0]
        # Neu max_id == True (Trong table users co it nhat 1 row)
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id+1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == 'carts':
        c.execute('SELECT MAX(cartId) FROM cart')
        # Tim kiem cartId lon nhat trong table cart va luu vao max_id
        max_id = c.fetchone()[0]
        # Neu max_id == True (Trong table cart co it nhat 1 row)
        if max_id:
            # Tang gia tri cua max_id len 1
            max_id = max_id+1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id


# Ham carousel dung de chon nhau nhien 1 so luong san pham nhat dinh tu table products
def carousel():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products ORDER BY RANDOM() LIMIT 5")
    # Chon ngau nhien 5 san pham tu table products va luu vao bien products
    products = c.fetchall()
    # Goi ham result_to_dict va truyen vao bien products
    return result_to_dict(products)


# Dinh tuyen ham index cho url '/'
@app.route('/', methods=['GET'])
def index():
    if 'logged_in' in session:
        # Kiem tra neu ton tai gia tri 'logged_in' trong session (User da dang nhap)
        # Render file index.html, truyen vao gia tri:
        # user=session['lname']: Gia tri cua lname trong table users
        return render_template('home.html', user=session['lname'], teams=teams(), carousel=carousel())
    # Neu khong ton tai gia tri ['logged_in'] trong session (User chua dang nhap)
    # Render file index.html va khong truyen vao tham so
    return render_template('home.html', teams=teams(), carousel=carousel())


# Ham teams dung de hien lay ra cac record tu table teams
def teams():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT teamName, teamImg FROM teams')
    # Tim kiem teamName, teamImg tu table teams va luu vao bien teams
    teams = c.fetchall()
    # Tao bien result la 1 empty list
    result = []
    for team in teams:
        dict = {"teamName": team[0], "teamImg": team[1]}
        # Tao moi bien dict voi kieu dictionary va them vao list result
        result.append(dict)
    conn.close()
    # Tra ve bien result
    return result


# Dinh tuyen ham team cho url '/team'
@app.route('/team', methods=['GET'])
def team():
    # Render file displayTeam.html va truyen vao gia tri cua bien result
    return render_template('displayTeam.html', teams=teams())


# Dinh tuyen ham get_team cho url '/team/ten doi bong' VD: '/team/manu'
@app.route('/team/<fteam>', methods=['GET'])
def get_team(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE team = ?', (fteam,))
    # Tim kiem cac san pham la ao dau cua manu va luu vao products
    products = c.fetchall()
    # Render file team.html va truyen vao gia tri cua bien products
    return render_template('team.html', items=result_to_dict(products))


# Dinh tuyen ham nation cho url '/nations'
@app.route('/nations', methods=['GET'])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE nation NOTNULL')
    # Tim kiem cac ban ghi co gia tri nation NOTNULL va luu vao products
    products = c.fetchall()
    # Render file nation.html va truyen vao gia tri cua bien products
    return render_template('nation.html', items=result_to_dict(products))


# Dinh tuyen ham search cho url '/search'
@app.route('/search', methods=['POST'])
def search():
    search_text = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products WHERE name LIKE '%"+search_text+"%'")
    # Tim cac san pham co ten gan dung voi search_text va luu vao bien products
    products = c.fetchall()
    # Render file search.html, truyen vao gia tri cua bien products da duoc bien doi thanh dictionary
    return render_template('search.html', items=result_to_dict(products))


# Dinh tuyen ham product cho url '/product/id' VD: '/product/1/
@app.route('/product/<id>', methods=['GET'])
def product(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        'SELECT name, price, sizeTitle, infoTitle FROM products WHERE productId = ?',
        (id,)
    )
    # Tim kiem san pham theo productId = id va luu vao product
    product = c.fetchone()
    c.execute("SELECT * FROM images WHERE productId = ?", (id,))
    # Tim kiem anh san pham theo productId va luu vao img
    img = c.fetchone()
    conn.close()
    # Luu cac gia tri can thiet vao bien result duoi dang dictionary
    result = {
        "productName": product[0], "productPrice": product[1], "sizeTitle": product[2], "sizeText": product[3],
        "infoTitle1": product[4], "infoText1": product[5], "infoTitle2": product[6], "infoText2": product[7],
        "sizeImg1": img[2], "sizeImg2": img[3], "img1": img[4], "img2": img[5], "img3": img[6], "img4": img[7],
    }
    # Render file product.html va truyen vao gia tri bien result
    return render_template('product.html', item=result)


# Dinh tuyen ham login cho url '/login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Neu method la POST, ay gia tri username va password tu html form
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        # Tim kiem ban ghi thoa man username va password luu vao bien user
        user = c.fetchone()
        if user:
            session['user'] = True
            session['user_id'] = user[0]
            session['user_username'] = username
            session['user_lname'] = user[5]
            cart = get_cart(user[0])
            session['cart'] = cart
            # Neu ton tai user, tao cac gia tri session can thiet va redirect ve index
            return redirect(url_for('index'))
        else:
            # Neu khong ton tai user, hien thong bao va yeu cau nhap lai
            return render_template('login-form.html', error='Invalid username or password')
    # Neu method la GET, render file login-form.html
    return render_template('login-form.html')


# Dinh tuyen ham logout cho url '/logout'
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    session.pop('user_username', None)
    session.pop('user_lname', None)
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
            max_id = get_max_id('users')
            c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', (max_id, username, password, email, fname, lname))
            conn.commit()
            # Them ban ghi moi vao table users va redirect ve login
            return redirect(url_for('login'))
        else:
            # Neu ton tai check (Da co ban ghi thoa man username hoac email)
            # Render register.html, truyen vao thong bao loi
            return render_template('register.html', error='Username or email already registered')
    else:
        # Neu method la GET, render file register.html
        return render_template('register.html')


# Ham get_cart voi tham so id dung de lay ra cac ban ghi trong table cart
def get_cart(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, productName, productPrice, quantity FROM cart WHERE userId = ?', (id,))
    # Tim kiem productId, productName, productPrice, quantity trong table cart theo userId va luu vao bien products
    products = c.fetchall()
    # Tao bien result la 1 empty list
    result = []
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        dict = {
            "productId": product[0], "productName": product[1], "productPrice": product[2], "productImg": img,
            "quantity": product[3]
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(dict)
    conn.close()
    # Tra ve bien result
    return result


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
        max_id = get_max_id('carts')
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


# Dinh tuyen ham update_cart cho url '/update'
@app.route('/update', methods=['POST'])
def update_cart():
    # Lay gia tri product_id, quantity tu html form
    product_id = request.form['productId']
    quantity = request.form['quantity']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    # Thay doi gia tri cua quantity trong table carts
    c.execute("UPDATE cart SET quantity = ? WHERE productId = ?", (quantity, product_id))
    conn.commit()
    conn.close()
    # Redirect ve ham view_cart
    return redirect(url_for('view_cart'))


# Dinh tuyen ham delete cho url '/delete'
@app.route('/delete', methods=['POST'])
def delete_cart():
    # Lay gia tri cua product_id tu html form
    product_id = request.form['productId']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    # Xoa ban ghi co gia tri bang product_id trong table carts
    c.execute("DELETE FROM cart WHERE productId = ?", (product_id,))
    conn.commit()
    conn.close()
    # Redirect ve ham view_cart
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


# Ham check_admin dung de kiem tra tai khoan admin da duoc dang nhap chua
def check_admin():
    # Kiem tra neu 'admin' co trong session (Tai khoan admin da duoc dang nhap)
    if 'admin' in session:
        # Neu co, tra ve gia tri True
        return True
    else:
        # Neu khong, tra ve gia tri False
        return False


# Dinh tuyen ham admin_view cho url '/admin'
@app.route('/admin', methods=['GET'])
def admin_view():
    # Goi ham check admin de kiem tra session
    if check_admin():
        # Render file adminView.html, truyen vao gia tri cua session['lname']
        return render_template('adminView.html', admin=session['admin_lname'])
    else:
        # Redirect ve trang dang nhap admin
        return redirect(url_for('admin_login'))


# Dinh tuyen ham admin_login cho url '/admin/login'
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Goi ham check admin de kiem tra session
    if request.method == 'POST':
        # Meu method la POST, lay gia tri username, password tu html form
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password,))
        # Tim kiem trong table admin theo gia tri username, password va luu vao admin
        admin = c.fetchone()
        if admin:
            session['admin'] = True
            session['admin_id'] = admin[0]
            session['admin_username'] = username
            session['admin_lname'] = admin[5]
            # Neu ton tai admin tao cac gia tri session can thiet va redirect ve admin_view
            return redirect(url_for('admin_view'))
        else:
            # Neu khong ton tai admin, render file adminLogin.html va truyen vao thong bao loi
            return render_template('adminLogin.html', error='Invalid username or password')
    else:
        # Neu method la GET, render file adminLogin.html
        return render_template('adminLogin.html')


# Dinh tuyen ham admin_logout cho url '/admin/logout'
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('admin_lname', None)
    # Xoa cac gia tri session va redirect ve admin_view
    return redirect(url_for('admin_view'))


# Dinh tuyen ham admin_search cho url '/admin/search'
@app.route('/admin/search', methods=['POST'])
def admin_search():
    # Lay gia tri search tu html form
    search = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price, quantity FROM products WHERE name LIKE '%"+search+"%'")
    # Tim cac san pham co ten gan dung voi search va luu vao bien products
    products = c.fetchall()
    result = []
    for product in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (product[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        dict = {
            "productId": product[0], "productName": product[1], "productPrice": product[2], "quantity": product[3],
            "productImg": img
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(dict)
    # Render file adminSearch.html, truyen vao gia tri cua bien result
    return render_template('adminSearch.html', admin=session['admin_lname'], items=result)


@app.route('/admin/update/<id>', methods=['GET', 'POST'])
def admin_update(id):
    if check_admin():
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == 'POST':
            team = request.form['team']
            nation = request.form['nation']
            name = request.form['name']
            price = request.form['price']
            quantity = request.form['quantity']
            sizeTitle = request.form['sizeTitle']
            infoTitle = request.form['infoTitle']
            img1 = request.form['img1']
            img2 = request.form['img2']
            img3 = request.form['img3']
            img4 = request.form['img4']
            c.execute(
                "UPDATE products SET team = ?, nation = ?, name = ?, price = ?, quantity = ?, sizeTitle = ?, infoTitle = ? WHERE productId = ?",
                (team, nation, name, price, quantity, sizeTitle, infoTitle, id)
            )
            conn.commit()
            c.execute(
                "UPDATE images SET img1 = ?, img2 = ?, img3 = ?, img4 = ? WHERE productId = ?",
                (img1, img2, img3, img4, id,)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin_update'))
        else:
            c.execute("SELECT team, nation, name, price, sizeTitle, infoTitle FROM products WHERE productId = ?", (id,))
            product = c.fetchone()
            result = {
                "team": product[0], "nation": product[1], "name": product[2], "price": product[3],
                "sizeTitle": product[4],
                "infoTitle": product[5]
            }
            return render_template('adminUpdate.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/update/quantity/<id>', methods=['POST'])
def admin_quantity(id):
    if check_admin():
        quantity = request.form['quantity']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("UPDATE products SET quantity = ? WHERE productId = ?", (quantity, id,))
        conn.commit()
        conn.close()
        msg = 'updated'
        return msg
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/update/price/<id>', methods=['POST'])
def admin_price(id):
    if check_admin():
        price = request.form['price']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("UPDATE products SET price = ? WHERE productId = ?", (price, id,))
        conn.commit()
        conn.close()
        msg = 'updated'
        return msg
    else:
        return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True, port=5005)
