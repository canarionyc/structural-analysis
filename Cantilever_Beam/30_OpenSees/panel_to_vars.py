# Create a safe dictionary to hold the panel's variables
config = {}

# Execute the raw text from the panel as Python code
exec(panel_text, {}, config)

# Push the variables to the Grasshopper component outputs
E = config['E']
G = config['G']
A = config['A']
Iy = config['Iy']
Iz = config['Iz']
J = config['J']
