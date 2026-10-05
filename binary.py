import math


class BinaryEncoder:
    def __init__(self, start_aux_id):
        self.next_aux_id = start_aux_id

    def encode_amo(self, variables):
        n = len(variables)
        if n <= 1:
            return []

        if n <= 4:
            clauses = []
            for i in range(n):
                for j in range(i + 1, n):
                    clauses.append([-variables[i], -variables[j]])
            return clauses

        clauses = []
        #Tính số lượng biến phụ
        k = math.ceil(math.log2(n))

        #Cấp phát k biến phụ
        Y = [self.next_aux_id + i for i in range(k)]
        self.next_aux_id += k

        #Ánh xạ mỗi biến X_i với một chuỗi nhị phân
        for i, var in enumerate(variables):
            #Chuyển chỉ số i thành chuỗi nhị phân
            binary_str = format(i, f'0{k}b')

            #X_i -> trạng thái của Y tương ứng với chuỗi nhị phân
            for bit_index, bit_value in enumerate(binary_str):
                y_var = Y[bit_index]
                if bit_value == '1':
                    # Nếu bit là 1: X_i -> Y_j
                    clauses.append([-var, y_var])
                else:
                    # Nếu bit là 0: X_i -> -Y_j
                    clauses.append([-var, -y_var])

        return clauses