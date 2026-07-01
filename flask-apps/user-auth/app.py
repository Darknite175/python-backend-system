# Flask User Authentication Application

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL', 'sqlite:///auth.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'your-jwt-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'bio': self.bio,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

# Utility functions
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_password_value):
    """Verify password"""
    return hash_password(password) == hash_password_value

def generate_token(user_id, expires_in=3600):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    """Validate password strength"""
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    if not any(c.isupper() for c in password):
        errors.append('Password must contain at least one uppercase letter')
    if not any(c.islower() for c in password):
        errors.append('Password must contain at least one lowercase letter')
    if not any(c.isdigit() for c in password):
        errors.append('Password must contain at least one number')
    return errors

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        errors = {}
        
        # Validate username
        if not data.get('username'):
            errors['username'] = ['Username is required']
        elif len(data.get('username', '')) < 3:
            errors['username'] = ['Username must be at least 3 characters']
        
        # Validate email
        if not data.get('email'):
            errors['email'] = ['Email is required']
        elif not validate_email(data['email']):
            errors['email'] = ['Invalid email format']
        
        # Validate password
        if not data.get('password'):
            errors['password'] = ['Password is required']
        else:
            pwd_errors = validate_password_strength(data['password'])
            if pwd_errors:
                errors['password'] = pwd_errors
        
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'error': 'Conflict',
                'message': 'Username already exists',
                'timestamp': datetime.utcnow().isoformat()
            }), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'error': 'Conflict',
                'message': 'Email already exists',
                'timestamp': datetime.utcnow().isoformat()
            }), 409
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            full_name=data.get('full_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate input
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Email and password are required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid email or password',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        # Verify password
        if not verify_password(data['password'], user.password_hash):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid email or password',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'user': user.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authorization header is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid authorization header',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'Not Found',
                'message': 'User not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/auth/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authorization header is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid authorization header',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'Not Found',
                'message': 'User not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Update fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'bio' in data:
            user.bio = data['bio']
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'User Auth API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002)
