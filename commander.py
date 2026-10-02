class CommanderEncoder:
    def __init__(self, start_aux_id ,group_size=3):
    # ID cho các biến phụ
        self.next_aux_id=start_aux_id
        self.group_size=group_size
    def get_new_var(self):
        var_id=self.next_aux_id
        self.next_aux_id +=1
        return var_id
    def encode_amo(self,variables):
        n= len(variables)
        if(n<=1):
            return []

        clauses=[]
    # Dùng Binomial(Pairwise) nếu số lượng phần tử < group_size
        if n<= self.group_size:
            for i in range(n):
                for j in range(i+1,n):
                    clauses.append([-variables[i], -variables[j]])
            return clauses

    # Chia nhóm các biến(Partitioning)
        groups=[variables[i:i+self.group_size] for i in range(0,n,self.group_size)]
        commander=[]

        for group in groups:
            if len(group)==1:
                commander.append(group[0])
            else:
                c=self.get_new_var()
                commander.append(c)
    # Luật AMO nội bộ trong các nhóm
                for i in range(len(group)):
                    for j in range(i+1,len(group)):
                        clauses.append([-group[i], -group[j]])
    # Luật chỉ huy sai(tất cả đều sai )
                for v in group:
                    clauses.append([c,-v])
    #Luật chỉ huy đúng( có ít nhất 1 đúng)
                alo_clause= [-c]+group
                clauses.append(alo_clause)

    # AMO giữa các chỉ huy
        clauses.extend(self.encode_amo(commander))
        return clauses