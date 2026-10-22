# 🐍 OOPS — Object-Oriented Programming in Python

A structured, hands-on learning repository where I build real mini-systems using Python OOP — one concept at a time.

Each folder is a self-contained **system** that demonstrates specific OOP concepts with working, runnable code and detailed notes.

---

## 📁 Repository Structure

```
OOPS/
├── 01_banking_system/
│   ├── banking_system.py    # Main implementation
│   └── README.md            # Concepts, API, and key learnings
└── README.md                # This file
```

> More systems will be added as I progress through OOP concepts.

---

## 🗺️ Learning Roadmap

| # | System | Key Concepts | Status |
|---|---|---|---|
| 01 | [Banking System](./01_banking_system/) | Encapsulation, Properties, Setters, Validation | ✅ Done |
| 02 | Library System | Inheritance, `super()` | 🔜 Next |
| 03 | School System | Multiple Inheritance, MRO | 🔜 Planned |
| 04 | E-Commerce Cart | Operator Overloading (`__add__`, `__str__`) | 🔜 Planned |
| 05 | Animal Kingdom | Polymorphism, Abstract Classes | 🔜 Planned |
| 06 | Task Manager | Dunder methods, `__repr__`, `__eq__` | 🔜 Planned |

---

## 01 — Banking System

> **Concepts**: Encapsulation · Properties · Setters · Data Validation

A `BankAccount` class that manages balances, validates inputs, and keeps a tamper-proof transaction history.

### Key snippets

**Private attributes + read-only property:**
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.__balance = balance   # private, name-mangled

    @property
    def balance(self):
        return self.__balance      # read-only: no setter defined
```

**Validated setter:**
```python
@owner.setter
def owner(self, value):
    if not value or not value.strip():
        raise ValueError("Owner name cannot be empty")
    self.__owner = value
```

**Safe history (returns a copy):**
```python
@property
def history(self):
    return list(self.__history)   # mutation-safe copy
```

📂 [See full code & notes →](./01_banking_system/)

---

## 🛠️ How to Run Any System

```bash
# Clone the repo
git clone https://github.com/Sanskar-bot/OOPS.git
cd OOPS

# Run a specific system
python 01_banking_system/banking_system.py
```

**Requirements**: Python 3.x — no external dependencies.

---

## 📖 About

This repo is my personal OOP learning journal. Every system I build here is:
- Written from scratch (no frameworks)
- Documented with concept explanations and code snippets
- Updated progressively as I learn new concepts

Feel free to follow along or use it as a reference!

---

*Made with 🧠 and ☕ by [Sanskar Phougat](https://github.com/Sanskar-bot)*
