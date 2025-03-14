# TASK 1: GUI CREATION

# Importing necessary packages
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import PIL.Image
from ttkthemes import ThemedTk
import csv
import tkinter as tk
from tkinter import ttk, filedialog 
from tkinter import messagebox

# Establishing a connection to the SQLite database
conn = sqlite3.connect('C:/Users/Pratyasha/Downloads/chemical_compounds.db')
c = conn.cursor()

# Creating the root window
root = tk.Tk()
root.configure(bg='LavenderBlush3') 
ttk.Style().theme_use('clam')
root.title("Chemical Compounds Database")

# Customizing styles
style = ttk.Style()
style.configure("Column.TFrame")  
style.configure("Treeview.Heading", font=('Times New Roman', 11), padding=[('', (5, 5, 5, 5))])
style.configure('Treeview', rowheight=124)  
style.configure("Custom.TButton", background="lavenderblush4")  
style.configure("Compounds.TLabel", background="LavenderBlush3")
style.configure("Savedata.TLabel", background="lavenderblush4")

# Create frames
button_frame = ttk.Frame(root, style="Button.TFrame", width=500)
button_frame.place(x=50, y=70, width=500, height=786)
column_frame = ttk.Frame(root, style="Column.TFrame")
column_frame.place(x=500, y=70, width=1000, height=786)
search_frame = ttk.Frame(root, style='Search.TFrame')
search_frame.place(x=1170, y=20, width=330, height=40)

# Labels
filters_heading = ttk.Label(button_frame, text="CUSTOMISABLE PARAMETERS ", font=('Times New Roman', 12))
filters_heading.grid(row=0, column=1, columnspan=3, padx=5, pady=10)
total_compounds_label = ttk.Label(root, text="TOTAL COMPOUNDS: 0", font=('Times New Roman', 12))
total_compounds_label.place(x=500, y=25)
remaining_compounds_label = ttk.Label(root, text="FILTERED COMPOUNDS : 0", font=('Times New Roman', 12))
remaining_compounds_label.place(x=750, y=25)

# Buttons
lipinski_button = ttk.Button(button_frame, text="Lipinski Rule", style="Custom.TButton")
bioavailability_button = ttk.Button(button_frame, text="Bioavailability", style="Custom.TButton")
lead_likeness_button = ttk.Button(button_frame, text="Lead Likeness", style="Custom.TButton")
ghose_rule_button = ttk.Button(button_frame, text="Ghose Rule", style="Custom.TButton")
reset_button = ttk.Button(button_frame, text="Clear Filters")

# Grid layout for buttons
lipinski_button.grid(row=18, column=1, columnspan=3, pady=20)
bioavailability_button.grid(row=18, column=2, columnspan=3, pady=20)
lead_likeness_button.grid(row=20, column=1, columnspan=3, pady=10)
ghose_rule_button.grid(row=20, column=2, columnspan=3, pady=10)
reset_button.grid(row=23, column=1, columnspan=5, pady=20)


# Criteria input fields
criteria_labels = ['MolWeight', 'RingCount', 'DonorCount', 'AcceptorCount', 'LogP', 'LogD', 'PSA', 'RotatableBonds', 'FAR','Refractivity','TotalAtoms']

criteria_entries = {}
for i, criteria in enumerate(criteria_labels):
    label_frame = tk.Frame(button_frame, background="lavenderblush4")
    label_frame.grid(row=i+2, column=1, padx=10)
    ttk.Label(label_frame, text=f"{criteria}:").pack()
    criteria_entries[criteria] = {}
    #criteria_entries[criteria]['from'] = ttk.Entry(button_frame, width=17, validate='key', validatecommand=(root.register(validate_numeric_input), '%P'))
    #criteria_entries[criteria]['to'] = ttk.Entry(button_frame, width=17, validate='key', validatecommand=(root.register(validate_numeric_input), '%P'))
    criteria_entries[criteria]['from'] = ttk.Entry(button_frame, width = 17)
    criteria_entries[criteria]['to'] = ttk.Entry(button_frame, width =17)
    criteria_entries[criteria]['from'].grid(row=i +2, column=2, padx=10,pady = 10)
    criteria_entries[criteria]['to'].grid(row=i +2, column=4, padx=10, pady=10)
    ttk.Label(button_frame, text="to").grid(row=i+2, column=3)  
    

