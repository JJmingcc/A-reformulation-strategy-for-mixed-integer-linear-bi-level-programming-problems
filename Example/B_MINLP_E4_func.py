from gurobipy import *



def BO_E5_func(P,D,C,A,c1,c2,c3,c4,b,iter,P_F):

    demo5_BO = Model('demo5_BO')

    # Variables
    y = demo5_BO.addVars(D,C,vtype=GRB.BINARY, name='y')
    x = demo5_BO.addVars(D,P,vtype=GRB.CONTINUOUS,lb = 0, name='x')
    s = demo5_BO.addVars(D,C,vtype=GRB.CONTINUOUS,lb = 0, name='s')
    z_c = demo5_BO.addVars(D,P,vtype=GRB.CONTINUOUS, lb = 0, name='z_c')


    # dual variables non-negative
    llambda_1 = demo5_BO.addVars(P,vtype=GRB.CONTINUOUS, lb = 0, name='llambda_1')
    llambda_2 = demo5_BO.addVars(D,vtype=GRB.CONTINUOUS, lb = 0, name='llambda_2')
    llambda_3 = demo5_BO.addVars(D,P,vtype=GRB.CONTINUOUS, lb = 0, name='llambda_3')
    llambda_4 = demo5_BO.addVars(D,P,vtype=GRB.CONTINUOUS, lb = 0, name='llambda_4')
    mu = demo5_BO.addVars(D,P,vtype=GRB.CONTINUOUS, name='mu')

    # Objective function of leader problem
    P_L = sum(c1[d,c] * y[d,c] for d in range(D) for c in range(C)) + sum(c2[d,p] * x[d,p] for d in range(D) for p in range(P))
    demo5_BO.setObjective(P_L, GRB.MINIMIZE)

    # Upper level Constraints
    demo5_BO.addConstrs(sum(s[d,c] for d in range(D)) >= b[c] for c in range(C))
    demo5_BO.addConstrs(s[d,c] <= 35*y[d,c] for d in range(D) for c in range(C))

    # Lower problem by using KKT conditions
    # primal feasbility
    demo5_BO.addConstrs(sum(x[d,p] for d in range(D)) <= A[p] for p in range(P))
    demo5_BO.addConstrs(x[d,p] <= 100 * z_c[d,p] for d in range(D) for p in range(P))
    demo5_BO.addConstrs(sum(s[d,c] for c in range(C)) - sum(x[d,p] for p in range(P)) <= 0 for d in range(D))   


    # Stationary feasbility
    demo5_BO.addConstr(sum(c3[d,p] for p in range(P) for d in range(D)) + sum(llambda_1[p] for p in range(P)) - sum(llambda_2[d] for d in range(D)) + sum(llambda_3[d,p] for p in range(P) for d in range(D)) - sum(llambda_4[d,p] for p in range(P) for d in range(D)) == 0)
    demo5_BO.addConstr(sum(c4[d,p] for p in range(P) for d in range(D)) - sum(100 * llambda_3[d,p] for p in range(P) for d in range(D)) + sum(mu[d,p] * (2 * z_c[d,p] - 1) for p in range(P) for d in range(D)) == 0) 
    
    # demo5_BO.addConstrs(c4[d,p] - 100 * llambda_3[d,p] + mu[d,p] * (2 * z_c[d,p] -1) == 0 for d in range(D) for p in range(P))
    # demo5_BO.addConstrs(c3[d,p] + llambda_1[p] - llambda_2[d] + llambda_3[d,p] - llambda_4[d,p] == 0 for d in range(D) for p in range(P))
    # demo5_BO.addConstrs(sum(c3[d,p] for p in range(P) for d in range(D)) + sum(llambda_1[p] for p in range(P)) - sum(llambda_2[d] for d in range(D)) + sum(llambda_3[d,p] for p in range(P) for d in range(D)) + sum(llambda_4[d,p] for p in range(P) for d in range(D)) == 0)
    # Complementary slackness 
    demo5_BO.addConstrs(llambda_1[p] * (sum(x[d,p] for d in range(D)) - A[p]) == 0 for p in range(P))
    demo5_BO.addConstrs(llambda_2[d] * (sum(s[d,c] for c in range(C)) - sum(x[d,p] for p in range(P))) == 0 for d in range(D))
    demo5_BO.addConstrs(llambda_3[d,p] * (x[d,p] - 100 * z_c[d,p]) == 0 for d in range(D) for p in range(P))
    demo5_BO.addConstrs(llambda_4[d,p] * x[d,p] == 0 for d in range(D) for p in range(P) )
    
    # Binary reformulation
    demo5_BO.addConstrs(z_c[d,p] * (z_c[d,p] - 1) == 0 for p in range(P) for d in range(D))

    if iter >= 2: 
        # for the first iteration, we don't have P_F_temp, we only have P_F from second iteration
        P_F_temp = demo5_BO.addVar(vtype=GRB.CONTINUOUS, name='P_F_temp')
        demo5_BO.addConstr(P_F_temp == sum(c3[d,p] * x[d,p] for p in range(P) for d in range(D)) + sum(c4[d,p] * z_c[d,p] for p in range(P) for d in range(D)))
        demo5_BO.addConstr(P_F_temp <= P_F - 0.1)
        # demo5_BO.addConstr(P_F_temp >= 100)


 
    demo5_BO.params.NonConvex = 2
    demo5_BO.setParam('OutputFlag',False)
    demo5_BO.optimize()


    zc_values = []
    y_values = []
    s_values = []
    x_values = []
    for v in demo5_BO.getVars():
        if v.varName.startswith('z'):
            zc_values.append(v.x)
        elif v.varName.startswith('s'):
            s_values.append(v.x)
        elif v.varName.startswith('x'):
            x_values.append(v.x)
        elif v.varName.startswith('y'):
            y_values.append(v.x)

    
    P_L = demo5_BO.objVal

    if iter >= 2: 
        P_F= P_F_temp.X
    else:
        P_F = P_F


    return P_L, P_F ,zc_values, y_values, s_values, x_values
