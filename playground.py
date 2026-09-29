from pysat.solvers import Glucose3
from binomial import binomial_amo
from sequential import SequentialEncoder
N=600

def var(r, c):
 return r*N+c+1

# Lấy thử 1 hàng để so sánh trực tiếp số clause sinh ra
sample_row_vars = [var(0, j) for j in range(N)]

bin_clauses = binomial_amo(sample_row_vars)

# Khởi tạo Sequential Encoder với ID biến phụ bắt đầu từ N*N + 1
seq_encoder = SequentialEncoder(N * N + 1)
seq_clauses = seq_encoder.encode_amo(sample_row_vars)

print(f"--- SO SÁNH KÍCH THƯỚC CHO 1 HÀNG/CỘT (N={N}) ---")
print(f"Binomial (Pairwise) sinh ra : {len(bin_clauses)} clauses")
print(f"Sequential Counter sinh ra  : {len(seq_clauses)} clauses")
print("-" * 50)

solver = Glucose3()

total_clauses_added = 0

for i in range(N):
    row_vars = [var(i,j) for j in range(N)]
    #ALO cho hàng
    solver.add_clause(row_vars)
    total_clauses_added += 1
    #AMO cho hàng
    row_amo= seq_encoder.encode_amo(row_vars)
    solver.append_formula(row_amo)
    total_clauses_added+=len(row_amo)

for j in range(N):
    col_vars = [var(i,j) for i in range(N)]
    #ALO cho cột
    solver.add_clause(col_vars)
    total_clauses_added += 1
    # AMO cho cột
    col_amo= seq_encoder.encode_amo(col_vars)
    solver.append_formula(col_amo)
    total_clauses_added+=len(col_amo)

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

# AMO cho đường chéo chính
for diag_vars in main_diagonals.values():
    # Chỉ xét các đường chéo có từ 2 ô trở lên
    if len(diag_vars) > 1:
        diag_amo= seq_encoder.encode_amo(diag_vars)
        solver.append_formula(diag_amo)
        total_clauses_added+=len(diag_amo)

# AMO cho đường chéo phụ
for diag_vars in anti_diagonals.values():
    if len(diag_vars) > 1:
        diag_amo= seq_encoder.encode_amo(diag_vars)
        solver.append_formula(diag_amo)
        total_clauses_added+=len(diag_amo)

print(f"Tổng số clause đã nạp vào solver : {total_clauses_added}")
print(f"ID biến phụ tiếp theo khả dụng   : {seq_encoder.next_aux_id}")
print("Đang tìm nghiệm...")

if solver.solve():
    print(f"Đã tìm thấy nghiệm cho {N}-Queens!")
    model = solver.get_model()
    # Lọc ra các biến mang giá trị dương (True)
    queens = [v for v in model if v > 0]
    print("Vị trí ID các quân Hậu:", queens)
else:
    print("UNSAT - Không tồn tại nghiệm.")