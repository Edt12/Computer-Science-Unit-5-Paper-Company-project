import sqlite3
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition #Kivy has screens not pop up windows so screen manage manager has different screens think of like switching between virtual desktops
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label#import widgets such as buttons and labels 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.core.window import Window
import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import hashlib

green = [0, 1, 0, 1] #RGBA values /255 
Grey=[0.8,0.8,0.8,1]
Black=[0,0,0,1]
KeyStore=[]
ProductNameStore=[]
#Creating Sqlite Database
conn=sqlite3.connect("DunderMifflinDatabase.db")#connects to database 
cursor=conn.cursor()#adds connection to cursor
Screenmanager=ScreenManager()#Each Screen is called by screen manager which is used for commands which involve changing between screens
#generates encryption key using Scrypt
def GenerateKey(UsernameAndPassword,salt):
    KeyDerivationFunction=Scrypt(salt=salt,length=32,n=2,r=1,p=1)
    UsernameAndPassword=str(UsernameAndPassword).encode()   
    Key=base64.urlsafe_b64encode(KeyDerivationFunction.derive(UsernameAndPassword))
    return Key

def Encrypt(Data):
     pass
def Decrypt(Data):
     pass


       
        
class Login(Screen):
   
    def __init__(self,**kwargs):
        Screen.__init__(self,**kwargs)
    
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255

        self.layout=FloatLayout()

        UsernameEntry=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5})
        self.add_widget(UsernameEntry)

        PasswordEntry=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.4})
        self.add_widget(PasswordEntry)

        EnterUsernameandPassword=Button(size_hint=(0.1,0.05),pos_hint={'x':0.7,'y':0.5},text="Enter",background_color=green)


        def LoginClick(self):
           
            
            ProductPos_hintX=0.0
            ProductPos_hintY=0.0
            ProductNumber=0
            #hashes Username
            Username=UsernameEntry.text
            EncodedUsername=Username.encode()
            HashedUsername=hashlib.sha3_512(EncodedUsername)
            #hashes password
            Password=PasswordEntry.text
            EncodedPassword=Password.encode()
            HashedPassword=hashlib.sha3_512(EncodedPassword)
            cursor.execute("SELECT * From UsersAndPasswords")
            Table=cursor.fetchall()
            if Table!=[]:
                for row in Table:#goes through every row in UserAndPasswords Table
                    #compare inputed hashed username and password when they are in hexdigest form as that is how they are stored in database
                    print("compare")
                
                    if row[1]== HashedUsername.hexdigest() and row[2]== HashedPassword.hexdigest():#rows in sqlite can be referenced through a list e.g row 0 is first column ,row 1 is second column
                        print("Both Correct")#Username.text and Password.text are text from login input boxes
                        #generate cipher for encryption
                        HexedHashedUsername=HashedUsername.hexdigest()
                        cursor.execute("Select Salt from UsersAndPasswords where Username=(?)",(HexedHashedUsername,))
                        Salt=cursor.fetchone()
                        UsernameAndPassword=HashedPassword.hexdigest()+HashedUsername.hexdigest()
                        Key=GenerateKey(UsernameAndPassword,salt=Salt[0])
                        cipher=Fernet(Key)
                        KeyStore.append(Key)
                        print(Key)
                        print(KeyStore)
                        print(KeyStore[0])
                        #defines encrypt and decrypt functions
                        def Decrypt(Data):
                            DecryptedData=cipher.decrypt(Data)
                            return DecryptedData
                        
                        def Encrypt(Data):
                            Data=str(Data)
                            DataBytes=bytes(Data, 'utf-8')
                            EncryptedData=cipher.encrypt(DataBytes)
                            return EncryptedData
                        print(Encrypt("steve"))
                        cursor.execute("SELECT * from Products")
                        Table=cursor.fetchall()
                        print(Table)
                        for row in Table: 
                            Screenmanager.current="Shopfront"
                            ShopfrontScreen=Screenmanager.get_screen("Shopfront")#get screen grabs an instance of a screen and is used to place widgets on different screens

                            ProductName=row[0]
                            ProductPrice=row[1]
                            cursor.execute("SELECT * from Products")
                        
                        

                            def ProductPress(self):
                                Quantity=0
                                ProductPressed=self.text
                                Quantity+=1

                                
                                cursor.execute("SELECT *FROM Basket Where Productname = (?)",(ProductPressed,))#First Searches for item in basket
                                Product=self.text#getting title then using it to search the database for its price then adding price to basket
                                cursor.execute("SELECT *FROM Products Where Productname = (?)",(Product,))
                               
                                EncryptedProduct=Encrypt(Product)
                                cursor.execute("Select Productname from Basket")
                                Basket=cursor.fetchall()
                                print(Basket)
                                def DecryptBasket(self):
                                    for row in Basket:
                                        print("Decrypting Basket")
                                        DecryptedProductName=Decrypt(row[0])
                                        ProductNameStore.append(DecryptedProductName)
                                        print(ProductNameStore)
                                        return ProductNameStore
                                def CompareBasketToProductPressed(self):
                                    print("Comparing Basket")
                                    print(ProductNameStore)
                                    Index=-1
                                    for i in ProductNameStore:
                                        Index+=1
                                        print(Index)
                                        ItemAlreadyInBasket=False    
                                        print("searching")
                                        if ProductNameStore[Index]==bytes(ProductPressed,'utf-8'):
                                            print("great Success")
                                            cursor.execute("Select Quantity from Basket where Productname=(?)",(EncryptedProduct,))
                                            TempQuantity=cursor.fetchone()
                                            Quantity=Decrypt(TempQuantity)
                                            Quantity+=1
                                            EncryptedQuantity2=Encrypt(Quantity)
                                            cursor.execute("Update Basket Set Quantity=? Where Productname=?",(EncryptedQuantity2,EncryptedProduct))
                                            conn.commit()
                                            ItemAlreadyInBasket=True
                                            return ItemAlreadyInBasket
                                        else:
                                            print("HE CANNOT AFFORD")
                                            return ItemAlreadyInBasket


                                DecryptBasket(self)
                                ItemAlreadyInBasket=CompareBasketToProductPressed(self)
                                Basket="stewetww"
                                
                                   

                    
                                if ItemAlreadyInBasket==False:
                                    print("adding to basket new ")
                                    EncryptedProductPrice=Encrypt(ProductPrice)
                                    EncryptedQuantity=Encrypt(Quantity)
                                    cursor.execute("INSERT INTO Basket(Productname,ProductPrice,Quantity)VALUES(?,?,?)",(EncryptedProduct,EncryptedProductPrice,EncryptedQuantity))
                                    conn.commit()

 
                        IndividualProduct=Button(size_hint=(0.2,0.1),pos_hint={'x':ProductPos_hintX,'y':ProductPos_hintY},text=str(ProductName),background_color=green,color=Black)
                        IndividualProduct.bind(on_press=ProductPress)
                        ShopfrontScreen.add_widget(IndividualProduct)
                        ProductPos_hintX+=0.2
                        ProductNumber+=1

                        ProductNumber_DividedBy5=ProductNumber/5
                        if ProductNumber_DividedBy5.is_integer():#is integer checks whether something is integer
                            ProductPos_hintX=0
                            ProductPos_hintY+=0.1
                    
            if row[0]== UsernameEntry.text and row[1]!= PasswordEntry.text:
                        print("incorrect")
                        
            if row[0]!= UsernameEntry.text and row[1]== PasswordEntry.text:
                        print("incorrect")

            if row[0]!= UsernameEntry.text and row[1]== PasswordEntry.text:
                        print("incorrect")
                   
        EnterUsernameandPassword.bind(on_press=LoginClick)
        self.add_widget(EnterUsernameandPassword)

        AddNewCustomer=Button(size_hint=(0.2,0.05),pos_hint={'x':0.7,'y':0.4},text=str("Add New Customer"),background_color=green)
        def AddCustomer(self):
            CustomerUsername=UsernameEntry.text
            CustomerPassword=PasswordEntry.text
            EncodedUsername=CustomerUsername.encode()#To hash first encode then hash
            HashedUsername=hashlib.sha3_512(EncodedUsername)
            EncodedPassword=CustomerPassword.encode()
            HashedPassword=hashlib.sha3_512(EncodedPassword)
            UserType="Customer"#all accounts made this way will be customer level access as higher levels only made by managers
            cursor.execute("Select Username from UsersAndPasswords")
            Usernames=cursor.fetchall()
            print(Usernames)
            def check():
                UsernameAlreadyUsed=False
                if Usernames!=[]:
                    for row in Usernames:
                        print("rowing")
                        if HashedUsername.hexdigest()==row[0]:
                            print("Checking")
                            UsernameAlreadyUse=True
                            return UsernameAlreadyUse
                        else:
                             return UsernameAlreadyUse
                else: 
                    return UsernameAlreadyUsed       
                        
            UsernameAlreadyUse=check()#function so commands below arent executed in a loop
            print(UsernameAlreadyUse)
            #Insert hashes into database as hex digest as by defualt their datatype is not supported
            if UsernameAlreadyUse==False:
                salt=os.urandom(32)
                cursor.execute("Insert into UsersAndPasswords (Username,Password,UserType,Salt)VALUES(?,?,?,?)",(HashedUsername.hexdigest(),HashedPassword.hexdigest(),UserType,salt))
                conn.commit()
                print("Adding")
            if UsernameAlreadyUse==True:
                UsernameEntry.text="Username Already Used"
                print("Not Adding")
            
            UsernameEntry.text=""
            PasswordEntry.text=""
        AddNewCustomer.bind(on_press=AddCustomer)
        self.add_widget(AddNewCustomer)
        LoginTitle=Label(text="Please Enter Your Username and Password",size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.6},color=Black)
        self.add_widget(LoginTitle)