# Function to filter based on user input
def filter_custom():
    # Construct the WHERE clause of the SQL query based on user input
    where_clause = []
    for criteria, entries in criteria_entries.items():
        from_val = entries['from'].get()
        to_val = entries['to'].get()
        if from_val and to_val:
            where_clause.append(f"{criteria} BETWEEN {from_val} AND {to_val}")
    
    # Join the WHERE clauses using 'AND'
    if where_clause:
        where_condition = " AND ".join(where_clause)
    else:
        # If no filters are provided, return all records
        where_condition = "1=1"

    # SQL query to retrieve filtered data
    sql_query = f"""
        SELECT 
            Name, MolWeight, RingCount, DonorCount, AcceptorCount, LogP, LogD,
            PSA, RotatableBonds, FAR, Refractivity, TotalAtoms, Image 
        FROM 
            Compounds 
        WHERE 
            {where_condition}
    """
    
    # Execute the SQL query and fetch the results
    c.execute(sql_query)
    rows = c.fetchall()

    # Clear the existing entries in the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Populate the treeview with the filtered data
    for i, row in enumerate(rows):
        # Open and resize the image
        img = Image.open(io.BytesIO(row[-1]))  
        img = img.resize((100, 100), PIL.Image.BILINEAR)
        img = ImageTk.PhotoImage(img)
        image_list.append(img)

        # Insert the row with the specified background color
        tree.insert("", "end", image=img, values=row[:-1], tags=("even_row" if i % 2 == 0 else "odd_row"))
        tree.tag_configure("even_row", background="LavenderBlush3")
        tree.tag_configure("odd_row", background="LavenderBlush4")
        
    update_compound_counts()

def update_compound_counts():
    # Count the total number of compounds in the database
    c.execute("SELECT COUNT(*) FROM Compounds")
    total_compounds = c.fetchone()[0]

    # Count the number of compounds remaining after applying the filter
    remaining_compounds = len(tree.get_children())

    # Update the labels displaying counts
    total_compounds_label.config(text=f"TOTAL COMPOUNDS: {total_compounds}")
    remaining_compounds_label.config(text=f"FILTERED COMPOUNDS: {remaining_compounds}")

# Button to apply custom filter
custom_filter_button = ttk.Button(button_frame, text="Apply Custom Filter", command=filter_custom)
custom_filter_button.grid(row=len(criteria_labels) +2, column=1, columnspan=5, padx = 10,pady=10)

# Create vertical and horizontal scrollbars
vertical_scrollbar = ttk.Scrollbar(column_frame, orient="vertical")
horizontal_scrollbar = ttk.Scrollbar(column_frame, orient="horizontal")

