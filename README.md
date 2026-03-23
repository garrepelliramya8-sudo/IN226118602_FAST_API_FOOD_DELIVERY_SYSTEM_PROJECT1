# 🍕 FastAPI Food Delivery Backend

## 📌 Project Overview

This project is a **Food Delivery Backend System** built using **FastAPI**.
It allows users to browse menu items, place orders, manage cart, and perform search, sorting, and pagination operations.

This project was developed as part of the **FastAPI Internship Final Project**, covering all core backend concepts from Day 1 to Day 6.

---

## 🚀 Features

* ✅ GET APIs (Menu, Orders, Summary)
* ✅ POST APIs with Pydantic Validation
* ✅ Helper Functions for reusable logic
* ✅ Full CRUD Operations (Create, Update, Delete)
* ✅ Cart System (Add, Remove, Checkout)
* ✅ Multi-step Workflow Implementation
* ✅ Search Functionality
* ✅ Sorting (Ascending/Descending)
* ✅ Pagination Support

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## 📂 Project Structure

```
FOOD_DELIVERY_FASTAPI
│
├── main.py
├── screenshots/
│   ├── Q1.png
│   ├── Q2.png
│   ├── ...
│   ├── Q20.png
```

---

## ⚙️ Setup & Installation

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository

```
git clone <your-repo-link>
cd FOOD_DELIVERY_FASTAPI
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

---

### 3️⃣ Activate Virtual Environment

#### ▶️ Windows

```
venv\Scripts\activate
```

#### ▶️ PowerShell (if error)

```
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\Activate.ps1
```

---

### 4️⃣ Install Dependencies

```
pip install fastapi uvicorn
```

---

### 5️⃣ Run the Server

```
uvicorn main:app --reload
```

---

### 6️⃣ Open Swagger UI

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

Here you can test all APIs.

---

## 📸 API Testing

All endpoints were tested using Swagger UI.
Screenshots for each question (Q1–Q20) are included in the `screenshots` folder.

---

## 📊 Concepts Covered

* Day 1: GET APIs & JSON responses
* Day 2: POST APIs & Pydantic validation
* Day 3: Helper functions & filtering
* Day 4: CRUD operations
* Day 5: Multi-step workflows (Cart & Checkout)
* Day 6: Search, Sort & Pagination

---

## 🎯 Key Endpoints

* `/menu` → Get all menu items
* `/orders` → View orders
* `/cart` → View cart
* `/cart/checkout` → Place order
* `/menu/search` → Search items
* `/menu/sort` → Sort items
* `/menu/page` → Pagination

---

## 🧠 Learning Outcome

Through this project, I gained hands-on experience in:

* Designing REST APIs
* Backend architecture using FastAPI
* Data validation with Pydantic
* Implementing real-world workflows
* Writing clean and modular code

---

## 🔗 GitHub Repository
https://github.com/garrepelliramya8-sudo/IN226118602_FAST_API_FOOD_DELIVERY_SYSTEM_PROJECT1


---

## 📢 Acknowledgement

This project was developed as part of the Generative AI Internship Program.

---
