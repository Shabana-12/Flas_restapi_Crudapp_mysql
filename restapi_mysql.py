
from flask import jsonify, Flask
from flask import  request
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass@1New'
app.config['MYSQL_DB'] = 'librarysys'
mysql = MySQL(app)


# GET ALL
@app.route('/')
@app.route('/alldata', methods=['GET'])
def data():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# GET ONE


@app.route('/select/<id>', methods=['GET'])
def userone(id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM books WHERE BookId="+id)
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        
        
@app.route('/add', methods=['POST'])
def add_book():
	
	try:
		_json = request.json
		_bookid = _json['BookId']
		_bookname = _json['BookName']
		_total= _json['total']
		# validate the received values
		if _bookid and _bookname and _total and request.method == 'POST':
			
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
			# save edits
			sql = "INSERT INTO books(BookId,BookName, total) VALUES(%s, %s, %s)"
			data = (_bookid, _bookname, _total,)
			
			cur.execute(sql, data)
			mysql.connection.commit()
			resp = jsonify('Books added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
  
#Update
@app.route('/update/<id>', methods=['PUT'])
def updates(id):
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    _bookname = request.json['BookName']
    _total = request.json['total']
    query = "update books set BookName = %s, total = %s Where BookId = %s"
    val=(_bookname,_total,id,)
    cur.execute(query,val)
    mysql.connection.commit()
    output = {'_bookname' : request.json['BookName'], '_total' : request.json['total'], 'Message': 'Success'}


    return jsonify({'result' : output})

		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
	
	try:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("DELETE FROM books WHERE BookId=%s", (id,))
		mysql.connection.commit()
		resp = jsonify('Book deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	       

if __name__ == "__main__":
    app.run(debug=True)