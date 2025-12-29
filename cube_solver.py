import cube_logic as logic
import json
import time


def load_algs():
    with open("steps.json", "r", encoding="utf-8") as f:
        return json.load(f)


ALGS = load_algs()

CROSS_STEPS = [
    ({"white", "green"}, "UF"),
    ({"white", "red"}, "UR"),
    ({"white", "blue"}, "UB"),
    ({"white", "orange"}, "UL"),
]

WHITE_CORNERS_STEPS = [
    ({"white", "green", "orange"}, "DFL"),
    ({"white", "blue", "orange"}, "DBL"),
    ({"white", "blue", "red"}, "DBR"),
    ({"white", "green", "red"}, "DFR"),
]

F2L_EDGES = [
    ({"green", "orange"}, "FR"),
    ({"blue", "orange"}, "BR"),
    ({"blue", "red"}, "BL"),
    ({"green", "red"}, "FL"),
]

YELLOW_EDGES = [
    ({"yellow", "orange"}, "UR"),
    ({"yellow", "blue"}, "UB"),
    ({"yellow", "red"}, "UL"),
    ({"yellow", "green"}, "UF"),
]

YELLOW_CORNERS = [
    ({"yellow", "green", "red"}, "UFR"),
    ({"yellow", "red", "blue"}, "UBR"),
    ({"yellow", "blue", "orange"}, "UBL"),
    ({"yellow", "orange", "green"}, "UFL"),
]

preauf = ""

METHOD = "LBL"


def fix_cube_orientation():
    if logic.cube["D"][1][1] == "white":
        logic.execute("x")
        logic.execute("x")
    elif logic.cube["F"][1][1] == "white":
        logic.execute("x")
    elif logic.cube["B"][1][1] == "white":
        logic.execute("x'")
    elif logic.cube["L"][1][1] == "white":
        logic.execute("z")
    elif logic.cube["R"][1][1] == "white":
        logic.execute("z'")

    if logic.cube["B"][1][1] == "green":
        logic.execute("y")
        logic.execute("y")
    elif logic.cube["R"][1][1] == "green":
        logic.execute("y")
    elif logic.cube["L"][1][1] == "green":
        logic.execute("y'")


def solve_cross():
    alg = []
    fix_cube_orientation()
    for colors, spot in CROSS_STEPS:
        pos = logic.find_edge_position(colors)
        move = ALGS[METHOD]["cross_setup"][pos]

        logic.execute(move)
        alg.extend(move.split())

        if not logic.is_edge_fully_solved("UF"):
            logic.execute("F U' R U")
            alg.extend("F U' R U".split())

        logic.execute("y")
        alg.append("\n y")
    alg.append("z")
    alg.append("z")
    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(f"SCRAMBLE: {' '.join(logic.scramble_sequence)}\n")
        f.write(f"CROSS: \n {' '.join(alg)}\n")

    logic.execute("z")
    logic.execute("z")


def solve_f2l_corners():
    alg = []

    for colors, spot in WHITE_CORNERS_STEPS:
        pos = logic.find_corner_position(colors)
        move = ALGS[METHOD]["corners"][pos]
        # print(pos)
        logic.execute(move)
        alg.extend(move.split())
        while not logic.is_corner_fully_solved("DFR"):
            logic.execute("R U R' U'")
            alg.extend("R U R' U'".split())
        logic.execute("y")
        alg.append("\n y")
    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"F2L Corners: {' '.join(alg)}\n")


def solve_f2l_edges():
    alg = []

    for colors, spot in F2L_EDGES:
        pos = logic.find_edge_position(colors)
        # print(pos)
        move = ALGS[METHOD]["f2l_edges"][pos]
        logic.execute(move)
        alg.extend(move.split())
        if logic.find_edge_position(colors) == "UF":
            logic.execute(ALGS[METHOD]["f2l_edges"]["UF"])
            alg.extend(ALGS[METHOD]["f2l_edges"]["UF"].split())
        if not logic.is_edge_fully_solved("FR"):
            logic.execute(ALGS[METHOD]["f2l_edges"]["SWAP"])
            alg.extend(ALGS[METHOD]["f2l_edges"]["SWAP"].split())
        logic.execute("y")
        alg.append("\n y")
    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"F2L Edges: {' '.join(alg)}\n")


f2l_alg = []


