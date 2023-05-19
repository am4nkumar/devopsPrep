from flask import Flask,jsonify, request
from db import db
from Product import Product
import configparser

def get_database_url():
    config = configparser.ConfigParser()
    config.read('/config/db.ini')
    database_configuration = config['mysql']
    host = database_configuration['host']
    username = database_configuration['username']
    db_password = open('/run/secrets/db_password')
    password = db_password.read()
    database = database_configuration['database']
    database_url = f'mysql://{username}:{password}@{host}/{database}'
    return database_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
db.init_app(app)

# curl http:/localhost:5000/products
@app.route('/products')
def get_products():
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


# curl http:/localhost:5000/product/1
@app.route('/product/<int:id>')
def get_product(id):
    product = Product.find_by_id(id)

    if product:
        return jsonify(product.json)
    return f'product wiht id {id} not found', 404

# curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:5000/product  , note : run in git bash!
@app.route('/product', methods =['POST'])
def post_product():
    request_product = request.json

    product = Product(None, request_product['name'])

    product.save_to_db()

    return jsonify(product.json), 201

# curl --header "Content-Type: application/json" --request PUT --data '{"name": "updated Product 2"}' -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods =['PUT'])
def put_product(id):
    existing_product = Product.find_by_id(id)
    if existing_product:
        updated_product = request.json
        existing_product.name = updated_product['name']
        existing_product.save_to_db()  
        return jsonify(existing_product.json), 200
    return f'product with id {id} not found', 404

# curl --request DELETE -v http:/localhost:5000/product/2
@app.route('/product/<int:id>', methods =['DELETE'])
def delete_product(id):
    existing_product = Product.find_by_id(id)
    if existing_product:
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Deleted product with id{id}'
        }), 200
   
    return f'product with id {id} not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')