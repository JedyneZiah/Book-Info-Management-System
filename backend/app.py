from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt 
from flask_cors import CORS, cross_origin
from models import db, User, Book
 
app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'login-api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
 
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
  
bcrypt = Bcrypt(app) 
CORS(app, supports_credentials=True)
db.init_app(app)
  
with app.app_context():
    db.create_all()
 
@app.route("/")
def welcome():
    return "Welcome to Book Information System API"
 
@app.route("/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    password = request.json["password"]
 
    user_exists = User.query.filter_by(email=email).first() is not None
 
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409
     
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
 
    session["user_id"] = new_user.id
 
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })
 
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
  
    user = User.query.filter_by(email=email).first()
  
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
  
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
      
    session["user_id"] = user.id
  
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route("/books", methods=["POST"])
def create_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    published_year = data.get("published_year")

    if not title or not author:
        return jsonify({"error": "Title and Author are required"}), 400

    new_book = Book(title=title, author=author, published_year=published_year)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "published_year": new_book.published_year
    }), 201

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "published_year": book.published_year
        })
    return jsonify(book_list)

@app.route("/books/<string:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "published_year": book.published_year
    })

@app.route("/books/<string:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.json
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.published_year = data.get("published_year", book.published_year)

    db.session.commit()

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "published_year": book.published_year
    })

@app.route("/books/<string:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"}), 200
if __name__ == "__main__":
    app.run(debug=True)