function [objMP_star,x_star,q_star,y_star] = DA_CCGMP(L,z_setMP)
% =========================================================================
% Master Problem
% Ella
% =========================================================================
infoPrefix = '--MP--: ';
% fprintf('%s\n',infoPrefix);

%% Master Problem
ProbSetup;
% bM1 = 10^3;
bM = 10^5;
bM3 = 10^5;
bM2 = max(lambda)+1;
   
cvx_begin
cvx_solver mosek
cvx_quiet(true)
% cvx_solver_settings('MSK_IPAR_INFEAS_REPORT_AUTO','MSK_ON')

% Define variable
variable x(M, N)       nonnegative    % Varibale x(i, j)
variable q(M)          nonnegative    % Variable q(i): Unmet demand
variable y(N)          binary         % Variable y(j): Protect decision
variable vphi(M, N)    nonnegative    % Variable vphi(i, j) = q_i*ze_j
variable chi(M, N)     nonnegative    % Variable chi(i, j) = x_{i,j}*ze_j

% Lower-level duplicate variables in upper-level
variable ze(N)         binary         % Variable ze(j): Attack decision
variable tauu(N, L)    nonnegative    % Variable tau(j,l)
variable zetta(N, L)   nonnegative    % Variable zeta(j,l) = y_j*tau^l_j
variable etta(L)       nonnegative    % Variable eta(l)


% Define Optimization Problem
minimize (sum(eVec.*y) + sum(phi.*q) + gam*sum(sum(dMat.*x)) ) 

% Define constraints
  subject to
  for i = 1: M
    sum(x(i, :)) + q(i) == lambda(i);
  end

  sum(eVec.*y) <= B;

  for j = 1: N
    sum(x(:, j)) <= Cap(j)*(1-ze(j));
    ze(j) <= 1- y(j);
  end

  sum(fVec.*ze) <= BA;

  for l =1:L
    sum(hVec.*ze) >= sum(hVec.*z_setMP(:,l))+sum(tauu(:,l)-...
      z_setMP(:,l).*tauu(:,l)-zetta(:,l))+etta(l)*(BA-sum(fVec.*z_setMP(:,l)));
    for j=1:N
      zetta(j,l) <= bM3 * y(j);
      zetta(j,l) <= tauu(j,l);
      zetta(j,l) >= tauu(j,l) + bM3 * y(j) - bM3;
      tauu(j,l) <= bM;
      etta(l) <= bM;
    end
  end

cvx_end

  for j=1:N
    if abs(y(j)) <= 1e-5
      y(j) = 0;
    elseif abs(y(j)) >= 1-1e-3
      y(j) = 1;
    end
    if abs(ze(j)) <= 1e-5
      ze(j) = 0;
    elseif abs(ze(j)) >= 1-1e-3
      ze(j) = 1;
    end
  end

%% Getting results
% Optimal solution
objMP_star = cvx_optval;
x_star = x;
q_star = q;
y_star = y;
fprintf('%s Objval_MP = %4.4f\n',infoPrefix,objMP_star);
fprintf('Set of protected EN (MP): [');
fprintf('%g ', y_star'.*(1:N));
fprintf(']\n');
fprintf('Set of attacked EN (MP): [');
fprintf('%g ', ze'.*(1:N));
fprintf(']\n');
end
