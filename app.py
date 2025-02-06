# This is the main application file that runs the Flask web application
from flask import Flask, render_template, request, redirect, url_for  # Import necessary Flask modules
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database operations
from datetime import datetime, timedelta  # Import datetime for timestamp handling and timedelta for streak calculation
import json
import pytz  # Add this import at the top
import calendar  # Add this import for calendar functions

# Create a Flask application instance
app = Flask(__name__)
# Configure the database URI - this tells Flask to use SQLite and create a file named fitness.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
# Create a SQLAlchemy instance to handle database operations
db = SQLAlchemy(app)

# Add this function to convert UTC to GMT+8
def get_gmt8_time():
    utc_time = datetime.utcnow()
    gmt8 = pytz.timezone('Asia/Singapore')  # Singapore uses GMT+8
    return pytz.utc.localize(utc_time).astimezone(gmt8)

# Main Exercise record
class Exercise(db.Model):
    # Primary key for unique identification of each exercise record
    id = db.Column(db.Integer, primary_key=True)
    # Type of exercise (e.g., "Bench Press", "Squats", etc.)
    type = db.Column(db.String(100), nullable=False)
    # Timestamp of when the exercise was recorded
    date = db.Column(db.DateTime, nullable=False)  # Remove default
    # Relationship with sets
    sets = db.relationship('ExerciseSet', backref='exercise', lazy=True)

    @staticmethod
    def create(type):
        return Exercise(
            type=type,
            date=get_gmt8_time()
        )

# Individual set records for each exercise
class ExerciseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)  # weight * reps for this set

# Define the Weight tracking database model
class Weight(db.Model):
    # Primary key for unique identification of each weight record
    id = db.Column(db.Integer, primary_key=True)
    # Body weight measurement
    weight = db.Column(db.Float, nullable=False)
    # Timestamp of when the weight was recorded
    date = db.Column(db.DateTime, nullable=False)  # Remove default

    @staticmethod
    def create(weight):
        return Weight(
            weight=float(weight),
            date=get_gmt8_time()
        )

# Define routes for the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle POST requests (form submissions)
    if request.method == 'POST':
        # Check if the form submission is for exercise logging
        if 'exercise' in request.form:
            # Get the selected date and convert it to GMT+8
            date_str = request.form['exercise_date']
            local_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            gmt8 = pytz.timezone('Asia/Singapore')
            local_date = gmt8.localize(local_date)
            
            # Get exercise type
            exercise_type = request.form['type']
            
            # Create new exercise record with selected date
            new_exercise = Exercise(
                type=exercise_type,
                date=local_date
            )
            db.session.add(new_exercise)
            db.session.flush()  # This gets us the exercise ID
            
            # Get number of sets
            num_sets = int(request.form['num_sets'])
            
            # Process each set
            for i in range(num_sets):
                weight = float(request.form[f'weight_{i+1}'])
                reps = int(request.form[f'reps_{i+1}'])
                total = weight * reps
                
                new_set = ExerciseSet(
                    exercise_id=new_exercise.id,
                    set_number=i+1,
                    weight=weight,
                    reps=reps,
                    total=total
                )
                db.session.add(new_set)
            
            db.session.commit()
            
        # Check if the form submission is for weight logging
        elif 'weight' in request.form:
            # Get weight value from the form
            weight = request.form['weight']
            # Create new weight record
            new_weight = Weight.create(weight)
            # Add the new weight to the database session
            db.session.add(new_weight)
            # Commit the changes to the database
            db.session.commit()
        # Redirect back to the index page after form submission
        return redirect(url_for('index'))

    # Handle GET requests (page display)
    # Get all exercises ordered by date (newest first)
    exercises = Exercise.query.order_by(Exercise.date.desc()).all()
    # Get all weight records ordered by date (newest first)
    weights = Weight.query.order_by(Weight.date.desc()).all()

    # Calculate statistics
    today = datetime.now(pytz.timezone('Asia/Singapore'))
    first_day = today.replace(day=1, hour=0, minute=0, second=0)
    last_day = today.replace(
        day=calendar.monthrange(today.year, today.month)[1], 
        hour=23, minute=59, second=59
    )
    
    # Count unique days with workouts this month
    monthly_sessions = db.session.query(
        db.func.date(Exercise.date)
    ).filter(
        Exercise.date >= first_day,
        Exercise.date <= last_day
    ).distinct().count()
    
    # Total number of exercises recorded
    total_exercises = Exercise.query.count()
    
    # Calculate streak (consecutive days with workouts)
    streak_days = 0
    current_date = today
    while Exercise.query.filter(
        Exercise.date >= current_date.replace(hour=0, minute=0, second=0),
        Exercise.date <= current_date.replace(hour=23, minute=59, second=59)
    ).first():
        streak_days += 1
        current_date -= timedelta(days=1)

    # Render the template with the exercise and weight data
    return render_template('index.html',
                         exercises=exercises,
                         weights=weights,
                         monthly_sessions=monthly_sessions,
                         total_exercises=total_exercises,
                         streak_days=streak_days)

# Run the application only if this file is executed directly
if __name__ == '__main__':
    # Create all database tables before running the app
    with app.app_context():
        db.drop_all()  # Be careful with this in production!
        db.create_all()
    # Run the Flask application in debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)