import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

 

 

app = Flask(__name__)
model = pickle.load(open('model_rand.pkl', 'rb'))

 

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

 

@app.route('/predict', methods=['POST'])
def predict():
    return render_template('predict.html')

 

@app.route('/about', methods=['POST'])
def about():
    return render_template('about.html')

 

@app.route('/heart', methods=['POST'])
def disease():
    return render_template('disease.html')

 

 

@app.route('/result', methods = ['POST'])
def result():
    # Extract form values

    age = float(request.form['age'])
    male = 1 if request.form['gender'] == 'male' else 0
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    ap_hi = int(request.form['systolic_bp'])
    ap_lo = int(request.form['diastolic_bp'])

    if(request.form['chol']== 'normal'):
        cholesterol = 1
    elif(request.form['chol']== 'medium'):
        cholesterol = 2
    elif(request.form['chol'] == 'high'):
        cholesterol = 3

    if(request.form['gluc']== 'normal'):
        gluc = 1
    elif(request.form['gluc']== 'medium'):
        gluc = 2
    elif(request.form['gluc'] == 'high'):
        gluc = 3



    '''   cholesterol = int(request.form['cholesterol'])

    gluc = int(request.form['glucose'])

    '''
    smoke = 1 if request.form['smoke'] == 'yes' else 0
    alco = 1 if request.form['alcohol'] == 'yes' else 0
    active = 1 if request.form['exercise'] == 'yes' else 0

    bmi = weight / (height*height)
    if (bmi > 0 and bmi <= 15):
        bmi_class = 0
    elif(bmi>15 and bmi <= 18.5):
        bmi_class = 1
    elif(bmi >18.5 and bmi <= 25):
        bmi_class = 2
    elif(bmi > 25 and bmi <=30):
        bmi_class = 3
    elif(bmi > 30 and bmi <=35):
        bmi_class = 4
    elif(bmi > 35 and bmi <=40 ):
        bmi_class = 5
    elif(bmi > 40):
        bmi_class = 6



 

    # Create a feature vector (input for the model)
    features = [age, male, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, bmi, bmi_class]

 

    # Create a DataFrame with appropriate column names
    df = pd.DataFrame([features], columns=["age", "male", "height", "weight", "ap_hi", "ap_lo", "cholesterol", "gluc", "smoke", "alco", "active", "bmi", "bmi_class"])

 

    # Perform prediction using the model
    prediction = model.predict(df)
    result = "Presence of Heart Disease" if prediction == 1 else "Absence of Heart Disease"

 

    return render_template('predict.html', prediction=result)

 

if __name__ == "__main__":
    app.run(debug=True)