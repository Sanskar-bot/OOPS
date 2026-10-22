class BankAccount:                                  
    def __init__(self, account_num, owner, balance=0, pin=None):
        if pin is None:
            raise ValueError("PIN is required")
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
    def is_locked(self):
        return self.__pincounter >= 3

    def __check_pin(self, pin):              # private helper — DRY pin logic
        if self.is_locked:
            raise Exception("Account locked")
        if pin != self.__pin:
            self.__pincounter += 1
            raise Exception("Wrong PIN")
        self.__pincounter = 0               # reset immediately on correct PIN

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

    def withdraw(self, amount, pin):
        self.__check_pin(pin)
        if amount > self.dailylimit:
            raise Exception("Crossed your daily limit")
        if amount <= 0 or amount > self.__balance:
            raise Exception("Can't withdraw")
        self.__balance -= amount
        self.__history.append(f"withdraw {amount}")


    def transfer(self, other, amount, pin):
        self.withdraw(amount, pin)           # withdraw already checks everything
        other.deposit(amount)
        self.__history.append(f"Transferred {amount} to {other.owner}")

      

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