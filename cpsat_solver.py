import time
from ortools.sat.python import cp_model


def solve_nqueens_cpsat(N):
    model = cp_model.CpModel()

    queens = [model.NewIntVar(0, N - 1, f'q_{i}') for i in range(N)]

    model.AddAllDifferent(queens)

    model.AddAllDifferent([queens[i] - i for i in range(N)])
    model.AddAllDifferent([queens[i] + i for i in range(N)])

    solver = cp_model.CpSolver()

    print(f"\n--- Giải {N}-Queens bằng CP-SAT ---")
    start_time = time.time()
    status = solver.Solve(model)
    solve_time = time.time() - start_time

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Tìm thấy nghiệm trong {solve_time:.4f} giây!")
    else:
        print("Không tồn tại nghiệm.")

for size in [50, 100, 500]:
    solve_nqueens_cpsat(size)