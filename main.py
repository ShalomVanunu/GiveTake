from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from bson.objectid import ObjectId
from pymongo import MongoClient



app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


cluster = MongoClient("mongodb+srv://MongoUser:Password1@clusterdb.ekaau.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster['givetake']
collection = db['products']
print("Done")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    products = collection.find()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        picture = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                picture = filename
        product = {
            'name': name,
            'details': details,
            'picture': picture
        }
        collection.insert_one(product)
        return redirect(url_for('index'))
    return render_template('add_product.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #app.run(debug=True, port=80, host="0.0.0.0")
