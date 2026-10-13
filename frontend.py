import msvcrt
from backend import Ecom


def masked_input(prompt):
    print(prompt, end="", flush=True)
    typed_password = ""
    while True:
        char = msvcrt.getch()

        if char in (b"\r", b"\n"):
            print("")
            break
        elif char == b"\x08":
            if len(typed_password) > 0:
                typed_password = typed_password[:-1]
                print("\b \b", end="", flush=True)
        else:
            try:
                decoded_char = char.decode("utf-8")
                typed_password += decoded_char
                print("*", end="", flush=True)
            except UnicodeDecodeError:
                pass

    return typed_password


class Market(Ecom):
    def __init__(self, shop_name):
        super().__init__(shop_name)

    def home_page(self, shop_name):
        self.speak(f"Welcome to {shop_name}")
        while True:
            print(f"""Welcome to {shop_name}
                 1. Create Account
                 2. login
                 3. About us
                 4. Exit  
                 """)
            print("Type your choice, or type 'v' to speak instead.")
            choice = input("Enter your choice: ")


            if choice.lower() == "v":
                self.speak("Please say your choice")
                choice = self.listen()
                print(f"DEBUG: choice after listening = '{choice}'")

            if "1" in choice or "create account" in choice:
                self.Create_account()
            elif "2" in choice or "login" in choice:
                self.login_user()
            elif "3" in choice or "about us" in choice:
                self.about_us()
            elif "4" in choice or "exit" in choice:
                print("Thanks for shopping with us....")
                self.speak("Thanks for shopping with us")
                exit()
            else:
                print("Invalid input")
 

    def Create_account(self):
        fullname = input("Enter your fullname: ")
        address = input("Enter your address: ")

        suggested_password = self.suggest_password()
        print(f"Suggested password: {suggested_password}")
        choice = input("Use this suggested password? Yes or No: ")

        if choice.lower() == "yes":
            password = suggested_password
        else:
            while True:
                password = masked_input("Enter your password: ")
                if self.is_valid_password(password):
                    break
                else:
                    print("Password must be at least 8 characters and include uppercase, lowercase, a number, and a special character. Please try again.")

        while True:
            email = input("Enter your email: ")
            if self.is_valid_email(email):
                if self.email_exists(email):
                    print("Email already exists. Please try a different email.")
                else:
                    break
            else:
                print("Invalid email format. Please try again.")

        self.send_otp(email, fullname)
        print(f"An OTP has been sent to {email}. Please check your inbox.")

        attempts = 0
        verified = False
        while attempts < 3:
            entered_otp = input("Enter the OTP sent to your email: ")
            if self.verify_otp(email, entered_otp):
                verified = True
                break
            else:
                attempts += 1
                print(f"Incorrect OTP. {3 - attempts} attempt(s) remaining.")

        if not verified:
            print("OTP verification failed. Account creation cancelled.")
            return

        result = self.Create_Account(fullname, address, password, email, "customer")
        print(result["message"])
        if result["status"] == False:
            return

        print("""
             Do you wish to login ?
             1. Yes 
             2. No
            """)
        choice = input("Choose: ")
        if choice == "1":
           self.login_user()
        elif choice == "2": 
           exit()
        else:
            print("Invalid Input")



    def login_user(self):
        while True:
            email = input("Enter email: ")
            password = masked_input("Enter your password: ")
            result = self.login_account(email, password)
            print(result["message"])

            if result["status"]:
                break
            else:
                print("Please try again.")

        if result["role"] == "admin":
            self.speak("Welcome Admin")
            self.admin_dashboard()
            return
        user = result["user"]
        self.speak(f"Welcome {user['fullname']}")
        self.Dashboard(user)




    def about_us(self):
        print("""
              
        Welcome to Jonzing Dope Market

        Buy it, Sell it, and Chill. It's already at your doorstep.
              

        What We Offer:
              
        Buy and sell almost anything on one trusted platform with secure payments.
              
        Enjoy quick deliveries, easy order tracking, and reliable customer support.
              
        Thanks for your patronage.
        """) 
        return       
    



    def Dashboard(self, user):
        while True:
            print(f"""
            Welcome {user['fullname']}

                1. View Profile
                2. View Available Products
                3. Search Product
                4. Add To Cart
                5. View Cart
                6. Remove from Cart
                7. Checkout
                8. View Orders
                0. Logout
                """)
            print("Type your choice, or type 'v' to speak instead.")
            choice = input("Choose action: ")

            if choice.lower() == "v":
                self.speak("Please say your choice")
                choice = self.listen()

            if choice == "1" or choice == "view profile":
                self.view_my_profile(user)
            elif choice == "2" or choice == "view available products":
                self.view_available_products()
            elif choice == "3" or choice == "search product":
                self.search_for_product(user)
            elif choice == "4" or choice == "add to cart":
                self.add_product_to_cart(user)
            elif choice == "5" or choice == "view cart":
                self.view_my_cart(user)
            elif choice == "6" or choice == "remove from cart":
                self.remove_item_from_cart(user)
            elif choice == "7" or choice == "checkout":
                self.checkout_cart(user)
            elif choice == "8" or choice == "view orders":
                self.view_orders(user)
            elif choice == "0" or choice == "logout":
                self.speak("Goodbye")
                break
            else:
                print("Invalid Input")
                
