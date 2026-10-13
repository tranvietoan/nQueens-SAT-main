import matplotlib.pyplot as plt

gurobi = sorted([0.0815, 0.0019, 0.0560])
cpsat = sorted([0.2410, 0.8997, 558.9518])
sat_binomial = sorted([0.0036, 0.0113, 11.6443])
sat_sequential = sorted([0.999,2408474])
sat_commander = sorted([0.0868, 0.0345, 3.7768])
sat_binary = sorted([255.7419, 0.0149, 1.0141])
sat_product = sorted([0.2996, 1.8833])

plt.figure(figsize=(10, 6))

# Vẽ các đường
plt.plot(range(1, len(gurobi) + 1), gurobi, marker='o', linestyle='-', label='Gurobi MIP')
plt.plot(range(1, len(cpsat) + 1), cpsat, marker='s', linestyle='-', label='CP-SAT')
plt.plot(range(1, len(sat_binomial) + 1), sat_binomial, marker='^', linestyle='--', label='SAT (Binomial)')
plt.plot(range(1, len(sat_sequential) + 1), sat_sequential, marker='p', linestyle='--', label='SAT (Sequential)')
plt.plot(range(1, len(sat_commander) + 1), sat_commander, marker='d', linestyle='--', label='SAT (Commander)')
plt.plot(range(1, len(sat_binary) + 1), sat_binary, marker='x', linestyle='--', label='SAT (Binary)')
plt.plot(range(1, len(sat_product) + 1), sat_product, marker='v', linestyle='--', label='SAT (Product)')

# Cấu hình trục Y dạng Logarit
plt.yscale('log')
plt.xticks([1, 2, 3], ['1st', '2nd', '3rd'])

plt.xlabel('Số lượng Instance ', fontsize=12)
plt.ylabel('Thời gian tìm kiếm $t_{search}$ (giây, thang log)', fontsize=12)
plt.title('Cactus Plot so sánh hiệu năng giải (Gurobi vs CP-SAT vs SAT Encodings)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)

plt.savefig('Template_latex/cactus_plot.png', dpi=300, bbox_inches='tight')
print("Đã xuất biểu đồ: cactus_plot.png")