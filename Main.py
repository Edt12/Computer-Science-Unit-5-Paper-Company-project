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
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import hashlib

green=[0, 1, 0, 1] #RGBA values /255 
Grey=[0.8,0.8,0.8,1]
Black=[0,0,0,1]
KeyStore=[]
ProductNameStore=[]
EncryptedProductNameStore=[]
ProductExistsOnScreen=[]
ProductsInBasket=[]
UserIDStore=[]
NumberOfTimesRefreshedPressed=[]
WidgetList=[]
AccessLevel=[]
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
def EmailAddressValid(EmailAddress):
    for letter in EmailAddress.text:
        if '@' in EmailAddress.text:
            print("Valid Email")
            return True
        else:
            EmailAddress.text="Must Contain @"
            return False
def NumberChecker(Input):
    try:
        int(Input)
    except ValueError:
        print("Not an Integer")
        return False         
def RefreshOrderView():
        print("working")
        cursor.execute("Select * from Orders")
        EncryptedOrders=cursor.fetchall()
        OrderViewScreen=Screenmanager.get_screen("OrderView")
        OrderViewScreen.clear_widgets()
        ItemXpos=0.1
        DeliveryAddressXpos=0.4
        PostcodeXPos=0.6
        CompleteButtonXpos=0.8
        Ypos=0.8
        ItemLabel=Label(text="Items",size_hint=(0.2,0.1),pos_hint={'x':0.1,'y':0.9},color=Black)
        OrderViewScreen.add_widget(ItemLabel)

        DeliveryAddressLabel=Label(text="Delivery Address",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)
        OrderViewScreen.add_widget(DeliveryAddressLabel)

        DeliveryPostcodeLabel=Label(text="Delivery Postcode",size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.9},color=Black)
        OrderViewScreen.add_widget(DeliveryPostcodeLabel)

                 
        Refresh=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text="Refresh",background_color=green,color=Black)
        Refresh.bind(on_press=lambda Refresh:RefreshOrderView())#lambda stores function in memory to be used when button is pressed
        OrderViewScreen.add_widget(Refresh)

        Back=Button(size_hint=(0.175,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)
        def BackClick(self):
            print(AccessLevel)
            if len(AccessLevel)==0:
                Screenmanager.current="Staff"
            if len(AccessLevel)==1:
                Screenmanager.current="Manager"

        Back.bind(on_press=BackClick)
        OrderViewScreen.add_widget(Back)
        for row in EncryptedOrders:
                OrderID=row[0]
                EncryptedItems=row[1]
                EncryptedDeliveryAddress=row[2]
                EncryptedPostcode=row[3]
                UserID=row[4]
                cursor.execute("Select Username from UsersAndPasswords Where UserID=(?)",str(UserID))
                HashedHexedUsername=cursor.fetchone()
                cursor.execute("Select Password from UsersAndPasswords Where UserID=(?)",str(UserID))
                HashedHexedPassword=cursor.fetchone()
                cursor.execute("Select Salt from UsersAndPasswords Where UserID=(?)",str(UserID))
                Salt=cursor.fetchone()
                
                #Taking all necessary data to make the encrytion key for the user then use it to decrypt their order
                UsernameAndPassword=HashedHexedPassword[0]+HashedHexedUsername[0]
                OrderEncryptionKey=GenerateKey(UsernameAndPassword=UsernameAndPassword,salt=Salt[0])
         
     
           
                DeliveryAddress=Decrypt(EncryptedDeliveryAddress,Key=OrderEncryptionKey)
                Postcode=Decrypt(EncryptedPostcode,Key=OrderEncryptionKey)
                Items=Decrypt(EncryptedItems,Key=OrderEncryptionKey)
           

                ItemsLabel=Label(text=Items,size_hint=(0.2,0.1),pos_hint={'x':ItemXpos,'y':Ypos},color=Black)
                OrderViewScreen.add_widget(ItemsLabel)
                
                DeliveryAddressLabel=Label(text=DeliveryAddress,size_hint=(0.2,0.1),pos_hint={'x':DeliveryAddressXpos,'y':Ypos},color=Black)
                OrderViewScreen.add_widget(DeliveryAddressLabel)
                                
                PostcodeLabel=Label(text=Postcode,size_hint=(0.2,0.1),pos_hint={'x':PostcodeXPos,'y':Ypos},color=Black)
                OrderViewScreen.add_widget(PostcodeLabel)

                CompleteButton=Button(size_hint=(0.2,0.1),pos_hint={'x':CompleteButtonXpos,'y':Ypos},text="Complete Order"+":"+str(OrderID),background_color=green,color=Black)
                def CompleteOrderClick(self):
                    Text=self.text
                    ListOfText=Text.split(":")
                    OrderID=ListOfText[1]
                    cursor.execute("Delete from Orders Where OrderID=(?)",OrderID)
                    conn.commit()
                    RefreshOrderView()
                    
                CompleteButton.bind(on_press=CompleteOrderClick)
                OrderViewScreen.add_widget(CompleteButton)



                
                Ypos-=0.1


       
        
class Login(Screen):
   
    def __init__(self,**kwargs):
        Screen.__init__(self,**kwargs)
    
        Window.clearcolor =(Grey)#sets background color for window to get value take each rgb value and divide by 255
        self.layout=FloatLayout()
        
        BackgroundImage=Image(source="Dunder-Mifflin-Symbol.png",pos_hint={'x':0.0,'y':0.7},size_hint=(0.2,0.4))
        self.add_widget(BackgroundImage)
       
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
            # hashes password
            Password=PasswordEntry.text
            EncodedPassword=Password.encode()
            HashedPassword=hashlib.sha3_512(EncodedPassword)
            cursor.execute("SELECT * From UsersAndPasswords")
            UsersAndPasswords=cursor.fetchall()
            if UsersAndPasswords!=[]:
                for row in UsersAndPasswords:#goes through every row in UserAndPasswords Table
                    #compare inputed hashed username and password when they are in hexdigest form as that is how they are stored in database
                    print("compare")
                
                    if row[1]== HashedUsername.hexdigest() and row[2]== HashedPassword.hexdigest():#rows in sqlite can be referenced through a list e.g row 0 is first column ,row 1 is second column
                        print("Both Correct")#Username.text and Password.text are text from login input boxes
                        UserType=row[4]
                        #generate cipher for encryption
                        HexedHashedUsername=HashedUsername.hexdigest()
                        cursor.execute("Select Salt from UsersAndPasswords where Username=(?)",(HexedHashedUsername,))
                        Salt=cursor.fetchone()
                        UsernameAndPassword=HashedPassword.hexdigest()+HashedUsername.hexdigest()
                        Key=GenerateKey(UsernameAndPassword,salt=Salt[0])
                        print(Key)
                        cipher=Fernet(Key)
                        KeyStore.append(Key)
                        cursor.execute("Select UserID from UsersAndPasswords Where Username=(?)",(HexedHashedUsername,))
                        UserID=cursor.fetchone()
                        print(UserID)
                        UserIDStore.append(UserID[0])
                        #defines encrypt and decrypt functions
                        def Decrypt(Data,Key):
                            cipher=Fernet(Key)
                            DecryptedData=cipher.decrypt(Data)
                            return DecryptedData
                        
                        def Encrypt(Data,Key):
                            cipher=Fernet(Key)
                            Data=str(Data)
                            DataBytes=bytes(Data, 'utf-8')
                            EncryptedData=cipher.encrypt(DataBytes)
                            return EncryptedData
                        cursor.execute("SELECT * from Products")
                        Table=cursor.fetchall()
                        print(Table)
                        print(Encrypt("Steve",Key=KeyStore[0]))
                        for row in Table:
                            if UserType=="Customer":
                                Screenmanager.current="Shopfront"
                                ShopfrontScreen=Screenmanager.get_screen("Shopfront")#get screen grabs an instance of a screen and is used to place widgets on different screens

                                ProductName=row[0]
                                ProductPrice=row[1]
                        
                        

                                def ProductPress(self):
                                    
                           

                                
                                                                   
                              
                            
                                    def CompareBasketToProductPressed(self):
                                        print("Comparing Basket")
                                        ProductPressed=self.text
                                  
                                    
                                        EncryptedProductPressed=Encrypt(ProductPressed,Key=KeyStore[0])
                                        ProductPressed=ProductPressed.encode()
                                        HashedProductPressed=hashlib.sha3_512(ProductPressed)
                                        cursor.execute("Select Quantity from Basket Where HashedProductName=(?)",(HashedProductPressed.hexdigest(),))
                                        EncryptedBasketQuantity=cursor.fetchone()
                                        print(EncryptedBasketQuantity)
                                        if EncryptedBasketQuantity!=None:
                                                    
                                            DecryptedBasketQuantity=Decrypt(EncryptedBasketQuantity[0],Key=KeyStore[0])
                                            BasketQuantity=DecryptedBasketQuantity.decode()
                                            BasketQuantity=int(BasketQuantity)
                                            print("great Success")
                                            print(BasketQuantity)
                                            BasketQuantity+=1
                                            print(BasketQuantity)
                                            EncryptedQuantity2=Encrypt(BasketQuantity,Key=KeyStore[0])
                                            cursor.execute("Update Basket Set Quantity=? Where HashedProductName=?",(EncryptedQuantity2,HashedProductPressed.hexdigest()))
                                            conn.commit()
                                                 
                                                
                                        if EncryptedBasketQuantity==None:
                                            print("adding to basket new ")
                                            Quantity=1
                                            EncryptedProductPrice=Encrypt(ProductPrice,Key=KeyStore[0])
                                            EncryptedQuantity=Encrypt(Quantity,Key=KeyStore[0])
                                            HashedProductPressed=hashlib.sha3_512(ProductPressed)
                                            cursor.execute("INSERT INTO Basket(ProductName,ProductPrice,Quantity,HashedProductName)VALUES(?,?,?,?)",(EncryptedProductPressed,EncryptedProductPrice,EncryptedQuantity,HashedProductPressed.hexdigest()))
                                            conn.commit()

                        
                                    
                               
                                    CompareBasketToProductPressed(self)
        

                        

                                IndividualProduct=Button(size_hint=(0.2,0.1),pos_hint={'x':ProductPos_hintX,'y':ProductPos_hintY},text=str(ProductName),background_color=green,color=Black)
                                IndividualProduct.bind(on_press=ProductPress)
                                ShopfrontScreen.add_widget(IndividualProduct)
                                ProductPos_hintX+=0.2
                                ProductNumber+=1

                                ProductNumber_DividedBy5=ProductNumber/5
                                if ProductNumber_DividedBy5.is_integer():#is integer checks whether something is integer
                                    ProductPos_hintX=0
                                    ProductPos_hintY+=0.1
                            if UserType=="Staff":
                                Screenmanager.current="Staff"
                            if UserType=="Manager":
                                Screenmanager.current="Manager"
                                


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
                UsernameAlreadyUse=False
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
                    return UsernameAlreadyUse
                        
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


def Decrypt(Data,Key):
    print(Data)
    cipher=Fernet(Key)
    DecryptedData=cipher.decrypt(Data)
    return DecryptedData.decode('utf-8')
                        
def Encrypt(Data,Key):
    print(Data)
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
        
        ExpirationMonth=Spinner(size_hint=(0.1,0.05),pos_hint={'x':0.4,'y':0.7},text="Month",values=("01","02","03","04","05","06","07","08","09","10","11","12"))
        self.add_widget(ExpirationMonth)
        
        ExpirationYear=Spinner(size_hint=(0.1,0.05),pos_hint={'x':0.5,'y':0.7},text="Year",values=("23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40"))
        self.add_widget(ExpirationYear)

        SecurityCode=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.6},text="Security Code")
        self.add_widget(SecurityCode)

        BillingAddress=TextInput(size_hint=(0.2,0.05),pos_hint={'x':0.4,'y':0.5},text="Billing Address")
        self.add_widget(BillingAddress)

      
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
        def RememberClick(self):
            cursor.execute("Select * from PaymentInfo Where UserID = (?)",str(UserIDStore[0]))
            PaymentInfoStored=cursor.fetchall()
            if PaymentInfoStored==[]:
                ExpirationDate=ExpirationMonth.text+"/"+ ExpirationYear.text
                if ExpirationDate=="/":
                        return
                if len(CardNumber.text)!=16:
                    CardNumber.text="Incorrect Length"
                    return
                if len(SecurityCode.text)!=3:
                    SecurityCode.text="Incorrect Length"
                    return
                print("working")
                if NumberChecker(CardNumber.text)==False:
                    CardNumber.text="Number Required"
                    return
                
                if NumberChecker(SecurityCode.text)==False:
                    SecurityCode.text="Number Required"
                    return
                
                if EmailAddressValid(EmailAddress)==False:
                    EmailAddress.text="Invalid Email Address"
                    return
                print("0")
                if len(DeliveryPostcode.text)!=6:
                    DeliveryPostcode.text="Incorrect Length"
                    return
                print("1")
                if CardNumber.text=="":
                    CardNumber.text="Required"
                    return
                print("2")
                if SecurityCode.text=="":
                    SecurityCode.text="Required"
                    return
                print("3")
                if DeliveryPostcode.text=="":
                    DeliveryPostcode.text="Required"
                    return
                print("4")
                if Postcode.text=="":
                    Postcode.text="Required"
                    return
                print("5")
                if BillingAddress.text=="":
                    BillingAddress.text="Required"
                    return
                print("6")
                print("Validation Checks Complete")
                EncryptedCardNumber=Encrypt(CardNumber.text,Key=KeyStore[0])
                EncryptedExpirationDate=Encrypt(ExpirationDate,Key=KeyStore[0])
                EncryptedPostcode=Encrypt(Postcode.text,Key=KeyStore[0])
                EncryptedSecurityCode=Encrypt(SecurityCode.text,Key=KeyStore[0])
                EncryptedEmailAddress=Encrypt(EmailAddress.text,Key=KeyStore[0])
                EncryptedBillingAddress=Encrypt(BillingAddress.text,Key=KeyStore[0])
                print("ITEMS ENCRYPTED")
                cursor.execute("Insert Into PaymentInfo(UserID,CardNumber,SecurityCode,ExpirationDate,BillingAddress,Postcode,EmailAddress) Values(?,?,?,?,?,?,?)",(UserIDStore[0],EncryptedCardNumber,EncryptedSecurityCode,EncryptedExpirationDate,EncryptedPostcode,EncryptedBillingAddress,EncryptedEmailAddress))
                conn.commit()
                print("Payment info added to database")
            else:
               print("Wrong")
        RememberButton.bind(on_press=RememberClick)
        self.add_widget(RememberButton)

        AutofillButton=Button(size_hint=(0.3,0.05),pos_hint={'x':0.7,'y':0.6},text="Autofill",background_color=green,color=Black)
        def AutofillClick(self):

            cursor.execute("Select*from PaymentInfo Where UserID=(?)",str(UserIDStore[0]))
            PaymentInformation=cursor.fetchall()
            for row in PaymentInformation:
                StoredCardNumber=Decrypt(row[0],Key=KeyStore[0])
                StoredSecurityCode=Decrypt(row[1],Key=KeyStore[0])
                StoredExpirationDate=Decrypt(row[2],Key=KeyStore[0])
                StoredBillingAddress=Decrypt(row[3],Key=KeyStore[0])
                StoredPostcode=Decrypt(row[4],Key=KeyStore[0])
                StoredEmailAddress=Decrypt(row[5],Key=KeyStore[0])




            CardNumber.text=StoredCardNumber
            SecurityCode.text=StoredSecurityCode
            SplitStoredExpirationDate=StoredExpirationDate.split("/")
            ExpirationMonth.text=SplitStoredExpirationDate[0]
            ExpirationYear.text=SplitStoredExpirationDate[1]
            BillingAddress.text=StoredBillingAddress
            Postcode.text=StoredPostcode
            EmailAddress.text=StoredEmailAddress

        AutofillButton.bind(on_press=AutofillClick)
        self.add_widget(AutofillButton)


        PayButton=Button(size_hint=(0.3,0.05),pos_hint={'x':0.7,'y':0.8},text="Pay",background_color=green,color=Black)
        def PayButtonClick(self):
            ExpirationDate=ExpirationMonth.text+"/"+ ExpirationYear.text
            print(ExpirationDate)
            if ExpirationDate=="/":
                return
            if len(CardNumber.text)!=16:
                CardNumber.text="Incorrect Length"
                return
            if len(SecurityCode.text)!=3:
                SecurityCode.text="Incorrect Length"
                return
            if NumberChecker(CardNumber.text)==False:
                CardNumber.text="Number Required"
                return
                
            if NumberChecker(SecurityCode.text)==False:
                SecurityCode.text="Number Required"
                return
                
            if EmailAddressValid(EmailAddress)==False:
                return
            print("1")
            if len(DeliveryPostcode.text)!=6:
                DeliveryPostcode.text!="Incorrect Length"
                return
            print("2")
            if CardNumber.text=="":
                CardNumber.text="Required"
                return
            print("3")
            if SecurityCode.text=="":
                SecurityCode.text="Required"
                return
            print("4")
            if DeliveryPostcode.text=="":
                DeliveryPostcode.text="Required"
                return
            print("5")
            if Postcode.text=="":
                Postcode.text="Required"
                return
            print("6")
            if BillingAddress.text=="":
                BillingAddress.text="Required"
                return
            print("7")
             
            DeliveryAddressOrder=DeliveryAddress.text
            EncryptedDeliveryAddress=Encrypt(DeliveryAddressOrder,Key=KeyStore[0])
            PreparedDeliveryPostcode=DeliveryPostcode.text
            EncryptedPostcode=Encrypt(PreparedDeliveryPostcode,Key=KeyStore[0])
            cursor.execute("Select Quantity,ProductName from Basket")
            Basket=cursor.fetchall()
            Products=""
            for row in Basket:
                Quantity=Decrypt(row[0],Key=KeyStore[0])
                Product=Decrypt(row[1],Key=KeyStore[0])
                QuantityAndProduct=Quantity+"x"+Product+","
                Products=Products+QuantityAndProduct
                print(Products)
          



            UserID=UserIDStore[0]
            EncryptedItems=Encrypt(Products,Key=KeyStore[0])
            print(UserID)
            cursor.execute("Insert into Orders (Items,DeliveryAddress,Postcode,UserID) Values(?,?,?,?)",(EncryptedItems,EncryptedDeliveryAddress,EncryptedPostcode,int(UserID)))
            conn.commit()
            CardNumber.text=""
            SecurityCode.text=""
            BillingAddress.text=""
            Country.text=""
            DeliveryPostcode.text=""
            EmailAddress.text=""
            DeliveryAddress.text=""
            DeliveryPostcode.text=""
            
            
        PayButton.bind(on_press=PayButtonClick)   
        self.add_widget(PayButton)
        #help button will be added later

