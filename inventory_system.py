

import json
from datetime import datetime


# Global variable to store inventory stock data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add quantity of an item to stock_data with validation and logging.
    """
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid item type or quantity type")
        return
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Remove quantity from item in stock_data, remove item if depleted.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Item '{item}' not found in inventory.")


def get_qty(item):
    """
    Return quantity of specified item.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from JSON file and return it.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"File {file} not found. Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file}. Starting with empty inventory.")
        return {}


def save_data(file="inventory.json"):
    """
    Save inventory data to JSON file.
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data))


def print_data():
    """
    Print inventory report.
    """
    print("Items Report")
    for item, qty in stock_data.items():
        print(item, "->", qty)


def check_low_items(threshold=5):
    """
    Return list of items with quantity below threshold.
    """
    result = []
    for item, qty in stock_data.items():
        if qty < threshold:
            result.append(item)
    return result


def main():
    """
    Demonstrate inventory system usage.
    """
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, now safely ignored
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()

    # Update the contents of stock_data dict in place to avoid global keyword
    loaded = load_data()
    stock_data.clear()
    stock_data.update(loaded)

    print_data()
    print("Eval-unsafe code removed for security.")


if __name__ == "__main__":
    main()

