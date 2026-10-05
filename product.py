import math
class ProductEncoder:
    def __init__(self, start_aux_id):
        self.next_aux_id=start_aux_id

    def encode_amo(self,variables):
        n=len(variables)
        if n<=1:
            return []
        if n<=4:
            clauses=[]
            for i in range(n):
                for j in range(i+1,n):
                    clauses.append([-variables[i],-variables[j]])
            return clauses
        # Tính toán kích thước lưới ảo
        p=math.ceil(math.sqrt(n))
        q=math.ceil(n/p)

        #Sinh biến phụ
        R = [self.next_aux_id + i for i in range(p)]
        self.next_aux_id += p

        C = [self.next_aux_id + i for i in range(q)]
        self.next_aux_id += q

        clauses = []

        #Luật chiếu tọa độ( luật truyền tin)
        for k, var in enumerate(variables):
            u = k // q
            v = k % q

            clauses.append([-var, R[u]])
            clauses.append([-var, C[v]])

        #Luật AMO trên hàng
        for i in range(p):
            for j in range(i+1,p):
                clauses.append([-R[i],-R[j]])

        #Luật AMO trên cột
        for i in range(q):
            for j in range(i+1,q):
                clauses.append([-C[i],-C[j]])

        return clauses