def solve_F2L():
    count = 0
    for (corner_colors, c_spot), (edge_colors, e_spot) in zip(
        WHITE_CORNERS_STEPS, F2L_EDGES
    ):
        alg = []
        corner_pos = logic.find_corner_position(corner_colors)
        move = ALGS[METHOD]["corners"][corner_pos]
        logic.execute(move)
        alg.extend(move.split())

        edge_pos = logic.find_edge_position(edge_colors)
        move = ALGS[METHOD]["edges"][edge_pos]
        logic.execute(move)
        alg.extend(move.split())

        f2l_algs = ALGS["CFOP"]["F2L"]

        if logic.cube["F"][0][2] == "white":
            if logic.cube["U"][1][0] == logic.cube["F"][1][1]:
                logic.execute(f2l_algs["1F"])
                alg.extend(f2l_algs["1F"].split())
            else:
                logic.execute(f2l_algs["0F"])
                alg.extend((f2l_algs["0F"]).split())
        elif logic.cube["U"][2][2] == "white":
            if logic.cube["U"][1][0] == logic.cube["F"][1][1]:
                logic.execute(f2l_algs["1U"])
                alg.extend(f2l_algs["1U"].split())
            else:
                logic.execute(f2l_algs["0U"])
                alg.extend((f2l_algs["0U"]).split())
        else:
            if logic.cube["U"][1][0] == logic.cube["F"][1][1]:
                logic.execute(f2l_algs["1R"])
                alg.extend((f2l_algs["1R"]).split())
            else:
                logic.execute(f2l_algs["0R"])
                alg.extend((f2l_algs["0R"]).split())
        count += 1
        logic.execute("y")
        alg.append("y")
        with open("recons.txt", "a", encoding="utf-8") as f:
            f.write(f"Pair {count}: {' '.join(alg)}\n")


def yellow_edge_orientation():
    yellow_up = {
        "UB": logic.cube["U"][0][1] == "yellow",
        "UL": logic.cube["U"][1][0] == "yellow",
        "UF": logic.cube["U"][2][1] == "yellow",
        "UR": logic.cube["U"][1][2] == "yellow",
    }

    global preauf
    count = sum(yellow_up.values())

    if count == 4:
        return "CROSS"
    if count == 0:
        return "DOT"

    if yellow_up["UL"] and yellow_up["UR"]:
        return "BELT"
    if yellow_up["UF"] and yellow_up["UB"]:
        logic.execute("U")
        preauf = "U"
        return "BELT"

    if yellow_up["UB"] and yellow_up["UL"]:
        return "L_SHAPE"
    if yellow_up["UL"] and yellow_up["UF"]:
        logic.execute("U")
        preauf = "U"
        return "L_SHAPE"
    if yellow_up["UF"] and yellow_up["UR"]:
        logic.execute("U2")
        preauf = "U2"
        return "L_SHAPE"
    if yellow_up["UR"] and yellow_up["UB"]:
        logic.execute("U'")
        preauf = "U'"
        return "L_SHAPE"


def is_yellow_face_solved():
    for row in logic.cube["U"]:
        for sticker in row:
            if sticker != "yellow":
                return False
    return True


# LBL METHOD
def eo():
    alg = []
    shape = yellow_edge_orientation()
    alg.append(preauf)
    alg.extend(ALGS[METHOD]["last_layer"][yellow_edge_orientation()].split())
    logic.execute(ALGS[METHOD]["last_layer"][yellow_edge_orientation()])

    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"Yellow cross: {' '.join(alg)}\n")


