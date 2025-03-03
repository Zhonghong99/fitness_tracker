# Fitness Tracker Web Application

A simple, clean, and effective web application to track your workouts and maintain your fitness journey. Built with Flask and SQLite.

## Features

- 📝 Log exercises with sets, reps, and weights
- 📅 Calendar view of workout history
- 📊 Track workout sessions and streaks
- 💪 Exercise information with target muscle groups
- 🌐 Responsive design for both desktop and mobile
- 🕒 Timezone support (GMT+8)
- 💭 Motivational quotes for workout inspiration

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Additional Libraries**:
  - FullCalendar.js for calendar view
  - Select2 for searchable dropdowns
  - Bootstrap Icons

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zhonghong99/fitness_tracker.git
cd fitness-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Project Structure

```
fitness_tracker/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── fitness.db            # SQLite database
└── templates/
    └── index.html        # Main template file
```

## Database Schema

### Exercise Table
- `id`: Primary key
- `type`: Exercise name
- `date`: Timestamp of exercise
- `sets`: Relationship with ExerciseSet

### ExerciseSet Table
- `id`: Primary key
- `exercise_id`: Foreign key to Exercise
- `set_number`: Set sequence number
- `weight`: Weight used
- `reps`: Repetitions performed
- `total`: Total volume (weight × reps)

## Usage

1. **Adding an Exercise**:
   - Select date and time
   - Choose exercise type
   - Enter number of sets
   - Input weight and reps for each set

2. **Viewing History**:
   - Calendar view shows all workout days
   - Click on dates to see detailed exercises
   - Track your workout streak
   - Monitor monthly workout sessions

3. **Exercise Information**:
   - Hover over info icon to see target muscles
   - Primary and secondary muscle groups displayed

## Mobile Access

Access your fitness tracker from any device:
1. Deploy using one of these options:
   - PythonAnywhere (Free)
   - Render
   - Railway
   - Fly.io
   - Local network

2. Access via web browser
3. Add to home screen for app-like experience

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Environment Variables

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///fitness.db
```

## Deployment

### Local Network
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
Access via local IP address (e.g., `http://192.168.1.100:5000`)

### Cloud Deployment
Follow deployment guides for:
- PythonAnywhere
- Render
- Railway
- Fly.io

## Future Enhancements

- [ ] User authentication
- [ ] Data export/import
- [ ] Progress charts
- [ ] Exercise images/videos
- [ ] Workout plans
- [ ] Personal records tracking

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Exercise data and muscle group information
- Motivational quotes collection
- Bootstrap themes and components
- Flask documentation and community

## Author

[Zhong Hong Lee]
- Email: [zhonghonglee9998@gmail.com]
