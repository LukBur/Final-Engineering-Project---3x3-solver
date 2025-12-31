import tkinter as tk
from cube_data import cube
import cube_logic as logic
import cube_solver as solver
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def drawFaceDynamic(canvas, face):
    size = 50
    canvas.delete("all")
    for row in range(3):
        for col in range(3):
            color = cube[face][row][col]
            x1, y1 = col * size, row * size
            x2, y2 = x1 + size, y1 + size
            canvas.create_rectangle(
                x1, y1, x2, y2, fill=color, outline="black", width=2
            )


flag_showed_reco = False
already_solved = False
movecount_table = []
movecount_table_LBL = []
movecount_table_CFOP = []
avg_movecount = 0
min_movecount = 250
max_movecount = 0


def update_label():
    global flag_showed_reco
    global already_solved
    global movecount_table
    # movecount_table = []

    if logic.is_solved() and not flag_showed_reco and not already_solved:
        if logic.movecount > 0:
            movecount_table.append(logic.movecount)
            if solver.METHOD == "CFOP":
                movecount_table_CFOP.append(logic.movecount)
            else:
                movecount_table_LBL.append(logic.movecount)
            update_chart()

            current_min = min(movecount_table)
            current_max = max(movecount_table)
            current_avg = sum(movecount_table) / len(movecount_table)

            label_cubestate.config(text="SOLVED")
            label_movecount.config(
                text=f"Movecount: {logic.movecount} \n Average movecount: {current_avg:.2f} \n min: {current_min} | max: {current_max} \n Solves done: {len(movecount_table)}"
            )

            # print("Cube solved in", f"{logic.movecount} moves ")
            with open("recons.txt", "a", encoding="utf-8") as f:
                f.write(f"Cube solved in {logic.movecount} moves! \n")

            flag_showed_reco = True
            already_solved = True
            # logic.movecount = 0

    else:
        label_cubestate.config(text=f"Scramble: {' '.join(logic.scramble_sequence)}")
        flag_showed_reco = False
        already_solved = False


def test_100():
    global min_movecount, max_movecount, already_solved, flag_showed_reco

    if solver.METHOD == "CFOP":
        for _ in range(99):
            already_solved = False
            flag_showed_reco = False

            logic.scramble_logic()
            handle_solve_step(solver.solve_cube_CFOP)
    else:
        for _ in range(99):
            already_solved = False
            flag_showed_reco = False

            logic.scramble_logic()
            handle_solve_step(solver.solve_cube_LBL)


def show_movecount_table():
    return movecount_table


def drawCube():
    faces = [
        ("U", canvas_U),
        ("L", canvas_L),
        ("F", canvas_F),
        ("R", canvas_R),
        ("B", canvas_B),
        ("D", canvas_D),
    ]
    for face_name, canv in faces:
        drawFaceDynamic(canv, face_name)
    update_label()


def handle_move(move_func):
    move_func()
    drawCube()


root = tk.Tk()
root.geometry("1580x780+1000+500")
root.title("Rubik's cube solver")


# UI
label_cubestate = tk.Label(root, text="Good luck!", font=("Times New Roman", 16))
# label_scramble()
label_movecount = tk.Label(root, text="twojtekst", font=("Times New Roman", 16))
label_instruction = tk.Label(
    root,
    text="Welcome to The 3x3 Learning App! \n Pick your method: (LBL, CFOP)",
    font=("Times New Roman", 22),
)
label_cubestate.pack(padx=20, pady=20)
label_movecount.place(x=1150, y=20)
label_instruction.place(x=900, y=150)


canvases = {}
for f in ["U", "L", "F", "R", "B", "D"]:
    canvases[f] = tk.Canvas(
        root, width=150, height=150, bg="lightgray", highlightthickness=0
    )

canvas_U, canvas_L, canvas_F = canvases["U"], canvases["L"], canvases["F"]
canvas_R, canvas_B, canvas_D = canvases["R"], canvases["B"], canvases["D"]

