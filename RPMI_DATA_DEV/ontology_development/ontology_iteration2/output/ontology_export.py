import networkx as nx

NODE_TYPES = [
    "build",
    "material",
    "system",
    "process",
    "part",
    "person",
    "organization",
    "tic",
    "sensor",
    "parameter"
]

EDGE_TYPES = [
    "uses_material",
    "produced_by",
    "executed_on_system",
    "has_process",
    "has_part",
    "generated_observation",
    "has_parameter",
    "operated_by",
    "belongs_to_org"
] 


def build_am_graph(
    build_df,
    material_df,
    system_df,
    process_df,
    tic_df,
    part_df,
    person_df
):

    G = nx.DiGraph()

    # -------------------------
    # 1. BUILD NODES
    # -------------------------

    for _, row in build_df.iterrows():
        G.add_node(row["build_id"], type="build")

    for _, row in material_df.iterrows():
        G.add_node(row["material_id"], type="material")

    for _, row in system_df.iterrows():
        G.add_node(row["system_id"], type="system")

    for _, row in process_df.iterrows():
        G.add_node(row["parameter_id"], type="parameter")

    for _, row in part_df.iterrows():
        G.add_node(row["built_part_id"], type="part")

    for _, row in person_df.iterrows():
        G.add_node(row["person_id"], type="person")

    for _, row in tic_df.iterrows():
        G.add_node(row["observation_id"], type="tic")

    # -------------------------
    # 2. CORE EDGES (ASTM backbone)
    # -------------------------

    # BUILD → MATERIAL
    for _, row in build_df.iterrows():
        for m in row.get("material_ids", []):
            G.add_edge(row["build_id"], m, relation="uses_material")

    # BUILD → SYSTEM
    for _, row in build_df.iterrows():
        G.add_edge(row["build_id"], row["am_system_id"], relation="executed_on_system")

    # BUILD → PART
    for _, row in part_df.iterrows():
        G.add_edge(row["build_id"], row["built_part_id"], relation="has_part")

    # PART → MATERIAL
    for _, row in part_df.iterrows():
        G.add_edge(row["built_part_id"], row["material_id"], relation="made_of")

    # PART → PROCESS
    for _, row in part_df.iterrows():
        G.add_edge(row["built_part_id"], row["process_sequence_id"], relation="has_process")

    # TIC → BUILD + SYSTEM
    for _, row in tic_df.iterrows():
        G.add_edge(row["observation_id"], row["build_id"], relation="generated_during")
        G.add_edge(row["observation_id"], row["system_id"], relation="measured_by")

    # PROCESS → SYSTEM
    for _, row in process_df.iterrows():
        G.add_edge(row["parameter_id"], row["system_id"], relation="parameter_of")

    return G


def validate_graph(G):

    required_nodes = {"build", "material", "system"}

    node_types = {data["type"] for _, data in G.nodes(data=True)}

    missing = required_nodes - node_types

    if missing:
        raise ValueError(f"Missing required node types: {missing}")

    print("Graph validation passed.")