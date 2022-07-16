#!/usr/bin/env python

import psycopg2
from psycopg2 import Error
import itertools
import os
from datetime import datetime

IMG_BASE = '/home/alex/damir-bot/admin_tg_bot/media/'


def get_product_detail(product_id):
    context_data = {}
    context_data['id'] = product_id

    cursor.execute(f"SELECT title FROM product_product WHERE id={product_id}")
    title = list(itertools.chain(*cursor.fetchall()))
    context_data['title'] = str(*title)

    cursor.execute(f"SELECT image FROM product_product WHERE id={product_id}")
    image = list(itertools.chain(*cursor.fetchall()))
    context_data['image'] = os.path.join(IMG_BASE, *image)

    cursor.execute(f"SELECT description FROM product_product WHERE id={product_id}")
    description = list(itertools.chain(*cursor.fetchall()))
    context_data['description'] = str(*description)

    cursor.execute(f"SELECT price FROM product_product WHERE id={product_id}")
    price = list(itertools.chain(*cursor.fetchall()))
    context_data['price'] = str(float(*price))

    cursor.execute(f"SELECT gender FROM product_product WHERE id={product_id}")
    gender = list(itertools.chain(*cursor.fetchall()))
    context_data['gender'] = str(*gender)

    cursor.execute(f"SELECT size FROM product_sizes WHERE s_id={product_id}")
    size = list(itertools.chain(*cursor.fetchall()))
    context_data['size'] = size

    cursor.execute(f"SELECT color FROM product_colors WHERE c_id={product_id}")
    color = list(itertools.chain(*cursor.fetchall()))
    context_data['color'] = color

    cursor.execute(f"SELECT oth_images FROM product_images WHERE p_id={product_id}")
    oth_images = list(itertools.chain(*cursor.fetchall()))
    context_data['oth_images'] = oth_images

    return context_data


def get_categories():
    cursor.execute("SELECT id, title FROM category_category")
    categories = list(itertools.chain(cursor.fetchall()))
    return categories


def get_id(table, data):
    cursor.execute(f"SELECT id FROM {table} WHERE title='{data}'")
    obj_id = list(itertools.chain(*cursor.fetchall()))
    return obj_id


def filter_table(table, data, gender):
    data = str(*data)
    cursor.execute(f"SELECT id, title FROM {table} WHERE (category_id='{data}') AND (gender='{gender}')")
    filtered = list(itertools.chain(cursor.fetchall()))
    return filtered


def save_sales(list_of_cart, contacts):
    for el in list_of_cart:
        id = el['id']
        title = el['title']
        size = el['size']
        color = el['color']
        price = el['price']
        created_at = str(datetime.now())
        contacts = contacts
        cursor.execute(f"""INSERT INTO sale_sale 
        (product_id, product_title, product_size, product_color, product_price, created_at, contacts)
        VALUES ({id}, '{title}', {size}, '{color}', '{price}', TIMESTAMP '{created_at}', '{contacts}')""")
        connection.commit()
    return


try:
    connection = psycopg2.connect(user="alex",
                                  password="Peaks",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="tg-bot")

    cursor = connection.cursor()

    # cursor.execute("SELECT title FROM product_product")
    # PRODUCTS = list(itertools.chain(*cursor.fetchall()))


except (Exception, Error) as error:
    print("Error working with PostgreSQL", error)
# finally:
#    if connection:
#        cursor.close()
#        connection.close()
