import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, make_response

app = Flask(__name__)
app.secret_key = 'e6008a019495ffa0b29f43ad'
sqldbname = 'database.db'


# Ham result_to_dict dung de chuyen products tu list ve dictionary
def user_result_to_dict(products):
    # Tao bien result la 1 empty list
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        new_dict = {"productId": item[0], "productName": item[1], "productPrice": item[2], "productImg": img}
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
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
            max_id = max_id + 1
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
            max_id = max_id + 1
        else:
            # Max_id == False (Trong table cart chua co ban ghi nao)
            # Gan max_id = 1
            max_id = 1
        # Tra ve max_id
        return max_id
    elif table_name == 'products':
        c.execute('SELECT MAX(productId) FROM products')
        max_id = c.fetchone()[0]
        if max_id:
            max_id = max_id + 1
            return max_id
        else:
            max_id = 1
        return max_id
    elif table_name == 'images':
        c.execute('SELECT MAX(imgId) FROM images')
        max_id = c.fetchone()[0]
        if max_id:
            max_id = max_id + 1
            return max_id
        else:
            max_id = 1
        return max_id
    elif table_name == 'order':
        c.execute('SELECT MAX(orderID) FROM "order"')
        max_id = c.fetchone()[0]
        if max_id:
            max_id = max_id + 1
            return max_id
        else:
            max_id = 1
        return max_id


# Ham carousel dung de chon nhau nhien 1 so luong san pham nhat dinh tu table products
def carousel():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products ORDER BY RANDOM() LIMIT 5")
    # Chon ngau nhien 5 san pham tu table products va luu vao bien products
    products = c.fetchall()
    # Goi ham result_to_dict va truyen vao bien products
    return user_result_to_dict(products)


# Dinh tuyen ham index cho url '/'
@app.route('/', methods=['GET'])
def index():
    # Render file index.html, truyen vao gia tri:
    # user=session['lname']: Gia tri cua lname trong table users
    return render_template('index.html', user=session['user_lname'], teams=teams(), carousel=carousel())


# Ham teams dung de hien lay ra cac record tu table teams
def teams():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT teamName, teamImg FROM teams')
    # Tim kiem teamName, teamImg tu table teams va luu vao bien teams
    teams = c.fetchall()
    # Tao bien result la 1 empty list
    result = []
    for item in teams:
        new_dict = {"teamName": item[0], "teamImg": item[1]}
        # Tao moi bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    conn.close()
    # Tra ve bien result
    return result


# Dinh tuyen ham team cho url '/team'
@app.route('/team', methods=['GET'])
def team():
    # Render file displayTeam.html va truyen vao gia tri cua bien result
    return render_template('displayTeam.html', user=session['user_lname'], teams=teams(), carousel=carousel())


# Dinh tuyen ham get_team cho url '/team/ten doi bong' VD: '/team/manu'
@app.route('/team/<fteam>', methods=['GET'])
def get_team(fteam):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE team = ?', (fteam,))
    # Tim kiem cac san pham la ao dau cua manu va luu vao products
    products = c.fetchall()
    c.execute("SELECT teamBanner FROM teams WHERE teamName = ?", (fteam,))
    banner = c.fetchone()[0]
    # Render file team.scss va truyen vao gia tri cua bien products
    return render_template('team.html', user=session['user_lname'], teams=teams(),
                           items=user_result_to_dict(products), banner=banner)


# Dinh tuyen ham nation cho url '/nations'
@app.route('/nations', methods=['GET'])
def nations():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, name, price FROM products WHERE nation NOTNULL')
    # Tim kiem cac ban ghi co gia tri nation NOTNULL va luu vao products
    products = c.fetchall()
    # Render file nation.html va truyen vao gia tri cua bien products
    return render_template('nation.html', user=session['user_lname'], items=user_result_to_dict(products))


# Dinh tuyen ham search cho url '/search'
@app.route('/search', methods=['POST'])
def search():
    search_text = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price FROM products WHERE name LIKE '%" + search_text + "%'")
    # Tim cac san pham co ten gan dung voi search_text va luu vao bien products
    products = c.fetchall()
    # Render file search.html, truyen vao gia tri cua bien products da duoc bien doi thanh dictionary
    return render_template('search.html', search=search_text, user=session['user_lname'],
                           items=user_result_to_dict(products))


