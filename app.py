from flask import Flask, jsonify, request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from BookModel import *
from UserModel import *
from settings import *
import json
from settings import *
import jwt
import datetime


app.config['SECRET_KEY'] = 'meow'




@app.route('/login', methods=['POST'])
def get_token():
	request_data = request.get_json()
	username = str(request_data['username'])
	password = str(request_data['password'])

	user  = User.query.filter_by(username=username).first()

	if not user or not check_password_hash(user.password, password):
		return Response('', 401, mimetype='application/json')
	else:	
		expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
		token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
		return token


def validStatusObject(statusObject):
	if ("status" in statusObject):
		return True
	else:
		return False


@app.route('/books')
def get_books():
	token = request.args.get('token')
	try:
		jwt.decode(token, app.config['SECRET_KEY'])
	except:
		invalidToeknErrorMsg = {
		"error" : "Need a valid token."
		}
		response = Response(json.dumps(invalidToeknErrorMsg), status=401, mimetype='application/json')
		return response
	return jsonify({'books': Book.get_all_books()})



def validBookObject(bookObject):
	if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
	else:
		return False

# /books/isbn_number
@app.route('/books/add', methods=['POST'])
def add_book():
	request_data = request.get_json(())
	if (validBookObject(request_data)):
		Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
		response = Response("", 201, mimetype='application/json')
		response.headers['Location'] = "/books/" + str(request_data['isbn'])
		return response
	else:
		invalidBookObjectErrorMsg = {
		"error" : "Inavlid book object passed in request",
		"helpString" : "Data passed in similar to this {'name' : 'bookname', 'price': 7.99, 'isbn' : 234243234}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response

@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
	return_value = Book.get_book(isbn)
	return jsonify(return_value)

#PUT /books/989713318
# {
# 	'name' : 'The Sydney life',
# 	'price' : 80.77
# }

def valid_put_request_data(request_data):
	if ("name" in request_data and "price" in request_data):
		return True
	else:
		False

def valid_patch_request_data(request_data):
	if ("name" in request_data and "price" in request_data):
		return True
	else:
		False

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	
	if (not valid_put_request_data(request_data)):
		invalidBookObjectErrorMsg = {
		"error" : "valid book object must be passed in the request",
		"helpString" : "Data passed in similar to this {'name' : 'bookname', 'price' : 7.99}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response
	Book.replace_book(isbn, request_data['name'], request_data['price'])
 
	response = Response("", status=204)
	return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	if (not valid_patch_request_data(request_data)):
		invalidBookObjectErrorMsg = {
		"error" : "valid book object must be passed in the request",
		"helpString" : "Data passed in similar to this {'name' : 'bookname', 'price' : 7.99}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response

	if ("name" in request_data):
		Book.update_book_name(isbn, request_data['name'])

	if ("price" in request_data):
		Book.update_book_price(isbn, request_data['price'])

	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response

#DELETE /books/<int:page_number>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
	if (Book.delete_book(isbn)):
		response = Response("", status=204)

	invalidBookObjectErrorMsg = {
	"error" : "Book with the ISBN number that was provided that was not found"
	}
	response = Response( invalidBookObjectErrorMsg , status=400, mimetype='application/json')
	return response


@app.route('/demo')
def test():
	return Response('True', status=200)



app.run(port=5000)