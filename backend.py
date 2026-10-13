import random as rd
import os
import datetime as dt


import bcrypt
import smtplib
import pyttsx3
from email.mime.text import MIMEText

import mysql.connector as sql
import speech_recognition as sr
import re
# print("Database connection successful")

# conn = sql.connect(
#     host = "127.0.0.1",
#     port = "3306",
#     user = "root",
#     password = "",
#     database = "Jonzing_vault"
#     )

# mycursor = conn.cursor(dictionary=True)
# conn.autocommit = True
# print("database connection successful")

# query = "ALTER TABLE product_table DROP COLUMN name "
# mycursor.execute(query)

# query = "ALTER TABLE Product_table ADD CONSTRAINT product UNIQUE(product)"
# mycursor.execute(query)



class Ecom:
        current_time = str(dt.datetime.now())
        
        def __init__(self, shop_name):
            self.Shop_name = shop_name
        
    
            try:
                self.conn = sql.connect(
                    host="127.0.0.1",
                    port="3306",
                    user="root",
                    password="",
                    database="Jonzing_vault"
                )
                self.mycursor = self.conn.cursor(dictionary=True)
                self.conn.autocommit = True
                print("Database connection successful")
            except sql.Error as e:
                print(f"Database connection failed: {e}")
                raise

            self.otp_store = {}
 

        
       

        def listen(self):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
                return ""
            except sr.RequestError:
                print("Speech service unavailable.")
                return ""


        def send_email(self, to_email, subject, body):
            sender_email = "samadadebisi2025@gmail.com"
            sender_password = "quoxddasqocraduj"

            try:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = to_email

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
                server.quit()
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")


        def speak(self, text):    
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                  print(f"Voice output failed: {e}")


        def is_valid_email(self, email):
            pattern = r"^[a-zA-Z][\w\.-]*@[\w\.-]+\.[a-zA-Z]{2,3}$"
            return re.match(pattern, email) is not None

        def is_valid_password(self, password):
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]).{8,}$"
            return re.match(pattern, password) is not None

        def hash_password(self, password):
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            return hashed.decode("utf-8")

        def check_password(self, password, hashed_password):
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

        def suggest_password(self):
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            digits = "0123456789"
            special = "!@#$%^&*"

            password_chars = [
                rd.choice(lowercase),
                rd.choice(uppercase),
                rd.choice(digits),
                rd.choice(special)
            ]

            all_chars = lowercase + uppercase + digits + special
            for _ in range(6):
                password_chars.append(rd.choice(all_chars))

            rd.shuffle(password_chars)
            return "".join(password_chars)

        def email_exists(self, email):
            try:
                query = "SELECT * FROM users_table WHERE email = %s"
                self.mycursor.execute(query, (email,))
                existing_user = self.mycursor.fetchone()
                return existing_user is not None
            except sql.Error as e:
                print(f"Database error: {e}")
                return False

        def send_otp(self, email, fullname):
            otp = str(rd.randint(100000, 999999))
            self.otp_store[email] = otp

            email_body = f"""
            Hi {fullname},

            Your One-Time Password (OTP) for account verification is: {otp}

            Please enter this code to complete your registration.
            """
            self.send_email(email, "Your OTP Verification Code", email_body)

        def verify_otp(self, email, entered_otp):
            correct_otp = self.otp_store.get(email)

            if correct_otp is None:
                return False

            if entered_otp.strip() == correct_otp:
                del self.otp_store[email]
                return True

            return False


        def Create_Account(self, fullname, address, password, email, role):
            if not self.is_valid_email(email):
                return{
                    "status": False,
                    "message": "Invalid email format"
                }

            if not self.is_valid_password(password):
                return{
                    "status": False,
                    "message": "Password must be at least 8 characters and include uppercase, lowercase, a number, and a special character"
                }
                    
            query = "SELECT * FROM users_table WHERE email = %s"
            self.mycursor.execute(query, (email,))
            existing_users = self.mycursor.fetchone()
            
            if existing_users:
                    return{
                        "status": False,
                        "message": "email Aready exist"
                    }

            try:   
                hashed_password = self.hash_password(password)
                query = "INSERT INTO users_table(fullname, address, password, email, role) VALUES(%s,%s,%s,%s,%s)"  
                values = (fullname, address, hashed_password, email, role) 
                self.mycursor.execute(query,values)
                self.conn.commit()

                email_body = f"""
                    
                Hi {fullname},
                Your Sign up is complete

                            NOTE####
                    We do not discriminate when offering our services,
                    we buy anything you're willing to sell including your DIGNITY

                    """
        
                self.send_email(email, "Welcome to Jonzing Dope Market!", email_body)
            
                return{
                    "status" : True,
                    "message": "Registration successful"
                }
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }


        
        def login_account(self, email, password):
            if email == "admin" and password == "admin123":
                return {
                    "status": True,
                    "message": "Admin login successful",
                    "role": "admin"
                }


            try:
                query = "SELECT * FROM users_table WHERE email = %s"
                value = (email,)
                self.mycursor.execute(query, value)
                user = self.mycursor.fetchone()

                if not user:
                    return {
                        "status": False,
                        "message": "Invalid details"
                    }

                if not self.check_password(password, user["password"]):
                    return {
                        "status": False,
                        "message": "Invalid details"
                    }

                return {
                    "status": True,
                    "message": f"Login successful, welcome {user['fullname']}",
                    "role": "user",
                    "user": user
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }

            
        def ins_product(self, product, description, category, quantity, price):
            try:
                query = "SELECT * FROM product_table WHERE product=%s"
                #  values = (email)
                self.mycursor.execute(query,(product,))
                product_table = self.mycursor.fetchone()
                if product_table:
                    pr_query = "UPDATE product_table SET quantity = quantity + %s WHERE product = %s"
                    self.mycursor.execute(pr_query,(quantity,product))
                    return{
                        "status": True,
                        "message": f"{product} quantity added"
                    }
                in_query = "INSERT INTO product_table (product, description, category, quantity, price)VALUES(%s, %s, %s, %s, %s)"
                in_values = (product, description, category, quantity, price)
                self.mycursor.execute(in_query,in_values)
                return{
                    "status":True,
                    "message": "Product added successfully"
                }

            except sql.Error as e:
                    return {
                        "status": False,
                        "message": f"Database error: {e}"
                    }

             
        
        def view_all_prod(self):
            try:
                query = "SELECT * FROM product_table"
                self.mycursor.execute(query)
                products = self.mycursor.fetchall()

                if not products:
                    return{
                        "status":False,
                        "message":"Product not available"
                    }
                
                
                final_message = ""

                for product_table in products:
                    final_message = final_message + f"""
                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        Product_ID : {product_table["id"]}
                        Product_name : {product_table["product"]}
                        Category : {product_table["category"]}
                        Product_Description : {product_table["description"]}
                        Price : {product_table["price"]}
                        """  
                return{
                        "status":True,
                        "message": final_message
                }
                 
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }


        

        def view_all_users(self):
            try:
                query = "SELECT * FROM users_table"
                self.mycursor.execute(query)
                users = self.mycursor.fetchall()

                if not users:
                    return{
                        "status":False,
                        "message":"No users available"
                    }
                
                for user in users:
                    print(f"""
            --------------------------
            User_ID : {user["id"]}
            Fullname : {user["fullname"]}
            Email : {user["email"]}
            Address : {user["address"]}
            Role : {user["role"]}
            """)

                return{
                    "status":True,
                    "message":"All users listed above"
                }   
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



        def view_all_orders(self):
                try:
                    query = "SELECT * FROM order_table"
                    self.mycursor.execute(query)
                    orders = self.mycursor.fetchall()

                    if not orders:
                        return{
                            "status":False,
                            "message":"No orders available"
                        }

                    print(orders)

                    return{
                        "status":True,
                        "message":"All orders listed above"
                    }

                except sql.Error as e:
                        return {
                            "status": False,
                            "message": f"Database error: {e}"
                        }



        def update_order_status(self, order_id, new_status):
            try:
                query = "SELECT * FROM order_table WHERE order_id = %s"
                self.mycursor.execute(query, (order_id,))
                order = self.mycursor.fetchone()

                if not order:
                    return{
                        "status":False,
                        "message":"Order not found"
                    }

                update_query = "UPDATE order_table SET status = %s WHERE order_id = %s"
                self.mycursor.execute(update_query, (new_status, order_id))
                self.conn.commit()
            
                return{
                    "status":True,
                    "message":f"Order {order_id} marked as {new_status}"
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }
 

                    

        def delete_user(self, email):
            try:
                query = "SELECT * FROM users_table WHERE email = %s"
                self.mycursor.execute(query, (email,))
                user = self.mycursor.fetchone()

                if not user:
                    return{
                        "status":False,
                        "message":"User not found"
                    }
                
                query = "DELETE FROM users_table WHERE email = %s"
                self.mycursor.execute(query, (email,))
                self.conn.commit()

                return{
                    "status":True,
                    "message":"User deleted successfully"
                }
            
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }
    



        def reset_password(self, email, new_password):
            try:
                query = "SELECT * FROM users_table WHERE email = %s"
                self.mycursor.execute(query, (email,))
                user = self.mycursor.fetchone()

                if not user:
                    return{
                        "status":False,
                        "message":"User not found"
                    }
                
                query = "UPDATE users_table SET password = %s WHERE email = %s"
                self.mycursor.execute(query, (new_password, email))
                self.conn.commit()

                return{
                    "status":True,
                    "message":"Password reset successfully"
                }
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



      

