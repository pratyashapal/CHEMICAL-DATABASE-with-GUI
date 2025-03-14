Database Design and Implementation

Database Schema

The database is built using SQLite, with a table Compounds that holds the following columns:

ID: Unique identifier for each compound.

Name: Name of the compound.

SMILES: SMILES notation of the compound.

Molecular Weight, LogP, LogD, PSA: Key molecular properties.

Ring Count, Rotatable Bond Count: Structural features.

Lipinski’s Rule of Five, Bioavailability, Lead-likeness: Drug-likeness attributes.

Fused Aromatic Rings: Structural analysis of aromatic systems in the compound.

Images: PNG images representing the chemical structure.

The RDKit library was used to handle molecular structure data, compute molecular descriptors, and assess the drug-likeness of the compounds based on established rules like Lipinski’s Rule of Five and Ghose’s Rule.

Database Population

A script was developed to:

Parse an SDF file containing molecular structures.

Extract relevant descriptors using RDKit.

Assess compliance with predefined rules (Lipinski, Ghose).

Store the data in the SQLite database.

Graphical User Interface (GUI)

The GUI, built with Tkinter in Python, allows users to interact with the chemical compounds database efficiently. Key features include:

Filters: Predefined filters (e.g., Lipinski’s Rule, Bioavailability) and custom filters for properties like molecular weight and ring count.

Search: A search box to find compounds by name, supporting partial matches.

Sorting: Sort compounds based on properties like molecular weight, ring count, etc.

Export: Users can save filtered data as a CSV file for further analysis.

Treeview: Displays compounds in a dynamic table, updating in real-time based on the filters applied.
The GUI is designed to be intuitive and user-friendly, making it easy to explore and manipulate large chemical datasets.

