from gurobipy import *



def BO_Eample_func(iter,P_F):
    # Here we gonna considder a mixed integer bilevel optimization problem
    # example 1 in paper
    demo2_BO = Model('demo2_BO')

    # Variables
    x_1 = demo2_BO.addVar(vtype=GRB.CONTINUOUS,lb = -10, name='x_1')
    x_2 = demo2_BO.addVar(vtype=GRB.CONTINUOUS,lb = -10, name='x_2')
    x_3 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, name='x_3')
    P_F_temp = demo2_BO.addVar(vtype=GRB.CONTINUOUS, name='P_F_temp')
    # y_1 = demo2_BO.addVar(vtype=GRB.BINARY, name='y_1')
    y_3 = demo2_BO.addVar(vtype=GRB.BINARY, name='y_3')
    # y_2 = demo2_BO.addVar(vtype=GRB.BINARY, name='y_2')
    y_c1 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_c1')
    y_c2 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_c2')
    mu1 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, name='mu1')
    mu2 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, name='mu2')

    # dual variables
    llambda_1 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_1')
    llambda_2 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_2')
    llambda_3 = demo2_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_3')


    # Objective function
    P_L = 4 * x_1 - x_2 + x_3 + 5 * y_c1 - 6 * y_3
    demo2_BO.setObjective(P_L, GRB.MINIMIZE)
    # Constraints
    # primal feasbility
    # demo2_BO.addConstr(x_1 >= -10)
    # demo2_BO.addConstr(x_1 <= 10)
    # demo2_BO.addConstr(x_2 >= -10)
    # demo2_BO.addConstr(x_2 <= 10)

    demo2_BO.addConstr(6.4 * x_1 + 7.2 * x_2 + 2.5 * x_3 <= 11.5)
    demo2_BO.addConstr(-8 * x_1 - 4.9 * x_2  - 3.2 * x_3 <= 5)
    demo2_BO.addConstr(3.3 * x_1 + 4.1 * x_2 + 0.02 * x_3 + 4 * y_c1 + 4.5 * y_c2 + 0.5 * y_3 <= 1)

    # stationary variable
    demo2_BO.addConstr(-2 + 2.5 * llambda_1 - 3.2 * llambda_2 + 0.02 * llambda_3 == 0)
    demo2_BO.addConstr(-1 + 4 * llambda_3 + mu1 * (2 * y_c1 - 1) == 0)
    demo2_BO.addConstr(5 + 4.5 * llambda_3 + mu2 * (2 * y_c2 - 1) == 0) 

    # Complementary slackness
    demo2_BO.addConstr(llambda_1 * (6.4 * x_1 + 7.2 * x_2 + 2.5 * x_3 - 11.5) == 0)
    demo2_BO.addConstr(llambda_2 * (-8 * x_1 - 4.9 * x_2  - 3.2 * x_3 - 5) == 0)
    demo2_BO.addConstr(llambda_3 * (3.3 * x_1 + 4.1 * x_2 + 0.02 * x_3 + 4 * y_c1 + 4.5 * y_c2 + 0.5 * y_3 - 1) == 0)
    demo2_BO.addConstr(y_c1 * (y_c1 - 1) == 0)
    demo2_BO.addConstr(y_c2 * (y_c2 - 1) == 0)  

    demo2_BO.params.NonConvex = 2
    demo2_BO.addConstr(P_F_temp == - x_1 + x_2 - 2 * x_3 - y_c1 + 5 * y_c2 + y_3)

    if iter >= 2: 
        demo2_BO.addConstr(P_F_temp == - x_1 + x_2 - 2 * x_3 - y_c1 + 5 * y_c2 + y_3)
        demo2_BO.addConstr(P_F_temp <= P_F - 0.1)
    else:
        demo2_BO.addConstr(P_F_temp == - x_1 + x_2 - 2 * x_3 - y_c1 + 5 * y_c2 + y_3)

    demo2_BO.setParam('OutputFlag',False)
    demo2_BO.optimize()

    x1_value = x_1.X
    x2_value = x_2.X
    x3_value = x_3.X
    y1_value = y_c1.X 
    y2_value = y_c2.X 
    y3_value = y_3.X
    y_c1_value = y_c1.X
    y_c2_value = y_c2.X 
    P_L = demo2_BO.objVal


    P_F_temp = P_F_temp.X

    return P_L, x1_value, x2_value, x3_value, y1_value, y2_value, y3_value, y_c1_value, y_c2_value, P_F_temp




def  BO_E1_func(iter,P_F):
    # Here we gonna considder a mixed integer bilevel optimization problem
    # example 1 in paper
    demo1_BO = Model('demo1_BO')

    # Variables
    x = demo1_BO.addVar(vtype=GRB.CONTINUOUS,lb = 0, name='x')
    y_c = demo1_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='y_c')
    # dual variables
    llambda_1 = demo1_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_1')
    llambda_2 = demo1_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_2')
    llambda_3 = demo1_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='llambda_3')
    mu_1 = demo1_BO.addVar(vtype=GRB.CONTINUOUS, lb = 0, name='mu_1')


    # Objective function
    obj_f = (x - 2)**2 + (y_c - 2)**2
    demo1_BO.setObjective(obj_f, GRB.MINIMIZE)

    # Constraints
    # primal feasbility
    demo1_BO.addConstr(-2 * x + 2 * y_c + 5 <= 0)
    demo1_BO.addConstr(x - y_c -1 <= 0)
    demo1_BO.addConstr(2 * x + 2 * y_c - 8 <= 0)

    # stationary conditions 
    demo1_BO.addConstr(2*y_c - 2 * llambda_1 - llambda_2 + 2 * llambda_3 + mu_1 * (3 * y_c**2 - 2 * y_c ) == 0)
    demo1_BO.addConstr(llambda_1 * (-2 * x - 2* y_c + 5) == 0)
    demo1_BO.addConstr(llambda_2 * (x - y_c - 1) == 0)
    demo1_BO.addConstr(llambda_3 * (2 * x + 2 * y_c - 8) == 0)
    demo1_BO.addConstr(y_c * (y_c - 1) * (y_c - 2) == 0) 


    demo1_BO.params.NonConvex = 2

    demo1_BO.optimize()
    if iter >= 2: 
        demo1_BO.addConstr(P_F_temp == - x_1 + x_2 - 2 * x_3 - y_c1 + 5 * y_c1 + y_3)
        demo1_BO.addConstr(P_F_temp <= P_F - 0.1)

    demo1_BO.setParam('OutputFlag',False)
    demo1_BO.optimize()

    x1_value = x_1.X
    x2_value = x_2.X
    x3_value = x_3.X
    y1_value = y_c1.X 
    y2_value = y_c2.X 
    y3_value = y_3.X
    y_c1_value = y_c1.X
    y_c2_value = y_c2.X 
    P_L = demo1_BO.objVal