def coll():
    global preauf
    alg = []
    while not is_yellow_face_solved():
        if (
            logic.cube["B"][0][0] == "yellow"
            and logic.cube["B"][0][2] == "yellow"
            and logic.cube["U"][2][2] == "yellow"
            and logic.cube["U"][2][0] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["U"])
            alg.extend(ALGS[METHOD]["OLL"]["U"].split())

        elif (
            logic.cube["F"][0][0] == "yellow"
            and logic.cube["F"][0][2] == "yellow"
            and logic.cube["B"][0][0] == "yellow"
            and logic.cube["B"][0][2] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["H"])
            alg.extend(ALGS[METHOD]["OLL"]["H"].split())

        elif (
            logic.cube["F"][0][2] == "yellow"
            and logic.cube["B"][0][0] == "yellow"
            and logic.cube["L"][0][0] == "yellow"
            and logic.cube["L"][0][2] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["PI"])
            alg.extend(ALGS[METHOD]["OLL"]["PI"].split())

        elif (
            logic.cube["F"][0][0] == "yellow"
            and logic.cube["B"][0][2] == "yellow"
            and logic.cube["U"][0][2] == "yellow"
            and logic.cube["U"][2][2] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["T"])
            alg.extend(ALGS[METHOD]["OLL"]["T"].split())

        elif (
            logic.cube["F"][0][0] == "yellow"
            and logic.cube["R"][0][2] == "yellow"
            and logic.cube["U"][0][0] == "yellow"
            and logic.cube["U"][2][2] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["L"])
            alg.extend(ALGS[METHOD]["OLL"]["L"].split())

        elif (
            logic.cube["F"][0][2] == "yellow"
            and logic.cube["R"][0][2] == "yellow"
            and logic.cube["B"][0][2] == "yellow"
            and logic.cube["U"][2][0] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["SUNE"])
            alg.extend(ALGS[METHOD]["OLL"]["SUNE"].split())

        elif (
            logic.cube["F"][0][0] == "yellow"
            and logic.cube["R"][0][0] == "yellow"
            and logic.cube["L"][0][0] == "yellow"
            and logic.cube["U"][0][2] == "yellow"
        ):
            logic.execute(ALGS[METHOD]["OLL"]["ANTISUNE"])
            alg.extend(ALGS[METHOD]["OLL"]["ANTISUNE"].split())

        else:
            logic.execute("U")
            alg.append("U")
    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"OLL: {' '.join(alg)}\n")


def cpll():
    alg = []
    if (
        logic.cube["L"][0][0] != logic.cube["L"][0][2]
        and logic.cube["F"][0][0] != logic.cube["F"][0][2]
        and logic.cube["R"][0][0] != logic.cube["R"][0][2]
        and logic.cube["B"][0][0] != logic.cube["B"][0][2]
    ):
        logic.execute(ALGS["LBL"]["CPLL"]["Y"])
        alg.extend(ALGS["LBL"]["CPLL"]["Y"].split())
        with open("recons.txt", "a", encoding="utf-8") as f:
            f.write(f"CPLL: {' '.join(alg)}\n")
        return
    elif (
        logic.cube["L"][0][0] == logic.cube["L"][0][2]
        and logic.cube["F"][0][0] == logic.cube["F"][0][2]
        and logic.cube["B"][0][0] == logic.cube["B"][0][2]
        and logic.cube["R"][0][0] == logic.cube["R"][0][2]
    ):
        with open("recons.txt", "a", encoding="utf-8") as f:
            f.write(f"CPLL: {'skip'}\n")
        return True
    else:
        while logic.cube["L"][0][0] != logic.cube["L"][0][2]:
            logic.execute("U")
            alg.append("U")

    logic.execute(ALGS["LBL"]["CPLL"]["J"])
    alg.extend(ALGS["LBL"]["CPLL"]["J"].split())

    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"CPLL: {' '.join(alg)}\n")


def epll():
    alg = []

    for _ in range(3):
        if logic.cube["F"][0][0] == logic.cube["F"][0][1] == logic.cube["F"][0][2]:
            break
        else:
            logic.execute("U")
            alg.append("U")

    if logic.cube["F"][0][0] == logic.cube["F"][0][1] == logic.cube["F"][0][2]:
        if logic.cube["R"][0][0] == logic.cube["R"][0][1] == logic.cube["R"][0][2]:
            while not logic.cube["F"][0][1] == logic.cube["F"][1][1]:
                logic.execute("U")
                alg.append("U")
        else:
            while not logic.cube["R"][0][0] == logic.cube["R"][0][1]:
                logic.execute(ALGS["LBL"]["EPLL"]["U"])
                alg.extend(ALGS["LBL"]["EPLL"]["U"].split())
            while not logic.cube["F"][0][1] == logic.cube["F"][1][1]:
                logic.execute("U")
                alg.append("U")

    else:
        logic.execute(ALGS["LBL"]["EPLL"]["U"])
        alg.extend(ALGS["LBL"]["EPLL"]["U"].split())

        if logic.cube["L"][0][0] == logic.cube["L"][0][1] == logic.cube["L"][0][2]:
            logic.execute("U'")
            alg.append("U'")
        elif logic.cube["R"][0][0] == logic.cube["R"][0][1] == logic.cube["R"][0][2]:
            logic.execute("U")
            alg.append("U")
        else:
            logic.execute("U2")
            alg.append("U2")

        while not logic.cube["R"][0][0] == logic.cube["R"][0][1]:
            logic.execute(ALGS["LBL"]["EPLL"]["U"])
            alg.extend(ALGS["LBL"]["EPLL"]["U"].split())
        while not logic.cube["F"][0][1] == logic.cube["F"][1][1]:
            logic.execute("U")
            alg.append("U")

    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"EPLL: {' '.join(alg)}\n")
        f.write("-" * 50 + "\n")

    fix_cube_orientation()


