import requests

BASE_URL = "http://127.0.0.1:5000"

def safe_print_response(res):
    try:
        if res.headers.get("Content-Type", "").startswith("application/json"):
            print(res.json())
        else:
            print("Non-JSON response:")
            print(res.text)
    except Exception:
        print("Error reading response:")
        print(res.text)


def menu():
    print("\n--- Inventory CLI ---")
    print("1. View Items")
    print("2. Add Item")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Fetch External Product")
    print("6. Exit")


while True:
    menu()
    choice = input("Choose: ")

    try:
        if choice == "1":
            res = requests.get(f"{BASE_URL}/items")
            safe_print_response(res)

        elif choice == "2":
            name = input("Name: ")
            qty = int(input("Quantity: "))
            res = requests.post(f"{BASE_URL}/items",
                                json={"name": name, "quantity": qty})
            safe_print_response(res)

        elif choice == "3":
            item_id = input("Item ID: ")
            qty = int(input("New Quantity: "))
            res = requests.patch(f"{BASE_URL}/items/{item_id}",
                                 json={"quantity": qty})
            safe_print_response(res)

        elif choice == "4":
            item_id = input("Item ID: ")
            res = requests.delete(f"{BASE_URL}/items/{item_id}")
            safe_print_response(res)

        elif choice == "5":
            barcode = input("Barcode: ")
            res = requests.get(f"{BASE_URL}/external/{barcode}")
            safe_print_response(res)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

    except requests.exceptions.ConnectionError:
        print(" Error: Flask server is not running.")
        print(" Run: python app.py")

    except ValueError:
        print(" Invalid input. Quantity must be a number.")