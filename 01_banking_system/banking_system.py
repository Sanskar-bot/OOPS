class BankAccount:                                  
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        self.__history=[]

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

    def withdraw(self, amount):
        if amount <= self.__balance and amount > 0:    # self.balance, not just balance
            self.__balance -= amount
            self.__history.append(f"withdraw {amount}")
        else:
            raise Exception("Can't withdraw")
          

    def transfer(self, other, amount):
        self.withdraw(amount)                        # raises an error if it fails, so the next line is skipped
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


a = BankAccount("ali", 500)
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
    BankAccount("", 100)
except ValueError as e:
    print(e)                   # Owner name cannot be empty

a.deposit(100)
h = a.history
h.append("fake")
print(a.history)               # ['deposit 100'], the fake line is not there
print(a.balance + 10)          # 610, works because balance is a number    # error, the setter works at creation