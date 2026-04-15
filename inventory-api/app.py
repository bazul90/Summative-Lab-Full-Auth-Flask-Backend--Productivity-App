from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = []
item_id = 1

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    global item_id
    data = request.json
    item = {
        "id": item_id,
        "name": data["name"],
        "quantity": data["quantity"],
        "barcode": data.get("barcode", "")
    }
    inventory.append(item)
    item_id += 1
    return jsonify(item), 201

# READ ALL
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(inventory)

# READ ONE
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    for item in inventory:
        if item["id"] == id:
            return jsonify(item)
    return {"error": "Item not found"}, 404

# UPDATE
@app.route('/items/<int:id>', methods=['PATCH'])
def update_item(id):
    data = request.json
    for item in inventory:
        if item["id"] == id:
            item.update(data)
            return jsonify(item)
    return {"error": "Item not found"}, 404

# DELETE
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    global inventory
    inventory = [item for item in inventory if item["id"] != id]
    return {"message": "Deleted"}

# EXTERNAL API
@app.route('/external/<barcode>', methods=['GET'])
def get_external(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    data = response.json()

    if data["status"] == 1:
        product = data["product"]
        return jsonify({
            "name": product.get("product_name"),
            "brand": product.get("brands")
        })
    return {"error": "Product not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)