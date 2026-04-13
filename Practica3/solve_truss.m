function [axiles, reactions] = solve_truss(nodes, bars, supports, loads)
%% Universal Direct Stiffness Method Solver for Statically Determinate Trusses
% nodes: [x, y]
% bars: [node_start, node_end]
% supports: [node_id, is_fixed_x, is_fixed_y] (1 = fixed, 0 = free)
% loads: [node_id, force_x, force_y]

num_nodes = size(nodes, 1);
num_bars = size(bars, 1);

% Count total reaction components
num_reactions = sum(supports(:, 2)) + sum(supports(:, 3));
num_unknowns = num_bars + num_reactions;

%% Build Applied Load Vector
P_applied = zeros(num_nodes * 2, 1);
for i = 1:size(loads, 1)
    n = loads(i, 1);
    P_applied(2*n - 1) = loads(i, 2); % X-force
    P_applied(2*n)     = loads(i, 3); % Y-force
end

%% Build Equilibrium Matrix [C]
C = zeros(num_nodes * 2, num_unknowns);

% 1. Internal bar forces
for i = 1:num_bars
    n1 = bars(i, 1);
    n2 = bars(i, 2);
    
    dx = nodes(n2, 1) - nodes(n1, 1);
    dy = nodes(n2, 2) - nodes(n1, 2);
    L = sqrt(dx^2 + dy^2);
    
    c = dx / L; 
    s = dy / L; 
    
    C(2*n1 - 1, i) = c;  
    C(2*n1, i)     = s;  
    C(2*n2 - 1, i) = -c; 
    C(2*n2, i)     = -s; 
end

% 2. Support reactions
reaction_idx = num_bars + 1;
for i = 1:size(supports, 1)
    n = supports(i, 1);
    
    if supports(i, 2) == 1 % X-direction fixed
        C(2*n - 1, reaction_idx) = 1;
        reaction_idx = reaction_idx + 1;
    end
    
    if supports(i, 3) == 1 % Y-direction fixed
        C(2*n, reaction_idx) = 1;
        reaction_idx = reaction_idx + 1;
    end
end

%% Solve System
X = C \ (-P_applied);

axiles = X(1:num_bars);
reactions = X(num_bars+1:end);

end