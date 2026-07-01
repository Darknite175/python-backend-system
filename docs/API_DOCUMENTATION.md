# API Documentation

Complete REST API documentation for all applications across different frameworks.

## Base URLs

- **Flask Task Management**: `http://localhost:5000/api`
- **Flask Blog API**: `http://localhost:5001/api`
- **Flask User Auth**: `http://localhost:5002/api`
- **Flask Inventory Manager**: `http://localhost:5003/api`

- **FastAPI Task Management**: `http://localhost:8000/api`
- **FastAPI Blog API**: `http://localhost:8001/api`
- **FastAPI User Auth**: `http://localhost:8002/api`
- **FastAPI Inventory Manager**: `http://localhost:8003/api`

- **Django Task Management**: `http://localhost:8000/api`
- **Django Blog API**: `http://localhost:8000/api`
- **Django User Auth**: `http://localhost:8000/api`
- **Django Inventory Manager**: `http://localhost:8000/api`

## 1. Task Management System API

### Endpoints

#### Create Task
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the Python backend system",
  "priority": "high",
  "due_date": "2026-12-31",
  "status": "pending"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Python backend system",
  "priority": "high",
  "due_date": "2026-12-31",
  "status": "pending",
  "created_at": "2026-07-01T10:30:00Z",
  "updated_at": "2026-07-01T10:30:00Z"
}
```

#### Get All Tasks
```http
GET /api/tasks
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the Python backend system",
    "priority": "high",
    "due_date": "2026-12-31",
    "status": "pending",
    "created_at": "2026-07-01T10:30:00Z",
    "updated_at": "2026-07-01T10:30:00Z"
  }
]
```

#### Get Task by ID
```http
GET /api/tasks/{id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Python backend system",
  "priority": "high",
  "due_date": "2026-12-31",
  "status": "pending",
  "created_at": "2026-07-01T10:30:00Z",
  "updated_at": "2026-07-01T10:30:00Z"
}
```

#### Update Task
```http
PUT /api/tasks/{id}
Content-Type: application/json

{
  "status": "in_progress",
  "priority": "medium"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project",
  "status": "in_progress",
  "priority": "medium",
  "updated_at": "2026-07-01T11:00:00Z"
}
```

#### Delete Task
```http
DELETE /api/tasks/{id}
```

**Response (204 No Content)**

### Validation Rules
- Title: Required, max 200 characters
- Priority: Must be 'low', 'medium', or 'high'
- Status: Must be 'pending', 'in_progress', or 'completed'
- Due date: Optional, must be future date

### Status Codes
- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 2. Blog API

### Endpoints

#### Create Article
```http
POST /api/articles
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Getting Started with Python",
  "content": "Python is a versatile language...",
  "category": "programming",
  "tags": ["python", "tutorial"]
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Getting Started with Python",
  "content": "Python is a versatile language...",
  "category": "programming",
  "tags": ["python", "tutorial"],
  "author_id": 1,
  "views": 0,
  "published": true,
  "created_at": "2026-07-01T10:30:00Z",
  "updated_at": "2026-07-01T10:30:00Z"
}
```

#### Get All Articles
```http
GET /api/articles?category=programming&limit=10&offset=0
```

**Response (200 OK):**
```json
{
  "total": 50,
  "articles": [
    {
      "id": 1,
      "title": "Getting Started with Python",
      "content": "Python is a versatile language...",
      "category": "programming",
      "views": 100,
      "published": true,
      "created_at": "2026-07-01T10:30:00Z"
    }
  ]
}
```

#### Get Article by ID
```http
GET /api/articles/{id}
```

#### Update Article
```http
PUT /api/articles/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Updated title",
  "content": "Updated content"
}
```

#### Delete Article
```http
DELETE /api/articles/{id}
Authorization: Bearer {token}
```

### Validation Rules
- Title: Required, max 300 characters
- Content: Required, min 100 characters
- Category: Required, must be valid category
- Tags: Optional, max 10 tags

---

## 3. User Authentication System

### Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2026-07-01T10:30:00Z"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer {access_token}
```

#### Update Profile
```http
PUT /api/auth/profile
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "full_name": "John Doe Updated",
  "bio": "Software developer"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

### Validation Rules
- Username: Required, 3-20 characters, alphanumeric
- Email: Required, valid email format, unique
- Password: Required, min 8 characters, must contain uppercase, lowercase, number, special char

---

## 4. Inventory Manager API

### Endpoints

#### Create Product
```http
POST /api/products
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "sku": "LAP-001",
  "price": 999.99,
  "quantity": 50,
  "category": "Electronics"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop",
  "sku": "LAP-001",
  "price": 999.99,
  "quantity": 50,
  "category": "Electronics",
  "created_at": "2026-07-01T10:30:00Z",
  "updated_at": "2026-07-01T10:30:00Z"
}
```

#### Get All Products
```http
GET /api/products?category=Electronics&in_stock=true&limit=20
```

#### Get Product by ID
```http
GET /api/products/{id}
```

#### Update Product
```http
PUT /api/products/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "quantity": 45,
  "price": 1099.99
}
```

#### Delete Product
```http
DELETE /api/products/{id}
Authorization: Bearer {token}
```

#### Update Stock
```http
POST /api/products/{id}/update-stock
Content-Type: application/json
Authorization: Bearer {token}

{
  "quantity_change": -5,
  "reason": "sold"
}
```

### Validation Rules
- Name: Required, max 200 characters
- SKU: Required, unique, alphanumeric
- Price: Required, must be positive number
- Quantity: Required, must be non-negative integer
- Category: Required, max 50 characters

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Validation Error",
  "message": "Invalid input",
  "details": {
    "field_name": ["Error message"]
  },
  "timestamp": "2026-07-01T10:30:00Z"
}
```

## Authentication

Protected endpoints require JWT token in Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## Testing with Postman

Import the provided Postman collection to test all endpoints:
- Collections are provided in `/postman-collections/`
- Environment variables are configured for different frameworks
