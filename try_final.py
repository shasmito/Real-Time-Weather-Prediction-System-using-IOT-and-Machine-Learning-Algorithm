import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *
import joblib  # Import the joblib module
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

from joblib import load

# Load the trained Decision Tree model
loaded_model = load('fish_prediction_model_decision_tree_82.35.joblib')

# Function to make predictions
def predict_fish():
    ph_value = float(ph_entry.get())
    temperature_value = float(temperature_entry.get())
    turbidity_value = float(turbidity_entry.get())

    # Prepare the data for prediction
    data = [[ph_value, temperature_value, turbidity_value]]

    # Make a prediction
    fish_prediction = loaded_model.predict(data)

    # Display the predicted fish species
    prediction_label.config(text=f'Predicted Fish: {fish_prediction[0]}')




# Create a function to fetch data from the MySQL database and calculate averages
def fetch_data():
    # Establish a connection to the database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='try'
    )
    cursor = conn.cursor()

    # Execute an SQL query to select all data from the table
    cursor.execute("SELECT * FROM sensor_data")
    data = cursor.fetchall()

    # Calculate average values for each column
    column_names = ["ID", "pH", "Temperature", "Turbidity"]
    column_sum = [0.0] * len(column_names)

    for row in data:
        for i in range(len(row)):
            column_sum[i] += row[i]

    average_values = [sum / len(data) for sum in column_sum]

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Create a new window to display the data and averages
    result_window = tk.Toplevel(root)

    # Create a frame for displaying column names and averages
    frame = tk.Frame(result_window)
    frame.pack()

    # Labels for column names and their average values
    for i in range(len(column_names)):
        label = tk.Label(frame, text=f"{column_names[i]} Average: {average_values[i]:.2f}")
        label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

    # Create a treeview widget to display the data in a table-like format
    tree = ttk.Treeview(result_window, columns=column_names)
    for name in column_names:
        tree.heading(name, text=name)

    for row in data:
        tree.insert("", "end", values=row)

    frame.pack()
    tree.pack()

# Create the main application window
root = tk.Tk()
# root.title("Database Data Viewer")
root.title("Fish Prediction")
root.geometry("300x250")

icon_photo = PhotoImage(file="fish.png")
root.iconphoto(True, icon_photo)
root.config(background="#ceeff2")

title_text = Label(root, text="Fish Prediction Application", font=('times', 14), fg='red', bg="#ceeff2")
title_text.pack()

# Create a button to fetch and display the data and averages
fetch_button = tk.Button(root, text="Fetch Data",
                         bg="#40b5f5",
                         activebackground="red"
                         , command=fetch_data)
fetch_button.pack()

ph_label = Label(root, text="pH:", font=('times', 11), bg="#ceeff2")
ph_label.pack()
ph_entry = Entry(root)
ph_entry.pack()

temperature_label = Label(root, text="Temperature:", font=('times', 11), bg="#ceeff2")
temperature_label.pack()
temperature_entry = Entry(root)
temperature_entry.pack()

turbidity_label = Label(root, text="Turbidity:", font=('times', 11), bg="#ceeff2")
turbidity_label.pack()
turbidity_entry = Entry(root)
turbidity_entry.pack()

predict_button = Button(root, text="Predict Fish", font=('times', 11), 
                        activebackground="#a0fab2", 
                        command=predict_fish)
predict_button.pack()

prediction_label = Label(root, text="", font=('times', 11), fg="#54eb68")
prediction_label.pack()


root.mainloop()