off_x, off_y = 50, 200
canvas_U.place(x=off_x + 150, y=off_y - 150)
canvas_L.place(x=off_x, y=off_y)
canvas_F.place(x=off_x + 150, y=off_y)
canvas_R.place(x=off_x + 300, y=off_y)
canvas_B.place(x=off_x + 450, y=off_y)
canvas_D.place(x=off_x + 150, y=off_y + 150)

# buttons
buttonframe = tk.Frame(root)
buttonframe.pack(side="bottom", anchor="e", padx=50, pady=50)
method_buttonframe = tk.Frame(root)
method_buttonframe.pack(side="bottom", anchor="s")

fig, ax = plt.subplots(figsize=(6, 2), dpi=80)
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
ax.set_title("Movecount History")
ax.set_xlabel("Solve #")
ax.set_ylabel("Moves")
ax.grid(True, linestyle="--", alpha=0.6)

fig_2, ax_2 = plt.subplots(figsize=(6, 2), dpi=80)
fig_2.patch.set_alpha(0.0)
ax_2.patch.set_alpha(0.0)
ax_2.set_title("Movecount History")
ax_2.set_xlabel("Solve #")
ax_2.set_ylabel("Moves")
ax_2.grid(True, linestyle="--", alpha=0.6)

chart_canvas_CFOP = FigureCanvasTkAgg(fig, master=root)
chart_widget_CFOP = chart_canvas_CFOP.get_tk_widget()
chart_widget_CFOP.place(x=370, y=380)

chart_canvas_LBL = FigureCanvasTkAgg(fig_2, master=root)
chart_widget_LBL = chart_canvas_LBL.get_tk_widget()
chart_widget_LBL.place(x=370, y=550)


def update_chart():
    method = solver.METHOD
    if method == "CFOP":
        # if not movecount_table_CFOP:
        #     return

        ax.clear()

        ax.plot(
            movecount_table_CFOP, marker="o", linestyle="-", color="b", label="Moves"
        )

        avg = sum(movecount_table_CFOP) / len(movecount_table_CFOP)
        ax.axhline(y=avg, color="r", linestyle="--", label=f"Avg: {avg:.1f}")

        ax.set_title("CFOP movecount chart")
        ax.set_xlabel("Solve")
        ax.set_ylabel("Movecount")
        ax.legend(loc="upper right", fontsize="small")
        ax.grid(True, alpha=0.3)

        chart_canvas_CFOP.draw()
    else:
        if not movecount_table_LBL:
            return

        ax_2.clear()
        ax_2.plot(
            movecount_table_LBL, marker="o", linestyle="-", color="b", label="Moves"
        )

        avg = sum(movecount_table_LBL) / len(movecount_table_LBL)
        ax_2.axhline(y=avg, color="r", linestyle="--", label=f"Avg: {avg:.1f}")

        ax_2.set_title("Movecount chart")
        ax_2.set_xlabel("Solve")
        ax_2.set_ylabel("Movecount")
        ax_2.legend(loc="upper right", fontsize="small")
        ax_2.grid(True, alpha=0.3)

        chart_canvas_LBL.draw()

def reset_charts():
    global movecount_table
    global movecount_table_CFOP
    global movecount_table_LBL
    global flag_showed_reco
    global already_solved
    initial_method = solver.METHOD
    movecount_table = [0]
    movecount_table_CFOP = [0]
    movecount_table_LBL = [0]
    flag_showed_reco = False
    already_solved = False
    ax.clear()
    ax_2.clear()
    solver.METHOD = "LBL"
    update_chart()
    solver.METHOD = "CFOP"
    update_chart()
    logic.movecount = 0
    update_label()
    solver.METHOD = initial_method
    flag_showed_reco = True
    already_solved = True
    movecount_table = []
    movecount_table_CFOP = []
    movecount_table_LBL = []