class ViewBasket(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass
class Shopfront(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()
        
        ShopfrontTitle=Label(text="Shopfront",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)
        self.add_widget(ShopfrontTitle)
        ViewBasketScreen=Screenmanager.get_screen("ViewBasket")

        def ViewBasketClick(self):
            Screenmanager.current="ViewBasket"
       
            cursor.execute("Select * From Basket")
            Basket=cursor.fetchall()
            ViewBasketScreen.clear_widgets() 
           

            ViewBasketScreen.layout=FloatLayout()
            ViewBasketTitle=Label(text="Basket View Screen",size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.9},color=Black)
            ViewBasketScreen.add_widget(ViewBasketTitle)

            CheckoutAndPay=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text=str("Checkout and Pay"),background_color=green,color=Black)
            def CheckoutAndPayClick(self):
                Screenmanager.current="PaymentScreen"
            
            CheckoutAndPay.bind(on_press=CheckoutAndPayClick)        
            ViewBasketScreen.add_widget(CheckoutAndPay)
        
            Back=Button(size_hint=(0.2,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)
            def BackClick(self):
                Screenmanager.current="Shopfront"
            Back.bind(on_press=BackClick)
            ViewBasketScreen.add_widget(Back)

            Ypos=0.8

            for row in Basket:
                DecryptedProduct=Decrypt(row[0],Key=KeyStore[0])
                DecryptedProductPrice=Decrypt(row[1],Key=KeyStore[0])
                DecryptedQuantity=Decrypt(row[2],Key=KeyStore[0])
           
                Product=Label(text=DecryptedProduct+"X"+DecryptedQuantity+" Price=£"+DecryptedProductPrice,size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':Ypos},color=Black)
                ViewBasketScreen.add_widget(Product)
                Ypos-=0.1

        Viewbasket=Button(size_hint=(0.2,0.1),pos_hint={'x':0.8,'y':0.9},text="ViewBasket",background_color=green,color=Black)
        Viewbasket.bind(on_press=ViewBasketClick)
        self.add_widget(Viewbasket)

            #help button will be added later

class Manager(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()
                                
        AccessLevel.append("1")
        AddAndRemoveUsers=Button(size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.7},text="AddAndRemoveUsers",background_color=green,color=Black)
        def UserScreen(self):
            Screenmanager.current="AddOrRemoveUsers"
        AddAndRemoveUsers.bind(on_press=UserScreen)
        self.add_widget(AddAndRemoveUsers)

        ViewOrders=Button(size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.5},text="ViewOrders",background_color=green,color=Black)
        def OrderViewScreen(self):
            Screenmanager.current="OrderView"
            RefreshOrderView()
        ViewOrders.bind(on_press=OrderViewScreen)
        self.add_widget(ViewOrders)

        AddAndRemoveProducts=Button(size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.3},text="AddOrRemoveProducts",background_color=green,color=Black)
        def AddAndRemoveProductsClick(self):
            Screenmanager.current="AddOrRemoveProduct"
        AddAndRemoveProducts.bind(on_press=AddAndRemoveProductsClick)
        self.add_widget(AddAndRemoveProducts)

