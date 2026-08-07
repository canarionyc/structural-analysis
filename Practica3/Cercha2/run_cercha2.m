%% Data Script: Cercha 2 (Ménsula)
clear; clc;

%% Geometry Definition
% Nodes 1-5: Top Chord. Nodes 6-10: Bottom Chord.
nodes = [ 0.0, 2.5;   % Node 1 (Wall top)
          2.5, 2.5;   % Node 2
          5.0, 2.5;   % Node 3
          7.5, 2.5;   % Node 4
         10.0, 2.5;   % Node 5
          0.0, 0.0;   % Node 6 (Wall bottom)
          2.5, 0.0;   % Node 7
          5.0, 0.0;   % Node 8
          7.5, 0.0;   % Node 9
         10.0, 0.0 ]; % Node 10

%% Connectivity
bars = [ 1, 2; 2, 3; 3, 4; 4, 5;          % Top chord
         6, 7; 7, 8; 8, 9; 9, 10;         % Bottom chord
         2, 7; 3, 8; 4, 9; 5, 10;         % Verticals
         1, 7; 2, 8; 3, 9; 4, 10 ];       % Diagonals

%% Boundary Conditions & Loads
% Format: [node_id, fix_x, fix_y]
supports = [ 1, 1, 1;   % Top left pinned to wall
             6, 1, 1 ]; % Bottom left pinned to wall

% Format: [node_id, force_x, force_y]
loads = [ 2, 0, -500;
          3, 0, -500;
          4, 0, -500;
          5, 0, -250 ];

%% Execution
[axiles, reactions] = solve_truss(nodes, bars, supports, loads);

%% Console Output
disp('--- ESFUERZOS AXILES ---');
for i = 1:size(bars, 1)
    fprintf('Barra %2d (Nodos %2d a %2d): %8.2f\n', i, bars(i,1), bars(i,2), axiles(i));
end

disp(' ');
disp('--- REACCIONES ---');
fprintf('Nodo 1 (Eje X): %8.2f\n', reactions(1));
fprintf('Nodo 1 (Eje Y): %8.2f\n', reactions(2));
fprintf('Nodo 6 (Eje X): %8.2f\n', reactions(3));
fprintf('Nodo 6 (Eje Y): %8.2f\n', reactions(4));

%% Visualization
plot_truss(nodes, bars, axiles, supports, loads, reactions, 'Cercha 2 (Ménsula)');

