# FakeAPI

**FakeAPI** is a lightweight REST API built with FastAPI for testing, prototyping, and learning purposes. It offers basic CRUD functionality for tasks and supports filtering, sorting, and pagination.

## 🚀 Features
- Prebuilt dataset with fake tasks
- Full CRUD operations
- Query support:
  - Pagination (`?page=1&page_size=5`)
  - Sorting (`?sort_by=-created_at`)
  - Filtering (`?status=pending`)
- Clean and modular codebase
- No database, no persistence — great for quick testing

## 🧪 Live Demo
**🌐 Demo URL:** [https://fakeapi-kynw.onrender.com](https://fakeapi-kynw.onrender.com)  
_This is a free Render deployment. If inactive, it may sleep and take up to **1 minute** to wake up._

## 📦 Tech Stack
- Python 3.12
- FastAPI
- Faker (static dataset with project-themed examples)
- Pydantic v2
- Poetry for dependency management