# Create the Treeview widget with vertical and horizontal scrollbars
tree = ttk.Treeview(column_frame, yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
vertical_scrollbar.config(command=tree.yview)
horizontal_scrollbar.config(command=tree.xview)

# Grid the widgets
tree.grid(row=0, column=0, sticky="nsew")
vertical_scrollbar.grid(row=0, column=1, sticky="ns")
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
column_frame.grid_columnconfigure(0, weight=1)
column_frame.grid_rowconfigure(0, weight=1)

# Tree
tree['columns'] = ('Name', 'MolWeight', 'RingCount', 'DonorCount', 'AcceptorCount', 'LogP', 'LogD', 'PSA', 'RotatableBonds', 'FAR', 'Refractivity', 'TotalAtoms')
tree.heading("#0", text="Structure")
tree.heading("Name", text="Name")
tree.heading("MolWeight", text="Molecular Weight")
tree.heading("RingCount", text="Ring Count")
tree.heading("DonorCount", text="Donors")
tree.heading("AcceptorCount", text="Acceptors")
tree.heading("LogP", text="LogP")
tree.heading("LogD", text="LogD")
tree.heading("PSA", text="PSA")
tree.heading("RotatableBonds", text="Rotatable Bonds")
tree.heading("FAR", text="FAR")
tree.heading("Refractivity", text="Refractivity")
tree.heading("TotalAtoms", text="TotalAtoms")


tree.grid(row=0, column=0, sticky="nsew")

tree.column("#0")
tree.column("Name", width=250) 
tree.column("MolWeight", width=120)
tree.column("RingCount", width=100)
tree.column("DonorCount", width=100)
tree.column("AcceptorCount", width=100)
tree.column("LogP", width=100)
tree.column("LogD", width=100)
tree.column("PSA", width=100)
tree.column("RotatableBonds", width=100)
tree.column("FAR", width=100)
tree.column("Refractivity", width=100)
tree.column("TotalAtoms", width=100)

for col in tree['columns']:
   tree.column(col, anchor='center')

# Initialize an empty list to store images
image_list = []

def populate_tree(where_clause=""):
    """
    Populate the treeview with compound data from the database.

    Parameters:
        where_clause (str): Optional WHERE clause for filtering data.

    Returns:
        tuple: A tuple containing the total number of compounds and the number of remaining compounds after applying the filter.
    """
    # Count the total number of compounds in the database
    c.execute("SELECT COUNT(*) FROM Compounds")
    total_compounds = c.fetchone()[0]
    
    # Execute the SQL query to fetch filtered data
    query = f'''SELECT Name, MolWeight, RingCount, DonorCount, AcceptorCount, LogP, LogD, 
                PSA, RotatableBonds, FAR, Refractivity, TotalAtoms, Image FROM Compounds'''
    
    if where_clause:
        query += f" WHERE {where_clause}"

    c.execute(query)
    rows = c.fetchall()

    # Clear the existing entries in the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Populate the treeview with the filtered data
    for i, row in enumerate(rows):
        # Open and resize the image
        img = Image.open(io.BytesIO(row[-1]))  
        img = img.resize((100, 100), PIL.Image.BILINEAR)
        img = ImageTk.PhotoImage(img)
        image_list.append(img)

        # Insert the row with the specified background color
        tree.insert("", "end", image=img, values=row[:-1], tags=("even_row" if i % 2 == 0 else "odd_row"))
        tree.tag_configure("even_row", background="LavenderBlush3")
        tree.tag_configure("odd_row", background="LavenderBlush4")

    # Count the number of compounds remaining after applying the filter
    c.execute(query)
    remaining_compounds = len(c.fetchall())

    # Return the counts
    return total_compounds, remaining_compounds

# Call populate_tree initially to display counts for all compounds
populate_tree()

# Create labels to display counts
total_compounds_label = ttk.Label(root, text="TOTAL COMPOUNDS: 0", font=('Times New Roman', 12))
total_compounds_label.place(x=500, y=25)
remaining_compounds_label = ttk.Label(root, text="FILTERED COMPOUNDS : 0", font=('Times New Roman', 12))
remaining_compounds_label.place(x=750, y=25)
style.configure("Compounds.TLabel", background="LavenderBlush3")

total_compounds_label.configure(style="Compounds.TLabel")
remaining_compounds_label.configure(style="Compounds.TLabel")

# List of columns with numeric values
numeric_columns = ['MolWeight', 'RingCount', 'DonorCount', 'AcceptorCount', 'LogP', 'LogD', 'PSA', 'RotatableBonds', 'FAR', 'Refractivity', 'TotalAtoms']

def sort_treeview(column):
    """
    Sort the Treeview widget based on the selected column.

    Parameters:
        column (str): The name of the column to sort by.
    """
    # Check if the column is a numeric column
    if column in numeric_columns:
        # Find the index of the column name
        column_index = tree['columns'].index(column)

        # Retrieve all items in the current column
        items = [(float(tree.item(child, 'values')[column_index]), child) for child in tree.get_children('')]

        # Sort the items based on the column values
        sorted_items = sorted(items, reverse=True, key=lambda x: x[0])

        # Move the items to their new positions
        for index, (value, child) in enumerate(sorted_items):
            tree.move(child, '', index)

        # Configure tags for even and odd rows
        tree.tag_configure("even_row", background="LavenderBlush3")
        tree.tag_configure("odd_row", background="LavenderBlush4")

        # Apply the tags to the rows after sorting
        for index, child in enumerate(tree.get_children('')):
            if index % 2 == 0:
                tree.item(child, tags=("even_row",))
            else:
                tree.item(child, tags=("odd_row",))

# Bind click events to the column headings to trigger sorting
for col in tree['columns']:
    tree.heading(col, text=col, command=lambda c=col: sort_treeview(c))  

# Function to update compound counts and populate tree
def update_and_populate(where_clause=""):
    """
    Update compound counts and repopulate the treeview with filtered data.

    Parameters:
        where_clause (str): Optional WHERE clause for filtering data.
    """
    total_compounds, remaining_compounds = populate_tree(where_clause)
    total_compounds_label.config(text=f"TOTAL COMPOUNDS: {total_compounds}")
    remaining_compounds_label.config(text=f"FILTERED COMPOUNDS: {remaining_compounds}")

def save_filtered_data():
    """Prompt the user to save the filtered data as a CSV file."""
    # Prompt the user to choose a file location for saving the CSV
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if filepath:
        print(f"File will be saved at: {filepath}")  # Print the file path to the console

        # Get the filtered data from the treeview
        data = []
        for child in tree.get_children():
            values = tree.item(child, "values")
            data.append(values)
        
        # Write the data to the CSV file
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "MolWeight", "RingCount", "DonorCount", "AcceptorCount", "LogP", "LogD",
                             "PSA", "RotatableBonds", "FAR", "Refractivity", "TotalAtoms"])
            writer.writerows(data)

