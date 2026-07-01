# Flask Task Management Application

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Models
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': 'Invalid input',
        'timestamp': datetime.utcnow().isoformat()
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Resource not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500

# Validation function
def validate_task(data):
    errors = {}
    
    if not data.get('title'):
        errors['title'] = ['Title is required']
    elif len(data.get('title', '')) > 200:
        errors['title'] = ['Title must be less than 200 characters']
    
    if data.get('priority') and data['priority'] not in ['low', 'medium', 'high']:
        errors['priority'] = ['Priority must be low, medium, or high']
    
    if data.get('status') and data['status'] not in ['pending', 'in_progress', 'completed']:
        errors['status'] = ['Status must be pending, in_progress, or completed']
    
    return errors

# Routes
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    try:
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Task.query
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        
        tasks = query.all()
        return jsonify({
            'total': len(tasks),
            'tasks': [task.to_dict() for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'error': 'Not Found',
                'message': f'Task with ID {task_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate input
        errors = validate_task(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Create task
        task = Task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            due_date=data.get('due_date')
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'error': 'Not Found',
                'message': f'Task with ID {task_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate input
        errors = validate_task(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            task.priority = data['priority']
        if 'status' in data:
            task.status = data['status']
        if 'due_date' in data:
            task.due_date = data['due_date']
        
        db.session.commit()
        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'error': 'Not Found',
                'message': f'Task with ID {task_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'message': f'Task with ID {task_id} deleted successfully',
            'timestamp': datetime.utcnow().isoformat()
        }), 204
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
        'service': 'Task Management API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