# Dinh tuyen ham product cho url '/product/id' VD: '/product/1/
@app.route('/product/<product_id>', methods=['GET'])
def product(product_id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT name, price, sizeTitle, infoTitle FROM products WHERE productId = ?", (product_id,))
    item = c.fetchone()
    c.execute("SELECT img1, img2, img3, img4 FROM images WHERE productId = ?", (product_id,))
    img = c.fetchone()
    result = {
        "productId": product_id,
        "productName": item[0],
        "productPrice": item[1],
        "productImg1": img[0],
        "productImg2": img[1],
        "productImg3": img[2],
        "productImg4": img[3],
        "sizeTitle": item[2],
        "infoTitle": item[3],
    }
    return render_template('product.html', user=session['user_lname'], item=result)


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
            session['user_email'] = user[3]
            session['user_fname'] = user[4]
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
    session.pop('user_email', None)
    session.pop('user_fname', None)
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
def get_cart(product_id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT productId, productName, productPrice, quantity FROM cart WHERE userId = ?', (product_id,))
    # Tim kiem productId, productName, productPrice, quantity trong table cart theo userId va luu vao bien products
    products = c.fetchall()
    # Tao bien result la 1 empty list
    result = []
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        new_dict = {
            "productId": item[0], "productName": item[1], "productPrice": item[2], "productImg": img,
            "quantity": item[3]
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    conn.close()
    # Tra ve bien result
    return result


# Dinh tuyen ham add_to_cart cho url '/cart/add'
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    req = request.get_json()
    product_id = int(req['productId'])
    quantity = int(req['quantity'])
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
            'INSERT INTO cart VALUES (?,?,?,?,?,?)',
            (max_id, session['user_id'], product_id, result[0], result[1], quantity)
        )
        conn.commit()
        conn.close()
    # Cap nhat lai cart
    session['cart'] = get_cart(session['user_id'])
    res = make_response(jsonify({'Msg': 'Added to cart'}))
    return res


# Dinh tuyen ham update_cart cho url '/cart/update'
@app.route('/cart/update', methods=['POST'])
def update_cart():
    req = request.get_json()
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in req:
        product_id = int(item['productId'])
        quantity = int(item['quantity'])
        # Thay doi gia tri cua quantity trong table carts
        c.execute("UPDATE cart SET quantity = ? WHERE productId = ?", (quantity, product_id))
        conn.commit()
    conn.close()
    session['cart'] = get_cart(session['user_id'])
    res = make_response(jsonify({'Msg': 'Updated cart'}))
    return res


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
    if 'user' in session:
        # Kiem tra neu ton tai gia tri 'logged_in' trong session (User da dang nhap) thi goi ham getCart()
        session['cart'] = get_cart(session['user_id'])
        cart = session.get('cart', [])
        # Render file cart.html, truyen vao gia tri bien cart
        return render_template('cart.html', user=session['user_lname'], items=cart)
    else:
        # Neu khong ton tai gia tri 'logged_in' trong session (User chua dang nhap)
        # Redirect ve trang login va hien thong bao yeu cau dang nhap de xem gio hang
        return render_template('login-form.html', cartError=True)


@app.route('/checkout', methods=['GET'])
def checkout():
    if 'user' in session:
        session['cart'] = get_cart(session['user_id'])
        cart = session.get('cart', [])
        return render_template('checkout.html', user=session['user_lname'], fname=session['user_fname'],
                               email=session['user_email'], items=cart)
    else:
        return redirect(url_for('login'))


# Ham check_admin dung de kiem tra tai khoan admin da duoc dang nhap chua
def check_admin():
    # Kiem tra neu 'admin' co trong session (Tai khoan admin da duoc dang nhap)
    if 'admin' in session:
        # Neu co, tra ve gia tri True
        return True
    else:
        # Neu khong, tra ve gia tri False
        return False


def admin_result_to_dict(products):
    result = []
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for item in products:
        c.execute("SELECT img1 FROM images WHERE productId = ?", (item[0],))
        # Tim kiem anh san pham tu table images theo productId va luu vao bien img
        img = c.fetchone()[0]
        new_dict = {
            "productId": item[0], "productName": item[1], "productPrice": item[2], "quantity": item[3],
            "productImg": img
        }
        # Tao moi 1 bien dict voi kieu dictionary va them vao list result
        result.append(new_dict)
    conn.close()
    # Tra ve bien result
    return result


# Dinh tuyen ham admin_view cho url '/admin'
@app.route('/admin', methods=['GET'])
def admin_view():
    # Goi ham check admin de kiem tra session
    if check_admin():
        # Render file adminView.html, truyen vao gia tri cua session['lname']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("SELECT productId, name, price, quantity FROM products")
        products = c.fetchall()
        result = admin_result_to_dict(products)
        return render_template('adminView.html', admin=session['admin_lname'], items=result)
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
    search_text = request.form['search']
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute("SELECT productId, name, price, quantity FROM products WHERE name LIKE '%" + search_text + "%'")
    # Tim cac san pham co ten gan dung voi search va luu vao bien products
    products = c.fetchall()
    result = admin_result_to_dict(products)
    # Render file adminSearch.html, truyen vao gia tri cua bien result
    return render_template('adminSearch.html', admin=session['admin_lname'], items=result)


def check_none(text):
    if text == 'None' or text == '':
        return None
    else:
        return text


@app.route('/admin/update/<product_id>', methods=['GET', 'POST'])
def admin_update(product_id):
    if check_admin():
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == 'POST':
            team = check_none(request.form['team'])
            nation = check_none(request.form['nation'])
            name = request.form['name']
            price = request.form['price']
            quantity = request.form['quantity']
            size_title = request.form['sizeTitle']
            info_title = request.form['infoTitle']
            img1 = request.form['img1']
            img2 = request.form['img2']
            img3 = request.form['img3']
            img4 = request.form['img4']
            c.execute(
                "UPDATE products SET "
                "team = ?, nation = ?, name = ?, price = ?, quantity = ?, sizeTitle = ?, infoTitle = ? "
                "WHERE productId = ?",
                (team, nation, name, price, quantity, size_title, info_title, product_id,)
            )
            conn.commit()
            c.execute(
                "UPDATE images SET img1 = ?, img2 = ?, img3 = ?, img4 = ? WHERE productId = ?",
                (img1, img2, img3, img4, product_id,)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin_view'))
        else:
            c.execute(
                "SELECT team, nation, name, price, quantity, sizeTitle, infoTitle FROM products WHERE productId = ?",
                (product_id,)
            )
            item = c.fetchone()
            result = {
                "id": product_id, "team": item[0], "nation": item[1], "name": item[2], "price": item[3],
                "quantity": item[4], "sizeTitle": item[5], "infoTitle": item[6]
            }
            c.execute("SELECT img1, img2, img3, img4 FROM images WHERE productId = ?", (product_id,))
            imgs = c.fetchone()
            img = {"img1": imgs[0], "img2": imgs[1], "img3": imgs[2], "img4": imgs[3]}
            return render_template('adminUpdate.html', item=result, img=img)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/update/price/<product_id>', methods=['POST'])
def admin_price(product_id):
    if check_admin():
        req = request.get_json()
        new_price = req['price']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("UPDATE products SET price = ? WHERE productId = ?", (new_price, product_id))
        conn.commit()
        res = make_response(jsonify({"id": product_id, "price": new_price}))
        return res
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/update/quantity/<product_id>', methods=['POST'])
def admin_quantity(product_id):
    if check_admin():
        req = request.get_json()
        new_quantity = req['quantity']
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("UPDATE products SET quantity = ? WHERE productId = ?", (new_quantity, product_id))
        conn.commit()
        res = make_response(jsonify({"id": product_id, "quantity": new_quantity}))
        return res
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/delete/<product_id>', methods=['POST'])
def admin_delete(product_id):
    if check_admin():
        req = request.get_json()
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE productId = ?", (product_id,))
        conn.commit()
        c.execute("DELETE FROM images WHERE productId = ?", (product_id,))
        conn.commit()
        conn.close()
        return req
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    if check_admin():
        conn = sqlite3.connect(sqldbname)
        c = conn.cursor()
        if request.method == 'POST':
            team = check_none(request.form['team'])
            nation = check_none(request.form['nation'])
            name = request.form['name']
            price = request.form['price']
            quantity = request.form['quantity']
            size_title = request.form['sizeTitle']
            info_title = request.form['infoTitle']
            img1 = request.form['img1']
            img2 = request.form['img2']
            img3 = request.form['img3']
            img4 = request.form['img4']
            product_id = get_max_id('products')
            img_id = get_max_id('images')
            c.execute(
                "INSERT INTO products VALUES(?,?,?,?,?,?,?,?)",
                (product_id, team, nation, name, price, quantity, size_title, info_title,)
            )
            conn.commit()
            c.execute("INSERT INTO images VALUES(?,?,?,?,?,?)", (img_id, product_id, img1, img2, img3, img4))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_view'))
        else:
            return render_template('adminAdd.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    orderId = get_max_id('order')
    userId = 1
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()

    c.execute('SELECT productId, quantity FROM cart WHERE userId = 1')
    order = c.fetchall()
    lstId = []
    lstQuant = []
    for i in range(0, len(order)):
        lstId.append(order[i][0])
        lstQuant.append(order[i][1])
    newLstId = str(lstId)[1:-1]
    newLstQuant = str(lstQuant)[1:-1]

    c.execute('DELETE FROM cart WHERE userId = ?', (userId,))
    conn.commit()

    c.execute('insert into "order" values(?,?,?,?)', (orderId, userId, newLstId, newLstQuant))
    conn.commit()

    c.execute('select * from "order" where orderId = ?', (orderId,))
    order = c.fetchone()
    return jsonify(order)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
