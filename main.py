from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field
import math

app = FastAPI()

# =========================================================
# Q1 — Home Route (GET + JSON)
# =========================================================
@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}


# =========================================================
# DATA STORAGE
# =========================================================
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 250, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 120, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Brownie", "price": 90, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Chicken Pizza", "price": 350, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "Fries", "price": 100, "category": "Snack", "is_available": True}
]

orders = []
order_counter = 1
cart = []


# =========================================================
# Q7 — Helper Functions (NO decorators)
# =========================================================

# Find menu item by ID
def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None

# Calculate bill (Q9 logic included)
def calculate_bill(price, quantity, order_type="delivery"):
    total = price * quantity
    if order_type == "delivery":
        total += 30   # delivery charge
    return total

# Filter logic (Q10)
def filter_menu_logic(category, max_price, is_available):
    result = []
    for item in menu:
        if category is not None and item["category"] != category:
            continue
        if max_price is not None and item["price"] > max_price:
            continue
        if is_available is not None and item["is_available"] != is_available:
            continue
        result.append(item)
    return result


# =========================================================
# Q2 — GET All Menu Items
# =========================================================
@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}


# =========================================================
# Q5 — Menu Summary (must be above /menu/{id})
# =========================================================
@app.get("/menu/summary")
def menu_summary():
    available = len([i for i in menu if i["is_available"]])
    categories = list(set([i["category"] for i in menu]))

    return {
        "total_items": len(menu),
        "available_items": available,
        "unavailable_items": len(menu) - available,
        "categories": categories
    }


# =========================================================
# Q10 — Filter Menu (Query params + helper)
# =========================================================
@app.get("/menu/filter")
def filter_menu(category: str = None, max_price: int = None, is_available: bool = None):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}


# =========================================================
# Q16 — Search Menu
# =========================================================
@app.get("/menu/search")
def search_menu(keyword: str):
    result = [
        i for i in menu
        if keyword.lower() in i["name"].lower()
        or keyword.lower() in i["category"].lower()
    ]

    if not result:
        return {"message": "No items found"}

    return {"items": result, "total_found": len(result)}


# =========================================================
# Q17 — Sort Menu
# =========================================================
@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_items = sorted(menu, key=lambda x: x[sort_by], reverse=(order == "desc"))

    return {
        "items": sorted_items,
        "sort_by": sort_by,
        "order": order
    }


# =========================================================
# Q18 — Pagination
# =========================================================
@app.get("/menu/page")
def paginate_menu(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    total_pages = math.ceil(len(menu) / limit)

    return {
        "page": page,
        "limit": limit,
        "total_items": len(menu),
        "total_pages": total_pages,
        "items": menu[start:start + limit]
    }


# =========================================================
# Q20 — Combined (Search + Sort + Pagination)
# =========================================================
@app.get("/menu/browse")
def browse_menu(keyword: str = None, sort_by: str = "price", order: str = "asc", page: int = 1, limit: int = 4):

    data = menu

    # filter
    if keyword:
        data = [i for i in data if keyword.lower() in i["name"].lower()]

    # sort
    data = sorted(data, key=lambda x: x[sort_by], reverse=(order == "desc"))

    # pagination
    start = (page - 1) * limit
    total_pages = math.ceil(len(data) / limit)

    return {
        "page": page,
        "total_pages": total_pages,
        "items": data[start:start + limit]
    }


# =========================================================
# Q3 — GET Menu Item by ID
# =========================================================
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    return item


# =========================================================
# Q4 — GET Orders
# =========================================================
@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# =========================================================
# Q19 — Orders Search & Sort
# =========================================================
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    return {"orders": result}


@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=(order == "desc"))
    return {"orders": sorted_orders}


# =========================================================
# Q6 — Pydantic Model (Validation)
# =========================================================
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"   # Q9


# =========================================================
# Q11 — New Menu Item Model
# =========================================================
class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


# =========================================================
# Q15 — Checkout Model
# =========================================================
class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


# =========================================================
# Q8 — Create Order (POST)
# =========================================================
@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)
    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order


# =========================================================
# Q11 — Add Menu Item (POST)
# =========================================================
@app.post("/menu")
def add_item(item: NewMenuItem, response: Response):

    for i in menu:
        if i["name"].lower() == item.name.lower():
            return {"error": "Duplicate item"}

    new_id = max(i["id"] for i in menu) + 1
    new_item = item.dict()
    new_item["id"] = new_id

    menu.append(new_item)
    response.status_code = 201

    return new_item


# =========================================================
# Q12 — Update Menu Item (PUT)
# =========================================================
@app.put("/menu/{item_id}")
def update_item(item_id: int, price: int = None, is_available: bool = None):

    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


# =========================================================
# Q13 — Delete Menu Item
# =========================================================
@app.delete("/menu/{item_id}")
def delete_item(item_id: int):

    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted successfully"}


# =========================================================
# Q14 — Cart System
# =========================================================
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):

    item = find_menu_item(item_id)
    if not item or not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Cart updated"}

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Item added to cart"}


@app.get("/cart")
def get_cart():
    total = 0

    for c in cart:
        item = find_menu_item(c["item_id"])
        total += item["price"] * c["quantity"]

    return {"cart": cart, "grand_total": total}


# =========================================================
# Q15 — Remove & Checkout
# =========================================================
@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):

    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Item removed"}

    return {"error": "Item not found in cart"}


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        return {"error": "Cart is empty"}

    placed_orders = []
    total = 0

    for c in cart:
        item = find_menu_item(c["item_id"])
        price = item["price"] * c["quantity"]
        total += price

        new_order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "total_price": price
        }

        orders.append(new_order)
        placed_orders.append(new_order)
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": placed_orders, "grand_total": total}