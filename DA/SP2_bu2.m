function [obj_val2,z_star] = DA_CCGSP2(obj_SP1,x_set,q_set,y_set,K)
% =========================================================================
% SubProblem 2
% Ella
% =========================================================================
infoPrefix = '--SP2--: ';
% fprintf('%s\n',infoPrefix);
%% Parameters
ProbSetup;

%% Subproblem 2
cvx_begin
cvx_solver mosek
cvx_quiet(true)

% Define variable
variable z(N)         binary         % Variable z(j): Attack decision

% Define Optimization Problem
minimize (sum(phi.*q_set) + gam*sum(sum(dMat.*x_set)) ) 

% Define constraints
  subject to

  for j = 1:N
    z(j) <= 1-y_set(j); 
    sum(z) <= K; 
  end

  (sum(x_set,1)*z) >= obj_SP1;
cvx_end

  for j=1:N
    if abs(z(j)) <= 1e-5
      z(j) = 0;
    elseif abs(z(j)) >= 1-1e-3
      z(j) = 1;
    end
  end

%% Getting results
% Optimal solution
z_star = z;
obj_val2 = cvx_optval;
end