save_button = ttk.Button(root, text="Save Filtered Data as CSV", command=save_filtered_data)
save_button.place(x=50, y=20)
style.configure("Savedata.TLabel", background="lavenderblush4")

# Modify filter functions to call update_and_populate
def filter_ghose_rule():
    """Apply Ghose Rule filter."""
    reset()
    update_and_populate('GhoseRule = 1')
    
    # Set the filter criteria values for Ghose Rule
    criteria_entries['MolWeight']['from'].insert(0, '160')
    criteria_entries['MolWeight']['to'].insert(0, '480')
    criteria_entries['LogP']['from'].insert(0, '-0.4')
    criteria_entries['LogP']['to'].insert(0, '5.6')
    criteria_entries['Refractivity']['from'].insert(0, '40')
    criteria_entries['Refractivity']['to'].insert(0, '130')
    criteria_entries['TotalAtoms']['from'].insert(0, '20')
    criteria_entries['TotalAtoms']['to'].insert(0, '70')

def filter_lipinski_rule():
    """Apply Lipinski Rule filter."""
    reset()
    update_and_populate('LipinskiRuleOfFive =1')
   
    criteria_entries['MolWeight']['from'].insert(0, '0')
    criteria_entries['DonorCount']['from'].insert(0, '0')
    criteria_entries['AcceptorCount']['from'].insert(0, '0')
    criteria_entries['MolWeight']['to'].insert(0, '500')
    criteria_entries['DonorCount']['to'].insert(0, '5')
    criteria_entries['AcceptorCount']['to'].insert(0, '10')
    criteria_entries['LogP']['to'].insert(0, '5')

