function [obj_val1,z_star] = DA_CCGSP1(y_set)
% =========================================================================
% SubProblem 1
% Ella
% =========================================================================
infoPrefix = '--SP1--: ';
% fprintf('%s\n',infoPrefix);
%% Parameters
ProbSetup;

%% Subproblem 1
cvx_begin
cvx_solver mosek
cvx_quiet(true)

% Define variable
variable z(N)         binary         % Variable z(j): Attack decision
  
% Define Optimization Problem
maximize (sum(hVec.*z))
subject to
  for j = 1:N
    z(j) <= 1-y_set(j); 
    sum(fVec.*z) <= BA; 
  end

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
obj_val1 = cvx_optval;
fprintf('Set of attacked EN (SP1): [');
fprintf('%g ', z_star'.*(1:N));
fprintf(']\n');
fprintf('%s Attacker_obj = %4.4f\n',infoPrefix,obj_val1);
end