class AddOrRemoveUsers(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)     
        self.layout=FloatLayout()
       
        RemoveUserTitle=Label(text="Remove User",size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.7},color=Black)
        self.add_widget(RemoveUserTitle)

        UserIDInput=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.5})
        self.add_widget(UserIDInput)
        RemoveUser=Button(size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.3},text="Remove User",background_color=green,color=Black)
        def RemoveUserClick(self):
            UserID=UserIDInput.text
            UserIDSearch=cursor.execute("Select*from UsersAndPasswords Where UserID=(?)",UserID)
            #checks to see if id user has entered exists and if it does deletes that row of table
            if UserIDSearch==[]:
                UserIDInput.text="Invalid UserID"
            else:
                cursor.execute("Delete from UsersAndPasswords Where UserID=(?)",UserID)
                conn.commit()
                UserIDInput.text="User Deleted"




        RemoveUser.bind(on_press=RemoveUserClick)
        self.add_widget(RemoveUser)

        AddUserTitle=Label(text="Add User",size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.9},color=Black)
        self.add_widget(AddUserTitle)

        UsernameInput=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.7})
        self.add_widget(UsernameInput)

        PasswordInput=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.5})
        self.add_widget(PasswordInput)
        
        UserTypeInput=Spinner(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.3},values=('Manager','Staff'))
        self.add_widget(UserTypeInput)

        AddUser=Button(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.1},text="Add User",background_color=green,color=Black)
        def AddUserClick(self):
            Username=UsernameInput.text
            Password=PasswordInput.text
            UserType=UserTypeInput.text
            EncodedUsername=Username.encode()#To hash first encode then hash
            HashedUsername=hashlib.sha3_512(EncodedUsername)
            EncodedPassword=Password.encode()
            HashedPassword=hashlib.sha3_512(EncodedPassword)
            cursor.execute("Select Username from UsersAndPasswords")
            Usernames=cursor.fetchall()
            print(Usernames)
            def check():
                UsernameAlreadyUse=False
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
                    return UsernameAlreadyUse
                        
            UsernameAlreadyUse=check()#function so commands below arent executed in a loop
            print(UsernameAlreadyUse)
            #Insert hashes into database as hex digest as by defualt their datatype is not supported
            if UsernameAlreadyUse==False:
                salt=os.urandom(32)
                cursor.execute("Insert into UsersAndPasswords (Username,Password,UserType,Salt)VALUES(?,?,?,?)",(HashedUsername.hexdigest(),HashedPassword.hexdigest(),UserType,salt))
                conn.commit()
                print("Adding")
            if UsernameAlreadyUse==True:
                UsernameInput.text="Username Already Used"
                print("Not Adding")
            
            UsernameInput.text=""
            PasswordInput.text=""
            UserTypeInput.text=""
        AddUser.bind(on_press=AddUserClick)
        self.add_widget(AddUser)
   

 





        Back=Button(size_hint=(0.2,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)#color is writing color background color is background
        def BackClick(self):
            Screenmanager.current="Manager"
        Back.bind(on_press=BackClick)#binds a function to happen when a button is pressed
        self.add_widget(Back)

class AddOrRemoveProduct(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)     
        self.layout=FloatLayout()
       
        AddProductTitle=Label(text="Add Product",size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.9},color=Black)
        self.add_widget(AddProductTitle)

        ProductNameInputRemoveProduct=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.5},text="ProductName")
        self.add_widget(ProductNameInputRemoveProduct)
        
        RemoveProduct=Button(size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.3},text="Remove Product",background_color=green,color=Black)
        def RemoveProductClick(self):
            ProductName=ProductNameInputRemoveProduct.text
            cursor.execute("Delete from Products Where Productname=(?)",(ProductName,))
            conn.commit()
            ProductNameInputRemoveProduct.text="Product Removed"
        RemoveProduct.bind(on_press=RemoveProductClick)
        self.add_widget(RemoveProduct)

        RemoveProductTitle=Label(text="Remove Product",size_hint=(0.2,0.1),pos_hint={'x':0.2,'y':0.9},color=Black)
        self.add_widget(RemoveProductTitle)

        
        ProductNameInputAddProduct=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.6},text="ProductName")
        self.add_widget(ProductNameInputAddProduct)

        ProductPriceInputAddProduct=TextInput(size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.4},text="Price")
        self.add_widget(ProductPriceInputAddProduct)
        
        AddProduct=Button(size_hint=(0.2,0.1),pos_hint={'x':0.6,'y':0.2},text="Add Product",background_color=green,color=Black)
        def AddProductClick(self):
            ProductName=ProductNameInputAddProduct.text
            ProductPrice=ProductPriceInputAddProduct.text
            cursor.execute("Select* from Products Where Productname=(?)",(ProductName,))
            ProductAlreadyExistsCheck=cursor.fetchall()
            if ProductAlreadyExistsCheck!=[]:
                ProductNameInputAddProduct.text="Product Already Exists"
            else:
                cursor.execute("Insert Into Products(Productname,ProductPrice)Values(?,?)",(ProductName,ProductPrice))
                conn.commit()
                ProductNameInputAddProduct.text="Product Added"
        AddProduct.bind(on_press=AddProductClick)
        self.add_widget(AddProduct)
        
        Back=Button(size_hint=(0.2,0.1),pos_hint={'x':0.0,'y':0.9},text="Back",background_color=green,color=Black)
        def BackClick(self):
            if len(AccessLevel)==1:
                Screenmanager.current="Manager"
            else:
                Screenmanager.current="Staff"
        Back.bind(on_press=BackClick)
        self.add_widget(Back)
      
      

        


