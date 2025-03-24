import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser

# Load the CSV file into a pandas DataFrame
csv_file = "output.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)



# Function to search for matching titles
def search_title():
    # Clear previous results
    for row in result_tree.get_children():
        result_tree.delete(row)
    
    query = title_entry.get().strip().lower()
    if not query:
        messagebox.showerror("Error", "Please enter a title to search!")
        return
    
    # Find matching rows
    filtered_df = df[df["title"].str.contains(query, case=False, na=False)]
    
    if filtered_df.empty:
        messagebox.showinfo("No Results", "No matching titles found.")
        return
    
    # Insert matching rows into the treeview
    for index, row in filtered_df.iterrows():
        result_tree.insert(
            "", "end", values=(row["title"], row["author"], row["date"], row["link"], row["author_link"])
        )




# Create the Tkinter GUI
root = tk.Tk()
root.title("Economics Publication Explorer")

# Create a frame for the search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

# Label and entry for title search
title_label = tk.Label(search_frame, text="Enter Title:")
title_label.pack(side=tk.LEFT, padx=5)
title_entry = tk.Entry(search_frame, width=50)
title_entry.pack(side=tk.LEFT, padx=5)

# Search button
search_button = tk.Button(search_frame, text="Search", command=search_title)
search_button.pack(side=tk.LEFT, padx=5)

# Create a Treeview (table) to display results
result_frame = tk.Frame(root)
result_frame.pack(pady=50)

columns = ("Title", "Author", "Date", "Link", "Author Link")
result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20)
result_tree.pack(side=tk.LEFT)

# Define column headings
for col in columns:
    result_tree.heading(col, text=col)
    result_tree.column(col, width=150 if col not in ("Link", "Author Link") else 300, anchor="w")

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
result_tree.config(yscrollcommand=scrollbar.set)

# Function to open the URL in a browser
def open_url(url):
    webbrowser.open(url)

# Function to handle row button clicks
def handle_row_selection(event):
    # Get clicked row and column
    region = result_tree.identify("region", event.x, event.y)
    if region != "cell":
        return
    
    row_id = result_tree.identify_row(event.y)
    column_id = result_tree.identify_column(event.x)
    
    if row_id and column_id:
        # Get the row's data
        row_values = result_tree.item(row_id, "values")
        
        # Determine which column was clicked
        if column_id == "#4":  # "Link" column
            url = row_values[3]  # Extract URL from the "Link" column
            open_url(url)
        elif column_id == "#5":  # "Author Link" column
            author_link = row_values[4]  # Extract URL from the "Author Link" column
            open_url(author_link)

# Bind click event to handle row button clicks
result_tree.bind("<Button-1>", handle_row_selection)

# Run the Tkinter main loop
root.mainloop()
