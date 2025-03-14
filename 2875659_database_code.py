# TASK 1: CREATING DATABASE

# Importing necessary libraries
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, Draw
import sqlite3
from PIL import Image
import io

# Establishing a connection to the SQLite database
conn = sqlite3.connect('C:/Users/Pratyasha/Downloads/chemical_compounds.db')
c = conn.cursor()

# Creating a table to store compound information if it doesn't exist already
c.execute('''CREATE TABLE IF NOT EXISTS Compounds
             (ID INTEGER PRIMARY KEY,
             Name TEXT,
             SMILES TEXT,
             MolWeight REAL,
             RingCount INTEGER,
             DonorCount INTEGER,
             AcceptorCount INTEGER,
             LogP REAL,
             LogD REAL,
             PSA REAL,
             RotatableBonds INTEGER,
             FAR INTEGER,
             Refractivity REAL,
             TotalAtoms INTEGER,
             LipinskiRuleOfFive BOOLEAN,
             Bioavailability BOOLEAN,
             LeadLikeness BOOLEAN,
             GhoseRule BOOLEAN,
             Image BLOB)''')

# Function to convert image to bytes
def image_to_bytes(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

# Function to count fused aromatic rings in a molecule
def count_fused_aromatic_ring(mol):
    rings = mol.GetRingInfo()
    aro_rings = mol.GetRingInfo().AtomRings()
    fused_aromatic_ring_count = 0
    aromatic_rings = []

    for i in range(rings.NumRings()):
        is_aromatic = False
        for atom_idx in aro_rings[i]:
            if mol.GetAtomWithIdx(atom_idx).GetIsAromatic():
                is_aromatic = True
                break
        if is_aromatic:
            aromatic_rings.append(i)

    for ring_idx in aromatic_rings:
        if rings.IsRingFused(ring_idx):
            fused_aromatic_ring_count += 1
    return fused_aromatic_ring_count

# Function to calculate Lipinski's rule of five
def calculate_lipinski_rule(mol):
    if Lipinski.NumHDonors(mol) <= 5 and Lipinski.NumHAcceptors(mol) <= 10 and Descriptors.MolWt(mol) <= 500 and Crippen.MolLogP(mol) <= 5:
        return True
    else:
        return False

# Function to calculate bioavailability
def calculate_bioavailability(mol):
    if Descriptors.MolWt(mol) <= 500 and Crippen.MolLogP(mol) <= 5 and Descriptors.NumHDonors(mol) <= 5 and Descriptors.NumHAcceptors(mol) <= 10 and Descriptors.NumRotatableBonds(mol) <= 10 and Descriptors.TPSA(mol) <= 200 and count_fused_aromatic_ring(mol) <= 5:
        return True
    else:
        return False

# Function to calculate lead likeness
def calculate_lead_likeness(mol):
    if Descriptors.MolWt(mol) < 450 and -4 <= float(mol.GetProp('LogD')) <= 4 and len(Chem.GetSymmSSSR(mol)) <= 4 and Descriptors.NumHDonors(mol) <= 5 and Descriptors.NumHAcceptors(mol) <= 8 and Descriptors.NumRotatableBonds(mol) <= 10:
        return True
    else:
        return False

# Function to calculate Ghose's rule
def calculate_ghose_rule(mol):
    if 480 > Descriptors.MolWt(mol) > 160 and 5.6 > Crippen.MolLogP(mol) > -0.4 and 130 > Descriptors.MolMR(mol) > 40 and 70 > mol.GetNumAtoms() > 20:
        return True
    else:
        return False

# Function to parse and populate the database with compound information from an SDF file
def parse_and_populate(sdf_file):
    suppl = Chem.SDMolSupplier(sdf_file)
    for idx, mol in enumerate(suppl, start=1):
        if mol is not None:
            name = mol.GetProp('Name')  
            smiles = Chem.MolToSmiles(mol)
            mol_weight = round(Descriptors.MolWt(mol), 2)
            ring_count = len(Chem.GetSymmSSSR(mol))  
            donor_count = Descriptors.NumHDonors(mol)  
            acceptor_count = Descriptors.NumHAcceptors(mol) 
            logp = round(Chem.Crippen.MolLogP(mol), 2)
            logd = mol.GetProp('LogD')
            polar_surface_area = round(Descriptors.TPSA(mol), 2)
            rotatable_bond_count = Descriptors.NumRotatableBonds(mol)  
            fused_aromatic_ring_count = count_fused_aromatic_ring(mol)
            refrac = round(Descriptors.MolMR(mol), 2)
            total_atoms = mol.GetNumAtoms()
            lipinski_rule = calculate_lipinski_rule(mol)
            bioavailability = calculate_bioavailability(mol)
            lead_likeness = calculate_lead_likeness(mol)
            ghose_rule = calculate_ghose_rule(mol)
            
            img = Chem.Draw.MolToImage(mol, size=(300, 300))
            img_bytes = image_to_bytes(img)
            
            c.execute('''INSERT INTO Compounds (ID, Name, SMILES, MolWeight, RingCount, DonorCount, AcceptorCount, LogP, LogD, PSA, RotatableBonds, FAR, Refractivity, TotalAtoms,  LipinskiRuleOfFive, Bioavailability, LeadLikeness, GhoseRule, Image)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)''',
                      (idx, name, smiles, mol_weight, ring_count, donor_count, acceptor_count, logp, logd, polar_surface_area, rotatable_bond_count, fused_aromatic_ring_count, refrac, total_atoms, lipinski_rule, bioavailability, lead_likeness, ghose_rule, img_bytes))
        else:
            print(f"Error parsing molecule at index {idx}")

# Path to the SDF file containing compound information
sdf_file = "C:/Users/Pratyasha/Downloads/Molecules14.sdf"

# Parsing and populating the database
parse_and_populate(sdf_file)

# Committing changes to the database and closing the connection
conn.commit()
conn.close()