class OrderView(Screen):
    pass
class Staff(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout=FloatLayout()

        ViewOrders=Button(size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.5},text="ViewOrders",background_color=green,color=Black)
        def OrderViewScreen(self):
            Screenmanager.current="OrderView"
            RefreshOrderView()

        ViewOrders.bind(on_press=OrderViewScreen)
        self.add_widget(ViewOrders)

        AddRemoveProducts=Button(size_hint=(0.2,0.1),pos_hint={'x':0.4,'y':0.3},text="AddOrRemoveProducts",background_color=green,color=Black)
        def AddRemoveProductsClick(self):
            Screenmanager.current="AddOrRemoveProduct"
        AddRemoveProducts.bind(on_press=AddRemoveProductsClick)
        self.add_widget(AddRemoveProducts)

     
    

def main():
  
    #payment information table will be added in future
    cursor.execute("""create table IF NOT EXISTS Products(
    Productname text Primary Key
    ,ProductPrice text(6)
    )""")

    cursor.execute("""create table IF NOT EXISTS Orders
    (OrderID integer Primary Key Autoincrement
    ,Items blob(128)
    ,DeliveryAddress blob(128)
    ,Postcode blob(128)
    ,UserID integer
    ,FOREIGN KEY(UserID) REFERENCES UsersAndPasswords(UserID)
    )""")


    cursor.execute("""create table IF NOT EXISTS Basket(
    ProductName blob(128)
    ,ProductPrice blob(128)
    ,Quantity blob (128)
    ,HashedProductName blob(512)
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
    ,EmailAddress blob(128)
    ,UserID integer
    ,FOREIGN KEY(UserID) REFERENCES UsersAndPasswords(UserID))""")#() next to text is length of the inputs in bytes and for text data type it is number of characters

    Screenmanager.add_widget(PaymentScreen(name="PaymentScreen"))#adds each screen to screenmanager to so they can be controlled
    Screenmanager.add_widget(ViewBasket(name="ViewBasket"))
    Screenmanager.add_widget(Shopfront(name="Shopfront"))
    Screenmanager.add_widget(Login(name="Login"))
    Screenmanager.add_widget(Manager(name="Manager"))
    Screenmanager.add_widget(AddOrRemoveUsers(name="AddOrRemoveUsers"))
    Screenmanager.add_widget(AddOrRemoveProduct(name="AddOrRemoveProduct"))
    Screenmanager.add_widget(OrderView(name="OrderView"))
    Screenmanager.add_widget(Staff(name="Staff"))
    Screenmanager.current="Login"


    class PaperApp(App):#app class contains screenmanager  
        def build(self):
            return Screenmanager 
    PaperApp().run()
  
    cursor.execute("Drop Table Basket")

    cursor.close()
main()