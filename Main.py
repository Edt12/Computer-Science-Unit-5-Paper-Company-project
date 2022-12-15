import sqlite3
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition #Kivy has screens not pop up windows so screen manage manager different screens think of like switching between virtual desktops
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label#import widgets such as buttons and labels 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.core.window import Window

green = [0, 1, 0, 1] #RGBA values /255
Grey=[0.8,0.8,0.8,1]
Black=[0,0,0,1]

#Creating Sqlite Database
conn=sqlite3.connect("DunderMifflinDatabase.db")#connects to database 
cursor=conn.cursor()#adds connection to cursor


class Shopfront(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()


sm=ScreenManager()
    
class Login(Screen):#Create different windows class
   
    def __init__(self,**kwargs):#Instead of using build to intialise use init as build does not work with screen class
        Screen.__init__(self,**kwargs)
    
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255

        self.layout=FloatLayout()#float layout allows you to place widgets anywhere

        Username=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5})#creates Input box called username,on size_hint first value is length second is width
        self.add_widget(Username)

        Password=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4})#creates Input box called username,on size_hint first value is length second is width
        self.add_widget(Password)

        EnterUsernameandPassword=Button(size_hint=(0.1,0.05),pos_hint={'x':0.7,'y':0.5},text="Enter",background_color=green)

   
        def LoginClick(self):
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            username=cursor.execute("SELECT Username From UsersAndPasswords")
            
            ProductPos_hintX=0.0
            ProductPos_hintY=0.0
            ProductNumber=0
          
            for row in Table:#goes through every column in UserAndPasswords
                if row[0]== Username.text and row[1]== Password.text:
                    print("Both Correct")
                    cursor.execute("SELECT * from Products")
                    Table=cursor.fetchall()
                    print(Table)
                    for row in Table: 
                        sm.current="shopfront"
                        print("steve")
                        ShopfrontScreen=sm.get_screen("shopfront")

                        ProductName=row[0]
                        ProductPrice=row[1]
                        #work out which where button is in title 
                        cursor.execute("SELECT * from Products")
                    
                        print(ProductName)
                        print(cursor.fetchall())

                        def ProductPress(self):
                            Quantity=0
                            ProductPressed=self.text
                            Quantity+=1
                            cursor.execute("SELECT *FROM Basket Where Productname = (?)",(ProductPressed,))#First Searches for item in basket
                            Search=cursor.fetchall()
                            print(Search)
                            if Search==[]:#if item not in basket
                                Product=self.text#getting title then using it to search the database for its price then adding price to basket
                                cursor.execute("SELECT *FROM Products Where Productname = (?)",(Product,))
                                ProductPrice=row[1]
                                print(ProductPrice)
                                cursor.execute("INSERT INTO Basket(Productname,ProductPrice,Quantity)VALUES(?,?,?)",(Product,ProductPrice,Quantity))
                                conn.commit()
                                cursor.execute("SELECT * FROM Basket")
                                cursor.fetchall()



                        IndividualProduct=Button(size_hint=(0.2,0.1),pos_hint={'x':ProductPos_hintX,'y':ProductPos_hintY},text=str(ProductName),background_color=green,color=Black)
                        IndividualProduct.bind(on_press=ProductPress)
                        ShopfrontScreen.add_widget(IndividualProduct)
                        ProductPos_hintX+=0.2
                        ProductNumber+=1

                        ProductNumber_DividedBy5=ProductNumber/5
                        if ProductNumber_DividedBy5.is_integer():#is integer checks whether something is integer
                            ProductPos_hintX=0
                            ProductPos_hintY+=0.1

                if row[0]== Username.text and row[1]!= Password.text:
                    Password.text==""
                    print("incorrect password")

                if row[0]!= Username.text and row[1]== Password.text:
                    Username.text==""
                    print("incorrect username")
                    
            

        EnterUsernameandPassword.bind(on_press=LoginClick)
        self.add_widget(EnterUsernameandPassword)

        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        self.add_widget(LoginTitle)
        
    



def main():
    cursor.execute("""create table IF NOT EXISTS Products(
    Productname text
    ,ProductPrice text
    )""")


    cursor.execute("""create table IF NOT EXISTS Basket(
    Productname text
    ,ProductPrice text
    ,Quantity text
    )""")

    #creates SQlite Database
    cursor.execute("""create table IF NOT EXISTS UsersAndPasswords 
    (Username text
    ,Password text 
    )""")#inside are columns/categorys



    sm.add_widget(Shopfront(name="shopfront"))
    sm.add_widget(Login(name="Login"))
    sm.current="Login"
    class PaperApp(App):
        def build(self):
            return sm 

    PaperApp().run()

    cursor.execute("SELECT * From UsersAndPasswords")
    test=cursor.fetchall()
    cursor.execute("Drop table Basket;")#because basket is temporary delete table at end
    cursor.close()
    print(test)

main()