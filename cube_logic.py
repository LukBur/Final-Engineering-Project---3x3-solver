# cube_logic.py
import random
from cube_data import cube, corners, edges, correct_corners, correct_edges
import time
import cube_solver as solver
import copy


def get_corner_colors(name):
    stickers = [name]
    for face, row, col in corners[name]:
        stickers.append(cube[face][row][col])
    return stickers


def is_solved():
    for face in cube:
        color = cube[face][0][0]
        for row in cube[face]:
            for cell in row:
                if cell != color:
                    return False
    return True


def rotate_U():
    cube["U"] = [list(row) for row in zip(*cube["U"][::-1])]
    temp = cube["F"][0].copy()
    cube["F"][0], cube["R"][0], cube["B"][0], cube["L"][0] = (
        cube["R"][0],
        cube["B"][0],
        cube["L"][0],
        temp,
    )
    global movecount
    movecount += 1


def rotate_U_prime():
    cube["U"] = [list(row) for row in zip(*cube["U"])][::-1]
    temp = cube["F"][0].copy()
    cube["F"][0], cube["L"][0], cube["B"][0], cube["R"][0] = (
        cube["L"][0],
        cube["B"][0],
        cube["R"][0],
        temp,
    )
    global movecount
    movecount += 1


def rotate_D():
    cube["D"] = [list(row) for row in zip(*cube["D"][::-1])]
    temp = cube["F"][2].copy()
    cube["F"][2], cube["L"][2], cube["B"][2], cube["R"][2] = (
        cube["L"][2],
        cube["B"][2],
        cube["R"][2],
        temp,
    )
    global movecount
    movecount += 1


def rotate_D_prime():
    cube["D"] = [list(row) for row in zip(*cube["D"])][::-1]
    temp = cube["F"][2].copy()
    cube["F"][2], cube["R"][2], cube["B"][2], cube["L"][2] = (
        cube["R"][2],
        cube["B"][2],
        cube["L"][2],
        temp,
    )
    global movecount
    movecount += 1


def rotate_L():
    cube["L"] = [list(row) for row in zip(*cube["L"][::-1])]
    temp = [cube["U"][i][0] for i in range(3)]
    for i in range(3):
        cube["U"][i][0] = cube["B"][2 - i][2]
        cube["B"][2 - i][2] = cube["D"][i][0]
        cube["D"][i][0] = cube["F"][i][0]
        cube["F"][i][0] = temp[i]
    global movecount
    movecount += 1


def rotate_L_prime():
    cube["L"] = [list(row) for row in zip(*cube["L"])][::-1]
    temp = [cube["U"][i][0] for i in range(3)]
    for i in range(3):
        cube["U"][i][0] = cube["F"][i][0]
        cube["F"][i][0] = cube["D"][i][0]
        cube["D"][i][0] = cube["B"][2 - i][2]
        cube["B"][2 - i][2] = temp[i]
    global movecount
    movecount += 1


def rotate_R():
    cube["R"] = [list(row) for row in zip(*cube["R"][::-1])]
    temp = [cube["U"][i][2] for i in range(3)]
    for i in range(3):
        cube["U"][i][2] = cube["F"][i][2]
        cube["F"][i][2] = cube["D"][i][2]
        cube["D"][i][2] = cube["B"][2 - i][0]
        cube["B"][2 - i][0] = temp[i]
    global movecount
    movecount += 1


def rotate_R_prime():
    cube["R"] = [list(row) for row in zip(*cube["R"])][::-1]
    temp = [cube["U"][i][2] for i in range(3)]
    for i in range(3):
        cube["U"][i][2] = cube["B"][2 - i][0]
        cube["B"][2 - i][0] = cube["D"][i][2]
        cube["D"][i][2] = cube["F"][i][2]
        cube["F"][i][2] = temp[i]
    global movecount
    movecount += 1


def rotate_F():
    cube["F"] = [list(row) for row in zip(*cube["F"][::-1])]
    temp = cube["U"][2].copy()
    cube["U"][2] = [cube["L"][2 - i][2] for i in range(3)]
    for i in range(3):
        cube["L"][i][2] = cube["D"][0][i]
    cube["D"][0] = [cube["R"][2 - i][0] for i in range(3)]
    for i in range(3):
        cube["R"][i][0] = temp[i]
    global movecount
    movecount += 1


def rotate_F_prime():
    cube["F"] = [list(row) for row in zip(*cube["F"])][::-1]
    temp = cube["U"][2].copy()
    cube["U"][2] = [cube["R"][i][0] for i in range(3)]
    for i in range(3):
        cube["R"][i][0] = cube["D"][0][2 - i]
    cube["D"][0] = [cube["L"][i][2] for i in range(3)]
    for i in range(3):
        cube["L"][i][2] = temp[2 - i]
    global movecount
    movecount += 1


