from gurobipy import *
import numpy as np
import random
import scipy
import math



def BO_E5_func(iter,P_F):
# Here we gonna considder a mixed integer bilevel optimization problem

# example 1 in paper
    demo3_BO = Model('demo3_BO')

    # Variables
    xp1 = demo3_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='xp1')
    xp2 = demo3_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='xp2')
    xq1 = demo3_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='xq1')
    xq2 = demo3_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='xq2')
    xq3 = demo3_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='xq3')  

    yp1 = demo3_BO.addVar(vtype=GRB.BINARY, name= 'yp1')
    yp2 = demo3_BO.addVar(vtype=GRB.BINARY, name= 'yp2')

    y_cq1 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_cq1')
    y_cq2 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_cq2')
    y_cq3 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_cq3')

    # dual variables
    llambda_1 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_1')
    llambda_2 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_2')
    llambda_3 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_3')
    llambda_4 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_4')
    llambda_5 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_5')
    llambda_6 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_6')
    llambda_7 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_7') 

    mu1 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, name='mu1')
    mu2 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, name='mu2') 
    mu3 = demo3_BO.addVar(vtype=GRB.CONTINUOUS, name='mu3') 

    P_F_temp = demo3_BO.addVar(vtype=GRB.CONTINUOUS, name='P_F_temp')
    # Objective function
    
    P_L = 30 * xp1 + 20 * xp2 - 50 * yp1 - 100 * yp2 + 10 * xq2 + 10 * xq3
    demo3_BO.setObjective(P_L, GRB.MAXIMIZE)

    # Upper level Constraints
    demo3_BO.addConstr(xp1 + xp2 <= 10)
    demo3_BO.addConstr(xp1 <= 10 * yp1)
    demo3_BO.addConstr(xp2 <= 10 * yp2)
    demo3_BO.addConstr(yp1 + yp2 <= 1)
    

    # primal feasbility
    demo3_BO.addConstr(xq1 + xq2 + xq3 - 10 <= 0)
    demo3_BO.addConstr(xq1 <= 10 * y_cq1)
    demo3_BO.addConstr(xq2 <= 10 * y_cq2)
    demo3_BO.addConstr(xq3 <= 10 * y_cq3)
    demo3_BO.addConstr(y_cq1 + y_cq2 + y_cq3 <= 1)
    demo3_BO.addConstr(xq1 + xq2 <= xp1)
    demo3_BO.addConstr(xq3 <= xp2)

    # stationary conditions
    demo3_BO.addConstr(40 - llambda_1 - llambda_2 - llambda_6 == 0)
    demo3_BO.addConstr(40 - llambda_1 - llambda_3 - llambda_6 == 0)
    demo3_BO.addConstr(65 - llambda_1 - llambda_4 - llambda_7 == 0)
    demo3_BO.addConstr(-100 + 10 * llambda_2 - llambda_5 - mu1 * (2* y_cq1  - 1) == 0)
    demo3_BO.addConstr(-250 + 10 * llambda_3 - llambda_5 - mu2 * (2* y_cq2  - 1) == 0)
    demo3_BO.addConstr(-100 + 10 * llambda_4 - llambda_5 - mu3 * (2* y_cq3  - 1) == 0)

    # stationary conditions 
    demo3_BO.addConstr(llambda_1 * (xq1 + xq2 + xq3 - 10) == 0)
    demo3_BO.addConstr(llambda_2 * (xq1 - 10 * y_cq1) == 0)
    demo3_BO.addConstr(llambda_3 * (xq2 - 10 * y_cq2) == 0)
    demo3_BO.addConstr(llambda_4 * (xq3 - 10 * y_cq3) == 0)
    demo3_BO.addConstr(llambda_5 * (y_cq1 + y_cq2 + y_cq3 - 1) == 0)
    demo3_BO.addConstr(llambda_6 * (xq1 + xq2 - xp1) == 0)  
    demo3_BO.addConstr(llambda_7 * (xq3 - xp2) == 0)

    demo3_BO.addConstr(y_cq1 * (y_cq1 - 1)== 0) 
    demo3_BO.addConstr(y_cq2 * (y_cq2 - 1)== 0) 
    demo3_BO.addConstr(y_cq3 * (y_cq3 - 1)== 0)
    if iter >= 2: 
        demo3_BO.addConstr(P_F_temp == 40 * xq1 + 40 * xq2 + 65 * xq3 - 100 * y_cq1 - 250 * y_cq2 - 100 * y_cq3)
        demo3_BO.addConstr(P_F_temp >= P_F + 0.1)


    demo3_BO.params.NonConvex = 2
    demo3_BO.setParam('OutputFlag',False)
    demo3_BO.optimize()

    if demo3_BO.status == 'infeasible':
        print("The problem is infeasible.")
    xq1_value = xq1.X
    xq2_value = xq2.X
    xq3_value = xq3.X
    xp1_value = xp1.X 
    xp2_value = xp2.X
    y_cq1_value = y_cq1.X
    y_cq2_value = y_cq2.X 
    y_cq3_value = y_cq3.X 
    P_L = demo3_BO.objVal


    if iter >= 2: 
        P_F_temp = P_F_temp.X
    else:
        P_F_temp = 0

    return P_L, xq1_value, xq2_value, xq3_value, xp1_value, xp2_value, y_cq1_value, y_cq2_value, y_cq3_value, P_F_temp


