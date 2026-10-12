import time
from ortools.sat.python import cp_model


def solve_nqueens_cpsat(N):
    print(f"\n--- Giải {N}-Queens bằng CP-SAT ---")

    start_build = time.time()

    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, N - 1, f'q_{i}') for i in range(N)]

    # 3 ràng buộc hàng( nghiễm nhiên đúng cột) và 2 đường chéo
    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] - i for i in range(N)])
    model.AddAllDifferent([queens[i] + i for i in range(N)])

    build_time = time.time() - start_build

    #Số lượng biến và ràng buộc
    nv = len(model.Proto().variables)
    nc = len(model.Proto().constraints)

    solver = cp_model.CpSolver()
    start_search=time.time()
    status = solver.Solve(model)
    search_time = time.time() - start_search

    print("-" * 40)
    print(f"Số lượng biến (nv)                 : {nv}")
    print(f"Số lượng ràng buộc (nc)            : {nc}")
    print(f"Thời gian Build Model (t_build)    : {build_time:.4f} giây")
    print(f"Thời gian Search Solver (t_search) : {search_time:.4f} giây")

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Tìm thấy nghiệm trong {search_time:.4f} giây!")
    else:
        print("Không tồn tại nghiệm.")

for size in [50, 100, 500]:
    solve_nqueens_cpsat(size)