def filter_bioavailability():
    """Apply Bioavailability filter."""
    reset() 
    update_and_populate("Bioavailability = 1")

    criteria_entries['MolWeight']['from'].insert(0, '0')
    criteria_entries['DonorCount']['from'].insert(0, '0')
    criteria_entries['AcceptorCount']['from'].insert(0, '0')
    criteria_entries['RotatableBonds']['from'].insert(0, '0')
    criteria_entries['PSA']['from'].insert(0, '0')
    criteria_entries['FAR']['from'].insert(0, '0')

    criteria_entries['MolWeight']['to'].insert(0, '500')
    criteria_entries['DonorCount']['to'].insert(0, '5')
    criteria_entries['AcceptorCount']['to'].insert(0, '10')
    criteria_entries['LogP']['to'].insert(0, '5')
    criteria_entries['RotatableBonds']['to'].insert(0, '10')
    criteria_entries['PSA']['to'].insert(0, '200')
    criteria_entries['FAR']['to'].insert(0, '5')

def filter_lead_likeness():
    """Apply Lead Likeness filter."""
    reset()
    update_and_populate("LeadLikeness = 1")
    
    criteria_entries['MolWeight']['from'].insert(0, '0')
    criteria_entries['MolWeight']['to'].insert(0, '450')
    criteria_entries['LogD']['from'].insert(0, '-4')
    criteria_entries['LogD']['to'].insert(0, '4')
    criteria_entries['RingCount']['from'].insert(0, '0')
    criteria_entries['DonorCount']['from'].insert(0, '0')
    criteria_entries['AcceptorCount']['from'].insert(0, '0')
    criteria_entries['RotatableBonds']['from'].insert(0, '0')
    criteria_entries['RingCount']['to'].insert(0, '4')
    criteria_entries['DonorCount']['to'].insert(0, '5')
    criteria_entries['AcceptorCount']['to'].insert(0, '8')
    criteria_entries['RotatableBonds']['to'].insert(0, '10')

def reset():
    """Reset all filter criteria."""
    # Clear all entry fields
    for criteria, entries in criteria_entries.items():
        entries['from'].delete(0, tk.END)
        entries['to'].delete(0, tk.END)

    # Apply the filter
    update_and_populate()
update_and_populate()

# Associate filtering functions with corresponding buttons
reset_button.config(command=reset)
ghose_rule_button.config(command=filter_ghose_rule)
lipinski_button.config(command=filter_lipinski_rule)
bioavailability_button.config(command=filter_bioavailability)
lead_likeness_button.config(command=filter_lead_likeness)

# Create a frame for the search box and search button
search_frame = ttk.Frame(root, style='Search.TFrame')
search_frame.place(x=1170, y=20, width=330, height=40)
search_frame.config(style="Compounds.TLabel")

search_box = ttk.Entry(search_frame, width=20)
search_box.grid(row=0, column=1, padx=(10, 10))

def search_compound():
    """Search for compounds by name."""
    search_query = search_box.get()
    if search_query:
        sql_query = f"""
            SELECT 
                Name, MolWeight, RingCount, DonorCount, AcceptorCount, LogP, LogD,
                PSA, RotatableBonds, FAR, Refractivity, TotalAtoms, Image 
            FROM 
                Compounds 
            WHERE 
                Name LIKE ?
        """
        c.execute(sql_query, ('%' + search_query + '%',))
        rows = c.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        # Populate the treeview with the filtered data
        for i, row in enumerate(rows):
            # Open and resize the image
            img = Image.open(io.BytesIO(row[-1]))  
            img = img.resize((100, 100), PIL.Image.BILINEAR)
            img = ImageTk.PhotoImage(img)
            image_list.append(img)

            # Insert the row with the specified background color
            tree.insert("", "end", image=img, values=row[:-1], tags=("even_row" if i % 2 == 0 else "odd_row"))
            tree.tag_configure("even_row", background="LavenderBlush3")
            tree.tag_configure("odd_row", background="LavenderBlush4")

# Button to apply search filter
search_button = ttk.Button(search_frame, text="Search Compound By Name", command=search_compound)
search_button.grid(row=0, column=2, padx=(10, 10))

root.mainloop()

conn.close()
