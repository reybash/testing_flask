from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://db:27017/")
db = client.mydatabase


@app.route("/api/<key>", methods=["GET", "POST", "PUT"])
def api(key):
    if request.method == "GET":
        value = db.mycollection.find_one({"_id": key})
        if value:
            return jsonify({key: value["_value"]})
        else:
            return jsonify({"message": "Key not found"}), 404

    elif request.method == "POST":
        data = request.json
        db.mycollection.insert_one({"_id": key, "_value": data["value"]})
        return jsonify({"message": "Created successfully"}), 201

    elif request.method == "PUT":
        data = request.json
        result = db.mycollection.update_one(
            {"_id": key}, {"$set": {"_value": data["value"]}}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Updated successfully"})
        else:
            return jsonify({"message": "Key not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
