from pymongo import MongoClient
from bson.objectid import ObjectId

MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "sneaker_market_db"

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

customers = db["customers"]
sneakers = db["sneakers"]


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Anna kokonaisluku.")


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Anna numero (esim. 199.99).")


def ask_bool(prompt: str) -> bool:
    val = input(prompt + " (y/n): ").strip().lower()
    return val in ("y", "yes", "k", "kylla", "kyllä", "true", "1")


def ask_object_id(prompt: str) -> ObjectId:
    while True:
        s = input(prompt).strip()
        try:
            return ObjectId(s)
        except Exception:
            print("Virheellinen _id. Kopioi _id sellaisenaan (24 heksamerkkiä).")


def add_customer():
    name = input("Nimi: ").strip()
    email = input("Email: ").strip()
    vip = ask_bool("VIP")
    res = customers.insert_one({"name": name, "email": email, "vip": vip})
    print("Lisätty customer _id =", res.inserted_id)


def list_customers():
    print("\nCUSTOMERS:")
    for c in customers.find():
        print(c["_id"], "|", c.get("name"), "|", c.get("email"), "| vip=", c.get("vip"))


def update_customer_vip():
    cid = ask_object_id("Customer _id: ")
    vip = ask_bool("Aseta VIP")
    res = customers.update_one({"_id": cid}, {"$set": {"vip": vip}})
    print("matched:", res.matched_count, "modified:", res.modified_count)


def delete_customer():
    cid = ask_object_id("Customer _id: ")
    res = customers.delete_one({"_id": cid})
    print("deleted:", res.deleted_count)


def add_sneaker():
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    size = ask_int("Size (int): ")
    price = ask_float("Price (number): ")
    in_stock = ask_int("In stock (int): ")

    doc = {
        "brand": brand,
        "model": model,
        "size": size,
        "price": price,
        "in_stock": in_stock
    }
    res = sneakers.insert_one(doc)
    print("Lisätty sneaker _id =", res.inserted_id)


def list_sneakers():
    print("\nSNEAKERS:")
    for s in sneakers.find():
        print(s["_id"], "|", s.get("brand"), s.get("model"),
              "| size=", s.get("size"),
              "| price=", s.get("price"),
              "| stock=", s.get("in_stock"))


def update_sneaker_stock():
    sid = ask_object_id("Sneaker _id: ")
    stock = ask_int("Uusi in_stock: ")
    res = sneakers.update_one({"_id": sid}, {"$set": {"in_stock": stock}})
    print("matched:", res.matched_count, "modified:", res.modified_count)


def delete_sneaker():
    sid = ask_object_id("Sneaker _id: ")
    res = sneakers.delete_one({"_id": sid})
    print("deleted:", res.deleted_count)


def menu():
    print("\n--- Sneaker Market (PyMongo) ---")
    print("1  List customers")
    print("2  Add customer")
    print("3  Update customer VIP")
    print("4  Delete customer")
    print("5  List sneakers")
    print("6  Add sneaker")
    print("7  Update sneaker stock")
    print("8  Delete sneaker")
    print("0  Exit")


def main():
    db.command("ping")

    while True:
        menu()
        choice = input("Valinta: ").strip()

        if choice == "1":
            list_customers()
        elif choice == "2":
            add_customer()
        elif choice == "3":
            update_customer_vip()
        elif choice == "4":
            delete_customer()
        elif choice == "5":
            list_sneakers()
        elif choice == "6":
            add_sneaker()
        elif choice == "7":
            update_sneaker_stock()
        elif choice == "8":
            delete_sneaker()
        elif choice == "0":
            print("Hei hei!, nähdään taas!")
            break
        else:
            print("Tuntematon valinta.")


if __name__ == "__main__":
    main()
