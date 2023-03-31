import pyodbc
import click
import os
from random import randint
from decimal import Decimal
import smtplib

connection = pyodbc.connect('Driver={SQL Server}; Server=.\SQLEXPRESS; Database=pythondb; Trusted_Connection=yes;')
cursor = connection.cursor()
user = None
smtpServer = "smtp.mail.ru"
port = 587
emailSender = "ripls56@mail.ru"
password = "zm6khN9074gGecQAX2iM"

def mail(receiverEmail):
    try:
        code = ""
        for i in range(6):
            code += str(randint(1, 9))
        # print(code)
        smpt = smtplib.SMTP(smtpServer, port)
        smpt.starttls()
        smpt.login(emailSender, password)
        smpt.sendmail(emailSender, receiverEmail, code)
    except Exception as e:
        print(e)
    finally:
        smpt.quit() 
        codeConfirm = input("Введите код с почты: ")
        if(code != codeConfirm):
            print("Неправильно")
            mail(receiverEmail)

class DataBase:
    
    def insertIngredient():
        try:
            os.system('cls')
            name = input("Введите название ингредиента: ")
            price = input("Введите цену ингредиента: ")
            buyprice = input("Введите закупочную цену ингредиента: ")
            insertQuery = f"INSERT INTO Ingredients (Ingredient_Name, Ingredient_Price, Ingredient_BuyPrice) VALUES ('{name}', {price}, {buyprice})"
            cursor.execute(insertQuery)
            connection.commit()
            click.pause(f"Игредиент '{name}' добавлен")
        except Exception as e:
            print(e)
    
    def updateIngredient(ingredients):
        try:
            os.system('cls')
            if(input("Изменить название? (Да / Нет) ")=="Да"):
                ingredients[1] = input("Введите новое название: ")
            if(input("Изменить цену?")=="Да"):
                ingredients[2] = input("Введите новую цену: ")
            updateQuery = f"UPDATE [dbo].[Ingredients] SET [Ingredient_Name] = '{ingredients[1]}', [Ingredient_Price] = {ingredients[2]} WHERE [ID_Ingredients] = {ingredients[0]}"
            cursor.execute(updateQuery)
            connection.commit()
            click.pause(f"Игредиент '{ingredients[1]}' изменен")
        except Exception as e:
            print(e)

    def deleteIngredient(ingredients):
        try:
            os.system('cls')
            if(input("Вы уверены? (Да / Нет) ")=="Да"):
                deleteQuery = f"DELETE FROM [dbo].[Ingredients] WHERE [ID_Ingredients] = {ingredients[0]}"
                cursor.execute(deleteQuery)
                connection.commit()
                click.pause(f"Игредиент '{ingredients[1]}' удален")
            else:
                click.pause(f"Игредиент '{ingredients[1]}' не удален")
        except Exception as e:
            print(e)
    
    def buyIngredient(ingredients):
        try:
            os.system('cls')
            balance = user[4]
            print(f"Закупка ингредиентов. Баланс: {balance}")
            count = int(input("Введите количество: "))
            price = ingredients[2] * count
            if balance < price:
                click.pause(f"Недостаточно средств, необходимо {price}.\n")
                return
            user[1] -= price
            insertQuery = f"UPDATE [dbo].[Ingredients] SET [ActualCount] = {ingredients[3]}+{count} WHERE [Ingredient_Name] = '{ingredients[1]}'"
            cursor.execute(insertQuery)
            insertQuery = f"UPDATE [dbo].[Users] SET [User_Balance] = {balance}-{price} WHERE [User_Login] = '{user[1]}'"
            cursor.execute(insertQuery)
            connection.commit()
            click.pause(f"""
                            Игредиент {ingredients[1]} закуплен в количестве {count}шт.
                            Теперь на складе {ingredients[3]+count}шт.
                        """)
        except Exception as e:
            print(e)
    
    def getAllIngredients():
        try:
            select_query = "SELECT * FROM Ingredients"
            cursor.execute(select_query)
            ingredients = cursor.fetchall()
            for i in ingredients:
                print(f"{i[0]} - {i[1]} - {i[2]} - {i[3]}")
            ingredientID = input("Введите номер ингредиента: ")
            ingredient = ingredients[int(ingredientID)-1]
            if ingredient is None:
                click.pause("Такого ингредиента нет")
                DataBase.getAllIngredients()
            else: 
                return ingredient
        except Exception as e:
            print(e)

    def buyProduct():
        print(f"""
            Пользователь: {user[1]}
            Ваш баланс составляет {user[4]} $.
            Действует акция за 2 или более купленных мега ролла 😎  вы получаете еще один В ПОДАРОК!
            """)
        ingrs = cursor.execute("SELECT * FROM Ingredients").fetchall()
        basePrice = 50
        orderCount = int(input(f"Сколько мега роллов вы хотите приобрести?({basePrice}/шт) : "))
        if orderCount >= 2:
            orderCount + 1
        orderPrice = basePrice * orderCount
        rolls = []
        for i in range(orderCount):
            print(f"Собери свой мега ролл ヾ(≧▽≦*)o №{i+1}")
            ingredientList = {"ingredients":[], "count":[], "price":0}
            while input("Вы хотите добавить дополнительные ингредиенты в заказ? (Да / Нет): ") == "Да":
                num = 1
                for i in ingrs:
                    print(f"{num} - {i[1]}: {i[2]} $")
                    num+=1
                ingrID = int(input("Введите номер ингредиента, который вы хотите добавить: "))-1
                addcount = int(input("Введите количество ингредиента, который вы хотите добавить: "))
                if ingrs[ingrID-1][3] < addcount:
                    click.pause("Извините, но на складе нет такого количества ингредиентов!\n ")
                    return
                orderPrice += float(ingrs[ingrID][2]) * addcount
                ingredientList["price"] += float(ingrs[ingrID][2]) * addcount
                ingredientList["ingredients"].append(ingrs[ingrID][0])
                ingredientList["count"].append(addcount)
                print(f"Вы добавили {ingrs[ingrID]} в заказ №{num}! ({addcount} шт)")
            rolls.append(ingredientList)
        sale = countSale()
        orderPrice -= orderPrice * (sale/100)
        print(f"Стоимость заказа составит - {orderPrice} (Скидка: {sale}%)")
        if input("Завершить заказ? (Да / Нет): ") != "Да":
            return
        if user[4] < orderPrice:
            click.pause("Недостаточно средств на счете!")
            return
        cursor.execute(f"UPDATE Users SET User_Balance = {user[4]} - {orderPrice} WHERE ID_User = {user[0]}")
        for item in rolls:
            d = item["price"]
            cursor.execute(f"INSERT INTO Orders (UserID, Order_Price, Order_Count, Order_Sale) VALUES ({user[0]}, {orderPrice}, {d}, {sale})")
            count = len(item["ingredients"])
            if(count > 0):
                orderID = cursor.execute("SELECT MAX(ID_Order) FROM Orders").fetchone()[0]
                for j in range(count):
                    ingID = item["ingredients"][j]
                    ingCount = item["count"][j]
                    cursor.execute(f"insert into Ingredient_Orders (OrderID, IngredientID, Count) values ({orderID}, {ingID}, {ingCount})")
        connection.commit()
        user[4] -= Decimal(orderPrice)
    
    def userHistory(userID):
        try:
            cursor.execute(f"SELECT * FROM Orders WHERE [USERID] = {userID}")
            orders = cursor.fetchall()
            print("История заказов:")
            if(len(orders)==0):
                print("Вы пока не совершили заказ, но никогда не поздно 🙂")
            else:
                for i in orders:
                    print(f"Заказ №{i[0]} \"{i[1]}\" на сумму {i[4]} [{i[3]}]")
                    cursor.execute(f"SELECT * FROM [Ingredient_Orders] inner join [dbo].[Ingredients] on IngredientID = ID_Ingredients WHERE [ORDERID] = {i[0]} order by ID_IngredientOrders")
                    ingredients = cursor.fetchall()
                    for j in ingredients:
                        print(f"Доп. ингредиент: {j[6]} - {j[3]}шт./{j[8]}р.")
            click.pause()
        except Exception as e:
            print(e)

    
    def getUserByLogin(login):
        try:
            selectQuery = f"SELECT * FROM Users WHERE User_Login = '{login}'"
            cursor.execute(selectQuery)
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(e)
    