def create_btn(txt, cmd, r, c, bg_color="yellow", w=7):
    btn = tk.Button(
        buttonframe,
        text=txt,
        font=("Arial", 18),
        width=w,
        command=lambda: handle_move(cmd),
        bg=bg_color,
    )
    btn.grid(row=r, column=c, sticky="nsew")


def pick_method(method):
    solver.METHOD = method
    label_instruction.config(
        text=f"METHOD: {method} \n Begin solving!",
        justify="center",
        font=("Times New Roman", 26),
        padx=150,
    )
    if method == "LBL":
        (
            create_btn(
                "DCROSS",
                lambda: handle_solve_step(solver.solve_cross),
                0,
                4,
                "bisque1",
            ),
        )
        create_btn(
            "F2LC",
            lambda: handle_solve_step(solver.solve_f2l_corners),
            1,
            4,
            "bisque1",
        )
        create_btn(
            "F2LE",
            lambda: handle_solve_step(solver.solve_f2l_edges),
            2,
            4,
            "bisque1",
        )
        create_btn("UCROSS", lambda: handle_solve_step(solver.eo), 3, 4, "bisque1")
        create_btn("EOLL", lambda: handle_solve_step(solver.eo), 3, 4, "bisque1")
        create_btn("COLL", lambda: handle_solve_step(solver.coll), 4, 4, "bisque1")
        create_btn("CPLL", lambda: handle_solve_step(solver.cpll), 5, 4, "bisque1")
        create_btn("EPLL", lambda: handle_solve_step(solver.epll), 6, 4, "bisque1")
        create_btn(
            "SOLVE",
            lambda: handle_solve_step(solver.solve_cube_LBL),
            0,
            2,
            "bisque1",
        )

    elif method == "CFOP":
        create_btn(
            "F2L", lambda: handle_solve_step(solver.solve_f2l_smart), 1, 4, "spring green"
        )
        create_btn(
            "OLL", lambda: handle_solve_step(solver.solve_OLL), 2, 4, "spring green"
        )
        (
            create_btn(
                "PLL", lambda: handle_solve_step(solver.solve_PLL), 3, 4, "spring green"
            ),
        )
        (
            create_btn(
                "SOLVE",
                lambda: handle_solve_step(solver.solve_cube_CFOP),
                0,
                2,
                "spring green",
            ),
            create_btn(
                "SOLVE",
                lambda: handle_solve_step(solver.solve_cube_CFOP),
                0,
                2,
                "spring green",
            ),
        )


method_buttonframe.place(x=off_x + 750, y=300)
method_button_LBL = tk.Button(
    method_buttonframe,
    text="LBL",
    font=("Arial", 22),
    width=7,
    command=lambda: pick_method("LBL"),
    bg="bisque1",
)
method_button_CFOP = tk.Button(
    method_buttonframe,
    text="CFOP",
    font=("Arial", 22),
    width=7,
    command=lambda: pick_method("CFOP"),
    bg="spring green",
)
reset_buttonframe = tk.Button(
    method_buttonframe,
    text="RESET STATS",
    font=("Arial", 22),
    width=10,
    command=lambda: reset_charts(),
    bg="red",

)
reset_buttonframe.pack(side="left")
method_button_LBL.pack(side="left", padx=50)
method_button_CFOP.pack(side="left")


