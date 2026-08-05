%% Truss Geometry and Node Definitions
% Coordinates [x, y]
nodes = [ 0.0, 0.0;   % Node 1: Bottom Left
          5.0, 0.0;   % Node 2: Bottom Mid-Left
         10.0, 0.0;   % Node 3: Bottom Mid-Right
         15.0, 0.0;   % Node 4: Bottom Right
          2.5, 3.0;   % Node 5: Top Left
          7.5, 3.0;   % Node 6: Top Center
         12.5, 3.0 ]; % Node 7: Top Right

%% Bar Connectivity (Elements)
% Defined by [Start_Node, End_Node]
bars = [ 1, 2;  % Bar 1
         2, 3;  % Bar 2
         3, 4;  % Bar 3
         5, 6;  % Bar 4
         6, 7;  % Bar 5
         1, 5;  % Bar 6
         5, 2;  % Bar 7
         2, 6;  % Bar 8
         6, 3;  % Bar 9
         3, 7;  % Bar 10
         7, 4 ];% Bar 11

num_nodes = size(nodes, 1);
num_bars = size(bars, 1);
num_unknowns = num_bars + 3;

%% External Loads (Applied Forces)
% Format: [Fx1; Fy1; Fx2; Fy2; ... ; Fx7; Fy7]
P_applied = zeros(num_nodes * 2, 1);
P_applied(2*5) = -200; % Node 5, Fy
P_applied(2*6) = -200; % Node 6, Fy
P_applied(2*7) = -200; % Node 7, Fy
P_applied(2*2) = -150; % Node 2, Fy
P_applied(2*3) = -150; % Node 3, Fy

%% Equilibrium Matrix Setup [C]
C = zeros(num_nodes * 2, num_unknowns);

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

% Support Reactions
C(2*1, num_bars + 1) = 1; % R1y
C(2*4 - 1, num_bars + 2) = 1; % R4x
C(2*4, num_bars + 3) = 1; % R4y

%% Solve the Linear System
X = C \ (-P_applied);
axiles = X(1:num_bars);
reactions = X(num_bars+1:end);

%% Print Results in Console
disp('--- ESFUERZOS AXILES ---');
disp('(+ = Tracción, - = Compresión)');
for i = 1:num_bars
    fprintf('Barra %2d (Nodos %d a %d): %8.2f\n', i, bars(i,1), bars(i,2), axiles(i));
end

disp(' ');
disp('--- REACCIONES EN LOS APOYOS ---');
fprintf('R1y (Nodo 1, Eje Y): %8.2f\n', reactions(1));
fprintf('R4x (Nodo 4, Eje X): %8.2f\n', reactions(2));
fprintf('R4y (Nodo 4, Eje Y): %8.2f\n', reactions(3));

%% PLOT 1: Geometry (STABIL "plotelem" Equivalent)
figure('Name', 'Geometría del Sistema', 'Color', 'w');
hold on; grid on; axis equal;

% Plot Bars
for i = 1:num_bars
    n1 = bars(i, 1); n2 = bars(i, 2);
    plot([nodes(n1,1), nodes(n2,1)], [nodes(n1,2), nodes(n2,2)], 'k-', 'LineWidth', 1.5);
end

% Plot Nodes
plot(nodes(:,1), nodes(:,2), 'ko', 'MarkerFaceColor', 'w', 'MarkerSize', 6);

% Plot Supports (Triangles for visualization)
plot(nodes(1,1), nodes(1,2)-0.2, 'b^', 'MarkerFaceColor', 'b', 'MarkerSize', 10);
plot(nodes(4,1), nodes(4,2)-0.2, 'b^', 'MarkerFaceColor', 'b', 'MarkerSize', 10);

% Labels and Title
title('Geometría Indeformada (Equivalente plotelem)');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
set(gca, 'FontSize', 11);

%% PLOT 2: Axial Forces (STABIL "plotforces" Equivalent)
figure('Name', 'Esfuerzos Axiles', 'Color', 'w');
hold on; axis equal; axis off;

title('Diagrama de Esfuerzos Axiles (Equivalente plotforces)');
% Add a legend using dummy plots
plot(NaN, NaN, 'b-', 'LineWidth', 2, 'DisplayName', 'Tracción (+)');
plot(NaN, NaN, 'r-', 'LineWidth', 2, 'DisplayName', 'Compresión (-)');
plot(NaN, NaN, 'k-', 'LineWidth', 1, 'DisplayName', 'Nulo (0)');
legend('Location', 'best');

% Plot colored bars based on force state
for i = 1:num_bars
    n1 = bars(i, 1); n2 = bars(i, 2);
    x_coords = [nodes(n1,1), nodes(n2,1)];
    y_coords = [nodes(n1,2), nodes(n2,2)];
    
    % Determine color: Blue for Tension, Red for Compression, Black for Zero
    if axiles(i) > 1e-5
        c = 'b'; lw = 2; % Tension
    elseif axiles(i) < -1e-5
        c = 'r'; lw = 2; % Compression
    else
        c = 'k'; lw = 1; % Zero force
    end
    
    % Draw the bar
    plot(x_coords, y_coords, '-', 'Color', c, 'LineWidth', lw);
    
    % Add text label with the value at the midpoint
    mid_x = mean(x_coords);
    mid_y = mean(y_coords);
    text(mid_x, mid_y, sprintf('%.1f', axiles(i)), ...
        'Color', c, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom', 'BackgroundColor', 'w', 'Margin', 1);
end

% Plot Nodes on top
plot(nodes(:,1), nodes(:,2), 'ko', 'MarkerFaceColor', 'w', 'MarkerSize', 4);