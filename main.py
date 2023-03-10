from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'products.db'
UPLOAD_FOLDER = 'static/uploads/'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        picture = request.files['picture']
        filename = picture.filename
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute('INSERT INTO products (name, details, picture) VALUES (?, ?, ?)', (name, details, filename))
        db.commit()
        return redirect('/')
    else:
        return render_template('add_product.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  #  app.run(debug=True, port=80, host="0.0.0.0")
