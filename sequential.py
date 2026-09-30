class SequentialEncoder:
    def __init__(self, start_aux_id):
    # Bộ đếm cấp phát ID
        self.next_aux_id = start_aux_id
    def get_new_var(self):
    # Hàm sinh ID mới cho biến phụ
        var_id = self.next_aux_id
        self.next_aux_id+=1
        return var_id
    def encode_amo(self,variables):
    # Luật AMO
        n=len(variables)
        if n<=1:
            return []
        clauses=[]

        s=[self.get_new_var() for _ in range(n-1)]
    # Luật biên trái x_i-> s_i
        clauses.append([-variables[0],s[0]])
    # Luật ở giữa 1<i<n
        for i in range(1,n-1):
            x_i=variables[i]
            s_prev=s[i-1]
            s_cur=s[i]

            # Luật truyền tin
            clauses.append([-s_prev,s_cur])
            clauses.append([-x_i,s_cur])

            # Luật cấm
            clauses.append([-s_prev,-x_i])
    # Luật biên phải
        clauses.append([-s[n-2],-variables[n-1]])

        return clauses