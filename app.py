from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load your trained model
try:
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: rf_model.pkl not found!")
    model = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Get form data - NOW INCLUDING AGE!
            age = float(request.form['Age(year)'])
            height = float(request.form['Current Height(cm)'])
            weight = float(request.form['Current Weight(kg)'])
            dad_height = float(request.form["Father's Height(cm)"])
            mom_height = float(request.form["Mother's Height(cm)"])

            # Validate inputs
            if any(val <= 0 for val in [age, height, weight, dad_height, mom_height]):
                return render_template('height.html', error="All values must be positive numbers")
            
            if age < 10 or age > 13:
                return render_template('height.html', error="Age must be between 10 and 13")
            
            if not model:
                return render_template('height.html', error="Model not available")
            
            # Make prediction - CORRECT ORDER: Age, Height, Father's Height, Mother's Height, Weight
            features = np.array([[age, height, dad_height, mom_height, weight]])
            prediction = model.predict(features)[0]
            
            return render_template('height.html', prediction=round(prediction, 2), error=None)
            
        except ValueError:
            return render_template('height.html', error="Please enter valid numbers")
        except Exception as e:
            return render_template('height.html', error=f"Prediction error: {str(e)}")
    
    # GET request
    return render_template('height.html', prediction=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)