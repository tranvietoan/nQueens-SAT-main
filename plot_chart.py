import matplotlib.pyplot as plt


N_values = [50, 100, 500]

pairwise = [1225, 4950, 124750]
sequential = [146, 296, 1496]
product = [149, 290, 1484]
commander = [170, 344, 1744]
binary = [300, 700, 4500]

plt.figure(figsize=(10, 6))

# Vẽ
plt.plot(N_values, pairwise, label='Binomial (Pairwise)', marker='o', linestyle='--', color='red')
plt.plot(N_values, binary, label='Binary Encoding', marker='s', color='orange')
plt.plot(N_values, commander, label='Commander (Nhóm 3)', marker='^', color='green')
plt.plot(N_values, sequential, label='Sequential Counter', marker='d', color='blue')
plt.plot(N_values, product, label='Product Encoding', marker='x', color='purple')

# Sử dụng trục Y dạng Logarit
plt.yscale('log')
plt.xticks(N_values)

# Gắn nhãn
plt.xlabel('Kích thước bàn cờ (N)', fontsize=12)
plt.ylabel('Số lượng mệnh đề ', fontsize=12)
plt.title('So sánh tốc độ tăng trưởng mệnh đề AMO ', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)


plt.savefig('clause_comparison.png', dpi=300, bbox_inches='tight')
print("Đã xuất biểu đồ thành file: clause_comparison.png")
plt.show()