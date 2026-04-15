#  Inventory Management System  
### Flask REST API + CLI + External API Integration

---

##  Project Overview

This project is a **Flask-based Inventory Management System** built for managing product stock in a small retail environment. It provides a REST API for CRUD operations, a CLI interface for user interaction, and integrates with an external product database (OpenFoodFacts API) to fetch real-time product information using barcodes.

---

##  Objectives

- Build a Flask REST API with full CRUD functionality
- Manage inventory items in memory
- Integrate external API for product lookup
- Build a CLI interface to interact with the system
- Implement unit tests for validation

---

##  System Architecture

CLI Application (cli.py)
        ↓
Flask REST API (app.py)
        ↓
In-Memory Inventory Store (Python list/dict)
        ↓
External API (OpenFoodFacts)

---

##  Project Structure

inventory-api/
│
├── app.py              # Flask REST API
├── cli.py              # Command Line Interface
├── test_app.py         # Unit tests
├── requirements.txt    # Dependencies
└── README.md           # Documentation

---

##  Installation

### 1. Clone Repository

git clone https://github.com/your-username/inventory-api.git
cd inventory-api

---

### 2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

---

### 3. Install Dependencies

pip install flask requests

OR

pip install -r requirements.txt

---

## ▶ Running the Application

### Start Flask API

python app.py

Server runs at:
http://127.0.0.1:5000

---

### Run CLI

python cli.py

---

##  API ENDPOINTS

---

### GET all items

GET /items

Response:
[
  {
    "id": 1,
    "name": "Milk",
    "quantity": 2,
    "barcode": "123456789"
  }
]

---

### POST add item

POST /items

Request:
{
  "name": "Peanut noodles",
  "quantity": 1,
  "barcode": "737628064502"
}

Response:
{
  "id": 1,
  "name": "Peanut noodles",
  "quantity": 1,
  "barcode": "737628064502"
}

---

### PUT update item

PUT /items/<id>

Request:
{
  "name": "Milk",
  "quantity": 10
}

Response:
{
  "id": 1,
  "name": "Milk",
  "quantity": 10,
  "barcode": ""
}

---

### DELETE item

DELETE /items/<id>

Response:
{
  "message": "Item deleted successfully"
}

---

##  EXTERNAL API INTEGRATION

### Endpoint

GET /external/<barcode>

Example:
GET /external/737628064502

Response:
{
  "name": "Thai peanut noodle kit includes stir-fry rice noodles & thai peanut seasoning",
  "brand": "Simply Asia, Thai Kitchen",
  "category": "Rice Noodles",
  "nutriscore": "d"
}

---

### External API Source

OpenFoodFacts API  
https://world.openfoodfacts.org/

---

##  CLI FEATURES

The CLI provides a menu-based system:

--- Inventory CLI ---
1. View Items
2. Add Item
3. Update Item
4. Delete Item
5. Fetch External Product
6. Exit

Features:
- Add inventory items
- View all items
- Update quantity
- Delete items
- Fetch product details using barcode

---

##  TESTING

Run tests using:

python -m unittest

Expected output:

....
----------------------------------------------------------------------
Ran X tests in 0.00s

OK

---



---

---
