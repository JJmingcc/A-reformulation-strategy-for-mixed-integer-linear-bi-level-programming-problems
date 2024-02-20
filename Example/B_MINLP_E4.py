from gurobipy import *
import numpy as np
import B_MINLP_E4_func



# Parameters

# Number of plant
P  =2
# Number of distribution centers
D = 2
# Number of customers   
C = 3

# Parameter

A_matrix = [135, 100]
# c1 with dimension d by c
c1_matrix = [[75,60,50],[80,30,65]]
# c2 - c3 with dimension d by p
c2_matrix  = [[21,30],[26,25]]
c3_matrix  = [[20,25],[20,25]]
c4_matrix  = [[100,80],[110,70]]
b = [55,65,15]

A = np.array(A_matrix)
c1 = np.array(c1_matrix)   
c2= np.array(c2_matrix)
c3 = np.array(c3_matrix)
c4 = np.array(c4_matrix)   
b = np.array(b)


K = 15 

P_F = 100
for i in range(K):
    iter = i+1
    P_L, P_F_temp_list,zc_values, y_values, s_values, x_values = B_MINLP_E4_func.BO_E5_func(P,D,C,A,c1,c2,c3,c4,b,iter,P_F)

    print("##################################Interation:", iter, "##################################") 
    print(f'Lower-level obj: {P_F}')
    print(f'Upper-cost: {P_L}')
    print(f'zc_values: {zc_values}')
    print(f'y_values: {y_values}')
    print(f's_values: {s_values}')
    print(f'x_values: {x_values}')
    print(f'P_F_temp_list: {P_F_temp_list}')



