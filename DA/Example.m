clear all
close all
f_best = 100000;
M = 100;

for Iter = 1:1000
%% Initialization
%% Define Subproblem
  cvx_begin
  cvx_quiet(true)
  cvx_solver Mosek
    
% Define variable
  variable  x(3)              
  variable  y(3)          binary    
  variable  lambdaa(3)    nonnegative
  variables nu1(3) nu2(3) nu3(3)         
  variable  sig(3)        nonnegative
  variable  muy(2)
  variable  gammaa(2)     
  
% Define objective func
  minimize ([4,-1,1]*x + [5,0,-6]*y) 
    
% Define constraints
  subject to
  
  [-1,1,-2]*x + [-1,5,1]*y <= f_best-0.1;

  x(1) >= -10;
  x(2) >= -10;
  x(1) <= 10;
  x(2) <= 10;

  [6.4,7.2,2.5]*x - 11.5 <= 0;
  [-8,-4.9,-3.2]*x - 5 <= 0;
  [3.3,4.1,0.02]*x + [4,4.5,0.5]*y - 1 <= 0;

%   gammaa=muy*y means gammaa=muy if y=1 and gammaa=0 if y=0
  for i =1:2
      gammaa(i) <= M*y(i);
      gammaa(i) >= -M*y(i);
      gammaa(i) <= muy(i) + M*(1-y(i));
      gammaa(i) >= muy(i) - M*(1-y(i));
  end
  -2+[2.5,-3.2,0.02]*lambdaa == 0;
  -1+4*lambdaa(3)+2*gammaa(1)-muy(1) == 0;
  5+4.5*lambdaa(3)+2*gammaa(2)-muy(2) == 0;

  %   nu1=lambdaa1*x
  %   nu2=lambdaa2*x
  %   nu3=lambdaa3*x
  %   sig=lambdaa*y
  for i =1:3
      nu1(i) <= M*x(i);
      nu1(i) >= -M*x(i);
      nu1(i) <= lambdaa(1)+M*(1-x(i));
      nu1(i) >= lambdaa(1)-M*(1-x(i));

      nu2(i) <= M*x(i);
      nu2(i) >= -M*x(i);
      nu2(i) <= lambdaa(2)+M*(1-x(i));
      nu2(i) >= lambdaa(2)-M*(1-x(i));

      nu3(i) <= M*x(i);
      nu3(i) >= -M*x(i);
      nu3(i) <= lambdaa(3)+M*(1-x(i));
      nu3(i) >= lambdaa(3)-M*(1-x(i));

      sig(i) <= M*y(i);
      sig(i) >= -M*y(i);
      sig(i) <= lambdaa(3)+M*(1-y(i));
      sig(i) >= lambdaa(3)-M*(1-y(i));
  end
  [6.4,7.2,2.5]*nu1-11.5*lambdaa(1) == 0;
  [-8,-4.9,-3.2]*nu2-5*lambdaa(2) == 0;
  [3.3,4.1,0.02]*nu3+[4,4.5,0.5]*sig -lambdaa(3) == 0;
  
cvx_end

    if strcmp(cvx_status,'Infeasible')
      break
    else
      f_best = [-1,1,-2]*x + [-1,5,1]*y;
    end
fprintf('Upper_Obj = %4.4f, Lower_Obj = %4.4f\n',cvx_optval,f_best);
end