def Decrypt(Data):
    print(Data)
    Key=KeyStore[0]
    cipher=Fernet(Key)
    DecryptedData=cipher.decrypt(Data)
    return DecryptedData.decode('utf-8')
                        
def Encrypt(Data):
    print(Data)
    Key=KeyStore[0]
    cipher=Fernet(Key)
    Data=str(Data)
    DataBytes=bytes(Data,'utf-8')
    EncryptedData=cipher.encrypt(DataBytes)
    return EncryptedData

#inputs-Payment Information
#outputs-Order(deliveryaddress and Order)
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
            ViewBasketScreen=Screenmanager.get_screen(Screenmanager.current)
            Screenmanager.current="Shopfront"
            ViewBasketScreen.clear_widgets()
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
            test=Encrypt("Steve")                     
            print(test)
            print("decrypttesst")
            print(Decrypt(test))
            Screenmanager.current="ViewBasket"
            ViewBasketScreen=Screenmanager.get_screen("ViewBasket")
            #In future need to add some way of getting the quantity of a specific item and removing the previous label if more items are added to basket after someone has already pressed viewbasket
            cursor.execute("Select * From Basket")
            Basket=cursor.fetchall()
            for row in Basket:
                print(type(row))
                DecryptedProduct=Decrypt(row[0])
                DecryptedProductPrice=Decrypt(row[1])
                DecryptedQuantity=Decrypt(row[2])
                Product=Label(text=DecryptedProduct+" "+DecryptedProductPrice+" "+DecryptedQuantity,size_hint=(0.2,0.1),pos_hint={'x':0.5,'y':0.5},color=Black)
                ViewBasketScreen.add_widget(Product) 
            
        
        Viewbasket=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text="ViewBasket",background_color=green,color=Black)
        Viewbasket.bind(on_press=ViewBasketClick)
        self.add_widget(Viewbasket)

            #help button will be added later

