%% Define Truss Geometry
clearvars
% Node coordinates [x, y]
nodes = [0 0; 2.5 3; 5 0; 7.5 3; 10 0; 12.5 3; 15 0];

%% Define Loads and Supports
% Applied nodal loads [Fx, Fy]
loads = [0 0; 0 -200; 0 -150; 0 -200; 0 -150; 0 -200; 0 0];

% Support conditions (1 = fixed, 0 = free)
% [dx, dy]
supports = [0 1;  % Node 1: Roller (y-fixed)
            0 0; 0 0; 0 0; 0 0; 0 0; 
            1 1]; % Node 7: Pin (x, y-fixed)

%% Calculate Global Reactions
% For a statically determinate structure, global equilibrium 
% sum(Fx) = 0, sum(Fy) = 0, sum(M) = 0 can be solved as a linear system.
total_load_y = sum(loads(:, 2));

% Taking moments about Node 1 (0,0)
moment_arms = nodes(:, 1); 
moments = loads(:, 2) .* moment_arms;
sum_moments = sum(moments);

% Reactions [RAy; RBx; RBy]
% RBy * 15 + sum_moments = 0
RBy = -sum_moments / 15;
RAy = -total_load_y - RBy;
RBx = -sum(loads(:, 1));

disp(['RAy = ', num2str(RAy)]);
disp(['RBy = ', num2str(RBy)]);