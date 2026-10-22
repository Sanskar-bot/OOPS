class BankAccount:                                  
    def __init__(self,account_num, owner, balance=0, pin=-1-1-1-1):
        self.__account_num=account_num
        self.owner = owner
        self.__balance = balance
        self.__history=[]
        self.__pin=pin
        self.__pincounter=0
        self.dailylimit=float('inf')

    @property
    def dailylimit(self):
        return self.__dailylimit
    
    @dailylimit.setter
    def dailylimit(self,value):
        if value<0:
            raise Exception ( " Limit cant be negative")
        self.__dailylimit=value
    


    @property
    def account_no(self):
        return self.__account_num

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self , value):
        if not value or not value.strip():
            raise ValueError("Owner name cannot be empty")
        self.__owner=value

    def show(self):
        print(self.owner, "has", self.__balance)

    def deposit(self, amount):                       # was "deposite", must match transfer's call
        if amount > 0:                               # was >=, zero is not a valid deposit
            self.__balance += amount
            self.__history.append(f"deposit {amount}")
        else:
            raise Exception("Incorrect amount")      # capital E in Exception

    def withdraw(self, amount , pin):
        if self.__pincounter>3:
            raise Exception("too many attempts")
        elif pin!=self.__pin:
            self.__pincounter+=1
            raise Exception("incorrect pin")
        
        if pin == self.__pin:
            if amount<=self.dailylimit:
                self.__pincounter=0
                if amount <= self.__balance and amount > 0:    # self.balance, not just balance
                    self.__balance -= amount
                    self.__history.append(f"withdraw {amount}")
                else:
                    raise Exception("Can't withdraw")
            else:
                raise Exception ("Crossed your daily Limit")
          

    def transfer(self, other, amount , pin):
        if self.__pincounter>3:
            raise Exception("too many attempts")
        elif pin!=self.__pin:
            self.__pincounter+=1
            raise Exception("incorrect pin")
        
        if pin == self.__pin:
            self.withdraw(amount,pin)                        # raises an error if it fails, so the next line is skipped
            other.deposit(amount)
            self.__history.append(f"Transfered {amount} to {other.owner}")
      

    @property
    def balance(self):
        return self.__balance

   
    def statement(self):
        print("Statement for", self.owner)
        for entry in self.__history:
            print(" ", entry)
          
    @property
    def history(self):
        return list(self.__history)       # a copy, so the real list stays safe


a = BankAccount(101 , "ali", 500 , 7000)
print(a.balance)               # 500
a.owner = "ali khan"           # accepted
print(a.owner)                 # ali khan

try:
    a.owner = "   "
except ValueError as e:
    print(e)                   # Owner name cannot be empty

try:
    a.balance = 1
except AttributeError as e:
    print(e)                   # property 'balance' of 'BankAccount' object has no setter

try:
    BankAccount(102 , "", 100 , 8000)
except ValueError as e:
    print(e)                   # Owner name cannot be empty

a.deposit(100)
h = a.history
h.append("fake")
print(a.history)               # ['deposit 100'], the fake line is not there
print(a.balance + 10)          # 610, works because balance is a number    # error, the setter works at creation
print(a.account_no)    

try:       # 101, the account number
    a.withdraw(50, 7000)       # works
except Exception as e:
    print(e)    


try:       # 101, the account number
    a.withdraw(50, 9999)       # works
except Exception as e:
    print(e)    
    
try:
    print(a.pin)  
except AttributeError as e:
    print(e)   

a.dailylimit = 200
try:
    a.withdraw(500, 1234)  
except Exception as e:
    print(e)

    # error: Over daily limit
try:
    a.dailylimit = -5   
except Exception as e:
    print(e)