def hash_gen():
    stickers = [
        logic.cube["U"][0][1],
        logic.cube["U"][1][0],
        logic.cube["U"][2][1],
        logic.cube["U"][1][2],
        logic.cube["U"][0][0],
        logic.cube["U"][2][0],
        logic.cube["U"][2][2],
        logic.cube["U"][0][2],
        logic.cube["F"][0][0],
        logic.cube["F"][0][2],
        logic.cube["B"][0][0],
        logic.cube["B"][0][2],
    ]

    return "".join(["1" if s == "yellow" else "0" for s in stickers])


def pll_hash_gen():
    color_values = {"red": 0, "green": 1, "blue": 1, "orange": 2}

    stickers = [
        logic.cube["L"][0][0],
        logic.cube["L"][0][1],
        logic.cube["L"][0][2],
        logic.cube["F"][0][0],
        logic.cube["F"][0][1],
        logic.cube["F"][0][2],
        logic.cube["R"][0][0],
        logic.cube["R"][0][1],
        logic.cube["R"][0][2],
        logic.cube["B"][0][0],
        logic.cube["B"][0][1],
        logic.cube["B"][0][2],
    ]

    hash = []
    for s in stickers:
        hash.append(color_values[s])
    # print("".join(str(h) for h in hash))
    return "".join(str(h) for h in hash)

    # for pll in PLLS.values():
    #     fix_cube_orientation()
    #     logic.execute("z")
    #     logic.execute("z")
    #     logic.execute(pll)
    #     hash = []
    #     for s in stickers:
    #         hash.append(color_values[s])
    # print(hash)
    #     solve_cube_LBL()

    # return hash


PLLS = {
    "T": "R U R' U' R' F R2 U' R' U' R U R' F'",
    "Ja": "R' U2 R U R' U2 L U' R U L'",
    "Jb": "R U R' F' R U R' U' R' F R2 U' R' U'",
    "F": "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
    "Aa": "x R' U R' D2 R U' R' D2 R2 x'",
    "Ab": "x R2 D2 R U R' D2 R U' R x'",
    "Ra": "R U R' F' R U2 R' U2 R' F R U R U2 R' U'",
    "Rb": "R2 F R U R U' R' F' R U2 R' U2 R U",
    "Ga": "R2 U R' U R' U' R U' R2 D U' R' U R D'",
    "Gb": "D R' U' R U D' R2 U R' U R U' R U' R2",
    "Gc": "R2 U' R U' R U R' U R2 D' U R U' R' D",
    "Gd": "R U R' U' D R2 U' R U' R' U R' U R2 D'",
    "Y": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
    "E": "x' R U' R' D R U R' D' R U R' D R U' R' D' x",
    "Na": "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
    "Nb": "R' U R U' R' F' U' F R U R' F R' F' R U' R",
    "V": "R' U R' U' R D' R' D R' U D' R2 U' R2 D R2",
    "Ua": "R U R' U R' U' R2 U' R' U R' U R",
    "Ub": "R' U R' U' R' U' R' U R U R2",
    "H": "R L U2 R' L' F' B' U2 F B",
    "Z": "R' U' R U' R U R U' R' U R U R2 U' R'",
}


