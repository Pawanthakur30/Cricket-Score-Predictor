from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 
    'Christchurch', 'Trinidad'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error_message = None
    if request.method == 'POST':
        try:
            batting_team = request.form['batting_team']
            bowling_team = request.form['bowling_team']
            city = request.form['city']
            current_score = int(request.form.get('current_score', 0))
            overs = float(request.form.get('overs', 0))
            wickets = int(request.form.get('wickets', 0))
            last_five = int(request.form.get('last_five', 0))

            # Check for valid overs
            if overs <= 0:
                crr = 0
            else:
                crr = current_score / overs

            balls_left = 120 - (overs * 6)
            wickets_left = 10 - wickets

            # Create DataFrame for prediction
            input_df = pd.DataFrame(
                {
                    'batting_team': [batting_team],
                    'bowling_team': [bowling_team],
                    'city': [city],
                    'current_score': [current_score],
                    'balls_left': [balls_left],
                    'wickets_left': [wickets_left],
                    'crr': [crr],
                    'last_five': [last_five]
                }
            )

            # Predict using the loaded model
            result = pipe.predict(input_df)
            prediction = int(result[0])

        except Exception as e:
            error_message = str(e)

    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), 
                           prediction=prediction, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
