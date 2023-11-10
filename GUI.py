import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Create a function to fetch data from the MySQL database and display the entire table
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

# Create the main application window
root = tk.Tk()
root.title("Temperature Data")
root.geometry("500x300")

title_text = Label(root, text="Temperature Data Viewer", font=('times', 14), fg='red')
title_text.pack()

# Create a button to fetch and display the entire table
fetch_button = tk.Button(root, text="Fetch Temperature Data", command=fetch_data)
fetch_button.pack()

root.mainloop()