# FRIDRICH METHOD
def solve_OLL():
    # preauf = []
    oll_hash = hash_gen()
    oll_map = ALGS["CFOP"]["OLL_MAP"]
    alg = []
    count = 0
    for _ in range(4):
        oll_hash = hash_gen()
        if oll_hash in oll_map:
            case_name = oll_map[oll_hash]
            logic.execute(ALGS["CFOP"]["OLL"][case_name])
            # alg.extend(ALGS["CFOP"]["OLL"][case_name].split())
            # preauf = " ".join(preauf)
            # print(
            #     f"OLL Solved: {case_name}: ({preauf}) {ALGS['CFOP']['OLL'][case_name]}"
            # )

            # with open("recons.txt", "a", encoding="utf-8") as f:
            #     f.write(f"OLL: {' '.join(alg)}\n")
            # return True
            break
        logic.execute("U")
        count += 1
        # alg.append("U")
        # preauf.append("U")

    if count % 4 == 1:
        alg.append("U")
    elif count % 4 == 2:
        alg.append("U2")
    elif count % 4 == 3:
        alg.append("U'")

    # logic.execute(ALGS["CFOP"]["OLL"][oll_map[oll_hash]])
    alg.extend(ALGS["CFOP"]["OLL"][case_name].split())

    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"OLL: {' '.join(alg)}\n")


def AUF(side="F"):
    alg = []
    count = 0
    while logic.cube[side][0][1] != logic.cube[side][1][1]:
        logic.execute("U")
        count += 1
    if count == 1:
        alg.append("U")
    elif count == 2:
        alg.append("U2")
    elif count == 3:
        alg.append("U'")

    return alg


