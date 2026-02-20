import xml.etree.ElementTree as ET

# Create the root element
root = ET.Element("GasDeliverySystem")

# --- Gas Delivery Units ---
gas_units = ET.SubElement(root, "GasDeliveryUnits")

# Define each unit
unit1 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF1", "unit_type": "hopper", "description": "Powder feeder hopper 1"})
unit2 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF2", "unit_type": "hopper", "description": "Powder feeder hopper 2"})
unit3 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF3", "unit_type": "hopper", "description": "Powder feeder hopper 3"})
unit4 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "PF4", "unit_type": "hopper", "description": "Powder feeder hopper 4"})
unit5 = ET.SubElement(gas_units, "Unit", attrib={"unit_id": "CP1", "unit_type": "center_purge_line", "description": "Central purge argon supply line"})

# --- Parameters for PF1 ---
pf1_params = ET.SubElement(unit1, "Parameters")
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 RPM"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Argon MFlow"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Powder Low"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Bottom Pressure"})
ET.SubElement(pf1_params, "Parameter", attrib={"name": "PF1 Argon: Warning High Level"})

# --- Parameters for Center Purge Line ---
cp_params = ET.SubElement(unit5, "Parameters")
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon MFlow"})
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon: Warning High Level"})
ET.SubElement(cp_params, "Parameter", attrib={"name": "Center Purge Argon VFlow"})

# --- Generate XML string ---
tree = ET.ElementTree(root)
tree.write("gas_delivery_ontology.xml", encoding="utf-8", xml_declaration=True)

# Optional: print it nicely
ET.indent(tree, space="  ")
tree.write("gas_delivery_ontology_pretty.xml", encoding="utf-8", xml_declaration=True)

print(tree)

#%%

from IPython.display import display

display(RPM_data.head(10))
display(argon_data.head(10))
display(hopper_warnings.head(10))

#%%

import pandas as pd

all_parameters = pd.concat([RPM_data, hopper_warnings, powder_data, pressure_data, argon_data], ignore_index=True)
all_parameters["subsystem"] = all_parameters["parameter_name"].str.extract(r"(RPM|Argon|Powder|Pressure|Warning|Alarm)")
pivoted = all_parameters.pivot_table(index="unit_id", columns="subsystem", values="parameter_name", aggfunc=lambda x: ", ".join(x))
display(pivoted)

#%%

from anytree import Node, RenderTree

# Create root
root = Node("Gas Delivery Units")

# Create child nodes
for unit in gas_delivery_units["unit_id"]:
    Node(unit, parent=root)

# Print tree
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")

#%%

#entity realtion diagram. use when hierarchy structure is done

'''graph ER {
	fontname="Helvetica,Arial,sans-serif"
	node [fontname="Helvetica,Arial,sans-serif"]
	edge [fontname="Helvetica,Arial,sans-serif"]
	layout=neato
	node [shape=box]; course; institute; student;
	node [shape=ellipse]; {node [label="name"] name0; name1; name2;}
		code; grade; number;
	node [shape=diamond,style=filled,color=lightgrey]; "C-I"; "S-C"; "S-I";

	name0 -- course;
	code -- course;
	course -- "C-I" [label="n",len=1.00];
	"C-I" -- institute [label="1",len=1.00];
	institute -- name1;
	institute -- "S-I" [label="1",len=1.00];
	"S-I" -- student [label="n",len=1.00];
	student -- grade;
	student -- name2;
	student -- number;
	student -- "S-C" [label="m",len=1.00];
	"S-C" -- course [label="n",len=1.00];

	label = "\n\nEntity Relation Diagram\ndrawn by NEATO";
	fontsize=20;
}'''