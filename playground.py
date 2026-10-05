import time

from pysat.solvers import Glucose3
from binomial import binomial_amo
from sequential import SequentialEncoder
from commander import CommanderEncoder
from product import ProductEncoder
N=25

def var(r, c):
 return r*N+c+1

# Lấy thử 1 hàng để so sánh trực tiếp số clause sinh ra
sample_row_vars = [var(0, j) for j in range(N)]

bin_clauses = binomial_amo(sample_row_vars)

# Khởi tạo Sequential Encoder với ID biến phụ bắt đầu từ N*N + 1
seq_encoder = SequentialEncoder(N * N + 1)
seq_clauses = seq_encoder.encode_amo(sample_row_vars)

cmd_encoder = CommanderEncoder(N * N + 1, group_size=3)
cmd_clauses = cmd_encoder.encode_amo(sample_row_vars)

prod_encoder = ProductEncoder(N * N + 1)
prod_clauses = prod_encoder.encode_amo(sample_row_vars)

print(f"--- SO SÁNH KÍCH THƯỚC CHO 1 HÀNG/CỘT (N={N}) ---")
print(f"Binomial (Pairwise) sinh ra : {len(bin_clauses)} clauses")
print(f"Sequential Counter sinh ra  : {len(seq_clauses)} clauses")
print(f"Commander (Nhóm 3) sinh ra  : {len(cmd_clauses)} clauses")
print(f"Product Encoding sinh ra    : {len(prod_clauses)} clauses")
print("-" * 55)

start_time = time.time()
solver = Glucose3()

total_clauses_added = 0
# Khởi tạo Commander với group_size=3
active_encoder = ProductEncoder(N*N+1)
for i in range(N):
    # Đánh số cho từng ô
    row_vars = [var(i,j) for j in range(N)]
    col_vars = [var(j,i) for j in range(N)]
    #ALO cho hàng và cột
    solver.add_clause(row_vars)
    solver.add_clause(col_vars)
    total_clauses_added += 2

    #AMO cho hàng và cột
    #row_amo=seq_encoder.encode_amo(row_vars)
    row_amo= active_encoder.encode_amo(row_vars)
    solver.append_formula(row_amo)

    #col_amo=seq_encoder.encode_amo(col_vars)
    col_amo= active_encoder.encode_amo(col_vars)
    solver.append_formula(col_amo)

    total_clauses_added+=len(row_amo) + len(col_amo)


main_diagonals = {}
anti_diagonals = {}

for i in range(N):
    for j in range(N):
        variable_id = var(i, j)

        key_main = i - j
        main_diagonals.setdefault(key_main,[]).append(variable_id)

        key_anti = i + j
        anti_diagonals.setdefault(key_anti,[]).append(variable_id)

# AMO cho đường chéo chính và đường chéo phụ
for diag_vars in list(main_diagonals.values()) + list(anti_diagonals.values()):
    # Chỉ xét các đường chéo có từ 2 ô trở lên
    if len(diag_vars) > 1:
        #diag_amo=seq_encoder.encode_amo(diag_vars)
        diag_amo= active_encoder.encode_amo(diag_vars)
        solver.append_formula(diag_amo)
        total_clauses_added+=len(diag_amo)


print(f"Tổng số clause đã nạp vào solver : {total_clauses_added}")
print(f"ID biến phụ tiếp theo khả dụng   : {seq_encoder.next_aux_id}")
print("Đang tìm nghiệm...")

if solver.solve():
    solve_time = time.time() - start_time
    print(f"Đã tìm thấy nghiệm cho {N}-Queens! trong {solve_time:.4f} giây!")
    model = solver.get_model()
    # Lọc ra các biến mang giá trị dương (True)
    queens = [v for v in model if v > 0]
    print("Vị trí ID các quân Hậu:", queens)
else:
    print("UNSAT - Không tồn tại nghiệm.")