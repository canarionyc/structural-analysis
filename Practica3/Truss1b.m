%% Truss Geometry and Node Definitions
clear;
% Coordinates [x, y]
% Nodes 1-4 are the bottom chord, Nodes 5-7 are the top chord
nodes = [ 0.0, 0.0;   % Node 1: Bottom Left (Roller support)
          5.0, 0.0;   % Node 2: Bottom Mid-Left
         10.0, 0.0;   % Node 3: Bottom Mid-Right
         15.0, 0.0;   % Node 4: Bottom Right (Pinned support)
          2.5, 3.0;   % Node 5: Top Left
          7.5, 3.0;   % Node 6: Top Center
         12.5, 3.0 ]; % Node 7: Top Right

%% Bar Connectivity (Elements)
% Defined by [Start_Node, End_Node]
bars = [ 1, 2;  % Bar 1:  Bottom chord
         2, 3;  % Bar 2:  Bottom chord
         3, 4;  % Bar 3:  Bottom chord
         5, 6;  % Bar 4:  Top chord
         6, 7;  % Bar 5:  Top chord
         1, 5;  % Bar 6:  Diagonal
         5, 2;  % Bar 7:  Diagonal
         2, 6;  % Bar 8:  Diagonal
         6, 3;  % Bar 9:  Diagonal
         3, 7;  % Bar 10: Diagonal
         7, 4 ];% Bar 11: Diagonal

num_nodes = size(nodes, 1);
num_bars = size(bars, 1);
num_unknowns = num_bars + 3; % 11 internal axials + 3 reactions

%% External Loads (Applied Forces)
% P_applied = matrix of zeros (num_nodes * 2, 1)
% Format: [Fx1; Fy1; Fx2; Fy2; ... ; Fx7; Fy7]
P_applied = zeros(num_nodes * 2, 1);

% Applying the downward vertical forces (Y-direction is the even index: 2 * Node)
P_applied(2*5) = -200; % Node 5, Fy
P_applied(2*6) = -200; % Node 6, Fy
P_applied(2*7) = -200; % Node 7, Fy
P_applied(2*2) = -150; % Node 2, Fy
P_applied(2*3) = -150; % Node 3, Fy

%% Equilibrium Matrix Setup [C]
% Equation: [C] * {X} = -{P_applied}
% Where {X} = [N1; N2; ...; N11; R1y; R4x; R4y]
C = zeros(num_nodes * 2, num_unknowns);

% 1. Populate matrix with Internal Forces (Direction Cosines)
for i = 1:num_bars
    n1 = bars(i, 1);
    n2 = bars(i, 2);
    
    % Calculate length and angles
    dx = nodes(n2, 1) - nodes(n1, 1);
    dy = nodes(n2, 2) - nodes(n1, 2);
    L = sqrt(dx^2 + dy^2);
    
    c = dx / L; % cosine
    s = dy / L; % sine
    
    % Force exerted BY the bar ON node 1 (Assuming Tension is positive)
    C(2*n1 - 1, i) = c;  % X-equation for n1
    C(2*n1, i)     = s;  % Y-equation for n1
    
    % Force exerted BY the bar ON node 2
    C(2*n2 - 1, i) = -c; % X-equation for n2
    C(2*n2, i)     = -s; % Y-equation for n2
end

% 2. Populate matrix with Support Reactions
% R1y acts at Node 1 in Y direction
C(2*1, num_bars + 1) = 1; 

% R4x acts at Node 4 in X direction
C(2*4 - 1, num_bars + 2) = 1; 

% R4y acts at Node 4 in Y direction
C(2*4, num_bars + 3) = 1;

%% Solve the Linear System
% Using the backslash operator to solve [C]{X} = -{P}
X = C \ (-P_applied);

%% Parse and Display Results
axiles = X(1:num_bars);
reactions = X(num_bars+1:end);

disp('--- AXIAL FORCES (AXILES) ---');
disp('(+ = Tension / Tracción, - = Compression / Compresión)');
for i = 1:num_bars
    fprintf('Bar %2d (Nodes %d to %d): %8.2f\n', i, bars(i,1), bars(i,2), axiles(i));
end

disp(' ');
disp('--- SUPPORT REACTIONS ---');
fprintf('R1y (Node 1, Y-axis): %8.2f\n', reactions(1));
fprintf('R4x (Node 4, X-axis): %8.2f\n', reactions(2));
fprintf('R4y (Node 4, Y-axis): %8.2f\n', reactions(3));

%%
plotdisp