N = 6; M = 30; G = 5;

MaxK = 5;
% K = 2; %floor(N*1/4);
beta = 0.2;
gam = 0.1;
% dMat = csvread('delayMat.csv');
% d_avg = mean(mean(dMat));
% aMat = dMat<d_avg;
% vg = 2.^(1:G)';
% v_max = max(vg);
% v_min = min(vg);
dMat = csvread('edgeDelay.csv');
dMat = dMat(1:M,1:N);

rng(1);
lambda = randi([5,40],M,1).*2;

budmin = 0.8; budmax = 2; %dollars
% hVec = budmin+(budmax-budmin)*rand(N,1); %dollars

budPromin = 0.05; budPromax = 0.3; %dollars
eVec = budPromin/2+(budPromax-budPromin)/2*rand(N,1); %dollars


B = 2;

q_vCost = 1*ones(N,1); %variable cost for activating EN j

Q = 1;
c = 1*ones(N,1); %fixed cost for activating EN j
Cap = 2.^randi([6,10],N,1); %Resource capacity

phi = 10*ones(M,1); %Penalty unmet

BA = MaxK;
hVec = Cap; % Damage from of attacking a node from attacker perspective/how important the node to the defender
% fVec = hVec./max(hVec)*min(eVec);
fVec = ones(N,1); % Cost of attacking a node