def registration():
    try:
        os.system('cls')
        userLogin = input("Введите логин: ")
        user = DataBase.getUserByLogin(userLogin)
        if user is not None:
            click.pause("Пользователь с таким логином уже существует\nНажмите любую кнопку для повторного ввода")
            registration()
        password = input("Введите пароль: ")
        password2 = input("Повторите пароль: ")
        if (password != password2):
            click.pause("Пароли не совпадают\nНажмите любую кнопку для повторного ввода")
            registration()
        roleID = input("Выберите роль: (1 - Пользователь, 2 - Администратор): ")
        toEmail = input("Введите почту: ")
        mail(toEmail)
        role = "Пользователь"
        match roleID:
            case "1":
                role = "Пользователь"
            case "2":
                role = "Администратор"
            case _:
                registration()
        insertQuery = f"INSERT INTO Users (User_Login, User_Password, User_Role, User_Mail) VALUES ('{userLogin}', '{password}', '{role}', '{toEmail}')"
        cursor.execute(insertQuery)
        connection.commit()
        click.pause("Вы успешно зарегистрировались, нажмите любую клавишу для перехода к окну авторизации")
        login()
    except Exception as e:
        print(e)

def login():
    try:
        global user
        os.system('cls')
        userLogin = input("Введите логин: ")
        password = input("Введите пароль: ")
        user = DataBase.getUserByLogin(userLogin)
        if user is None:
            click.pause("Пользователь не найден\nНажмите любую кнопку для повторного ввода")
            login()
        else:
            if user[2] != password:
                click.pause("Неверный пароль\nНажмите любую кнопку для повторного ввода")
                login()
        mail(user[7])
    except Exception as e:
        print(e)


