# Python Backend System with Database Integration and REST APIs

A comprehensive full-stack Python application demonstrating backend development with multiple frameworks, databases, and complete REST API implementations.

## Project Overview

This project implements four different backend applications using multiple Python frameworks (Flask, FastAPI, Django) and database systems (SQLite, MySQL, PostgreSQL).

### Applications Included

1. **Task Management System** - CRUD operations for task tracking
2. **Blog API** - Article management and publishing platform
3. **User Authentication System** - Secure user management and auth
4. **Inventory Manager** - Stock and inventory tracking

### Frameworks

- **Flask** - Lightweight and flexible
- **FastAPI** - Modern, fast, with automatic documentation
- **Django** - Full-featured with ORM and admin panel

### Databases

- **SQLite** - Lightweight, file-based
- **MySQL** - Relational, scalable
- **PostgreSQL** - Robust, advanced features

## Project Structure

```
python-backend-system/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   ├── SETUP_GUIDE.md
│   └── screenshots/
│
├── flask-apps/
│   ├── task-management/
│   ├── blog-api/
│   ├── user-auth/
│   └── inventory-manager/
│
├── fastapi-apps/
│   ├── task-management/
│   ├── blog-api/
│   ├── user-auth/
│   └── inventory-manager/
│
├── django-apps/
│   ├── task-management/
│   ├── blog-api/
│   ├── user-auth/
│   └── inventory-manager/
│
└── shared/
    ├── database_configs/
    ├── models/
    └── utilities/
```

## Features

### Core Features
- ✅ CRUD Operations (Create, Read, Update, Delete)
- ✅ Input Validation
- ✅ Error Handling
- ✅ Structured Project Architecture
- ✅ Database Schema Design
- ✅ Secure Database Queries
- ✅ REST API Endpoints
- ✅ Proper HTTP Status Codes
- ✅ API Documentation
- ✅ Testing with Postman

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Darknite175/python-backend-system.git
cd python-backend-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running Applications

### Flask Applications
```bash
cd flask-apps/task-management
python app.py
```

### FastAPI Applications
```bash
cd fastapi-apps/blog-api
uvicorn main:app --reload
```

### Django Applications
```bash
cd django-apps/user-auth
python manage.py runserver
```

## API Testing

All APIs are documented and can be tested using:
- **Postman** - Import provided collection
- **curl** - Command line testing
- **Browser** - For GET requests
- **FastAPI Docs** - Automatic interactive documentation at `/docs`

## Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Setup Guide](docs/SETUP_GUIDE.md)

## Technologies Used

### Backend Frameworks
- Flask
- FastAPI
- Django

### Databases
- SQLite
- MySQL
- PostgreSQL

### Tools & Libraries
- SQLAlchemy (ORM)
- Pydantic (Validation)
- pytest (Testing)
- Postman (API Testing)

## Skills Demonstrated

✅ Python & OOP
✅ REST API Development
✅ Database Design
✅ Error Handling & Debugging
✅ Input Validation
✅ Security Best Practices
✅ Project Architecture
✅ Documentation
✅ Testing

## License

MIT License - feel free to use this project for learning purposes.

## Author

Darknite175

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
