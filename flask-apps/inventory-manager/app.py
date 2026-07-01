# Flask Inventory Manager Application

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL', 'sqlite:///inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Models
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sku': self.sku,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'in_stock': self.quantity > 0,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity_change': self.quantity_change,
            'reason': self.reason,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

# Validation
def validate_product(data):
    errors = {}
    
    if not data.get('name'):
        errors['name'] = ['Name is required']
    elif len(data.get('name', '')) > 200:
        errors['name'] = ['Name must be less than 200 characters']
    
    if not data.get('sku'):
        errors['sku'] = ['SKU is required']
    elif len(data.get('sku', '')) > 50:
        errors['sku'] = ['SKU must be less than 50 characters']
    
    if not data.get('price'):
        errors['price'] = ['Price is required']
    else:
        try:
            price = float(data['price'])
            if price < 0:
                errors['price'] = ['Price must be positive']
        except ValueError:
            errors['price'] = ['Price must be a number']
    
    if 'quantity' in data:
        try:
            qty = int(data['quantity'])
            if qty < 0:
                errors['quantity'] = ['Quantity cannot be negative']
        except ValueError:
            errors['quantity'] = ['Quantity must be an integer']
    
    return errors

# Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with filtering"""
    try:
        category = request.args.get('category')
        in_stock = request.args.get('in_stock', type=lambda x: x.lower() == 'true')
        
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        if in_stock:
            query = query.filter(Product.quantity > 0)
        
        products = query.all()
        return jsonify({
            'total': len(products),
            'products': [product.to_dict() for product in products]
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'error': 'Not Found',
                'message': f'Product with ID {product_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate
        errors = validate_product(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Check SKU uniqueness
        if Product.query.filter_by(sku=data['sku']).first():
            return jsonify({
                'error': 'Conflict',
                'message': 'SKU already exists',
                'timestamp': datetime.utcnow().isoformat()
            }), 409
        
        product = Product(
            name=data['name'],
            description=data.get('description'),
            sku=data['sku'],
            price=float(data['price']),
            quantity=int(data.get('quantity', 0)),
            category=data.get('category')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'error': 'Not Found',
                'message': f'Product with ID {product_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate
        errors = validate_product(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'quantity' in data:
            product.quantity = int(data['quantity'])
        if 'category' in data:
            product.category = data['category']
        
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/products/<int:product_id>/update-stock', methods=['POST'])
def update_stock(product_id):
    """Update product stock"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'error': 'Not Found',
                'message': f'Product with ID {product_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        data = request.get_json()
        if not data or 'quantity_change' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'quantity_change is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        quantity_change = int(data['quantity_change'])
        new_quantity = product.quantity + quantity_change
        
        if new_quantity < 0:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Insufficient stock',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Record movement
        movement = StockMovement(
            product_id=product_id,
            quantity_change=quantity_change,
            reason=data.get('reason', 'adjustment'),
            notes=data.get('notes')
        )
        
        product.quantity = new_quantity
        db.session.add(movement)
        db.session.commit()
        
        return jsonify({
            'product': product.to_dict(),
            'movement': movement.to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'error': 'Not Found',
                'message': f'Product with ID {product_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return '', 204
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
        'service': 'Inventory Manager API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5003)
