from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017'
mongo = MongoClient(app.config['MONGO_URI'])

API = '/api/v1'

@app.route('/', methods=['GET'])
def index():
    return "Hello!"

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    if data:
        # Dapatkan koleksi (collection) MongoDB
        mycollection = mongo.db.mycollection
        # Tambahkan data ke koleksi
        mycollection.insert_one(data)
        return jsonify({"message": "Data berhasil ditambahkan."})
    else:
        return jsonify({"message": "Data tidak valid."})

# get database from MONGO
@app.route(f'{API}/list_databases', methods=['GET'])
def list_databases():
    # Dapatkan daftar semua database
    databases = mongo.list_database_names()
    return jsonify(databases)

# Dapatkan daftar koleksi dari database tertentu
@app.route(f'{API}/collections/<db_name>', methods=['GET'])
def list_collections(db_name):
    if db_name not in mongo.list_database_names():
        return jsonify({"message": "Database Not Found."}),400
    try:
        # Switch ke database yang diberikan dalam URL
        db = mongo[db_name]
        collections = db.list_collection_names()
        return jsonify(collections)
    except Exception as e:
        return jsonify({"error": str(e)}),500

@app.route(f'{API}/data/<db_name>/<collection_name>', methods=['GET'])
def get_data(db_name, collection_name):
    if db_name not in mongo.list_database_names():
        return jsonify({"message": "Database Not Found."}),400
    try:
        # Switch ke database yang diberikan dalam URL
        db = mongo[db_name]

        if collection_name not in db.list_collection_names():
            return jsonify({"message": "Collection Not Found."}),400
        
        # Dapatkan koleksi yang diberikan dalam URL
        mycollection = db[collection_name]
        # Dapatkan semua data dari koleksi
        data = mycollection.find()
        # Buat list kosong untuk menampung data
        response = []
        # Tambahkan setiap data ke list
          # Dapatkan semua data dari koleksi
        data = list(mycollection.find())

        for d in data:
            # Ubah _id menjadi string
            d['_id'] = str(d['_id'])
            # Tambahkan data ke list
            response.append(d)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}),500

if __name__ == '__main__':
    app.run()