def retrieve_input(event=None):
    input_text = text_box.get("1.0", "end-1c")
    move_list = input_text.split()

    m_map = {
        "U": logic.rotate_U,
        "U'": logic.rotate_U_prime,
        "U2": logic.rotate_U2,
        "D": logic.rotate_D,
        "D'": logic.rotate_D_prime,
        "D2": logic.rotate_D2,
        "L": logic.rotate_L,
        "L'": logic.rotate_L_prime,
        "L2": logic.rotate_L2,
        "R": logic.rotate_R,
        "R'": logic.rotate_R_prime,
        "R2": logic.rotate_R2,
        "F": logic.rotate_F,
        "F'": logic.rotate_F_prime,
        "F2": logic.rotate_F2,
        "B": logic.rotate_B,
        "B'": logic.rotate_B_prime,
        "B2": logic.rotate_B2,
        "x": logic.rotate_x,
        "x'": logic.rotate_x_prime,
        "y": logic.rotate_y,
        "y'": logic.rotate_y_prime,
        "z": logic.rotate_z,
        "z'": logic.rotate_z_prime,
    }

    for m in move_list:
        if m in m_map:
            m_map[m]()
    logic.scramble_sequence = " ".join(move_list).split()
    drawCube()
    text_box.delete("1.0", "end")

    return "break"


moves_map = [
    ("U", logic.rotate_U, 2, 0, "light yellow"),
    ("U'", logic.rotate_U_prime, 3, 0, "light yellow"),
    ("U2", logic.rotate_U2, 1, 0, "light yellow"),
    ("D", logic.rotate_D, 4, 0, "light yellow"),
    ("D'", logic.rotate_D_prime, 5, 0, "light yellow"),
    ("D2", logic.rotate_D2, 6, 0, "light yellow"),
    ("L", logic.rotate_L, 4, 1, "light yellow"),
    ("L'", logic.rotate_L_prime, 5, 1, "light yellow"),
    ("L2", logic.rotate_L2, 6, 1, "light yellow"),
    ("R", logic.rotate_R, 1, 1, "light yellow"),
    ("R'", logic.rotate_R_prime, 2, 1, "light yellow"),
    ("R2", logic.rotate_R2, 3, 1, "light yellow"),
    ("F", logic.rotate_F, 1, 2, "light yellow"),
    ("F'", logic.rotate_F_prime, 2, 2, "light yellow"),
    ("F2", logic.rotate_F2, 3, 2, "light yellow"),
    ("B", logic.rotate_B, 4, 2, "light yellow"),
    ("B'", logic.rotate_B_prime, 5, 2, "light yellow"),
    ("B2", logic.rotate_B2, 6, 2, "light yellow"),
    ("x", logic.rotate_x, 1, 3, "light yellow"),
    ("x'", logic.rotate_x_prime, 2, 3, "light yellow"),
    ("y", logic.rotate_y, 3, 3, "light yellow"),
    ("y'", logic.rotate_y_prime, 4, 3, "light yellow"),
    ("z", logic.rotate_z, 5, 3, "light yellow"),
    ("z'", logic.rotate_z_prime, 6, 3, "light yellow"),
    ("scramble", logic.scramble_logic, 0, 1, "dark sea green"),
    ("execute", retrieve_input, 0, 0, "pale green"),
    ("CROSS", lambda: handle_solve_step(solver.solve_cross), 0, 4, "light yellow"),
    # ("F2LC", lambda: handle_solve_step(solver.solve_f2l_corners), 1, 4, "light yellow"),
    # ("F2LE", lambda: handle_solve_step(solver.solve_f2l_edges), 2, 4, "light yellow"),
    # ("UCROSS", lambda: handle_solve_step(solver.eo), 3, 6),
    # ("OLL", lambda: handle_solve_step(solver.solve_OLL), 4, 6),
    # ("CPLL", lambda: handle_solve_step(solver.cpll), 5, 5),
    ("test 100", lambda: handle_solve_step(test_100), 0, 3, "light yellow"),
]

for txt, cmd, r, col, color in moves_map:
    create_btn(txt, cmd, r, col, color, w=2 if txt == "scramble" else 7)


text_box = tk.Text(root, height=1, width=20, font=("Times New Roman", 26))
text_box.bind("<Return>", retrieve_input)
text_box.pack()


def handle_solve_step(solve_func):
    result = solve_func()
    drawCube()


drawCube()
root.mainloop()
