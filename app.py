from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017'
mongo = MongoClient(app.config['MONGO_URI'])

API = '/api/v1'

@app.route('/', methods=['GET'])
def index():
    databases = mongo.list_database_names()
    return jsonify(databases)

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
    try:
        # Switch ke database yang diberikan dalam URL
        db = mongo[db_name]
        collections = db.list_collection_names()
        return jsonify(collections)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
