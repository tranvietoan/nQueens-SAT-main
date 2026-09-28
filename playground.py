from pysat.solvers import Glucose3
from binomial import binomial_amo
N=8

def var(r, c):
 return r*N+c+1

solver = Glucose3()


for i in range(N):
    row_vars = [var(i,j) for j in range(N)]
    #ALO cho hàng
    solver.add_clause(row_vars)
    #AMO cho hàng
    for j1 in range(N):
        for j2 in range(j1+1,N):
            solver.add_clause([-row_vars[j1],-row_vars[j2]])

for j in range(N):
    col_vars = [var(i,j) for i in range(N)]
    #ALO cho cột
    (solver.add_clause(col_vars))
    # AMO cho cột
    for i1 in range(N):
        for i2 in range(i1+1,N):
            solver.add_clause([-col_vars[i1],-col_vars[i2]])


main_diagonals = {}
anti_diagonals = {}

for i in range(N):
    for j in range(N):
        variable_id = var(i, j)

        key_main = i - j
        if key_main not in main_diagonals:
            main_diagonals[key_main] = []
        main_diagonals[key_main].append(variable_id)

        key_anti = i + j
        if key_anti not in anti_diagonals:
            anti_diagonals[key_anti] = []
        anti_diagonals[key_anti].append(variable_id)

# AMO cho hàng và cột
for i in range(N):
    row_vars = [var(i, j) for j in range(N)]
    solver.append_formula(binomial_amo(row_vars))

for j in range(N):
    col_vars = [var(i, j) for i in range(N)]
    solver.append_formula(binomial_amo(col_vars))

# AMO cho đường chéo chính
for diag_vars in main_diagonals.values():
    # Chỉ xét các đường chéo có từ 2 ô trở lên
    if len(diag_vars) > 1:
        solver.append_formula(binomial_amo(diag_vars))

# AMO cho đường chéo phụ
for diag_vars in anti_diagonals.values():
    if len(diag_vars) > 1:
        solver.append_formula(binomial_amo(diag_vars))

print("Đang tìm nghiệm...")
if solver.solve():
    print(f"Đã tìm thấy nghiệm cho {N}-Queens!")
    model = solver.get_model()
    # Lọc ra các biến mang giá trị dương (True)
    queens = [v for v in model if v > 0]
    print("Vị trí ID các quân Hậu:", queens)
else:
    print("UNSAT - Không tồn tại nghiệm.")