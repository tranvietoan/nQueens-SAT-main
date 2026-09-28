

def binomial_amo(variables):
     clauses =[]
     n=len(variables)
     for i in range(n):
         for j in range(i+1,n):
             clauses.append([-variables[i],-variables[j]])
     return clauses


