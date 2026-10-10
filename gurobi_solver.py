import time
import gurobipy as gp
from gurobipy import GRB


def solve_nqueens_gurobi(N):
    print(f"\n--- Giải {N}-Queens bằng Gurobi MIP ---")

    m = gp.Model(f"nqueens_{N}")
    m.setParam('OutputFlag', 0)
    m.setParam('TimeLimit', 3600)

    x = m.addVars(N, N, vtype=GRB.BINARY, name="x")

    m.addConstrs((x.sum(i, '*') == 1 for i in range(N)), name="row")
    m.addConstrs((x.sum('*', j) == 1 for j in range(N)), name="col")

    for d in range(-N + 1, N):
        m.addConstr(gp.quicksum(x[i, i - d] for i in range(N) if 0 <= i - d < N) <= 1, name=f"diag1_{d}")

    for d in range(2 * N - 1):
        m.addConstr(gp.quicksum(x[i, d - i] for i in range(N) if 0 <= d - i < N) <= 1, name=f"diag2_{d}")

    # Thời gian
    start_time = time.time()
    m.optimize()
    solve_time = time.time() - start_time

    if m.status == GRB.OPTIMAL:
        print(f"Tìm thấy nghiệm trong {solve_time:.4f} giây!")
    else:
        print("Không tìm thấy nghiệm hoặc vượt quá giới hạn thời gian/biến.")


for size in [50,100,500]:
    solve_nqueens_gurobi(size)