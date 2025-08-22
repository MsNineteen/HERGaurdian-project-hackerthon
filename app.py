from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set secret key and database URI
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///herguardian.db')  # Fallback to default
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models import db
db.init_app(app)

# Create tables (first run only)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# API to get testimonials
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify([{
        "id": t.id,
        "text": t.text,
        "author": t.author,
        "location": t.location,
        "avatar": t.avatar
    } for t in testimonials])

# API to add a new testimonial (admin-only in production)
@app.route('/api/testimonials', methods=['POST'])
def add_testimonial():
    data = request.json
    new_testimonial = Testimonial(
        text=data['text'],
        author=data['author'],
        location=data['location'],
        avatar=data.get('avatar', '')
    )
    db.session.add(new_testimonial)
    db.session.commit()
    return jsonify({"message": "Testimonial added!"}), 201

# API for user signup
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if not data.get('email') or not data.get('name'):
        return jsonify({"error": "Email and name are required"}), 400
    
    new_user = User(email=data['email'], name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered!"}), 201