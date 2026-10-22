# 01 — Banking System

A simple **Banking System** built from scratch using Python OOP to practice core concepts.

---

## 🧠 OOP Concepts Covered

| Concept | Where It Appears |
|---|---|
| **Encapsulation** | `__balance`, `__history`, `__account_num` are private; exposed only via properties |
| **Properties (`@property`)** | `balance`, `owner`, `history`, `account_no` — controlled read access |
| **Setters (`@setter`)** | `owner` setter validates the name before allowing assignment |
| **Data validation** | Empty owner → `ValueError`; bad amounts → `Exception` |
| **Immutable-style access** | `history` returns a copy so callers can't mutate the internal list |
| **Private ID field** | `__account_num` stored privately; `account_no` property exposes it read-only |

---

## 📦 Class: `BankAccount`

```python
class BankAccount:
    def __init__(self, account_num, owner, balance=0):
        self.__account_num = account_num  # private — must use __ or property breaks
        self.owner = owner                # goes through the setter (validates!)
        self.__balance = balance          # private
        self.__history = []               # private transaction log
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
| `account_no` | ❌ Read-only | Exposes the private `__account_num`; account number never changes |

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

### 5. Private ID with read-only property — and the name-mangling gotcha ✅

When you expose an ID via a `@property`, the backing store **must be private** (`__account_num`), not public (`account_num`). If they don't match, the property silently reads a non-existent mangled name and raises `AttributeError` at runtime.

```python
# ❌ WRONG — property returns self.__account_num but __init__ stores self.account_num
def __init__(self, account_num, ...):
    self.account_num = account_num   # stored as .account_num (public)

@property
def account_no(self):
    return self.__account_num        # looks for ._BankAccount__account_num → AttributeError!

# ✅ CORRECT — both sides use the private name
def __init__(self, account_num, ...):
    self.__account_num = account_num  # stored as ._BankAccount__account_num

@property
def account_no(self):
    return self.__account_num         # finds it correctly → returns the value
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
101
```
