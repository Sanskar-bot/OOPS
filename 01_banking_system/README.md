# 01 — Banking System

A simple **Banking System** built from scratch using Python OOP to practice core concepts.

---

## 🧠 OOP Concepts Covered

| Concept | Where It Appears |
|---|---|
| **Encapsulation** | `__balance`, `__history`, `__account_num`, `__pin` are private; exposed only via properties |
| **Properties (`@property`)** | `balance`, `owner`, `history`, `account_no`, `dailylimit` — controlled read access |
| **Setters (`@setter`)** | `owner` setter validates name; `dailylimit` setter rejects negatives |
| **Data validation** | Empty owner → `ValueError`; bad amounts / negative limit → `Exception` |
| **Immutable-style access** | `history` returns a copy so callers can't mutate the internal list |
| **Private ID field** | `__account_num` stored privately; `account_no` property exposes it read-only |
| **PIN protection** | `__pin` and `__pincounter` are private; wrong PIN increments counter; locks after 3 fails |
| **Daily spending limit** | `__dailylimit` defaults to `float('inf')`; `withdraw` checks amount before proceeding |

---

## 📦 Class: `BankAccount`

```python
class BankAccount:
    def __init__(self, account_num, owner, balance=0, pin=-4):
        self.__account_num = account_num  # private — must use __ or property breaks
        self.owner = owner                # goes through the setter (validates!)
        self.__balance = balance          # private
        self.__history = []               # private transaction log
        self.__pin = pin                  # private — never accessible from outside
        self.__pincounter = 0             # tracks wrong attempts
        self.dailylimit = float('inf')    # goes through setter (validates!)
```

### Key Methods

| Method | Description |
|---|---|
| `deposit(amount)` | Adds money; logs to history; raises if `amount <= 0` |
| `withdraw(amount, pin)` | Validates PIN + daily limit + balance before deducting |
| `transfer(other, amount, pin)` | Validates PIN, then withdraws from self and deposits into `other` |
| `statement()` | Prints all history entries |

### Key Properties

| Property | Setter? | Notes |
|---|---|---|
| `balance` | ❌ Read-only | Protects against direct mutation |
| `owner` | ✅ Validated | Rejects empty / whitespace-only strings |
| `history` | ❌ Read-only | Returns a **copy** — mutations on the copy don't affect the real log |
| `account_no` | ❌ Read-only | Exposes the private `__account_num`; account number never changes |
| `dailylimit` | ✅ Validated | Rejects negative values; defaults to `float('inf')` (no limit) |

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

### 6. PIN protection with lockout ✅

Sensitive operations (`withdraw`, `transfer`) require a PIN. Wrong attempts are tracked privately. After 3 failures the account locks.

```python
def __check_pin(self, pin):              # private helper
    if self.is_locked:
        raise Exception("Account locked")
    if pin != self.__pin:
        self.__pincounter += 1
        raise Exception("Wrong PIN")
    self.__pincounter = 0               # reset immediately on correct PIN
```

> `__pin` is fully private — `a.pin` raises `AttributeError`. That's intentional: the PIN should never be readable from outside.

### 7. Daily spending limit with validated setter ✅

A `dailylimit` property with a setter enforces that the limit can't be negative. It defaults to `float('inf')` (no limit). The `withdraw` method checks the limit before touching the balance.

```python
@dailylimit.setter
def dailylimit(self, value):
    if value < 0:
        raise Exception("Limit can't be negative")
    self.__dailylimit = value

# Inside withdraw — checked AFTER pin validation:
if amount > self.dailylimit:
    raise Exception("Crossed your daily limit")
```

### 8. `pin=None` default closes a security hole ✅

With `pin=-4` as the default, `BankAccount(101, "ali", 500)` silently created an account where `withdraw(50, -4)` would succeed. Changing the default to `None` and rejecting it at construction forces every account to have an explicit PIN.

```python
def __init__(self, account_num, owner, balance=0, pin=None):
    if pin is None:
        raise ValueError("PIN is required")   # can't forget the PIN
```

### 9. DRY — extract duplicate logic into a private helper ✅

`withdraw` and `transfer` both had identical lock-check + wrong-PIN + counter logic. That's a violation of DRY (Don't Repeat Yourself). Moving it into `__check_pin` means fixing a PIN bug in one place fixes it everywhere.

```python
# Before: ~10 lines duplicated in both methods
# After: each method calls one line
def withdraw(self, amount, pin):
    self.__check_pin(pin)      # all PIN logic lives here
    ...

def transfer(self, other, amount, pin):
    self.withdraw(amount, pin) # withdraw already checks everything
    ...
```

### 10. Counter reset was happening too late ✅

In the old code, `self.__pincounter = 0` was nested inside the daily-limit check. A correct PIN + over-limit amount never cleared the counter, meaning repeated over-limit attempts would eventually lock the account even though the PIN was always right. Moving the reset into `__check_pin` (right after PIN verification) fixes this.

```python
# ❌ OLD — reset inside nested if, never reached on limit error
if pin == self.__pin:
    if amount <= self.dailylimit:
        self.__pincounter = 0     # skipped if amount > limit!
        ...

# ✅ NEW — reset happens immediately after the PIN is verified
def __check_pin(self, pin):
    ...
    self.__pincounter = 0         # always cleared on correct PIN
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
Wrong PIN
'BankAccount' object has no attribute 'pin'
Wrong PIN
 Limit cant be negative
```
