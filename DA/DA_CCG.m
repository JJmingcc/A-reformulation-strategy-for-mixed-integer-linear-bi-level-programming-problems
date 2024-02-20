% ==================================================
% DA CCG
% 11-15-22
% Anh-Duong
% ==================================================
% ==================================================

clear all
close all
infoPrefix=sprintf('--%s--',mfilename); % all info displayed by this function includes this prefix

saveDiary=true; % flag to save diary
resultsDir='resultsCCG'; % directory to save results

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

obj_val_Vec = [];

for K = MaxK % K: maximum number of node failures
  % Initialization
  LB = -Inf; UB = Inf;
  L = 0;  

  z_set = []; UB_Set = []; LB_Set = [];
  x_setMP = []; q_setMP = []; y_setMP = []; 

  % Initialized to terminate the while loop
  exitFlag = 0;
  % Initialized to terminate the convergence loop
  epsilon = 0.001;

while (exitFlag == 0)
  % Using Strong Duality
  [obj_MP,x_MP,q_MP,y_MP] = DA_CCGMP(L,z_set);
  x_setMP = cat(3,x_setMP,full(x_MP)); 
  q_setMP = cat(2,q_setMP,full(q_MP)); 
  y_setMP = cat(2,y_setMP,full(y_MP));   
  LB = obj_MP; LB_Set = [LB_Set,LB];

  % Solve SP1
  [obj_SP1,z_SP1] = DA_CCGSP1(y_MP);
  
  z_set = cat(2,z_set,full(z_SP1));

  obj_SP2 = DA_CCGSP2(obj_SP1,z_SP1);
%   [obj_SP2,z_SP2] = DA_CCGSP2(obj_SP1,x_MP,q_MP,y_MP,K);

  UB = min(UB,sum(eVec.*y_MP) + obj_SP2); 
  UB_Set = [UB_Set,UB];

  fprintf('%s Iteration %i: UB = %4.4f and LB = %4.4f\n',infoPrefix,L,UB,LB);
  
    
  if (UB - LB) <= epsilon*UB
    exitFlag = 1;
  else
    L = L+1;
  end
end

  % Optimal solution
    z_star = z_SP1;
    y_star = y_MP;
    x_star = x_MP;
    q_star = q_MP;
    obj_val = UB;
    
fprintf('K=%d \n',K);
fprintf('Set of attacked EN: [');
fprintf('%g ', z_star'.*(1:N));
fprintf(']\n');
fprintf('Set of protected EN: [');
fprintf('%g ', y_star'.*(1:N));
fprintf(']\n');
fprintf('Optimal value:%4.4f \n',obj_val);
save(sprintf('%s/resultsK%d.mat',resultsDir,K),'x_star','z_star','y_star','q_star','obj_val','gam','beta','N','M','K','eVec','dMat','lambda');

obj_val_Vec = [obj_val_Vec,obj_val];
end
save(sprintf('%s/results.mat',resultsDir),'obj_val_Vec','gam','beta','N','M','K','eVec','dMat','lambda');

if(saveDiary)
  diary off;
end
