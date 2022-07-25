import random
import sqlite3

import requests


class Atm:
    TL_BANKNOTES = {
        "200 TL": 200,
        "100 TL": 100,
        "50 TL": 50,
        "20 TL": 20,
        "10 TL": 10,
        "5 TL": 5,
        "1 TL": 1
    }
    USD_BANKNOTES = {
        "100 USD": 100,
        "50 USD": 50,
        "20 USD": 20,
        "10 USD": 10,
        "5 USD": 5,
        "2 USD": 2,
        "1 USD": 1
    }
    EUR_BANKNOTES = {
        "500 EUR": 500,
        "200 EUR": 200,
        "100 EUR": 100,
        "50 EUR": 50,
        "20 EUR": 20,
        "10 EUR": 10,
        "5 EUR": 5,
        "2 EUR": 2,
        "1 EUR": 1
    }

    def api_url(self, currency1, currency2, amount, typ):

        # https://www.exchangerate-api.com/ is the API that was used.

        if typ == "conversion_result":

            url = f'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/{currency1}/{currency2}/{amount}'
            # currency1 is base_code , currency2 is target_code
            # DON'T FORGET TO ADD YOUR API KEY TO "YOUR-API-KEY" SECTION
            response = requests.get(url)
            data = response.json()
            result = data['conversion_result']  # like USD to TL >>> 500 * 17.50
            return result

        elif typ == "conversion_rate":

            url = f'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/{currency1}/{currency2}'
            # currency1 is base_code , currency2 is target_code
            # DON'T FORGET TO ADD YOUR API KEY TO "YOUR-API-KEY" SECTION
            response = requests.get(url)
            data = response.json()
            result = data['conversion_rate']  # like 1 USD is 17.55 TL
            return result

    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.user_name = ""
        self.user_id = 0
        self.gender = ""
        self.user_code = ""

        self.status = True
        self.is_everything_okay = False
        self.is_main_run_active = True
        self.is_run_active = True

        self.connect_database()

    def main_run(self):
        while self.is_main_run_active:
            self.first_menu()

            # choice = self.first_menu_choice()
            choice = self.all_choice(min_num=1, max_num=3, msg1="\033[1;32mSuccessfully exited the program.\033[m")

            if choice == 1:
                self.login()
            if choice == 2:
                self.signup()
            if choice == 3:
                self.system_exit()

    def run(self):
        while self.is_run_active:
            self.menu()

            # choice = self.choice()
            choice = self.all_choice(min_num=1, max_num=8, msg1="\033[1;32mYou successfully sign out.\033[m")

            if choice == 1:
                self.deposit_money()
            if choice == 2:
                self.withdraw_money()
            if choice == 3:
                self.show_my_assets()
            if choice == 4:
                self.pay_bills()
            if choice == 5:
                self.queue_from_bank()
            if choice == 6:
                self.send_money()
            if choice == 7:
                self.account_settings()
            if choice == 8:
                self.is_run_active = False
                self.is_main_run_active = True
                self.main_run()

    def first_menu(self):
        print(f"\033[1;36m{self.name} ATM\033[m".center(105, "-"))
        print(f"Welcome to {self.name} ATM, please dial the number of the transaction you want to do")
        print(
            """1 - Login\n"""
            """2 - Sign up\n"""
            """3 - Exit\n"""
        )

    def login(self):
        login_run = True
        while login_run:
            try:
                print("\033[93mPress 0 to cancel\033[m")
                self.user_name = input("Enter your name: ")

                if self.user_name == "0":
                    break
                else:
                    password = int(input("Enter your password: "))
                    self.cursor.execute(
                        f"SELECT password FROM customers WHERE name='{self.user_name}' AND password={password}")
                    if not self.cursor.fetchone():
                        print("\033[31mLogin has failed!\033[m")
                        print("Password or name is wrong! Please try again.")
                        print(
                            "Did you forget your password ? Press '1' to change your password, Press '0' to cancel and return back to login screen. ")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            while True:
                                print("\033[93mPress 0 to cancel\033[m")
                                try:
                                    user_name = input("Please enter your name again: ").lower().capitalize()
                                    if user_name == "0":
                                        login_run = False
                                        break
                                    user_email = input("Please enter your email: ").lower()
                                    if user_email == "0":
                                        login_run = False
                                        break
                                    security = input("What is your mother's maiden name?: ").lower().capitalize()
                                    if security == "0":
                                        login_run = False
                                        break
                                    self.cursor.execute(
                                        f"SELECT security_question FROM customers WHERE name = '{user_name}' AND email = '{user_email}'")

                                    security_question = list(self.cursor.fetchall())[0][0]

                                    if security == security_question and self.user_name == user_name:
                                        while True:
                                            try:
                                                print("\033[93mPress 0 to cancel\033[m")
                                                new_password = int(
                                                    input(
                                                        "Enter your new a six digit password: (For example: 398023) "))

                                                if new_password == 0:
                                                    break

                                                # elif new_password == 5:
                                                #     first_menu = False
                                                #     self.is_main_run_active = False
                                                #     self.run()
                                                #     break

                                                else:
                                                    new_password_again = int(input("Enter your new password again: "))
                                                    if len(str(
                                                            new_password)) != 6:  # or len(str(new_password_again)) != 6
                                                        print(
                                                            "\033[31mYour password must be a six digit password. Please try again.\033[m\n")
                                                        continue

                                                    elif new_password != new_password_again:
                                                        print(
                                                            "\033[31mYour passwords do not match. Please try again.\033[m\n")
                                                        continue

                                                self.cursor.execute(
                                                    f"UPDATE customers SET password = {new_password} WHERE name = '{self.user_name}' AND security_question = '{security_question}'")
                                                self.connect.commit()
                                                print(f"\033[1;32mYou successfully updated your password.\033[m")
                                                login_run = False
                                                break
                                            except ValueError:
                                                print("\033[mPassword must be an integer.\033[m\n")
                                    else:
                                        print(
                                            "\033[31mYour name, email, or answer to the security question do not match. Please try again !\033[m")
                                        continue

                                    break
                                except IndexError:
                                    print(
                                        "\033[31mYour name, email, or answer to the security question do not match. Please try again !\033[m")
                                    continue



                        elif choice == "0":
                            break

                        continue

                    self.cursor.execute(
                        f"SELECT rowid FROM customers WHERE name = '{self.user_name}' and password = {password}")
                    rowid = list(self.cursor.fetchall())[0][0]
                    self.connect.commit()

                    self.user_id = rowid

                    self.is_main_run_active = False

                    self.is_run_active = True

                    self.is_everything_okay = True

                    break
            except ValueError:
                print("\033[31mPassword must be an integer!\033[m\n")

    def signup(self):

        while True:
            print("\033[93mPress 0 to cancel\033[m")
            print("\033[32mFirstly, thanks for choosing our bank.\033[m")
            new_name = input("Please enter your name: ").lower().title()
            if new_name == "0":
                break
            new_surname = input("Please enter your surname: ").lower().capitalize()
            if new_surname == "0":
                break
            while True:
                try:
                    new_age = int(input("Please enter your age: "))
                    if new_age <= 0:
                        print("\033[31mYou entered invalid age. Please try again.\033[m\n")
                        continue
                    break
                except ValueError:
                    print("\033[31mAge must be an integer.\033[m\n")

            new_email = input("Please enter your e-mail: ").lower()
            if new_email == "0":
                break
            new_city = input("Please enter your city: ").lower().capitalize()
            if new_city == "0":
                break
            gender_title = ""

            while True:

                new_gender = input("Please enter your gender(Male/Female): ").lower().capitalize()
                if new_gender == "Male":
                    gender_title = "Mr."
                    break
                elif new_gender == "Female":
                    gender_title = "Mrs./Ms."
                    break
                else:
                    print('\033[31mYou entered invalid value. Please try again.\033[m\n')
                    continue

            while True:
                try:
                    new_password = int(input("Create a six digit password: (For example: 398023) "))
                    new_password_again = int(input("Enter your password again: "))

                    if len(str(new_password)) != 6:  # or len(str(new_password_again)) != 6
                        print("\033[31mYour password must be a six digit password. Please try again.\033[m\n")
                        continue

                    if new_password != new_password_again:
                        print("\033[31mYour passwords do not match. Please try again.\033[m\n")
                        continue

                    break
                except ValueError:
                    print("\033[31mPassword must be an integer.\033[m\n")

            print("Security question : What is your mother's maiden name?")
            security_question = input("Enter your answer: ").lower().capitalize()

            if security_question == "0":
                break

            self.cursor.execute(
                f"INSERT INTO customers VALUES({self.user_id},'{new_name}','{new_surname}','{new_email}','{new_city}','{new_gender}',{new_password},{new_age},0,0,0,'False','{security_question}',)"
            )
            self.cursor.execute(
                f"SELECT rowid FROM customers WHERE name='{new_name}' AND password={new_password}")
            self.user_id = list(self.cursor.fetchall())[0][0]

            self.cursor.execute(
                f"UPDATE customers SET id = {self.user_id} WHERE name = '{new_name}' and surname = '{new_surname}'")
            self.connect.commit()

            print(
                f"\033[1;32m*----Your registration successfully completed! Welcome to Blabla Bank family {gender_title} {new_name} {new_surname}!----*\033[m")

            self.main_run()
            break

    def menu(self):
        self.cursor.execute(f"SELECT gender FROM customers WHERE name='{self.user_name}'")
        self.gender = list(self.cursor.fetchall())

        title = ""
        if self.gender == [('Male',)]:
            title = "Mr."
        elif self.gender == [('Female',)]:
            title = "Mrs./Ms."

        message = f"Welcome {title} {self.user_name}, what would you like to do ?"
        print("-" * len(message))
        print(message)
        print("-" * len(message))

        usd_tl = self.api_url("USD", "TRY", typ="conversion_rate", amount=0)
        tl_usd = self.api_url("TRY", "USD", typ="conversion_rate", amount=0)
        eur_tl = self.api_url("EUR", "TRY", typ="conversion_rate", amount=0)
        tl_eur = self.api_url("TRY", "EUR", typ="conversion_rate", amount=0)
        usd_eur = self.api_url("USD", "EUR", typ="conversion_rate", amount=0)
        eur_usd = self.api_url("EUR", "USD", typ="conversion_rate", amount=0)
        print(f"USD/TL : {usd_tl:}   -   TL/USD : {tl_usd}")
        print(f"EUR/TL : {eur_tl}   -   TL/EUR : {tl_eur}")
        print(f"USD/EUR : {usd_eur}   -   EUR/USD : {eur_usd}")

        print("-" * len(message))
        url = 'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/TRY'
        # DON'T FORGET TO ADD YOUR API KEY TO "YOUR-API-KEY" SECTION
        response = requests.get(url)
        data = response.json()

        last_update_date = data['time_last_update_utc']

        print(f"\033[95mLast update: {last_update_date}\033[m")
        print("-" * len(message))

        print(
            """1 - DEPOSIT MONEY\n"""
            """2 - WITHDRAW MONEY\n"""
            """3 - SHOW MY BALANCE\n"""
            """4 - PAY THE BILLS\n"""
            """5 - TAKE A QUEUE\n"""
            """6 - TRANSFER MONEY\n"""
            """7 - ACCOUNT SETTINGS\n"""
            """8 - SIGN OUT\n"""
        )
        self.cursor.execute(
            f"SELECT notification FROM customers WHERE name = '{self.user_name}' AND rowid = {self.user_id}")
        notification = list(self.cursor.fetchall())[0][0]

        if notification == "True":
            print(f"\033[93mMoney has transferred to your account!\033[m")
            print(f"\033[93mPress 3 (SHOW MY BALANCE) to see!\033[m")

    def deposit_money(self):

        def helps_me_to_write_less_code(amount_deposited, currency, currency_long_name, currency_short_name):
            self.cursor.execute(f"SELECT {currency} FROM customers WHERE name ='{self.user_name}'")
            current_amount_list = list(self.cursor.fetchall())

            current_amount = current_amount_list[0][0]  # not [(250,)] it gives us 250

            current_amount += amount_deposited
            self.cursor.execute(f"UPDATE customers SET {currency}={current_amount} WHERE name='{self.user_name}'")
            self.connect.commit()

            print(f"\033[1;32mYour money has been successfully deposited into your {currency_long_name} account.\033[m")
            print(
                f"\033[1;33mTOTAL {currency_long_name} BALANCE: {current_amount:,.2f} {currency_short_name}\033[m".upper().replace(
                    ",",
                    "."))
            print("-" * 98)

        while True:
            print("\033[1;36mWELCOME TO DEPOSIT SECTION\033[m".center(105, "-"))
            print(
                """1 - Turkish Lira(TL)\n"""
                """2 - American Dollar(USD)\n"""
                """3 - Euro(EUR)\n"""
                """4 - Go back to the menu"""
            )
            print("Choose the currency you want to deposit or press 4 to go back to the menu.")
            choice = self.all_choice(min_num=1, max_num=4, msg1="")

            if choice == 1 or choice == 2 or choice == 3:
                while True:
                    try:
                        amount_deposited = int(input("Enter the amount you want to deposit: "))
                        if amount_deposited < 0:
                            print("\033[31mYour choice must be more than -1 (Minus one)\033[m")
                            continue
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")

                if choice == 1:

                    helps_me_to_write_less_code(amount_deposited, "tl", "Turkish Lira", "TL")

                elif choice == 2:

                    helps_me_to_write_less_code(amount_deposited, "usd", "American Dollar", "USD")

                elif choice == 3:

                    helps_me_to_write_less_code(amount_deposited, "eur", "Euro", "EUR")

            elif choice == 4:
                self.is_main_run_active = False
                self.run()
                break

    def withdraw_money(self):

        def show_current_amount(currency):
            self.cursor.execute(f"SELECT {currency} FROM customers WHERE name ='{self.user_name}'")
            current_amount_list = list(self.cursor.fetchall())

            current_amount = current_amount_list[0][0]  # not [(250,)] it gives us 250

            return current_amount

        def helps_me_to_write_less_code(amount_withdrawn, currency, currency_short_name, currency_list_name,
                                        currency_long_name):
            self.cursor.execute(f"SELECT {currency} FROM customers WHERE name ='{self.user_name}'")
            current_amount_list = list(self.cursor.fetchall())

            current_amount = current_amount_list[0][0]  # not [(250,)] it gives us 250

            if amount_withdrawn <= current_amount:

                current_amount -= amount_withdrawn

                self.cursor.execute(f"UPDATE customers SET {currency}={current_amount} WHERE name='{self.user_name}'")
                self.connect.commit()

                for i in currency_list_name.values():
                    amount_of_money = int(amount_withdrawn / i)

                    if amount_of_money > 0:
                        amount_withdrawn = amount_withdrawn % i
                        print(f"{amount_of_money} pieces of {i} {currency_short_name} banknotes were returned.")

                print(
                    f"\033[1;32mYour money has been successfully withdrawn from your {currency_long_name} account.\033[m")
                print(
                    f"\033[1;33mTOTAL {currency_long_name} BALANCE: {current_amount:,.2f} {currency_short_name}\033[m".upper().replace(
                        ",", "."))
                print("-" * 98)

            else:
                print("\033[31mYou can't withdraw this amount of money.\033[m")
                print("\033[31mYou are exceeding your current balance.\033[m")
                print(f"Your current balance: {current_amount:,.2f} {currency_short_name} ".replace(",", "."))
                print("Please try again!")

        while True:
            print("\033[1;36mWELCOME TO WITHDRAW SECTION\033[m".center(105, "-"))
            print(
                f"""1 - Turkish Lira(TL) >>>>> Your current balance: {show_current_amount("tl"):,.2f} TL\n2 - American Dollar(USD) >>>>> Your current balance: {show_current_amount("usd"):,.2f} USD\n3 - Euro(EUR) >>>>> Your current balance: {show_current_amount("eur"):,.2f} EUR\n4 - Go back to the menu""".replace(
                    ",", "."),
                # f"""2 - American Dollar(USD) >>>>> Your current balance: {show_current_amount("usd"):,.2f} USD\n""".replace(",","."),
                # f"""3 - Euro(EUR) >>>>> Your current balance: {show_current_amount("eur"):,.2f} EUR\n""".replace(",","."),
                # f"""4 - Go back to the menu"""
            )
            print("Choose the currency you want to withdraw or press 4 to go back to the menu.")
            choice = self.all_choice(min_num=1, max_num=4, msg1="")
            if choice == 1 or choice == 2 or choice == 3:
                while True:
                    try:
                        amount_withdrawn = int(input("Enter the amount you want to deposit: "))
                        if amount_withdrawn < 0:
                            print("\033[31mYour choice must be more than -1 (Minus one)\033[m")
                            continue
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")

                if choice == 1:

                    helps_me_to_write_less_code(amount_withdrawn, "tl", "TL", self.TL_BANKNOTES, "Turkish Lira")


                elif choice == 2:

                    helps_me_to_write_less_code(amount_withdrawn, "usd", "USD", self.USD_BANKNOTES, "American Dollar")

                elif choice == 3:

                    helps_me_to_write_less_code(amount_withdrawn, "eur", "EUR", self.EUR_BANKNOTES, "Euro")

            elif choice == 4:
                self.is_main_run_active = False
                self.run()
                break

    def show_my_assets(self):

        def print_assets(currency_short_name, currency_long_name, amount):
            amount_colored = f"\033[1;32m{amount:,.2f}\033[m".replace(",", ".")
            message = f"Your total {currency_long_name} balance is {amount_colored} {currency_short_name}"
            print("-" * 95)
            print(message)

        def choosing_from_database(currency):
            self.cursor.execute(f"SELECT {currency} FROM customers WHERE name='{self.user_name}'")
            all_assets_list = list(self.cursor.fetchall())
            all_assets = all_assets_list[0][0]

            return all_assets

        # IF YOU DON'T WANT TO USE API, YOU CAN USE CODES BETWEEN STARS

        # ********************************************************

        # def count_total_amount(currency1, currency2, currency3, value1, value2, currency_short, currency_long):
        #     # 16.07.2022 01:33 1 Dollar is 17.40 TL , 1 Euro is 17.55 TL
        #
        #     total_currency = currency1 + currency2 * value1 + currency3 * value2
        #     total_currency_colored = f"\033[1;36m{total_currency:,.2f}\033[m".replace(",", ".")
        #
        #     print("-" * 95)
        #     print(f"Your total balance in terms of {currency_long} is {total_currency_colored} {currency_short}")
        #     print("-" * 95)

        # ********************************************************

        def count_total_amount_api(currency_code1, currency_code2, currency_code3, currency1, amount1, amount2,
                                   currency_short, currency_long):
            # value_from_usd_to_tl = self.api_url("USD", "TRY",amount1)  # if amount is 1000 >>> 1000 * 17.50 >>> 17500 TL
            value_from_cc2_to_cc1 = self.api_url(currency_code2, currency_code1, amount1,
                                                 typ="conversion_result")  # if amount is 1000 >>> 1000 * 17.50 >>> 17500 TL
            value_from_cc3_to_cc1 = self.api_url(currency_code3, currency_code1, amount2, typ="conversion_result")
            # for example currency_code1 = "TRY", currency_code2 = "USD", currency_code3 = "EUR"

            total_amount = currency1 + value_from_cc2_to_cc1 + value_from_cc3_to_cc1
            total_amount_colored = f"\033[1;36m{total_amount:,.2f}\033[m".replace(",", ".")

            message = f"Your total balance in terms of {currency_long} is {total_amount_colored} {currency_short}"

            print("-" * 95)
            print(message)
            # print("-" * 95)

        print("\033[1;36mWELCOME TO MY ASSETS SECTION\033[m".center(103, "-"))
        print(
            """1- Show my assets\n"""
            """2- Go back to menu\n"""
        )
        choice = self.all_choice(1, 2, "")

        if choice == 1:
            # Different Style

            # tl = choosing_from_database("tl")
            # usd = choosing_from_database("usd")
            # eur = choosing_from_database("eur")
            #
            # print("-" * 95)
            #
            # title = "{0:<12} {1:<15} {2:<4}"
            # body = "{tl:<12,.2f} {usd:<15,.2f} {eur:<4,.2f}"
            # print(title.format("Turkish Lira", "American Dollar", "Euro"))
            # print(title.format("-" * 12, "-" * 15, "-" * 12))
            # print(body.format(
            #     tl= float(tl),
            #     usd=float(usd),
            #     eur=float(eur)
            # ).replace(",","."))
            # print("-" * 95)

            tl = choosing_from_database("tl")
            usd = choosing_from_database("usd")
            eur = choosing_from_database("eur")

            print_assets("TL", "Turkish Lira", tl)
            print_assets("USD", "American Dollar", usd)
            print_assets("EUR", "Euro", eur)

            # IF YOU DON'T WANT TO USE API, YOU CAN USE CODES BETWEEN STARS

            # ********************************************************

            # 16.07.2022 01:33 1 Dollar is 17,40 TL , 1 Euro is 17,55 TL

            # count_total_amount(
            #     currency1=tl,
            #     currency2=usd,
            #     currency3=eur,
            #     value1=17.40,
            #     value2=17.55,
            #     currency_short="TL",
            #     currency_long="Turkish Lira")
            #
            # count_total_amount(
            #     currency1=usd,
            #     currency2=tl,
            #     currency3=eur,
            #     value1=0.057,
            #     value2=1.01,
            #     currency_short="USD",
            #     currency_long="American Dollar")
            #
            # count_total_amount(
            #     currency1=eur,
            #     currency2=usd,
            #     currency3=tl,
            #     value1=0.99,
            #     value2=0.057,
            #     currency_short="EUR",
            #     currency_long="Euro")

            # ********************************************************

            count_total_amount_api(
                currency_code1="TRY",
                currency_code2="USD",
                currency_code3="EUR",
                currency1=tl,
                amount1=usd,
                amount2=eur,
                currency_short="TL",
                currency_long="Turkish Lira"
            )
            count_total_amount_api(
                currency_code1="USD",
                currency_code2="TRY",
                currency_code3="EUR",
                currency1=usd,
                amount1=tl,
                amount2=eur,
                currency_short="USD",
                currency_long="American Dollar"
            )
            count_total_amount_api(
                currency_code1="EUR",
                currency_code2="USD",
                currency_code3="TRY",
                currency1=eur,
                amount1=usd,
                amount2=tl,
                currency_short="EUR",
                currency_long="Euro"
            )

            self.cursor.execute(f"UPDATE customers SET notification = 'False' WHERE rowid = {self.user_id}")
            self.connect.commit()

            url = 'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/TRY'
            response = requests.get(url)
            data = response.json()

            last_update_date = data['time_last_update_utc']
            print("-" * 95)
            print(f"\033[95mLast update: {last_update_date}\033[m".center(103, "-"))
            print("-" * 95)

    def pay_bills(self):

        def show_bills(min_num, max_num, bill_type):

            bill_amount = random.randint(min_num, max_num)

            it_is_working = True

            tl_usd = self.api_url("TRY", "USD", bill_amount, typ="conversion_result")
            tl_eur = self.api_url("TRY", "EUR", bill_amount, typ="conversion_result")

            while it_is_working:
                print("-" * 90)
                print(f"Your {bill_type} bill is {bill_amount} TL")
                print(f"Your {bill_type} bill is {tl_usd:,.2f} USD".replace(",", "."))
                print(f"Your {bill_type} bill is {tl_eur:,.2f} EUR".replace(",", "."))
                print("-" * 90)
                print("Which asset would you like to pay with?")
                print(
                    """1 - Turkish Lira\n"""
                    """2 - American Dollar\n"""
                    """3 - Euro\n"""
                    """4 - Cancel"""
                )
                asset_choice = self.all_choice(1, 4, "")

                currency = ""

                if asset_choice == 1:
                    currency = "tl"

                elif asset_choice == 2:
                    currency = "usd"
                    bill_amount = tl_usd

                elif asset_choice == 3:
                    currency = "eur"
                    bill_amount = tl_eur
                elif asset_choice == 4:
                    print("Your process has been cancelled, returning back to the menu.")
                    break

                print("For paying your bill enter your password again.")

                while True:
                    try:
                        password = int(input("Enter your password: "))
                        self.cursor.execute(
                            f"SELECT password FROM customers WHERE password={password}")
                        if not self.cursor.fetchone():
                            print("\033[31mProcess has failed!\033[m")
                            print("Password is wrong! Please try again.")
                            continue

                        self.cursor.execute(f"SELECT {currency} FROM customers WHERE name ='{self.user_name}'")
                        current_amount_list = list(self.cursor.fetchall())

                        current_amount = current_amount_list[0][0]  # not [(250,)] it gives us 250

                        if current_amount >= bill_amount:
                            current_amount = current_amount - bill_amount

                            self.cursor.execute(
                                f"UPDATE customers SET {currency} = {current_amount} WHERE name='{self.user_name}'")
                            self.connect.commit()

                            print(f"Your electricity bill has been successfully paid.")
                            print(f"Your current balance: {current_amount:,.2f} {currency.upper()} ".replace(",", "."))
                            it_is_working = False

                        else:
                            print(f"\033[31mYou can't pay your {bill_type} bill right now.\033[m")
                            print("\033[31mYour bill is exceeding your current balance.\033[m")
                            print(f"Your current balance: {current_amount:,.2f} {currency.upper()} ".replace(",", "."))
                            print("Please try again!")

                        break
                    except ValueError:
                        print("\033[31mPassword must be an integer!\033[m\n")

        while True:
            print("\033[1;36mWELCOME TO INVOICE PAYMENT PART\033[m".center(104, "-"))
            print(
                """1- Electricity bill\n"""
                """2- Water bill\n"""
                """3- Gas bill\n"""
                """4- Phone bill\n"""
                """5- Internet bill\n"""
                """6- Go back to menu\n"""
            )
            choice = self.all_choice(1, 7, "")
            match choice:
                case 1:
                    show_bills(
                        min_num=0,
                        max_num=500,
                        bill_type="Electricity"

                    )
                case 2:
                    show_bills(
                        min_num=0,
                        max_num=500,
                        bill_type="Water"

                    )
                case 3:
                    show_bills(
                        min_num=0,
                        max_num=500,
                        bill_type="Gas"

                    )
                case 4:
                    show_bills(
                        min_num=0,
                        max_num=500,
                        bill_type="Phone"

                    )
                case 5:
                    show_bills(
                        min_num=0,
                        max_num=500,
                        bill_type="Internet"

                    )
                case 6:
                    self.is_main_run_active = False
                    self.run()
                    break

    def queue_from_bank(self):
        print("\033[1;36mWELCOME TO TAKING QUEUE FROM THE BANK\033[m".center(105, "-"))
        print(
            """1- Take a queue\n"""
            """2- Go back to menu\n"""
        )
        choice = self.all_choice(1, 2, "")

        if choice == 1:
            random_queue = random.randint(1, 100)
            random_queue_zerofill = str(random_queue).zfill(2)
            print(f"\033[1;32mYou successfully took a queue, your row number is: {random_queue_zerofill}\033[m")

        elif choice == 2:

            self.is_main_run_active = False
            self.run()

    def send_money(self):

        print("\033[1;36mWELCOME TO TRANSFER MONEY SECTION\033[m".center(105, "-"))

        self.cursor.execute("SELECT name,surname,email FROM customers")

        allCustomers = self.cursor.fetchall()

        convertAllStr = lambda x: [str(y) for y in x]

        latest_rowid = 0

        def transfer_money(amount_transferred, person_choice, currency_choice, currency_long_name, currency_short_name):
            self.cursor.execute(f"SELECT {currency_choice} FROM customers WHERE name ='{self.user_name}'")
            current_amount_list = list(self.cursor.fetchall())

            current_amount = current_amount_list[0][0]  # not [(250,)] it gives us 250

            self.cursor.execute(f"SELECT {currency_choice} FROM customers WHERE rowid = {person_choice}")

            opponent_amount = list(self.cursor.fetchall())[0][0]
            # to update the balance of the person to whom we send money

            if amount_transferred <= current_amount:

                current_amount -= amount_transferred
                self.cursor.execute(
                    f"UPDATE customers SET {currency_choice}={current_amount} WHERE name='{self.user_name}'")
                opponent_amount += amount_transferred
                self.cursor.execute(
                    f"UPDATE customers SET {currency_choice}={opponent_amount} WHERE rowid ={person_choice}")
                self.cursor.execute(f"UPDATE customers SET notification = 'True' WHERE rowid = {person_choice}")
                self.connect.commit()

                print(
                    f"\033[1;32m{amount_transferred} {currency_short_name} has been successfully transferred from your {currency_long_name} account.\033[m")
                print(
                    f"\033[1;33mTOTAL {currency_long_name} BALANCE: {current_amount:,.2f} {currency_short_name}\033[m".upper().replace(
                        ",",
                        "."))


            else:
                print("\033[31mYou can't transfer this amount of money.\033[m")
                print("\033[31mYou are exceeding your current balance.\033[m")
                print(f"Your current balance: {current_amount:,.2f} {currency_short_name} ".replace(",", "."))
                print("Please try again!")

        while True:
            for i, j in enumerate(allCustomers, 1):
                print("-" * 50)
                print("{}) {} ".format(i, " ".join(convertAllStr(j))))
                latest_rowid = i
                print("-" * 50)
            print("-" * 50)
            print(f"{latest_rowid + 1}) Go back to menu")
            print("-" * 50)

            person_choice = self.all_choice(1, latest_rowid + 1, "")

            if person_choice == self.user_id:
                print("\033[31mYou can't choose yourself. Please try again.\033[m")
                continue

            elif person_choice == latest_rowid + 1:
                self.is_main_run_active = False
                self.run()
                break

            print("Which currency asset do you want to send money from?")
            print(
                """1 - Turkish Lira\n"""
                """2 - American Dollar\n"""
                """3 - Euro\n"""
                """4 - Cancel\n"""
                """5 - Go back to menu\n"""
            )
            currency_choice = self.all_choice(1, 5, "")
            if currency_choice == 4:
                continue
            print("How much do you want to send?")

            if currency_choice == 1 or currency_choice == 2 or currency_choice == 3:
                while True:
                    try:
                        amount = int(input("Enter the amount you want to send: "))
                        if amount <= 0:
                            print("\033[31mYour choice must be more than 0 (Zero)\033[m")
                            continue
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")
                if currency_choice == 1:
                    transfer_money(
                        currency_long_name="Turkish Lira",
                        currency_short_name="TL",
                        person_choice=person_choice,
                        currency_choice="tl",
                        amount_transferred=amount

                    )
                if currency_choice == 2:
                    transfer_money(
                        currency_long_name="American Dollar",
                        currency_short_name="USD",
                        person_choice=person_choice,
                        currency_choice="usd",
                        amount_transferred=amount
                    )
                if currency_choice == 3:
                    transfer_money(
                        currency_long_name="Euro",
                        currency_short_name="EUR",
                        person_choice=person_choice,
                        currency_choice="eur",
                        amount_transferred=amount
                    )


            elif currency_choice == 5:
                self.is_main_run_active = False
                self.run()
                break

    def account_settings(self):

        print("\033[1;36mWELCOME TO ACCOUNT SETTINGS\033[m".center(105, "-"))

        first_menu = True
        second_menu = True

        while first_menu:
            title = ""
            if self.gender == [('Male',)]:
                title = "Mr."
            elif self.gender == [('Female',)]:
                title = "Mrs./Ms."
            greeting = f"Hi {title} {self.user_name} How can we help you ?"
            print("-" * len(greeting))
            print(greeting)
            print("-" * len(greeting))
            print(
                """1 - Change my informations\n"""
                """2 - Change my password\n"""
                """3 - Delete my account\n"""
                """4 - Go back to menu\n"""
            )
            choice = self.all_choice(1, 4, "")

            if choice == 1:

                while second_menu:

                    forewords = [
                        "My name:",
                        "My surname:",
                        "My email:",
                        "My city:",
                        "My gender:",
                        "My answer to the security question:",

                    ]

                    self.cursor.execute(
                        f"SELECT name,surname,email,city,gender,security_question FROM customers WHERE name = '{self.user_name}'")

                    allCustomers = self.cursor.fetchone()

                    convertAllStr = lambda x: [str(y) for y in x]

                    for index, (foreword, infos) in enumerate(zip(forewords, allCustomers), start=1):
                        print("{} - {} {}".format(index, foreword, "".join(convertAllStr(infos))))

                    self.cursor.execute(f"SELECT age FROM customers WHERE name = '{self.user_name}'")
                    my_age = self.cursor.fetchall()[0][0]

                    print(f"7 - My age: {my_age}")
                    print("8 - Return back\n9 - Go back to main menu\n")

                    print("What information would you like to change?")
                    choice = self.all_choice(1, 9, "")

                    if choice == 1:

                        new_Value = input(f"Enter new name: ").lower().capitalize()
                        self.cursor.execute(f"UPDATE customers SET name = '{new_Value}' WHERE id = {self.user_id} ")
                        self.user_name = new_Value
                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your name.\033[m")
                        continue

                    elif choice == 2:
                        new_Value = input(f"Enter new surname: ").lower().capitalize()
                        self.cursor.execute(f"UPDATE customers SET surname = '{new_Value}' WHERE id = {self.user_id} ")

                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your surname.\033[m")
                        continue

                    elif choice == 3:
                        new_Value = input(f"Enter new email: ").lower()
                        self.cursor.execute(f"UPDATE customers SET email = '{new_Value}' WHERE id = {self.user_id} ")

                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your email.\033[m")
                        continue

                    elif choice == 4:
                        new_Value = input(f"Enter new city: ").lower().capitalize()
                        self.cursor.execute(f"UPDATE customers SET city = '{new_Value}' WHERE id = {self.user_id} ")

                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your city.\033[m")
                        continue

                    elif choice == 5:

                        # self.cursor.execute(
                        #     f"SELECT gender FROM customers WHERE name = '{self.user_name}'")
                        #
                        # my_gender = self.cursor.fetchone() #('Male',)
                        #
                        # print(str(my_gender))

                        while True:

                            new_Value = input("Enter new gender(Male/Female): ").lower().capitalize()

                            if new_Value == "Male" or new_Value == "Female":

                                self.cursor.execute(
                                    f"UPDATE customers SET gender = '{new_Value}' WHERE id = {self.user_id} ")

                                self.connect.commit()
                                print(f"\033[1;32mYou successfully updated your gender.\033[m")
                                break

                            else:
                                print("\033[31mYour choice must be Male or Female. Please try again.\033[m")
                                continue

                        continue
                    elif choice == 6:
                        print("Security question : What is your mother's maiden name?")
                        new_Value = input(f"Enter new answer to the security question: ").lower().capitalize()
                        self.cursor.execute(
                            f"UPDATE customers SET security_question = '{new_Value}' WHERE id = {self.user_id} ")

                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your answer to the security question.\033[m")
                        continue

                    elif choice == 7:
                        while True:
                            try:
                                new_Value = int(input("Enter new age: "))
                                if new_Value <= 0:
                                    print("\033[31mYour choice must be more than -1 (Minus one)\033[m")
                                    continue
                                self.cursor.execute(
                                    f"UPDATE customers SET age = {new_Value} WHERE id = {self.user_id} ")

                                self.connect.commit()
                                print(f"\033[1;32mYou successfully updated your age.\033[m")
                                break
                            except ValueError:
                                print(
                                    "\033[31mYour choice must be integer number. Please type in the correct type!\033[m")
                        continue

                    elif choice == 8:
                        break
                    elif choice == 9:
                        self.is_run_active = True
                        self.main_run()
                        second_menu = False
                        first_menu = False

            elif choice == 2:
                while True:
                    try:
                        print("\033[93mPress 4 to return back to menu, Press 5 to go back to main menu\033[m")
                        new_password = int(input("Enter your new a six digit password: (For example: 398023) "))

                        if new_password == 4:
                            break

                        elif new_password == 5:
                            first_menu = False
                            self.is_main_run_active = False
                            self.run()
                            break

                        else:
                            new_password_again = int(input("Enter your new password again: "))
                            if len(str(new_password)) != 6:  # or len(str(new_password_again)) != 6
                                print("\033[31mYour password must be a six digit password. Please try again.\033[m\n")
                                continue

                            elif new_password != new_password_again:
                                print("\033[31mYour passwords do not match. Please try again.\033[m\n")
                                continue

                        self.cursor.execute(
                            f"UPDATE customers SET password = {new_password} WHERE name = '{self.user_name}'")
                        self.connect.commit()
                        print(f"\033[1;32mYou successfully updated your password.\033[m")
                        break
                    except ValueError:
                        print("\033[mPassword must be an integer.\033[m\n")

            elif choice == 3:
                print("\033[93mWe are sorry to hear that you want to delete your account.\033[m")
                while True:
                    try:
                        print("\033[95mPress 4 to return back to menu, Press 5 to go back to main menu\033[m")
                        password = int(input("Please enter your a six digit password to delete your account: "))
                        if password == 4:
                            break

                        elif password == 5:
                            first_menu = False
                            self.is_main_run_active = False
                            self.run()
                            break
                        else:
                            password_again = int(input("Enter your new password again: "))
                            if len(str(password)) != 6:  # or len(str(new_password_again)) != 6
                                print("\033[31mYour password must be a six digit password. Please try again.\033[m\n")
                                continue

                            elif password != password_again:
                                print("\033[31mYour passwords do not match. Please try again.\033[m\n")
                                continue
                        self.cursor.execute(
                            f"DELETE FROM customers WHERE name = '{self.user_name}' and password = {password}")
                        self.connect.commit()
                        print(f"\033[1;32mYou successfully deleted your account :(\033[m")
                        print(f"\033[1;32mI hope we can see you again!\033[m")
                        first_menu = False
                        self.is_main_run_active = True
                        self.is_run_active = False

                        break
                    except ValueError:
                        print("\033[mPassword must be an integer.\033[m\n")

            elif choice == 4:
                first_menu = False
                self.is_main_run_active = False
                self.run()
                break

    def system_exit(self):
        self.is_main_run_active = False

        self.status = False

    def connect_database(self):

        self.connect = sqlite3.connect("atm.db")
        self.cursor = self.connect.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS customers(id INT,name TEXT,surname TEXT,email TEXT,city TEXT,gender TEXT,password INT,age INT,tl INT,usd INT,eur INT,notification TEXT,security_question TEXT)")

        self.connect.commit()

        # self.cursor.execute(
        #     "CREATE TABLE IF NOT EXISTS customers("
        #     "id INT",
        #     "name TEXT,"
        #     "surname TEXT,"
        #     "email TEXT,"
        #     "city TEXT,"
        #     "gender TEXT,"
        #     "password INT,"
        #     "age INT,tl INT,usd INT,eur INT)"
        # )

    def all_choice(self, min_num, max_num, msg1):
        while True:
            try:
                process = int(input("Enter your choice: "))
                if process < min_num or process > max_num:
                    print(
                        f"\033[31mYour choice must be between {min_num} - {max_num}, please select correct number!\033[m")
                    continue  # let's go back to loop
                if process == max_num:
                    print(msg1)
                    # break
                break
            except ValueError:
                print("\033[31mYour choice must be integer number. Please type in the correct type!\033[m")

        return process


ATM = Atm("OOP BANK", "Turkey")

while ATM.status:

    ATM.main_run()

    if ATM.is_everything_okay:
        ATM.run()
