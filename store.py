from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/")
def index():
    return template("index.html")

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')

@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189250',
                             password='JXt2DCwAje',
                             db='sql11189250',
                             cursorclass=pymysql.cursors.DictCursor )

#List All Categories
@get('/categories')
def get_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS","CATEGORIES":result,"CODE":200})
    except:
        return json.dumps({"STATUS":"ERROR","MSG":"Internal Error","CODE":500})

#List All Products
@get('/products')
def get_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS":"SUCCESS","PRODUCTS":result,"CODE":200})
    except:
        return json.dumps({"STATUS":"ERROR","MSG":"Internal Error","CODE":500})

#Creating a Category
@post('/category')
def create_category():
    name = request.POST.get("name")
    if(name == ""):
        return json.dumps({"STATUS":"ERROR","MSG":"Name Parameter is missing","CODE":400})
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from categories where name = '{}';".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            if(len(result) == 0):
                sql2 = "INSERT into categories(name) values('{}');".format(name)
                cursor.execute(sql2)
                connection.commit()
                cat_id = cursor.lastrowid
                return json.dumps({"STATUS":"SUCCESS","CAT_ID":cat_id,"CODE":201,"MSG":"Category created successfully"})
            else:
                raise ValueError("category exists")
    except ValueError as e:
        return json.dumps({"STATUS":"ERROR","MSG":"Category already exists","CODE":200})
    except Exception as e:
        return json.dumps({"STATUS":"ERROR","MSG":"Internal Error","CODE":500})

#Delete a Category
@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE from categories where id = {};".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return json.dumps(
                    {"STATUS": "SUCCESS", "CODE": 201, "MSG": "The category was deleted successfully"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": repr(e) + "Internal Error", "CODE": 500})

run(host='localhost', port=8080)
