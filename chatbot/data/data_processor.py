import json
import pandas as pd
import logging
import re
import sqlite3
from .product_catalog import add_product, create_tables, get_db_connection

logging.basicConfig(level=logging.INFO)

def extract_price(price_string):
    # Extract the first occurrence of a price (assumes $ is used)
    match = re.search(r'\$\s*(\d+(?:\.\d{2})?)', price_string)
    if match:
        return float(match.group(1))
    return 0  # Default price if no match is found

def preprocess_product_data(file_path, category):
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data = pd.read_excel(file_path).to_dict('records')
    else:
        raise ValueError("Unsupported file format. Please use JSON or Excel.")

    processed_data = []
    for index, item in enumerate(data, start=1):
        if category == 'curtain_driver':
            price_string = str(item.get('Text1', '0'))
            processed_item = {
                'id': f'DRIVER{index:04d}',
                'name': item.get('Text', ''),
                'price': extract_price(price_string),
                'description': item.get('Text2', ''),
                'image_url': item.get('Image_URL', ''),
                'categories': [category]
            }
        else:
            try:
                price = float(item.get('Text1', 0))
            except ValueError:
                price = 15.5  # Default price if conversion fails

            processed_item = {
                'id': f'{category.upper()}{index:04d}',
                'name': item.get('Text', ''),
                'price': price,
                'description': item.get('Text2', ''),
                'image_url': item.get('Image_URL', ''),
                'categories': [category]
            }
        processed_data.append(processed_item)

    return processed_data

def import_product_data(file_path, product_type):
    create_tables()  # Ensure tables exist
    
    if file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except UnicodeDecodeError:
            # If UTF-8 fails, try with ISO-8859-1 encoding
            with open(file_path, 'r', encoding='iso-8859-1') as file:
                data = json.load(file)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path).to_dict('records')
    else:
        raise ValueError("Unsupported file format. Please use JSON or XLSX.")

    # Print the structure of the first item
    if data:
        print(f"Structure of the first item in {product_type} data:")
        print(json.dumps(data[0], indent=2))

    conn = get_db_connection()
    cursor = conn.cursor()

    for index, item in enumerate(data, start=1):
        # Generate a product ID if 'id' is not present
        product_id = f"{product_type.upper()}{index:04d}"
        name = item.get('name', '')
        price = item.get('price', 0.0)
        description = item.get('description', '')
        image_url = item.get('image', '')

        cursor.execute('''
        INSERT OR REPLACE INTO products (id, name, price, description, image_url)
        VALUES (?, ?, ?, ?, ?)
        ''', (product_id, name, price, description, image_url))

    conn.commit()
    conn.close()

    print(f"Imported {len(data)} {product_type} into the database.")

def import_ikea_curtain_data(file_path):
    data = pd.read_excel(file_path)
    for index, row in data.iterrows():
        add_product(
            id=f"DRIVER{index+1:04d}",
            name=row['Text'],
            price=float(row['Text1']),
            categories=['curtain_driver'],
            description=row['Text2'],
            image_url=row.get('Image_URL', '')  # Assuming there might be an Image_URL column
        )
    print(f"Imported {len(data)} IKEA curtain drivers into the database.")
