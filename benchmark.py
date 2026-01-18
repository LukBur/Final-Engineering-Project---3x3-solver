# benchmark.py
import time, psutil, gc
import cube_logic as logic
import cube_solver as solver

for i in range(1000):
    logic.scramble_logic()
    start = time.perf_counter()
    solver.solve_cube_CFOP()
    elapsed = time.perf_counter() - start
    print(
        f"{i + 1}: {elapsed:.4f}s, RAM: {psutil.virtual_memory().used / (1024**2):.1f}MB"
    )
    gc.collect()
