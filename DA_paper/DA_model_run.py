
from gurobipy import *
import numpy as np
import random
import DA_model_func



J = 5
I = 5

random.seed(2)
def generate_random_vector(lp,up,size):
    return np.random.uniform(lp,up,size)


# Cost parameter generate
# Activation cost for activate EN (j)
e = generate_random_vector(1,1,J)
# unmet demand for AP (j)
phi = generate_random_vector(10,20,I)

# Resource capacity for each EN j
Cap = generate_random_vector(30,50,J)

# generate delay matrix between AP i and EN j
delay = np.random.uniform(5,30,(I,J))

# generate the demand vector at each AP i
llambda = generate_random_vector(10,30,I)

# Total Budget
B_D = J
# delay penalty
rho = 0.01
# Damage from of attacking a node from attacker perspective/how important the node to the defender
h = generate_random_vector(10,20,J)


# budget for attacking
B_A = 3
# cost of attacking a node
# if f = ones(J,1), then the cost of attacking each node is the same and this constraints will be simplied to sum_{j} z[j] <= B_A, where B_a is number of node that attacker can attack
f = generate_random_vector(1,1,J) 

K = 15

P_F = 0
for i in range(K):
    iter = i+1
    attacked_node, activate_node,z_values,y_values,q_values,x_values,P_F_temp,P_L = DA_model_func.DA_model_func(e,phi,Cap,delay,llambda,B_D,B_A,rho,f,h,I,J,P_F,iter)
    P_F = P_F_temp

    print("##################################Interation:", iter, "##################################") 
    print("z", z_values)
    print("y", y_values)
    print(f'Total number of nodes attacked: {attacked_node}')
    print(f'Total number of nodes activated: {activate_node}')
    print(f'Lower-Total damage: {np.sum(h*z_values)}')
    print(f'Upper-cost: {P_L}')
