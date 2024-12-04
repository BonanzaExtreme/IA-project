# app/routes.py
import pandas as pd
from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import User
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define a Blueprint for routes
bp = Blueprint('main', __name__)

# Example exercise data
dataset_path = '../gym-exercise-data/megaGymDataset.csv'
exercises_df = pd.read_csv(dataset_path)
exercises_df['Id'] = exercises_df.index + 1


def recommend_exercise(user_profile, exercises):
    exercise_descriptions = [
        f"{exercise['Title']} {exercise['Description']} {exercise['Type']} {exercise['BodyPart']} {exercise['Equipment']} {exercise['Level']} {exercise['Age']} {exercise['Reps']} {exercise['Instructions']}" for exercise in exercises
    ]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(exercise_descriptions)
    
    user_profile_description = f"{user_profile['level']} {user_profile['age']} {user_profile['goal']} {user_profile['equipment']} {user_profile['body_part']}"
    user_profile_vector = vectorizer.transform([user_profile_description])
    cosine_similarities = cosine_similarity(user_profile_vector, tfidf_matrix)
    similar_indices = cosine_similarities.argsort()[0][::-1]
    recommendations = []
    for i in similar_indices[:5]:
        exercise = exercises[i]
        recommendations.append({
            'name': exercise['Title'],  
            'description': exercise['Description'],
            'type': exercise['Type'],
            'equipment': exercise['Equipment'],
            'target': exercise['BodyPart'],  
            'instructions': exercise['Instructions'], 
            'reps': exercise['Reps'], 
        })
    return recommendations


@bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(name=username).first():
            flash("Username already exists. Please choose another one.", "danger")
        else: 
            hashed_password = generate_password_hash(password)
            new_user = User(name=username, password=hashed_password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('main.login'))
    
    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(name=username).first()   
    
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html')


    
@bp.route('/workouts')
@login_required
def home():
    exercises = exercises_df.to_dict(orient='records')
    return render_template('index.html', exercises=exercises)


@bp.route('/generate_workout', methods=['GET'])
@login_required
def generate_workout_page():
    return render_template('generateworkout.html')

@bp.route('/generate_workout', methods=['POST'])
@login_required
def generate_workout():
    print(f"Received request method: {request.method}")
    print(f"Request data: {request.json}")
    user_data = request.json  
    exercises = exercises_df.to_dict(orient='records')
    recommendations = recommend_exercise(user_data, exercises)
    return jsonify(recommendations)
 

@bp.route('/myworkout', methods=['GET'])
@login_required
def my_workout():
    exercises = exercises_df.to_dict(orient='records')
    liked_exercises_str = request.args.getlist('liked_exercises', '') 
    
    if liked_exercises_str:
        liked_exercises = list(map(int, liked_exercises_str.split(',')))  
    else:
        liked_exercises = []

    return render_template('myworkout.html', exercises=exercises, liked_exercises=liked_exercises) 


@bp.route('/myworkout', methods=['POST'])
def my_workout_post():
    exercises = exercises_df.to_dict(orient='records')
    user_data = request.json 
    liked_exercises = user_data.get('liked_exercises', []) 

    recommendations = []
    if liked_exercises:
        recommendations = recommend_from_likes(liked_exercises, exercises)

    
    return jsonify(recommendations)
    

def recommend_from_likes(liked_exercises, exercises):
    
    liked_exercise_details = [exercise for exercise in exercises if exercise['Id'] in liked_exercises]
    
   
    liked_descriptions = [
        f"{exercise['Title']} {exercise['Description']} {exercise['Type']} {exercise['BodyPart']} {exercise['Equipment']} {exercise['Level']} {exercise['Age']} {exercise['Reps']} {exercise['Instructions']}" 
        for exercise in liked_exercise_details
    ]
    
    
    liked_profile = " ".join(liked_descriptions)
    
   
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([desc for exercise in exercises for desc in [f"{exercise['Title']} {exercise['Description']} {exercise['Type']} {exercise['BodyPart']} {exercise['Equipment']} {exercise['Level']} {exercise['Age']} {exercise['Reps']} {exercise['Instructions']}"]])
    
   
    liked_profile_vector = vectorizer.transform([liked_profile])
    
   
    cosine_similarities = cosine_similarity(liked_profile_vector, tfidf_matrix)
    similar_indices = cosine_similarities.argsort()[0][::-1]
    

    recommendations = []
    for i in similar_indices[:6]:
        exercise = exercises[i]
        recommendations.append({
            'name': exercise['Title'],  
            'description': exercise['Description'],
            'type': exercise['Type'],
            'equipment': exercise['Equipment'],
            'target': exercise['BodyPart'],  
            'instructions': exercise['Instructions'], 
            'reps': exercise['Reps'], 
        })
    
    return recommendations

