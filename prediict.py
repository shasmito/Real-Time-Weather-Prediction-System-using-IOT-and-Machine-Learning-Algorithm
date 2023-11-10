import joblib
import tkinter as tk
from tkinter import *

# Load the trained logistic regression model
loaded_model = joblib.load("logistic_regression_model.pkl")

# Function to make predictions
def predict_weather():
    try:
        precipitation = float(precipitation_entry.get())
        temp_max = float(temp_max_entry.get())
        temp_min = float(temp_min_entry.get())
        wind = float(wind_entry.get())

        # Prepare the data for prediction
        data = [[precipitation, temp_max, temp_min, wind]]

        # Make a prediction
        weather_prediction = loaded_model.predict(data)

        # Display the predicted weather label
        prediction_label.config(text=f'Predicted Weather: {weather_prediction[0]}')
    except ValueError:
        prediction_label.config(text="Invalid input. Please enter numeric values.")

# Create the main application window
root = tk.Tk()
root.title("Weather Prediction")
root.geometry("300x250")

title_text = Label(root, text="Weather Prediction Application", font=('times', 14), fg='red')
title_text.pack()

precipitation_label = Label(root, text="Precipitation (mm):", font=('times', 11))
precipitation_label.pack()
precipitation_entry = Entry(root)
precipitation_entry.pack()

temp_max_label = Label(root, text="Max Temperature (°C):", font=('times', 11))
temp_max_label.pack()
temp_max_entry = Entry(root)
temp_max_entry.pack()

temp_min_label = Label(root, text="Min Temperature (°C):", font=('times', 11))
temp_min_label.pack()
temp_min_entry = Entry(root)
temp_min_entry.pack()

wind_label = Label(root, text="Wind Speed (km/h):", font=('times', 11))
wind_label.pack()
wind_entry = Entry(root)
wind_entry.pack()

predict_button = Button(root, text="Predict Weather", font=('times', 11), command=predict_weather)
predict_button.pack()

prediction_label = Label(root, text="", font=('times', 11), fg="#54eb68")
prediction_label.pack()

root.mainloop()
