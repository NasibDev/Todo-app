# Import Flask and other libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the model and the scaler
model = pickle.load(open('diabetes.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Create a Flask app
app = Flask(__name__)

# Define the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the predict page
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the form
    input_data = [float(x) for x in request.form.values()]
    value1=input_data[0]
    value2=input_data[1]
    value3=input_data[2]
    value4=input_data[3]
    value5=input_data[4]
    value6=input_data[5]
    value7=input_data[6]
    value8=input_data[7]

    # Convert the input data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    # Reshape the input data
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    # Standardize the input data
    standarized_input_data = scaler.transform(input_data_reshaped)
    # Make the prediction using the model
    prediction = model.predict(standarized_input_data)
    # Convert the prediction to a string
    if(prediction[0]==0):
        output = 'The person is not diabetic'
    else:
        output = 'The person is diabetic'
    # Render the result page with the output
    return render_template('result.html', prediction_text=output, value1=value1, value2=value2, value3=value3, value4=value4, value5=value5, value6=value6, value7=value7, value8=value8)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
