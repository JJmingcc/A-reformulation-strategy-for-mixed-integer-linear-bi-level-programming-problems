% ==================================================
% DA paper
% 10-25-22
% Anh-Duong
% ==================================================
% ==================================================

clear all
close all
infoPrefix=sprintf('--%s--',mfilename); % all info displayed by this function includes this prefix

saveDiary=true; % flag to save diary
resultsDir='results'; % directory to save results

% create resultsDir if doesn't exist
if ~exist(resultsDir, 'dir')
  mkdir(resultsDir);
  fprintf('%s mkdir %s\n',infoPrefix,resultsDir);
end

% keep a diary for the run
if(saveDiary)
  diaryFilename=sprintf('%s/diary.txt',resultsDir);
  fprintf('%s Saving Command Window text to %s\n',infoPrefix,diaryFilename);   
  diary(diaryFilename); 
  diary on;
end

% print current time
fprintf('%s\n',datestr(now));

%% Parameters
ProbSetup;
M_0 = 10^5;
M_1 = 10^5*ones(N,1);
M_2 = 10^5;
bM = max(lambda)*10;

obj_val_Vec = [];
maxIter = 10;
f_best = -10^8;
%%
for K = MaxK % K: maximum number of node failures
 for Iter = 0:maxIter
% Initialization
% Define Subproblem
  cvx_begin
  cvx_quiet(true)
  cvx_solver Mosek
    
% Define variable
  variable x(M, N)       nonnegative    % Varibale x(i, j): workload from area i assigned to EN j
  variable q(M)          nonnegative    % Variable q(i): Unmet demand
  variable z(N)          binary         % Variable z(j): Attack decision (binary)
  variable y(N)          binary         % Variable y(j): Protect decision (binary)
  variable Pii(N)        nonnegative    % Variable Pii(j): Dual variable
  variable Sigg          nonnegative    % Variable Sigg: Dual variable
  variable muy(N)                       % Variable mu(j): Dual variable
  variable deltta(N)                    % Variable deltta(j): Linearized variable
  variable u_1(N)        binary         % Variable u_1(j)
  variable u_2           binary         % Variable u_2
  variable chi(M, N)     nonnegative    % Variable chi(i, j) = x_{i,j}*z_j
    
% Define objective func
  minimize (sum(eVec.*y) + sum(phi.*q) + gam*sum(sum(dMat.*x)) ) 
    
% Define constraints
  subject to
  % chi(i, j) = x_{i,j}*z_j
  for i = 1:M
    for j = 1:N
      chi(i,j) <= bM * z(j);
      chi(i,j) <= x(i,j);
      chi(i,j) >= x(i,j) + bM * z(j) - bM;
    end
  end

%   sum(Cap.*z) >= f_best+0.1;
%   sum(q) >= f_best+0.1;
  sum(sum(chi)) >= f_best+0.1;

  for j = 1: N
    Cap(j)*(1-z(j)) - sum(x(:, j)) >= 0;
%     Pii(j) + 2*deltta(j) - muy(j) + Sigg == 0;
%     Pii(j) + 2*deltta(j) - muy(j) + Sigg - Cap(j) == 0;
%     Pii(j) + 2*deltta(j) - muy(j) + Sigg - hVec(j) == 0;
    Pii(j) + 2*deltta(j) - muy(j) + fVec(j)*Sigg - hVec(j) == 0;

    % Linearize
    % deltta(j) = muy(j)*z(j);
    deltta(j) <= M_0 * z(j);
    deltta(j) <= muy(j);
    deltta(j) >= -M_0 * z(j);
    deltta(j) >= muy(j) + M_0 * z(j) - M_0;
    
    z(j) <= 1 - y(j);
    1 - y(j) - z(j) <= u_1(j)*M_1(j);  
    Pii(j) <= (1 - u_1(j))*M_1(j);
  end

  for i = 1: M
    sum(x(i, :)) + q(i) == lambda(i);
  end

  sum(eVec.*y) <= B;
% y(2)==1;y(5)==1;y(7)==1;y(9)==1;y(10)==1;
% y(1)==0;y(3)==1;y(4)==1;y(6)==0;y(8)==1;
  
  sum(fVec.*z) <= BA;
  K - sum(z) <= u_2*M_2;
  Sigg <= (1 - u_2)*M_2;
  
cvx_end

for j=1:N
    if abs(z(j)) <= 1e-5
      z(j) = 0;
    elseif abs(z(j)) >= 1-1e-3
      z(j) = 1;
    end
    if abs(y(j)) <= 1e-5
      y(j) = 0;
    elseif abs(y(j)) >= 1-1e-3
      y(j) = 1;
    end
end

fprintf('Iter=%d: cvx_status=%s, Obj_val=%4.4f, Obj_lower_val=%4.4f \n',Iter,cvx_status,cvx_optval,sum(sum(hVec.*z)));
% fprintf('K=%d \n',K);
% fprintf('Set of attacked EN: [');
% fprintf('%g ', z'.*(1:N));
% fprintf(']\n');
% fprintf('Set of protected EN: [');
% fprintf('%g ', y'.*(1:N));
% fprintf(']\n');

%% Getting results
% Status of solving prob
    if strcmp(cvx_status,'Infeasible')
      break
    else
      f_best = sum(sum(hVec.*z));
    end

% Optimal solution
    z_star = z;
    y_star = y;
    x_star = x;
    q_star = q;
    f_star = cvx_optval;
 end
% Optimal value
    obj_val = f_star;
    C_unmet = sum(phi.*q_star);
    C_delay = full(sum(sum(dMat.*x_star)));
    
fprintf('K=%d \n',K);
fprintf('Set of attacked EN: [');
fprintf('%g ', z_star'.*(1:N));
fprintf(']\n');
fprintf('Set of protected EN: [');
fprintf('%g ', y_star'.*(1:N));
fprintf(']\n');
fprintf('Optimal value:%4.4f, Attacker_obj = %4.4f \n',obj_val,f_best);

save(sprintf('%s/resultsK%d.mat',resultsDir,K),'x_star','z_star','y_star','q_star','obj_val','gam','beta','N','M','K','eVec','dMat','lambda');

obj_val_Vec = [obj_val_Vec,obj_val];
end
save(sprintf('%s/results.mat',resultsDir),'obj_val_Vec','gam','beta','N','M','K','eVec','dMat','lambda');

if(saveDiary)
  diary off;
end