def rotate_B():
    cube["B"] = [list(row) for row in zip(*cube["B"][::-1])]
    temp = cube["U"][0].copy()
    cube["U"][0] = [cube["R"][i][2] for i in range(3)]
    for i in range(3):
        cube["R"][i][2] = cube["D"][2][2 - i]
    cube["D"][2] = [cube["L"][i][0] for i in range(3)]
    for i in range(3):
        cube["L"][i][0] = temp[2 - i]
    global movecount
    movecount += 1


def rotate_B_prime():
    cube["B"] = [list(row) for row in zip(*cube["B"])][::-1]
    temp = cube["U"][0].copy()
    cube["U"][0] = [cube["L"][2 - i][0] for i in range(3)]
    for i in range(3):
        cube["L"][i][0] = cube["D"][2][i]
    cube["D"][2] = [cube["R"][2 - i][2] for i in range(3)]
    for i in range(3):
        cube["R"][i][2] = temp[i]
    global movecount
    movecount += 1


# --- Złożone rotacje (2 i osie) ---
def rotate_U2():
    rotate_U()
    rotate_U()
    global movecount
    movecount -= 1


def rotate_D2():
    rotate_D()
    rotate_D()
    global movecount
    movecount -= 1


def rotate_L2():
    rotate_L()
    rotate_L()
    global movecount
    movecount -= 1


def rotate_R2():
    rotate_R()
    rotate_R()
    global movecount
    movecount -= 1


def rotate_F2():
    rotate_F()
    rotate_F()
    global movecount
    movecount -= 1


def rotate_B2():
    rotate_B()
    rotate_B()
    global movecount
    movecount -= 1


def rotate_x():
    cube["U"], cube["F"], cube["D"], cube["B"] = (
        cube["F"],
        cube["D"],
        cube["B"],
        cube["U"],
    )
    cube["L"] = [list(row) for row in zip(*cube["L"])][::-1]
    cube["R"] = [list(row) for row in zip(*cube["R"][::-1])]
    for f in ["D", "B"]:
        cube[f] = [r[::-1] for r in cube[f][::-1]]


def rotate_x_prime():
    cube["U"], cube["F"], cube["D"], cube["B"] = (
        cube["B"],
        cube["U"],
        cube["F"],
        cube["D"],
    )
    cube["L"] = [list(row) for row in zip(*cube["L"][::-1])]
    cube["R"] = [list(row) for row in zip(*cube["R"])][::-1]
    for f in ["U", "B"]:
        cube[f] = [r[::-1] for r in cube[f][::-1]]


def rotate_y():
    cube["F"], cube["R"], cube["B"], cube["L"] = (
        cube["R"],
        cube["B"],
        cube["L"],
        cube["F"],
    )
    cube["U"] = [list(row) for row in zip(*cube["U"][::-1])]
    cube["D"] = [list(row) for row in zip(*cube["D"])][::-1]


def rotate_y_prime():
    cube["F"], cube["R"], cube["B"], cube["L"] = (
        cube["L"],
        cube["F"],
        cube["R"],
        cube["B"],
    )
    cube["U"] = [list(row) for row in zip(*cube["U"])][::-1]
    cube["D"] = [list(row) for row in zip(*cube["D"][::-1])]


def rotate_z():
    cube["U"], cube["R"], cube["D"], cube["L"] = (
        cube["L"],
        cube["U"],
        cube["R"],
        cube["D"],
    )
    cube["F"] = [list(row) for row in zip(*cube["F"][::-1])]
    cube["B"] = [list(row) for row in zip(*cube["B"])][::-1]
    for f in ["U", "D", "R", "L"]:
        cube[f] = [list(row) for row in zip(*cube[f][::-1])]


def rotate_z_prime():
    cube["U"], cube["R"], cube["D"], cube["L"] = (
        cube["R"],
        cube["D"],
        cube["L"],
        cube["U"],
    )
    cube["F"] = [list(row) for row in zip(*cube["F"])][::-1]
    cube["B"] = [list(row) for row in zip(*cube["B"][::-1])]
    for f in ["U", "D", "R", "L"]:
        cube[f] = [list(row) for row in zip(*cube[f])][::-1]


moves_list = [
    rotate_U,
    rotate_U_prime,
    rotate_L,
    rotate_L_prime,
    rotate_F,
    rotate_F_prime,
    rotate_R,
    rotate_R_prime,
    rotate_B,
    rotate_B_prime,
    rotate_D,
    rotate_D_prime,
]

# used only in scramble_logic
notation_map = {
    0: {
        rotate_U: "U",
        rotate_U_prime: "U'",
        rotate_U2: "U2",
        rotate_D: "D",
        rotate_D_prime: "D'",
        rotate_D2: "D2",
    },
    1: {
        rotate_L: "L",
        rotate_L_prime: "L'",
        rotate_L2: "L2",
        rotate_R: "R",
        rotate_R_prime: "R'",
        rotate_R2: "R2",
    },
    2: {
        rotate_F: "F",
        rotate_F_prime: "F'",
        rotate_F2: "F2",
        rotate_B: "B",
        rotate_B_prime: "B'",
        rotate_B2: "B2",
    },
}

