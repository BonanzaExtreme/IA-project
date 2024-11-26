# app/routes.py

from flask import Blueprint, render_template, request, jsonify

# Define a Blueprint for routes
bp = Blueprint('main', __name__)

# Example exercise data
exercises = [
    {"name": "Push-up", "muscle": "Chest", "goal": "muscle-building", "equipment": "None", "duration": 10},
    {"name": "Squat", "muscle": "Legs", "goal": "muscle-building", "equipment": "None", "duration": 15},
    {"name": "Dumbbell Curl", "muscle": "Biceps", "goal": "muscle-building", "equipment": "Dumbbells", "duration": 10},
    {"name": "Running", "muscle": "Full Body", "goal": "weight-loss", "equipment": "None", "duration": 30}
]

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/generateworkout')
def workout():
    return render_template('generateworkout.html')  

@bp.route('/myworkout')
def my_workout():
    return render_template('myworkout.html') 


@bp.route('/recommend', methods=['POST'])
def recommend_workout():
    data = request.get_json()

    goal = data.get('goal')
    equipment = data.get('equipment')
    time_available = data.get('time')

    filtered_exercises = [
        exercise for exercise in exercises
        if exercise['goal'] == goal
        and (equipment.lower() in exercise['equipment'].lower() or exercise['equipment'] == 'None')
        and exercise['duration'] <= time_available
    ]

    return jsonify(filtered_exercises)
