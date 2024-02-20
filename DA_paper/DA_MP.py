from gurobipy import *
import numpy as np
import random


def DA_CCG_MP(e,phi,Cap,delay,llambda,B_D,B_A,rho,f,I,J,alpha,z_opt,L):
    

# Create a new model
    DA_MP = Model("DA_MP")

# Create variables
    y = DA_MP.addVars(J,L, vtype=GRB.BINARY, name="y")
    q = DA_MP.addVars(I,L, vtype=GRB.CONTINUOUS, lb = 0, name="q")
    x = DA_MP.addVars(I,J,L, vtype=GRB.CONTINUOUS, lb = 0, name="x")

# Set objective
    MP_fn = sum(e[j]*y[j] for j in range(J)) + sum(phi[i] * q[i] for i in range(I)) + sum(rho * sum(delay[i,j]*x[i,j] for j in range(J)) for i in range(I))
    DA_MP.setObjective(MP_fn, GRB.MINIMIZE)

# add constraints  
    DA_MP.addConstrs((sum(x[i,j] for j in range(J)) + q[i] == llambda[i] for i in range(I)), "Demand")
    DA_MP.addConstrs((sum(x[i,j] for i in range(I)) <= Cap[j]*(1 - z[j]) for j in range(J)), "Capacity")
    DA_MP.addConstr(sum(e[j]*y[j] for j in range(J)) <= B_D, "Budget")
    DA_MP.addConstrs((q[i] <= alpha * llambda[i] for i in range(I)), "QoS")

    



    DA_MP.setParam('OutputFlag',False)
    DA_MP.optimize()

    y_values = []
    q_values = []
    x_values = []
    for v in DA_MP.getVars():
        if v.varName.startswith('z'):
            z_values.append(v.x)
        elif v.varName.startswith('y'):
            y_values.append(v.x)
        elif v.varName.startswith('q'):
            q_values.append(v.x)
        elif v.varName.startswith('x'):
            x_values.append(v.x)

# Total number of nodes get attacked
    attacked_node = sum(z_values)

    activate_node = sum(y_values)
    print(f'Total number of nodes attacked: {attacked_node}')
    print(f'Total number of nodes activated: {activate_node}')
    print(f'Total cost: {DA_MP.objVal}')
    return attacked_node, activate_node,z_values,y_values,q_values,x_values
