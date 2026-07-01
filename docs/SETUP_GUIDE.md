# Complete Setup Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- virtualenv or venv
- Git
- PostgreSQL (optional, for production)
- MySQL (optional, for production)

## Step 1: Clone Repository

```bash
git clone https://github.com/Darknite175/python-backend-system.git
cd python-backend-system
```

## Step 2: Create Virtual Environment

### On Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DB_TYPE=sqlite
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password
DB_NAME=python_backend_system
```

## Step 5: Database Setup

### Using SQLite (Recommended for Development)

No additional setup required. The database file will be created automatically.

### Using MySQL

1. Install MySQL Server
2. Create database:
```sql
CREATE DATABASE python_backend_system;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON python_backend_system.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

3. Update `.env`:
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=password
DB_NAME=python_backend_system
```

### Using PostgreSQL

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE python_backend_system;
CREATE USER admin WITH PASSWORD 'password';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE python_backend_system TO admin;
```

3. Update `.env`:
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password
DB_NAME=python_backend_system
```

## Step 6: Running Applications

### Flask Applications

#### Task Management
```bash
cd flask-apps/task-management
python app.py
# Access at http://localhost:5000
```

#### Blog API
```bash
cd flask-apps/blog-api
python app.py
# Access at http://localhost:5001
```

#### User Auth
```bash
cd flask-apps/user-auth
python app.py
# Access at http://localhost:5002
```

#### Inventory Manager
```bash
cd flask-apps/inventory-manager
python app.py
# Access at http://localhost:5003
```

### FastAPI Applications

#### Task Management
```bash
cd fastapi-apps/task-management
uvicorn main:app --reload --port 8000
# Access at http://localhost:8000
# Docs at http://localhost:8000/docs
```

#### Blog API
```bash
cd fastapi-apps/blog-api
uvicorn main:app --reload --port 8001
# Access at http://localhost:8001/docs
```

#### User Auth
```bash
cd fastapi-apps/user-auth
uvicorn main:app --reload --port 8002
# Access at http://localhost:8002/docs
```

#### Inventory Manager
```bash
cd fastapi-apps/inventory-manager
uvicorn main:app --reload --port 8003
# Access at http://localhost:8003/docs
```

### Django Applications

Django uses a unified approach with multiple apps:

```bash
cd django-apps/project-root

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
# Access at http://localhost:8000
```

## Step 7: Testing with Postman

### Import Collection
1. Open Postman
2. Click "Import"
3. Select collection from `/postman-collections/`
4. Import environment variables

### Testing Workflow
1. Start your chosen application
2. Open Postman collection
3. Run requests from the collection
4. Verify responses and status codes

## Step 8: Database Initialization

### Flask/FastAPI
Databases are created automatically when models are defined.

### Django
```bash
cd django-apps/project-root
python manage.py migrate
python manage.py loaddata initial_data  # Optional: Load sample data
```

## Common Issues and Solutions

### Issue: Port Already in Use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: Database Connection Failed
1. Check database server is running
2. Verify connection string in `.env`
3. Check username and password
4. Ensure database exists

### Issue: Import Errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Permission Denied
```bash
# Make scripts executable
chmod +x *.py  # macOS/Linux
```

## Deployment

### Production Setup

1. Use environment-appropriate database (PostgreSQL recommended)
2. Set `ENVIRONMENT=production` in `.env`
3. Change `DEBUG=False`
4. Set strong `SECRET_KEY` and `JWT_SECRET`
5. Use HTTPS
6. Set up proper logging
7. Configure CORS appropriately

### Using Gunicorn (Flask/FastAPI)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using uWSGI (Django)
```bash
uwsgi --http :8000 --wsgi-file django-apps/project-root/config/wsgi.py --master --processes 4
```

## Useful Commands

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

### Run Tests
```bash
pytest
pytest --cov=.  # With coverage
```

### Database Migration (Django)
```bash
python manage.py makemigrations
python manage.py migrate
```

## Next Steps

1. Read API documentation
2. Import Postman collections
3. Test endpoints
4. Modify code and experiment
5. Build additional features
6. Deploy to production

## Support

For issues or questions:
1. Check the documentation
2. Review error messages carefully
3. Check your `.env` configuration
4. Verify database is running
5. Check that ports are available
