import mysql.connector
import joblib
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Function to fetch temperature data from the MySQL database and display the entire table
def fetch_data():
    # Establish a connection to the database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='dht'
    )
    cursor = conn.cursor()

    # Execute an SQL query to select all data from the table
    cursor.execute("SELECT * FROM tbl")
    data = cursor.fetchall()

    # Calculate maximum and minimum values of the 'temp' column
    max_temp = max(data, key=lambda x: x[1])[1]
    min_temp = min(data, key=lambda x: x[1])[1]

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Create a new window to display the entire table and maximum/minimum values
    result_window = tk.Toplevel(root)

    # Create labels to display maximum and minimum values
    max_temp_label = tk.Label(result_window, text=f"Maximum Temperature: {max_temp}°C")
    max_temp_label.pack()

    min_temp_label = tk.Label(result_window, text=f"Minimum Temperature: {min_temp}°C")
    min_temp_label.pack()

    # Create a treeview widget to display the data in a table-like format
    column_names = [desc[0] for desc in cursor.description]
    tree = ttk.Treeview(result_window, columns=column_names, show='headings')

    for name in column_names:
        tree.heading(name, text=name)

    for row in data:
        tree.insert('', 'end', values=row)

    tree.pack()

# Load the trained logistic regression model
loaded_model = joblib.load("logistic_regression_model.pkl")

# Function to make weather predictions
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
root.title("Combined Application")
root.geometry("600x300")

title_text = Label(root, text="Temperature Data and Weather Prediction", font=('times', 14), fg='red')
title_text.pack()

# Create a frame for temperature data
frame_temp = tk.Frame(root)
frame_temp.pack(side="left")

frame_weather = tk.Frame(root)
frame_weather.pack(side="right")

# Temperature Data Section
temp_label = Label(frame_temp, text="Temperature Data", font=('times', 12), fg='blue')
temp_label.pack()

# Create a button to fetch and display temperature data
fetch_button = tk.Button(frame_temp, text="Fetch Temperature Data", command=fetch_data)
fetch_button.pack()

# Weather Prediction Section
weather_label = Label(frame_weather, text="Weather Prediction", font=('times', 12), fg='blue')
weather_label.pack()

precipitation_label = Label(frame_weather, text="Precipitation (mm):", font=('times', 11))
precipitation_label.pack()
precipitation_entry = Entry(frame_weather)
precipitation_entry.pack()

temp_max_label = Label(frame_weather, text="Max Temperature (°C):", font=('times', 11))
temp_max_label.pack()
temp_max_entry = Entry(frame_weather)
temp_max_entry.pack()

temp_min_label = Label(frame_weather, text="Min Temperature (°C):", font=('times', 11))
temp_min_label.pack()
temp_min_entry = Entry(frame_weather)
temp_min_entry.pack()

wind_label = Label(frame_weather, text="Wind Speed (km/h):", font=('times', 11))
wind_label.pack()
wind_entry = Entry(frame_weather)
wind_entry.pack()

predict_button = Button(frame_weather, text="Predict Weather", font=('times', 11), command=predict_weather)
predict_button.pack()

prediction_label = Label(frame_weather, text="", font=('times', 11), fg="#54eb68")
prediction_label.pack()

root.mainloop()
