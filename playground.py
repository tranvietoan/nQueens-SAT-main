import time

from pysat.solvers import Glucose3
from binomial import binomial_amo
from sequential import SequentialEncoder
from commander import CommanderEncoder
from product import ProductEncoder
from binary import BinaryEncoder
N=500
def var(r, c):
 return r*N+c+1

# Lấy thử 1 hàng để so sánh trực tiếp số clause sinh ra
sample_row_vars = [var(0, j) for j in range(N)]
start_aux = N * N + 1

bin_clauses = binomial_amo(sample_row_vars)

# Khởi tạo Sequential Encoder với ID biến phụ bắt đầu từ N*N + 1
seq_encoder = SequentialEncoder(start_aux)
seq_clauses = seq_encoder.encode_amo(sample_row_vars)

cmd_encoder = CommanderEncoder(start_aux, group_size=3)
cmd_clauses = cmd_encoder.encode_amo(sample_row_vars)

prod_encoder = ProductEncoder(start_aux)
prod_clauses = prod_encoder.encode_amo(sample_row_vars)

binary_encoder = BinaryEncoder(start_aux)
binary_clauses= binary_encoder.encode_amo(sample_row_vars)

print(f"--- SO SÁNH KÍCH THƯỚC CHO 1 HÀNG/CỘT (N={N}) ---")
print(f"Binomial (Pairwise) sinh ra : {len(bin_clauses)} clauses")
print(f"Sequential Counter sinh ra  : {len(seq_clauses)} clauses")
print(f"Commander (Nhóm 3) sinh ra  : {len(cmd_clauses)} clauses")
print(f"Product Encoding sinh ra    : {len(prod_clauses)} clauses")
print(f"Binary Encoding sinh ra    : {len(binary_clauses)} clauses")
print("-" * 55)


def run_solver_with_encoder(encoder_name):
    print(f"\n--- Giải {N}-Queens bằng phương pháp: {encoder_name} ---")

    # Bắt đầu đo thời gian Build
    start_build = time.time()
    solver = Glucose3()

    start_aux_id = N * N + 1
    if encoder_name == "Binomial":
        encoder = None
    elif encoder_name == "Sequential":
        encoder = SequentialEncoder(start_aux_id)
    elif encoder_name == "Commander":
        encoder = CommanderEncoder(start_aux_id, group_size=3)
    elif encoder_name == "Product":
        encoder = ProductEncoder(start_aux_id)
    elif encoder_name == "Binary":
        encoder = BinaryEncoder(start_aux_id)
    else:
        print("Tên phương pháp không hợp lệ!")
        return

    total_clauses_added = 0


    def get_amo_clauses(vars_list):
        if encoder_name == "Binomial":
            return binomial_amo(vars_list)
        else:
            return encoder.encode_amo(vars_list)

    for i in range(N):
        # Đánh số cho từng ô
        row_vars = [var(i,j) for j in range(N)]
        col_vars = [var(j,i) for j in range(N)]
        #ALO cho hàng và cột
        solver.add_clause(row_vars)
        solver.add_clause(col_vars)
        total_clauses_added += 2

        #AMO cho hàng và cột
        row_amo = get_amo_clauses(row_vars)
        col_amo = get_amo_clauses(col_vars)

        solver.append_formula(row_amo)
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
            diag_amo= get_amo_clauses(diag_vars)
            solver.append_formula(diag_amo)
            total_clauses_added+=len(diag_amo)

    build_time = time.time() - start_build

    if encoder_name == "Binomial":
        nv = N * N
    else:
        nv = encoder.next_aux_id - 1

    nc = total_clauses_added

    start_search = time.time()
    is_sat = solver.solve()
    search_time = time.time() - start_search

    print("-" * 40)
    print(f"Số lượng biến (nv)                 : {nv}")
    print(f"Số lượng mệnh đề (nc)              : {nc}")
    print(f"Thời gian Build Model (t_build)    : {build_time:.4f} giây")
    print(f"Thời gian Search Solver (t_search) : {search_time:.4f} giây")

    if is_sat:
        print("\n=> TRẠNG THÁI: TÌM THẤY NGHIỆM")
        model = solver.get_model()
        queens = [v for v in model if v > 0]
        print("Vị trí ID các quân Hậu:", queens)
    else:
        print("\n=> TRẠNG THÁI: KHÔNG TỒN TẠI NGHIỆM (Hoặc timeout)")

    # Dọn dẹp bộ nhớ
    solver.delete()

run_solver_with_encoder("Binary")