def userInterface():
    os.system('cls')
    match(input("Выберите функцию:  (1 - Составить заказ, 2 - Просмотреть историю заказов: ")):
        case "1":
            DataBase.buyProduct()
            return
        case "2":
            DataBase.userHistory(user[0])
            return
        case _:
            userInterface()

def countSale():
    sale = 0
    if(randint(1, 6)==5):
        print("Таракан?! Да вы сами подкинули не верим, но на первый раз держите скидку в 30% 🫥")
        sale += 30
    match(user[5]):
        case "Бронзовая":
            sale += 5
        case "Серебряная":
            sale += 10
        case "Золотая":
            sale += 20
    return sale

def adminInterface():
    match(input("Выберите функцию!  (1 - Выбор игредиента, 2 - Добавление ингредиента, 3 - История): ")):
        case "1":
            select = DataBase.getAllIngredients()
            match(input(f"Действие с ингредиентом '{select[1]}'  (1 - Закупка, 2 - Изменение, 3 - Удаление): ")):
                case "1":
                    DataBase.buyIngredient(select)
                case "2":
                    DataBase.updateIngredient(select)
                case "3":
                    DataBase.deleteIngredient(select)
                case _:
                    click.pause()
        case "2":
            DataBase.insertIngredient()
        case "3":
            users = cursor.execute("SELECT * FROM Users")
            for i in users:
                print(f"{i[0]} - {i[1]}")
            id = input("Введите номер пользователя, историю которого хотите посмотреть:")
            os.system('cls')
            DataBase.userHistory(id)
            return
        case _:
            adminInterface()


if __name__ == "__main__":
    os.system('cls')
    print("Кифас （￣︶￣）↗")
    action = input("Добро пожаловать, выберите дальнейшее действие  (1 - Авторизация, 2 - Регистрация): ")
    try:
        match(action):
            case "1":
                login()
            case "2":
                registration()
            case _:
                exit()
        while 1:
            os.system('cls')
            print(f"""
                    Добро пожаловать: {user[1]}!
                    Вход выполнен под ролью: {user[3]}
                    Баланс: {user[4]} $
                  """)
            match(user[3]):
                case "Администратор":
                    adminInterface()
                case "Пользователь":
                    userInterface()
        click.pause("Нажмите любую клавишу для выхода")
    except Exception as e:
        print(e)
