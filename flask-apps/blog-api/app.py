# Flask Blog API Application

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Models
class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    author = db.Column(db.String(100), default='Anonymous')
    views = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author,
            'views': self.views,
            'published': self.published,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Validation
def validate_article(data):
    errors = {}
    
    if not data.get('title'):
        errors['title'] = ['Title is required']
    elif len(data.get('title', '')) > 300:
        errors['title'] = ['Title must be less than 300 characters']
    
    if not data.get('content'):
        errors['content'] = ['Content is required']
    elif len(data.get('content', '')) < 100:
        errors['content'] = ['Content must be at least 100 characters']
    
    return errors

# Routes
@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get all articles with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category')
        
        query = Article.query
        
        if category:
            query = query.filter_by(category=category)
        
        total = query.count()
        articles = query.paginate(page=page, per_page=limit)
        
        return jsonify({
            'total': total,
            'page': page,
            'per_page': limit,
            'pages': articles.pages,
            'articles': [article.to_dict() for article in articles.items]
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get a specific article"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({
                'error': 'Not Found',
                'message': f'Article with ID {article_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        # Increment views
        article.views += 1
        db.session.commit()
        
        return jsonify(article.to_dict()), 200
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/articles', methods=['POST'])
def create_article():
    """Create a new article"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate
        errors = validate_article(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        article = Article(
            title=data['title'],
            content=data['content'],
            category=data.get('category'),
            author=data.get('author', 'Anonymous'),
            published=data.get('published', True)
        )
        
        db.session.add(article)
        db.session.commit()
        
        return jsonify(article.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """Update an article"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({
                'error': 'Not Found',
                'message': f'Article with ID {article_id} not found',
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
        errors = validate_article(data)
        if errors:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Invalid input',
                'details': errors,
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
        if 'category' in data:
            article.category = data['category']
        if 'author' in data:
            article.author = data['author']
        if 'published' in data:
            article.published = data['published']
        
        db.session.commit()
        return jsonify(article.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Delete an article"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({
                'error': 'Not Found',
                'message': f'Article with ID {article_id} not found',
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        db.session.delete(article)
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
        'service': 'Blog API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
