import json
import pickle

import numpy as np
import requests
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Replace with your Mistral AI API endpoint and key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
API_KEY = "elOzXDIBZlvgVGCtGjrkLT6UFyQwxovJ"

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load the trained model and tokenizer
model = load_model('nlp.h5')
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# Maximum length of input sequences
max_len = 100

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

def chat_with_mistral(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/chat', methods=['POST'])
def chat():
    # Retrieve user message from the request
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get response from Mistral AI
    mistral_response = chat_with_mistral(user_input)

    # Return the response to the frontend
    return jsonify({"message": mistral_response})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            flash('Login successful!', 'success')
            if username == 'admin':  # Redirect admin user to the admin page
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        flash('Access denied: Admins only!', 'danger')
        return redirect(url_for('home'))

    # Fetch all users from the database
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input text from the request
    input_text = request.json.get("text", "")
    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Preprocess the input text for both inputs
    sequences = tokenizer.texts_to_sequences([input_text])
    padded_sequences = pad_sequences(sequences, maxlen=50, padding='post', truncating='post')  # Ensure maxlen=50

    # Pass the same padded input for both branches
    prediction = model.predict([padded_sequences, padded_sequences])  # Input1 and Input2
    predicted_class = np.argmax(prediction)

    # Map predicted class to sentiment
    label_map = {0: "joy", 1: "sadness", 2: "fear", 3: "anger"}
    sentiment = label_map.get(predicted_class, "Unknown")

    # Return the prediction as a JSON response
    return jsonify({"sentiment": sentiment, "confidence": float(np.max(prediction))})


@app.route('/sentiment', methods=['GET'])
def sentiment_page():
    # Render the sentiment analysis page
    return render_template('sentiment.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/remove_user/<int:user_id>', methods=['POST'])
def remove_user(user_id):
    if session.get('user') != 'admin':
        flash('Access denied: Admins only!', 'danger')
        return redirect(url_for('home'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} removed successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