mod3moves = []

scramble_sequence = []
solve_sequence = []
movecount = 0


def scramble_logic(num_moves=20, scramble=""):
    global scramble_sequence
    scramble_sequence = []

    global solve_sequence
    solve_sequence = []

    if scramble != "":
        return scramble

    iterator = 0

    # possible_moves = list(notation_map.keys())
    solver.fix_cube_orientation()
    for _ in range(num_moves):
        i = iterator % 3
        move_func = random.choice(list(notation_map[i].keys()))
        move_func()

        scramble_sequence.append(notation_map[i][move_func])
        iterator += 1
    result = " ".join(scramble_sequence)

    global movecount
    movecount = 0

    # print(f"Scramble: {result}")
    return result


def execute(sequence):
    m_map = {
        "U": rotate_U,
        "U'": rotate_U_prime,
        "U2": rotate_U2,
        "D": rotate_D,
        "D'": rotate_D_prime,
        "D2": rotate_D2,
        "L": rotate_L,
        "L'": rotate_L_prime,
        "L2": rotate_L2,
        "R": rotate_R,
        "R'": rotate_R_prime,
        "R2": rotate_R2,
        "F": rotate_F,
        "F'": rotate_F_prime,
        "F2": rotate_F2,
        "B": rotate_B,
        "B'": rotate_B_prime,
        "B2": rotate_B2,
        "x": rotate_x,
        "x'": rotate_x_prime,
        "y": rotate_y,
        "y'": rotate_y_prime,
        "z": rotate_z,
        "z'": rotate_z_prime,
    }
    for move in sequence.split():
        if move in m_map:
            m_map[move]()
            solve_sequence.append(move)


def get_physical_edge_colors(edge_name):
    pos = edges[edge_name]
    return {
        cube[pos[0][0]][pos[0][1]][pos[0][2]],
        cube[pos[1][0]][pos[1][1]][pos[1][2]],
    }


def get_physical_corner_colors(corner_name):
    pos = corners[corner_name]
    return {
        cube[pos[0][0]][pos[0][1]][pos[0][2]],
        cube[pos[1][0]][pos[1][1]][pos[1][2]],
        cube[pos[2][0]][pos[2][1]][pos[2][2]],
    }


def find_edge_position(target_colors):
    for name in edges:
        if get_physical_edge_colors(name) == target_colors:
            return name
    return None


def find_corner_position(target_colors):
    for name in corners:
        if get_physical_corner_colors(name) == target_colors:
            return name
    return None


CROSS_ORDER = [
    {"white", "green"},  # UF
    {"white", "orange"},  # UL
    {"white", "blue"},  # UB
    {"white", "red"},  # UR
]

CORNERS_ORDER = [
    {"white", "green", "red"},  # UFR
    {"white", "green", "orange"},  # UFL
    {"white", "blue", "orange"},  # UBL
    {"white", "blue", "red"},  # UBR
]

F2L_ORDER = [
    {"green", "red"},  # FR
    {"green", "orange"},  # FL
    {"blue", "orange"},  # BL
    {"blue", "red"},  # BR
]


def is_corner_fully_solved(corner_name):
    for face, r, c in corners[corner_name]:
        sticker_color = cube[face][r][c]
        center_color = cube[face][1][1]

        if sticker_color != center_color:
            return False
    return True


def is_edge_fully_solved(edge_name):
    for face, r, c in edges[edge_name]:
        sticker_color = cube[face][r][c]
        center_color = cube[face][1][1]

        if sticker_color != center_color:
            return False
    return True


def run_statistical_comparison(n=100):
    global cube
    results = {"LBL": [], "CFOP": [], "CFOP_wins": 0, "LBL_wins": 0, "Ties": 0}

    for _ in range(n):
        # 1. Generujemy scramble
        scramble_logic()
        scramble_state = copy.deepcopy(cube)

        # 2. Testujemy LBL
        global solve_sequence
        solve_sequence = []
        solver.solve_cube_LBL()
        lbl_count = len(solve_sequence)
        results["LBL"].append(lbl_count)

        # Przywracamy stan kostki
        cube = copy.deepcopy(scramble_state)

        # 3. Testujemy CFOP
        solve_sequence.clear()
        solver.solve_cube_CFOP()
        cfop_count = len(solve_sequence)
        results["CFOP"].append(cfop_count)

        # 4. Porównujemy
        if cfop_count < lbl_count:
            results["CFOP_wins"] += 1
        elif lbl_count < cfop_count:
            results["LBL_wins"] += 1
        else:
            results["Ties"] += 1

    return results
