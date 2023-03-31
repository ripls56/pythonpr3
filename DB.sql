set ansi_nulls on
go
set ansi_padding on
go
set quoted_identifier on 
go

use [master]
go

drop database [pythondb]
go

CREATE DATABASE [pythondb]
go

use [pythondb]
go

CREATE TABLE Ingredients (
    ID_Ingredients INT PRIMARY KEY IDENTITY(1,1),
    Ingredient_Name NVARCHAR(max) NOT NULL,
    Ingredient_Price DECIMAL(10, 2) DEFAULT 25,
	ActualCount INT NOT NULL DEFAULT 0,
	Ingredient_BuyPrice  DECIMAL(10, 2) DEFAULT 15,
);

CREATE TABLE Users (
    ID_User INT PRIMARY KEY IDENTITY(1,1),
    User_Login VARCHAR(50) NOT NULL,
    User_Password VARCHAR(50) NOT NULL,
    User_Role VARCHAR(20) CHECK (User_Role IN ('������������', '�������������')) NOT NULL,
    User_Balance DECIMAL(18,2) DEFAULT 5000,
    User_Card VARCHAR(20) CHECK (User_Card IN ('���', '���������', '����������', '�������')) DEFAULT '���',
	User_SumBuy DECIMAL(18,2) DEFAULT 0,
	User_Mail VARCHAR(max) NOT NULL,
	CONSTRAINT CK_User_Card CHECK ((User_Card = '���' AND User_SumBuy = 0) OR (User_Card = '���������' AND User_SumBuy = 5000) OR (User_Card = '����������' AND User_SumBuy = 15000) OR (User_Card = '�������' AND User_SumBuy = 25000))
);

CREATE TABLE Orders (
    ID_Order INT PRIMARY KEY IDENTITY(1,1),
    Order_ProductName VARCHAR(MAX) NOT NULL DEFAULT('���� ����'),
    Order_Count INT NOT NULL,
    Order_Date DATETIME NOT NULL DEFAULT(GETDATE()),
	Order_Price DECIMAL(18,2) DEFAULT 0,
	Order_Sale int not null default 0,
	UserID int not null,
	FOREIGN KEY (UserID) REFERENCES Users(ID_User)
);

CREATE TABLE Ingredient_Orders(
    ID_IngredientOrders INT PRIMARY KEY IDENTITY(1,1),
    IngredientID INT NOT NULL,
	OrderID INT NOT NULL,
    Count INT NOT NULL,
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(ID_Ingredients),
	FOREIGN KEY (OrderID) REFERENCES Orders(ID_Order)
);

INSERT INTO [dbo].[Users]
([User_Login],[User_Password],[User_Role],[User_Balance], [User_Mail]) VALUES
('test', 'test123', '������������', 15000, 'kanada.smirnov@yandex.ru'),
('user', 'user', '������������', 5000, 'kanada.smirnov@yandex.ru'),
('admin', 'admin', '�������������', 0, 'kanada.smirnov@yandex.ru')
GO

INSERT INTO [dbo].[Ingredients]
([Ingredient_Name],[Ingredient_Price],[ActualCount],[Ingredient_BuyPrice]) VALUES 
('�������� ���������', 100, 200, 250),
('������� HS', 50, 200, 150),
('���� ����', 25, 200, 50),
('���� ����������', 25, 200, 50),
('������ ��������', 25, 200, 100),
('������ ������������', 25, 200, 100),
('��������� ���', 25, 200, 50),
('������ ������', 50, 200, 250),
('����� �������', 100, 200, 250),
('����� ������������', 5, 200, 10)
GO