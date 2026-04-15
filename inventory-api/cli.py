import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    print("\n1. View Items")
    print("2. Add Item")
    print("3. Delete Item")
    print("4. Fetch External Product")
    print("5. Exit")

while True:
    menu()
    choice = input("Choose: ")

    if choice == "1":
        res = requests.get(f"{BASE_URL}/items")
        print(res.json())

    elif choice == "2":
        name = input("Name: ")
        qty = int(input("Quantity: "))
        res = requests.post(f"{BASE_URL}/items",
                            json={"name": name, "quantity": qty})
        print(res.json())

    elif choice == "3":
        id = input("Item ID: ")
        res = requests.delete(f"{BASE_URL}/items/{id}")
        print(res.json())

    elif choice == "4":
        barcode = input("Barcode: ")
        res = requests.get(f"{BASE_URL}/external/{barcode}")
        print(res.json())

    elif choice == "5":
        break