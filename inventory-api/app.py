from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# In-memory database

inventory = []
next_id = 1



# HOME

@app.route('/')
def home():
    return jsonify({"message": "Inventory API running"}), 200



# CREATE ITEM

@app.route('/items', methods=['POST'])
def create_item():
    global next_id

    data = request.get_json()

    if not data or "name" not in data or "quantity" not in data:
        return jsonify({"error": "name and quantity required"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "quantity": data["quantity"],
        "barcode": data.get("barcode", "")
    }

    inventory.append(item)
    next_id += 1

    return jsonify(item), 201



# GET ALL ITEMS

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(inventory), 200



# GET SINGLE ITEM

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404



# UPDATE ITEM

@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json() or {}

    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404


# =========================
# DELETE ITEM
# =========================
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory

    for item in inventory:
        if item["id"] == item_id:
            inventory = [i for i in inventory if i["id"] != item_id]
            return jsonify({"message": "Item deleted"}), 200

    return jsonify({"error": "Item not found"}), 404



# EXTERNAL API (FIXED 403 + SAFE)

@app.route('/external/<barcode>', methods=['GET'])
def external_product(barcode):
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

        # FIX: 
        headers = {
            "User-Agent": "InventoryManagementSystem/1.0 (student project)"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return jsonify({
                "error": "External API request failed",
                "status_code": response.status_code
            }), 502

        try:
            data = response.json()
        except ValueError:
            return jsonify({
                "error": "Invalid JSON response from external API",
                "raw_response": response.text[:200]
            }), 502

        if data.get("status") == 1:
            product = data.get("product", {})

            return jsonify({
                "name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "category": product.get("categories", "Unknown"),
                "nutriscore": product.get("nutriscore_grade", "unknown")
            }), 200

        return jsonify({"error": "Product not found"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Network error contacting external API",
            "details": str(e)
        }), 500



# RUN APP

if __name__ == '__main__':
    app.run(debug=True)