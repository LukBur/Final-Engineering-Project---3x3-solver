cube = {
    "U": [["white"] * 3 for _ in range(3)],
    "L": [["orange"] * 3 for _ in range(3)],
    "F": [["green"] * 3 for _ in range(3)],
    "R": [["red"] * 3 for _ in range(3)],
    "B": [["blue"] * 3 for _ in range(3)],
    "D": [["yellow"] * 3 for _ in range(3)],
}

corners = {
    "UFR": [("U", 2, 2), ("F", 0, 2), ("R", 0, 0)],
    "UFL": [("U", 2, 0), ("F", 0, 0), ("L", 0, 2)],
    "UBL": [("U", 0, 0), ("B", 0, 2), ("L", 0, 0)],
    "UBR": [("U", 0, 2), ("B", 0, 0), ("R", 0, 2)],
    "DFR": [("D", 0, 2), ("F", 2, 2), ("R", 2, 0)],
    "DFL": [("D", 0, 0), ("F", 2, 0), ("L", 2, 2)],
    "DBL": [("D", 2, 0), ("B", 2, 2), ("L", 2, 0)],
    "DBR": [("D", 2, 2), ("B", 2, 0), ("R", 2, 2)],
}

correct_corners = {
    "UFR": {"white", "green", "red"},
    "UFL": {"white", "green", "orange"},
    "UBL": {"white", "blue", "orange"},
    "UBR": {"white", "blue", "red"},
    "DFR": {"yellow", "green", "red"},
    "DFL": {"yellow", "green", "orange"},
    "DBL": {"yellow", "blue", "orange"},
    "DBR": {"yellow", "blue", "red"},
}

edges = {
    "UF": [("U", 2, 1), ("F", 0, 1)],
    "UL": [("U", 1, 0), ("L", 0, 1)],
    "UR": [("U", 1, 2), ("R", 0, 1)],
    "UB": [("U", 0, 1), ("B", 0, 1)],
    "DF": [("D", 0, 1), ("F", 2, 1)],
    "DL": [("D", 1, 0), ("L", 2, 1)],
    "DR": [("D", 1, 2), ("R", 2, 1)],
    "DB": [("D", 2, 1), ("B", 2, 1)],
    "FL": [("F", 1, 0), ("L", 1, 2)],
    "FR": [("F", 1, 2), ("R", 1, 0)],
    "BL": [("B", 1, 2), ("L", 1, 0)],
    "BR": [("B", 1, 0), ("R", 1, 2)],
}

correct_edges = {
    "UF": {"white", "green"},
    "UL": {"white", "orange"},
    "UR": {"white", "red"},
    "UB": {"white", "blue"},
    "DF": {"yellow", "green"},
    "DL": {"yellow", "orange"},
    "DR": {"yellow", "red"},
    "DB": {"yellow", "blue"},
    "FL": {"green", "orange"},
    "FR": {"green", "red"},
    "BL": {"blue", "orange"},
    "BR": {"blue", "red"},
}