def solve_PLL():
    alg = []
    plls = ALGS["CFOP"]["PLL"]
    count_U = 0
    count_Y = 0
    for _ in range(3):
        if logic.cube["L"][0][0] != logic.cube["L"][0][2]:
            logic.execute("U")
            count_U += 1
        else:
            break

    for _ in range(3):
        if logic.cube["L"][0][1] != logic.cube["L"][1][1]:
            logic.execute("U")
            logic.execute("y'")

            count_U += 1
            count_Y += 1
        else:
            break

    if count_U % 4 == 1:
        alg.append("U")
    elif count_U % 4 == 2:
        alg.append("U2")
    elif count_U % 4 == 3:
        alg.append("U'")

    if count_Y % 4 == 1:
        alg.append("y'")
    elif count_Y % 4 == 2:
        alg.append("y2")
    elif count_Y % 4 == 3:
        alg.append("y")

    # 22nd case - PLL SKIP
    if logic.is_solved():
        with open("recons.txt", "a", encoding="utf-8") as f:
            f.write(f"PLL SKIP {' '.join(alg)}\n")
        return True

    # 3 cases: (T J J) + 9 more ...
    if (
        logic.cube["L"][0][0] == logic.cube["L"][0][2]
        and logic.cube["F"][0][0] != logic.cube["F"][0][2]
    ):
        if logic.cube["L"][0][0] == logic.cube["L"][0][1]:
            if logic.cube["R"][0][1] == logic.cube["R"][1][1]:
                logic.execute(plls["F"])  # F
                alg.extend(plls["F"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
            elif logic.cube["F"][0][1] == logic.cube["F"][1][1]:
                logic.execute(plls["Ja"])  # Ja
                alg.extend(plls["Ja"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
            elif logic.cube["B"][0][1] == logic.cube["B"][1][1]:
                logic.execute(plls["Jb"])  # Jb
                alg.extend(plls["Jb"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True

        # 9 cases: (R R G G G G A A T)
        if (
            logic.cube["B"][0][2] == logic.cube["B"][0][1]
            and logic.cube["F"][0][1] == logic.cube["F"][0][0]
        ):
            logic.execute(plls["T"])  # T
            alg.extend(plls["T"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        if logic.cube["B"][0][2] == logic.cube["B"][0][1]:
            logic.execute(plls["Rb"])  # Rb
            alg.extend(plls["Rb"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        elif logic.cube["F"][0][0] == logic.cube["F"][0][1]:
            logic.execute(plls["Ra"])  # Ra
            alg.extend(plls["Ra"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        elif logic.cube["R"][0][0] == logic.cube["R"][0][1]:
            if logic.cube["F"][0][1] == logic.cube["F"][0][2]:
                logic.execute("U")
                logic.execute(plls["Aa"])  # Aa
                alg.extend("U")
                alg.extend(plls["Aa"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
            else:
                logic.execute(plls["Gd"])  # Gd
                alg.extend(plls["Gd"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
        elif logic.cube["F"][0][1] == logic.cube["F"][0][2]:
            logic.execute(plls["Ga"])  # Ga
            alg.extend(plls["Ga"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        elif logic.cube["R"][0][2] == logic.cube["R"][0][1]:
            if logic.cube["B"][0][1] == logic.cube["B"][0][0]:
                logic.execute("U2")
                logic.execute(plls["Ab"])  # Ab
                alg.append("U2")
                alg.extend(plls["Ab"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
            else:
                logic.execute(plls["Gb"])  # Gb
                alg.extend(plls["Gb"].split())
                alg.extend(AUF())
                with open("recons.txt", "a", encoding="utf-8") as f:
                    f.write(f"PLL: {' '.join(alg)}\n")
                return True
        elif logic.cube["B"][0][0] == logic.cube["B"][0][1]:
            logic.execute(plls["Gc"])  # Gc
            alg.extend(plls["Gc"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True

    # 4 cases: (U U H Z)

    if logic.cube["B"][0][0] == logic.cube["B"][0][2]:
        for _ in range(4):
            if logic.cube["F"][0][0] == logic.cube["F"][0][1]:
                if logic.cube["R"][0][1] == logic.cube["L"][0][0]:
                    logic.execute(plls["Ub"])
                    alg.extend(plls["Ub"].split())
                    alg.extend(AUF())
                    with open("recons.txt", "a", encoding="utf-8") as f:
                        f.write(f"PLL: {' '.join(alg)}\n")
                    return True
                else:
                    logic.execute(plls["Ua"])
                    alg.extend(plls["Ua"].split())
                    alg.extend(AUF())
                    with open("recons.txt", "a", encoding="utf-8") as f:
                        f.write(f"PLL: {' '.join(alg)}\n")
                    return True
            logic.execute("U")
        if logic.cube["F"][0][1] == logic.cube["L"][0][0]:
            logic.execute(plls["Z"])
            alg.extend(plls["Z"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        elif logic.cube["F"][0][1] == logic.cube["R"][0][0]:
            logic.execute("U")
            logic.execute(plls["Z"])
            alg.extend(plls["Z"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True
        else:
            logic.execute(plls["H"])
            alg.extend(plls["H"].split())
            alg.extend(AUF())
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"PLL: {' '.join(alg)}\n")
            return True

    # 5 cases: (Y E Na Nb V)
    pll_map = ALGS["CFOP"]["Y-PLL_MAP"]

    count = 0
    found = False
    for i in range(4):
        h = pll_hash_gen()
        if h in pll_map:
            pll_name = pll_map[h]
            pll = ALGS["CFOP"]["PLL"][pll_name]

            logic.execute(pll)
            alg.extend(pll.split())
            # print(f"PLL Matched: {pll_name}")
            # with open("recons.txt", "a", encoding="utf-8") as f:
            #     f.write(f"PLL: {' '.join(pll)}\n")
            break

        logic.execute("U")
        count += 1

    if count % 4 == 1:
        alg.append("U")
    elif count % 4 == 2:
        alg.append("U2")
    elif count % 4 == 3:
        alg.append("U'")

    count = 0
    for _ in range(4):
        if logic.cube["F"][0][1] == logic.cube["F"][1][1]:
            break
        logic.execute("U")
        count += 1

    if count % 4 == 1:
        alg.append("U")
    elif count % 4 == 2:
        alg.append("U2")
    elif count % 4 == 3:
        alg.append("U'")

    with open("recons.txt", "a", encoding="utf-8") as f:
        f.write(f"PLL: {' '.join(alg)}\n")

    return True


def PLL_solved():
    return (
        logic.cube["L"][0][0] == logic.cube["L"][0][1] == logic.cube["L"][0][2]
        and logic.cube["F"][0][0] == logic.cube["F"][0][1] == logic.cube["F"][0][2]
    )


def solve_cube_LBL():
    if logic.is_solved():
        # print("The cube can't be more solved than solved :)")
        return
    solve_cross()
    solve_f2l_corners()
    solve_f2l_edges()
    eo()
    coll()
    cpll()
    epll()


def solve_cube_CFOP():
    if logic.is_solved():
        # print("The cube can't be more solved than solved :)")
        return
    solve_cross()
    # solve_f2l_corners()

    # solve_f2l_edges()

    solve_F2L()
    solve_OLL()
    solve_PLL()
