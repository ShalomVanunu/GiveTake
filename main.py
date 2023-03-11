from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
import io



app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


cluster = MongoClient("mongodb+srv://MongoUser:Password1@clusterdb.ekaau.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster['givetake']
collection = db['products']
fs = GridFS(db)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    products = db.products.find()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        picture = request.files['picture']
        tel = request.form['tel']
        picture_id = fs.put(picture, content_type=picture.content_type, filename=picture.filename)
        db.products.insert_one({'name': name, 'details': details,'tel': tel, 'picture_id': picture_id})
        return redirect(url_for('index'))
    else:
        return render_template('add_product.html')

@app.route('/picture/<picture_id>')
def picture(picture_id):
    file = fs.get(ObjectId(picture_id))
    file_stream = io.BytesIO(file.read())
    if file:
        return send_file(file_stream, mimetype='image/jpeg')


if __name__ == '__main__':
    pass
    #app.run(debug=True, port=80, host="0.0.0.0")
