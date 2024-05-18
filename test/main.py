from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests

app = Flask(__name__)
sqldbname = 'database.db'
app.secret_key = 'test'

# Dinh tuyen ham index cho url mac dinh
@app.route('/', methods=['get'])
def index():
    # Render file index.html khi trinh duyet tro den url '/' (url mac dinh)
    return render_template('index.html')

# Dinh tuyen ham team cho url '/team/ten doi bong' vd: '/team/manu'
@app.route('/team/<team>', methods=['get'])
def team(team):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE team = ?', (team,))
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



if __name__ == '__main__':
    app.run(debug=True, port=5000)