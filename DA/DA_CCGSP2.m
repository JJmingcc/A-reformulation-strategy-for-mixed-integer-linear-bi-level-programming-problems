function obj_val2 = DA_CCGSP2(obj_SP1,z_set)
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
variable x(M, N)       nonnegative    % Varibale x(i, j)
variable q(M)          nonnegative    % Variable q(i): Unmet demand

% Define Optimization Problem
minimize (sum(phi.*q) + gam*sum(sum(dMat.*x)) ) 

% Define constraints
  subject to

  for j = 1: N
    sum(x(:, j)) <= Cap(j)*(1-z_set(j));
  end
  
  for i = 1: M
    sum(x(i, :)) + q(i) == lambda(i);
  end

cvx_end

%% Getting results
% Optimal solution
obj_val2 = cvx_optval;
end