# User Section
        

        def all_available_products(self):
            try:
                query = "SELECT * FROM product_table WHERE quantity > 0"
                self.mycursor.execute(query)
                products = self.mycursor.fetchall()

                if not products:
                    return{
                        "status":False,
                        "message":"No products currently available"
                    }

                print(products)

                return{
                    "status":True,
                    "message":"Available products listed above"
                }
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



        def search_product(self, search_prod):
            try:
                query = "SELECT * FROM product_table WHERE product = %s"
                self.mycursor.execute(query, (search_prod,))
                products = self.mycursor.fetchall()

                if not products:
                    return{
                        "status":False,
                        "message":"No matching products found"
                    }

                return{
                    "status":True,
                    "products": products
                }
            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }

        


        def add_to_cart(self, user_id, product_name, quantity):
            try:
                query = "SELECT * FROM product_table WHERE product = %s"
                self.mycursor.execute(query, (product_name,))
                product = self.mycursor.fetchone()

                if not product:
                    return{
                        "status":False,
                        "message":"Product not found"
                    }

                query = "INSERT INTO carts_table (user_id, product_id, quantity, description) VALUES (%s, %s, %s, %s)"
                values = (user_id, product["id"], quantity, product["description"])
                self.mycursor.execute(query, values)
                self.conn.commit()

                return{
                    "status":True,
                    "message":f"{product['product']} added to cart successfully"
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }
    



        def view_cart(self, user_id):
            try:
                query = """SELECT carts_table.cart_id, carts_table.quantity, product_table.product, product_table.price
                            FROM carts_table
                            JOIN product_table ON carts_table.product_id = product_table.id
                            WHERE carts_table.user_id = %s"""
                self.mycursor.execute(query, (user_id,))
                cart_items = self.mycursor.fetchall()

                if not cart_items:
                    return{
                        "status":False,
                        "message":"Your cart is empty"
                    }

                return{
                    "status":True,
                    "items": cart_items
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



        def remove_from_cart(self, cart_id):
            try:
                query = "SELECT * FROM carts_table WHERE cart_id = %s"
                self.mycursor.execute(query, (cart_id,))
                item = self.mycursor.fetchone()

                if not item:
                    return{
                        "status":False,
                        "message":"Item not found in cart"
                    }

                query = "DELETE FROM carts_table WHERE cart_id = %s"
                self.mycursor.execute(query, (cart_id,))
                self.conn.commit()

                return{
                    "status":True,
                    "message":"Item removed from cart successfully"
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



        def checkout(self, user_id, user_email):
            try:
                check_query = "SELECT * FROM carts_table WHERE user_id = %s"
                self.mycursor.execute(check_query, (user_id,))
                cart_items = self.mycursor.fetchall()

                if not cart_items:
                    return{
                        "status":False,
                        "message":"Your cart is empty"
                    }

                insert_query = """INSERT INTO order_table (user_id, product_id, status)
                                    SELECT user_id, product_id, 'pending' FROM carts_table WHERE user_id = %s"""
                self.mycursor.execute(insert_query, (user_id,))

                delete_query = "DELETE FROM carts_table WHERE user_id = %s"
                self.mycursor.execute(delete_query, (user_id,))

                self.conn.commit()

                self.send_email(user_email, "Order Confirmation", "Your order has been placed successfully!")

                return{
                    "status":True,
                    "message":"Order placed successfully!"
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }



        def view_my_orders(self, user_id):
            try:
                query = "SELECT * FROM order_table WHERE user_id = %s"
                self.mycursor.execute(query, (user_id,))
                orders = self.mycursor.fetchall()

                if not orders:
                    return{
                        "status":False,
                        "message":"You have no orders yet"
                    }

                return{
                    "status":True,
                    "orders": orders
                }

            except sql.Error as e:
                return {
                    "status": False,
                    "message": f"Database error: {e}"
                }
            