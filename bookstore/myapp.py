from flask import Flask
from flask import render_template
from flask import redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
import os
import werkzeug
from werkzeug.utils import secure_filename
app = Flask(__name__ )

# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/books")
# def bookstore():
#     return books

# @app.route("/books/<int:id>")
# def books_profile(id):
#     booklist=list(filter(lambda book: book['id']==id,books))
#     print(booklist)
#     if booklist:
#         return booklist[0]
#     return "Book Not Found"

# @app.route("/books/home")
# def books_home():
#     return render_template("books/home.html", books=books )



# @app.route("/books/land")
# def books_land():
#     return render_template("books/landing.html", books=books )
                        
            
# @app.route("/bookstore/<int:id>", endpoint="books.show")
# def books_show(id):
#     bookshow=list(filter(lambda book: book['id']==id,books))
#     print(bookshow)
#     if bookshow:
#         return render_template("books/details.html",books=bookshow[0])
#     return "Book Not Found"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/books/images/'

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///project.db"
db=SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    num_pages = db.Column(db.Integer)  
    price = db.Column(db.Float)       
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    def __repr__(self):
        return f"Book(id={self.id}, name={self.name})" 

    def __str__(self):
        return f"{self.name}"
    
@app.route("/dbooks", endpoint='books.index')
def books_index():
    bookss=Book.query.all()
    return render_template("books/book.html", bookss=bookss)
    
@app.route("/dbooks/<int:id>", endpoint='books.showw')
def books_showw(id):
    book = Book.query.get_or_404(id)  
    if book:
        return render_template("books/show.html", book=book,num_pages=book.num_pages, price=book.price)


@app.errorhandler(404)
def get_404(error):
    return render_template("error404.html")

@app.route("/delete/<int:id>", endpoint='books.delete')
def delete_book(id):
    book_to_delete = Book.query.get_or_404(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('books.index'))

@app.route("/books/create", methods=['GET', 'POST'], endpoint='books.create')
def create_book():
    if request.method == 'POST':
        name = request.form['name']
        image_file = request.files['image']
        num_pages = request.form.get('num_pages')
        price = request.form.get('price')

        if image_file:
            filename = (image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            image_path = None
        book = Book(name=name, image=image_path, num_pages=num_pages, price=price, created_at=datetime.utcnow())
        
        db.session.add(book)
        db.session.commit()
        
        return redirect(url_for('books.index'))
    
    return render_template("books/create.html")


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['image']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             flash('File successfully uploaded')
#             return redirect(url_for('upload_file'))
#         else:
#             flash('Invalid file format')
#     return render_template('upload.html')

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/booksedit/<int:id>", methods=['GET', 'POST'], endpoint='books.edit')
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.name = request.form.get('name')
        book.price = request.form.get('price')
        book.num_pages = request.form.get('num_pages')
        
        
        image = request.files.get('image')
        if image:
            
            image_filename = werkzeug.utils.secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            book.image = image_filename

        
        book.updated_at = datetime.utcnow()

        db.session.commit()
        return redirect(url_for('books.index'))
    
    return render_template("books/edit.html", book=book)

    


if __name__ == '__main__':
    app.run(debug=True)