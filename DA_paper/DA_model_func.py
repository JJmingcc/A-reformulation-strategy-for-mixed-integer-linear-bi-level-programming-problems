from gurobipy import *


def DA_model_func(e,phi,Cap,delay,llambda,B_D,B_A,rho,f,h,I,J,P_F,iter):
    
    print("iter:", iter)
# Create a new model
    DA_model = Model("DA_decomp")

# Create variables
    z_c = DA_model.addVars(J, vtype=GRB.CONTINUOUS, lb = 0, ub = 1, name="z")
    # z = DA_model.addVars(J, vtype=GRB.BINARY,  name="z")
    y = DA_model.addVars(J, vtype=GRB.BINARY, name="y")
    q = DA_model.addVars(I, vtype=GRB.CONTINUOUS, lb = 0, name="q")
    x = DA_model.addVars(I, J, vtype=GRB.CONTINUOUS, lb = 0, name="x")
# dual variables
    dual_pi = DA_model.addVars(J, vtype=GRB.CONTINUOUS, lb = 0, name="dual_pi")
    dual_mu = DA_model.addVars(J, vtype=GRB.CONTINUOUS, lb = 0, name="dual_mu") 
    dual_sigma = DA_model.addVar(lb = 0, vtype=GRB.CONTINUOUS, name="dual_sigma")  


# Set objective
    P_L = sum(e[j]*y[j] for j in range(J)) + sum(phi[i] * q[i] for i in range(I)) + sum(rho * sum(delay[i,j]*x[i,j] for j in range(J)) for i in range(I))
    DA_model.setObjective(P_L, GRB.MINIMIZE)

# Upper level constraints  
    DA_model.addConstrs((sum(x[i,j] for j in range(J)) + q[i] == llambda[i] for i in range(I)), "Demand")
    DA_model.addConstrs((sum(x[i,j] for i in range(I)) <= Cap[j] * (1 - z_c[j]) * y[j] for j in range(J)), "Capacity")
    DA_model.addConstr(sum(e[j]*y[j] for j in range(J)) <= B_D, "Budget")
    # primal feasible for lower level problem
    DA_model.addConstrs(1 - y[j] - z_c[j] >= 0 for j in range(J))
    DA_model.addConstr(B_A - sum(f[j]*z_c[j] for j in range(J)) >= 0)
    DA_model.addConstrs(z_c[j] * (z_c[j] - 1 ) == 0 for j in range(J))
    # stationary condition
    DA_model.addConstrs(-h[j] + dual_pi[j] + f[j] * dual_sigma  + dual_mu[j] * (2 * z_c[j] - 1) == 0 for j in range(J))
    # complementary slackness
    DA_model.addConstrs(dual_pi[j] * (y[j] + z_c[j] - 1) == 0 for j in range(J))
    DA_model.addConstrs(dual_mu[j] * z_c[j] == 0 for j in range(J)) 
    DA_model.addConstr(dual_sigma * (B_A - sum(f[j] * z_c[j] for j in range(J))) == 0)


    if iter >= 1: 
        P_F_temp = DA_model.addVar(vtype=GRB.CONTINUOUS, name="P_F_temp")
        DA_model.addConstr(P_F_temp == sum(h[j]*z_c[j] for j in range(J)))
        DA_model.addConstr(P_F_temp >= P_F + 0.1)

    DA_model.setParam('OutputFlag',False)
    DA_model.params.NonConvex = 2
    DA_model.optimize()

    z_values = []
    y_values = []
    q_values = []
    x_values = []
    for v in DA_model.getVars():
        if v.varName.startswith('z'):
            z_values.append(v.x)
        elif v.varName.startswith('y'):
            y_values.append(v.x)
        elif v.varName.startswith('q'):
            q_values.append(v.x)
        elif v.varName.startswith('x'):
            x_values.append(v.x)

            
    if iter >= 1: 
        P_F_temp = P_F_temp.X
    else:
        P_F_temp = 0
    P_L = DA_model.objVal
# Total number of nodes get attacked
    attacked_node = sum(z_values)
    activate_node = sum(y_values)

    return attacked_node, activate_node,z_values,y_values,q_values,x_values,P_F_temp,P_L
