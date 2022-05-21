from app import app
import pymysql
from auth import auth_required
from config import mysql
from flask import jsonify
from flask import request
import requests


@app.route('/createaddress', methods =['POST'])
@auth_required
def create_address():
    try:
        _json = request.json
        _street = _json['street']
        _number = _json['number']
        _city = _json['city']
        _country = _json['country']
        _clientkey = _json['clientkey']
        if _street and _number and _city and _country and _clientkey and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO address(street, number, city, country, clientkey) VALUES(%s,%s, %s, %s, %s)"
            bindData = (_street, _number, _city, _country, _clientkey)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Endereço adicionado!')
            response.status_code == 200
            return response
        else:
            return showMessage()
    except Exception as e:
       response = jsonify({"Message": f"{e}"})
       return response
    finally:
        cursor.close() 
        conn.close() 

@app.route('/address') 
@auth_required
def addresslist():
    try:  
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT  * FROM address;")
        cliRow = cursor.fetchall()  
        response = jsonify(cliRow)
        response.status_code == 200
        return response
    except Exception as e:
       reponse = jsonify({"Message": f"{e}"})
       return response
    finally:
        cursor.close()
        conn.close()

#select por id
@app.route('/address/<int:id_address>')
@auth_required
def address_detail(id_address):
    try:  
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_address, street, number, city, country, clientkey FROM address WHERE id_address=%s", id_address)
        cliRow = cursor.fetchall()  
        response = jsonify(cliRow)
        response.status_code == 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


    #######

@app.route('/updateaddress', methods=['PUT'])
@auth_required
def update_address():
    try:
        _json = request.json
        _id_address = _json['id_address']
        _street = _json['street']
        _number = _json['number']
        _city = _json['city']
        _country = _json['country']
        _clientkey  = _json['clientkey']
        if _street and _number and _city and _country and _id_address and request.method == 'PUT':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE address SET street=%s, number=%s, city=%s, country=%s clientkey=%s WHERE id_address=%s"
            bindData = (_street, _number, _city, _country, _id_address, _clientkey)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Address Updated!')
            response.status_code == 200
            return response
        else:
            return showMessage()
    except Exception as e:
       reponse = jsonify({"Message": f"{e}"})
       return reponse
    finally:
        cursor.close() 
        conn.close() 

@app.route('/deleteaddress/<int:id_address>', methods=['DELETE'])
@auth_required
def delete_address(id_address):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM address WHERE id_address =%s", (id_address,))
		conn.commit()
		response = jsonify('Address deleted successfully!')
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
    



@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


    
if __name__ == "__main__":
    app.run(debug=True)