def main():
  
    #payment information table will be added in future
    cursor.execute("""create table IF NOT EXISTS Products(
    Productname text Primary Key
    ,ProductPrice text(6)
    )""")


    cursor.execute("""create table IF NOT EXISTS Basket(
    Productname blob(128)
    ,ProductPrice blob(128)
    ,Quantity blob (128)
    )""")

    #creates SQlite Database
    cursor.execute("""create table IF NOT EXISTS UsersAndPasswords
    (UserID integer Primary Key Autoincrement
    ,Username blob (512) 
    ,Password blob (512)
    ,Salt int(32)
    ,Usertype text
    )""")#inside are columns/categorys

    cursor.execute("""create Table IF NOT EXISTS PaymentInfo(
     CardNumber blob(128) Primary Key
    ,SecurityCode blob(128)
    ,ExpirationDate blob(128)
    ,BillingAddress blob(128)
    ,Postcode blob(128)
    ,UserID integer
    ,FOREIGN KEY(UserID) REFERENCES UsersAndPasswords(UserID))""")#() next to text is length of the inputs in bytes and for text data type it is number of characters

    Screenmanager.add_widget(PaymentScreen(name="PaymentScreen"))#adds each screen to screenmanager to so they can be controlled
    Screenmanager.add_widget(ViewBasket(name="ViewBasket"))
    Screenmanager.add_widget(Shopfront(name="Shopfront"))
    Screenmanager.add_widget(Login(name="Login"))
    Screenmanager.current="Login"

  
    class PaperApp(App):#app class contains screenmanager  
        def build(self):
            return Screenmanager 
    PaperApp().run()
    cursor.execute("Drop Table Basket")

    cursor.close()
main()