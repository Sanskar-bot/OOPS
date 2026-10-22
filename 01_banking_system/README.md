# 01 — Banking System

A simple **Banking System** built from scratch using Python OOP to practice core concepts.

---

## 🧠 OOP Concepts Covered

| Concept | Where It Appears |
|---|---|
| **Encapsulation** | `__balance` and `__history` are private; exposed only via properties |
| **Properties (`@property`)** | `balance`, `owner`, `history` — controlled read access |
| **Setters (`@setter`)** | `owner` setter validates the name before allowing assignment |
| **Data validation** | Empty owner → `ValueError`; bad amounts → `Exception` |
| **Immutable-style access** | `history` returns a copy so callers can't mutate the internal list |

---

## 📦 Class: `BankAccount`

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner          # goes through the setter (validates!)
        self.__balance = balance    # private
        self.__history = []         # private transaction log
```

### Key Methods

| Method | Description |
|---|---|
| `deposit(amount)` | Adds money; logs to history; raises if `amount <= 0` |
| `withdraw(amount)` | Deducts money if sufficient balance; raises otherwise |
| `transfer(other, amount)` | Withdraws from self, deposits into `other`; atomic-style |
| `statement()` | Prints all history entries |

### Key Properties

| Property | Setter? | Notes |
|---|---|---|
| `balance` | ❌ Read-only | Protects against direct mutation |
| `owner` | ✅ Validated | Rejects empty / whitespace-only strings |
| `history` | ❌ Read-only | Returns a **copy** — mutations on the copy don't affect the real log |

---

## 💡 Key Learning Moments

### 1. Private attributes with name mangling
```python
self.__balance = balance   # stored as _BankAccount__balance
```
Accessing `a.__balance` from outside raises `AttributeError`.

### 2. Read-only property (no setter)
```python
@property
def balance(self):
    return self.__balance

# This will raise AttributeError:
a.balance = 1000
```

### 3. Validated setter
```python
@owner.setter
def owner(self, value):
    if not value or not value.strip():
        raise ValueError("Owner name cannot be empty")
    self.__owner = value
```

### 4. Safe history copy
```python
@property
def history(self):
    return list(self.__history)  # caller gets a copy, not a reference
```

---

## ▶️ Run

```bash
python banking_system.py
```

Expected output:
```
500
ali khan
Owner name cannot be empty
property 'balance' of 'BankAccount' object has no setter
Owner name cannot be empty
['deposit 100']
610
```
