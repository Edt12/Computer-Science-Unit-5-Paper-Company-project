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
#Note this protype currently only covers the customer user type in future manager and employee functions will be added
#Creating Sqlite Database
conn=sqlite3.connect("DunderMifflinDatabase.db")#connects to database 
cursor=conn.cursor()#adds connection to cursor
Screenmanager=ScreenManager()#Each Screen is called by screen manager which is used for commands which involve changing between screens
class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()#Float Layout is a layout in which widgets by defualt are not postioned

        PaymentScreenTitle=Label(text="Payment Screen",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)#Size_hint is size relative to screen size pos_hint is position relative to screen size e.g 0.1=one tenth
        self.add_widget(PaymentScreenTitle)

        Back=Button(size_hint=(0.2,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)#color is writing color background color is background
        def BackClick(self):
            Screenmanager.current="Shopfront"
        Back.bind(on_press=BackClick)#binds a function to happen when a button is pressed
        self.add_widget(Back)

        CardNumber=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.8},text="Card Number")
        self.add_widget(CardNumber)
        
        ExpirationDate=TextInput(size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.7},text="Expiration Date")
        self.add_widget(ExpirationDate)

        SecurityCode=TextInput(size_hint=(0.1,0.05),pos_hint={'x':0.4,'y':0.7},text="Security Code")
        self.add_widget(SecurityCode)

        BillingAddress=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.6},text="Billing Address")
        self.add_widget(BillingAddress)

        BillingAddressLine2=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5},text="Billing Address Line 2")
        self.add_widget(BillingAddressLine2)

        Country=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4},text="Country")
        self.add_widget(Country)

        Postcode=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.3},text="Postcode")
        self.add_widget(Postcode)

        EmailAddress=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.2},text="Email Address")
        self.add_widget(EmailAddress)


        DeliveryAddress=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.1},text="Delivery Address")
        self.add_widget(DeliveryAddress)


        DeliveryPostcode=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.0},text="Delivery Postcode")
        self.add_widget(DeliveryPostcode)

        RememberButton=Button(size_hint=(0.3,0.05),pos_hint={'x':0.7,'y':0.7},text="Remember my Payment information",background_color=green,color=Black)
        #in future a function which reads all the numbers into a database will be added
        self.add_widget(RememberButton)

        PayButton=Button(size_hint=(0.3,0.05),pos_hint={'x':0.7,'y':0.8},text="Pay",background_color=green,color=Black)
        def PayButtonClick(self):
            CardNumber.text=""
            SecurityCode.text=""
            ExpirationDate.text=""
            BillingAddress.text=""
            BillingAddressLine2.text=""
            Country.text=""
            Postcode.text=""
            EmailAddress.text=""
            DeliveryAddress.text=""
            DeliveryPostcode.text=""
        PayButton.bind(on_press=PayButtonClick)   
        self.add_widget(PayButton)
        #help button will be added later


class ViewBasket(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()
        ViewBasketTitle=Label(text="Basket View Screen",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)
        self.add_widget(ViewBasketTitle)

        CheckoutAndPay=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text=str("Checkout and Pay"),background_color=green,color=Black)
        def CheckoutAndPayClick(self):
            Screenmanager.current="PaymentScreen"
        
        CheckoutAndPay.bind(on_press=CheckoutAndPayClick)        
        self.add_widget(CheckoutAndPay)
        
        Back=Button(size_hint=(0.2,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)
        def BackClick(self):
            Screenmanager.current="Shopfront"
        Back.bind(on_press=BackClick)
        self.add_widget(Back)
        #help button will be added later
class Shopfront(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()
        ShopfrontTitle=Label(text="Shopfront",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)
        self.add_widget(ShopfrontTitle)

        def ViewBasketClick(self):
            Screenmanager.current="ViewBasket"
            ViewBasketScreen=Screenmanager.get_screen("ViewBasket")
            #In future need to add some way of getting the quantity of a specific item and removing the previous label if more items are added to basket after someone has already pressed viewbasket
            cursor.execute("Select * From Basket")
            Table=cursor.fetchall()
            Product=Label(text=str(Table),size_hint=(0.2,0.1),pos_hint={'x':0.5,'y':0.5},color=Black)
            ViewBasketScreen.add_widget(Product)
            
        
        Viewbasket=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text="ViewBasket",background_color=green,color=Black)
        Viewbasket.bind(on_press=ViewBasketClick)
        self.add_widget(Viewbasket)

            #help button will be added later


       
        
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
          
            for row in Table:#goes through every row in UserAndPasswords Table
                if row[0]== Username.text and row[1]== Password.text:#rows in sqlite can be referenced through a list e.g row 0 is first column ,row 1 is second column
                    print("Both Correct")#Username.text and Password.text are text from login input boxes
                    cursor.execute("SELECT * from Products")
                    Table=cursor.fetchall()
                    print(Table)
                    for row in Table: 
                        Screenmanager.current="Shopfront"
                        print("steve")
                        ShopfrontScreen=Screenmanager.get_screen("Shopfront")#get screen grabs an instance of a screen and is used to place widgets on different screens

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
                        print("incorrect")
                        
            if row[0]!= Username.text and row[1]== Password.text:
                        print("incorrect")

            if row[0]!= Username.text and row[1]== Password.text:
                        print("incorrect")
                        
            

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

    Screenmanager.add_widget(PaymentScreen(name="PaymentScreen"))#adds each screen to screenmanager to so they can be controlled
    Screenmanager.add_widget(ViewBasket(name="ViewBasket"))
    Screenmanager.add_widget(Shopfront(name="Shopfront"))
    Screenmanager.add_widget(Login(name="Login"))
    Screenmanager.current="Login"
    class PaperApp(App):#app class contains screenmanager
        def build(self):
            return Screenmanager 

    PaperApp().run()


    cursor.execute("Drop table Basket;")#because basket is temporary delete table at end
    cursor.close()

main()