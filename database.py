import mysql.connector as sql
# print("import successful")

conn = sql.connect(
  host = "127.0.0.1",
  port = "3306",
  user = "root",
  password = "",
  database = "jonzing_vault"
)

mycursor = conn.cursor()
conn.autocommit = True
# print("Database connection successful")


# query = "CREATE DATABASE Jonzing_vault"
# mycursor.execute(query)
# print("Database creation successful")

#Users Table
# query = """CREATE TABLE Users_table(
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     fullname VARCHAR(100) NOT NULL,
#     address VARCHAR(100) NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     email VARCHAR(50) UNIQUE NOT NULL,
#     role ENUM("admin", "vendor", "customer") NOT NULL DEFAULT "customer",
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""



# Product Table
# query = """CREATE TABLE Product_table(
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     product VARCHAR(100) NOT NULL,
#     description VARCHAR(200) NOT NULL,
#     category VARCHAR(100) NOT NULL,
#     quantity VARCHAR (10) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""

# query = "ALTER TABLE Product_table ADD COLUMN price DECIMAL(10,2) NOT NULL"
# mycursor.execute(query)
# print("Column added successfully")


# Carts Table
# query = """CREATE TABLE carts_table(
#     cart_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     product_id INT NOT NULL,
#     description VARCHAR(200) NOT NULL,
#     order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES Users_table(id),
#     FOREIGN KEY (product_id) REFERENCES Product_table(id)
#     )
#     """


# Order Table
# query = """CREATE TABLE order_table(
#     order_id INT AUTO_INCREMENT PRIMARY KEY,
#     product_id INT NOT NULL,
#     status ENUM('pending','delivered', 'cancelled') NOT NULL DEFAULT 'pending',
#     ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""


# Order Item Table
query = """CREATE TABLE order_item_table(
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users_table(id),
    FOREIGN KEY (product_id) REFERENCES Product_table(id),
    FOREIGN KEY (order_id) REFERENCES order_table(order_id)
    )
    """



mycursor.execute(query)
print("Table created successfully")