# ADMIN'S SECTION

    def admin_dashboard(self):
        while True:
            print("""
            Welcome Admin
            You now have access to the admin dashboard.
                
            1. Add Product
            2. View All Product
            3. View All Users
            4. View & update Orders
            5. Delete User Account 
            6. Reset User Password   
            7. Logout  
            """)
            print("Type your choice, or type 'v' to speak instead.")
            choice = input("Enter your choice: ")

            if choice.lower() == "v":
                self.speak("Please say your choice")
                choice = self.listen()

            if choice == "1" or choice == "add product":
                self.add_product()
            elif choice == "2" or choice == "view all product":
                self.view_all_product()
            elif choice == "3" or choice == "view all users":
                self.view_users()
            elif choice == "4" or choice == "view and update orders":
                self.view_admin_orders()
            elif choice == "5" or choice == "delete user account":
                self.delete_user_account()
            elif choice == "6" or choice == "reset user password":
                self.reset_user_password()
            elif choice == "7" or choice == "logout":
                self.speak("Goodbye")
                exit()
            else:
                print("Invalid Input")

    def add_product(self):
        product = input("Enter the product: ")
        category = input("Product Category: ")
        description = input("Product Description: ")
        quantity = input("Quantity: ")
        price = input("Price: ")
        result = self.ins_product(product, description, category, quantity, price)
        if result["status"]:
            print(result["message"])
            return
        else:
            print(result["message"])

    def view_all_product(self):
        result = self.view_all_prod()
        if result["status"]:
            print(result["message"])
            return
        print(result["message"])

    def view_users(self):
        result = self.view_all_users()
        if not result["status"]:
            print(result["message"])

    def view_admin_orders(self):
        result = self.view_all_orders()
        if not result["status"]:
            print(result["message"])
            return

        order_id = input("Enter Order ID to update status (or press Enter to skip): ")
        if order_id == "":
            return

        new_status = input("Enter new status (pending/shipped/completed/cancelled): ")
        update_result = self.update_order_status(order_id, new_status)
        print(update_result["message"])

    def delete_user_account(self):
        email = input("Enter the email of the user to delete: ")
        result = self.delete_user(email)
        print(result["message"])

    def reset_user_password(self):
        email = input("Enter the email of the user: ")
        new_password = input("Enter the new password: ")
        result = self.reset_password(email, new_password)
        print(result["message"])



# THE USER SECTION'S

    def view_my_profile(self, user):
            print(f"""
        --------------------------
        Fullname : {user['fullname']}
        Email : {user['email']}
        Address : {user['address']}
        Role : {user['role']}
        """)

    def view_available_products(self):
        result = self.all_available_products()
        if not result["status"]:
            print(result["message"])


    def search_for_product(self,user):
     search_prod = input("Enter exact product name to search: ")
     result = self.search_product(search_prod)

     if not result["status"]:
          print(result["message"])
          return

     for product in result["products"]:
          print(f"""
            --------------------------
            Product_ID : {product["id"]}
            Product_name : {product["product"]}
            Category : {product["category"]}
            Description : {product["description"]}
            Price : {product["price"]}
            """)

                  
     choice = input("Add this product to cart? Yes or No: ")
     if  choice.lower() == "yes":
         quantity = input("Enter quantity: ")
         cart_result = self.add_to_cart(user["id"], search_prod, quantity)
         print(cart_result["message"])
     else:
        print("Okay, not added to cart.")

          
    def add_product_to_cart(self, user):
        product_name = input("Enter the product name to add to cart: ")
        quantity = input("Enter quantity: ")

        result = self.add_to_cart(user["id"], product_name, quantity)
        print(result["message"])


    def view_my_cart(self, user):
        result = self.view_cart(user["id"])

        if not result["status"]:
            print(result["message"])
            return

        for item in result["items"]:
            print(f"""
            --------------------------
            Cart_ID : {item["cart_id"]}
            Product : {item["product"]}
            Quantity : {item["quantity"]}
            Price : {item["price"]}
            """) 



    def remove_item_from_cart(self, user):
        self.view_my_cart(user)
        cart_id = input("Enter the Cart ID to remove: ")
        result = self.remove_from_cart(cart_id)
        print(result["message"])

    

    def checkout_cart(self, user):
        result = self.checkout(user["id"], user["email"])
        print(result["message"])



    def view_orders(self, user):
        result = self.view_my_orders(user["id"])

        if not result["status"]:
            print(result["message"])
            return

        for order in result["orders"]:
            query = "SELECT * FROM product_table WHERE id = %s"
            self.mycursor.execute(query, (order["product_id"],))
            product = self.mycursor.fetchone()

            print(f"""
            --------------------------
            Order_ID : {order["order_id"]}
            Product : {product["product"]}
            Status : {order["status"]}
            Ordered_At : {order["ordered_at"]}
            """)







shop = Market("Jonzing Dope Market")
shop.home_page("Jonzing Dope Market")