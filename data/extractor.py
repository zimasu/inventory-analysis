import requests
import csv

from config import PRESTASHOP_BASE_URL, PRESTASHOP_API_KEY, INVENTORY_FILE, SALES_FILE

BASE_URL = PRESTASHOP_BASE_URL
API_KEY = PRESTASHOP_API_KEY


def fetch_list(resource):
    url = f"{BASE_URL}/{resource}?ws_key={API_KEY}&output_format=JSON"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[resource]


def fetch_one(resource, resource_id):
    url = f"{BASE_URL}/{resource}/{resource_id}?ws_key={API_KEY}&output_format=JSON"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[resource[:-1]]


def fetch_product_ids():
    items = fetch_list("products")
    ids = [item["id"] for item in items]
    print(f"Found {len(ids)} products")
    return ids


def fetch_product_details(product_ids):
    products = []
    for pid in product_ids:
        print(f"  Fetching product {pid}...")
        p = fetch_one("products", pid)
        name = p["name"][0]["value"] if isinstance(p["name"], list) else p["name"]
        products.append(
            {
                "id": p["id"],
                "reference": p.get("reference", ""),
                "name": name,
                "price": float(p["price"]),
                "wholesale_price": float(p["wholesale_price"]),
                "quantity": 0,
            }
        )
    return products


def fetch_stock(products):
    print("Fetching stock levels...")
    stock_map = {}
    stock_entries = fetch_list("stock_availables")
    for entry in stock_entries:
        s = fetch_one("stock_availables", entry["id"])
        product_id = int(s["id_product"])
        quantity = int(s["quantity"])
        stock_map[product_id] = stock_map.get(product_id, 0) + quantity
    for p in products:
        p["quantity"] = stock_map.get(int(p["id"]), 0)
    return products


def fetch_sales(products):
    print("Fetching sales history...")
    order_entries = fetch_list("orders")
    print(f"  Found {len(order_entries)} orders")
    order_date_map = {}
    for entry in order_entries:
        order = fetch_one("orders", entry["id"])
        order_id = int(order["id"])
        date_raw = order["date_add"]
        month = date_raw[:7]
        order_date_map[order_id] = month
    order_detail_entries = fetch_list("order_details")
    print(f"  Found {len(order_detail_entries)} order line items")
    sales_by_month = {}
    for entry in order_detail_entries:
        od = fetch_one("order_details", entry["id"])
        product_id = int(od["product_id"])
        quantity_sold = int(od["product_quantity"])
        order_id = int(od["id_order"])
        month = order_date_map.get(order_id, "unknown")
        key = (product_id, month)
        sales_by_month[key] = sales_by_month.get(key, 0) + quantity_sold
    total_sales_map = {}
    for (product_id, month), qty in sales_by_month.items():
        total_sales_map[product_id] = total_sales_map.get(product_id, 0) + qty
    for p in products:
        p["sales_volume"] = total_sales_map.get(int(p["id"]), 0)
    return products, sales_by_month


def save_sales_history_to_csv(sales_by_month, filename=SALES_FILE):
    if not sales_by_month:
        print("No sales history to save — no orders found.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "month", "units_sold"])
        writer.writeheader()
        for (product_id, month), units_sold in sorted(sales_by_month.items()):
            writer.writerow(
                {
                    "product_id": product_id,
                    "month": month,
                    "units_sold": units_sold,
                }
            )
    print(f"Saved sales history to {filename}")


def save_to_csv(products, filename=INVENTORY_FILE):
    if not products:
        print("Nothing to save — product list is empty.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} rows to {filename}")


if __name__ == "__main__":
    ids = fetch_product_ids()
    products = fetch_product_details(ids)
    products = fetch_stock(products)
    products, sales_by_month = fetch_sales(products)
    save_to_csv(products, INVENTORY_FILE)
    save_sales_history_to_csv(sales_by_month, SALES_FILE)
    print("Done!")
