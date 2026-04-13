%% STABIL 3.1 + Excel Importer: Automated Truss Solver
clear; clc;

% Define the Excel filename
% (Cambia este nombre por el de tu archivo real)
filename = 'Cerchas_Data2.xlsx'; 
truss_name = 'Cercha 2 (Desde Excel)';

disp(['--- IMPORTANDO DATOS DE: ', filename, ' ---']);

%% 1. Import Data from Excel
% Read the 'Nodes' sheet
nodes_table = readtable(filename, 'Sheet', 'Nodes');

% Read the 'Elements' sheet
elements_table = readtable(filename, 'Sheet', 'Elements');

%% 2. Parse Geometry (Nodos)
% STABIL nodes format: [NodeID, X, Y, Z]
num_nodes = height(nodes_table);
nodes = [nodes_table.Node, nodes_table.X, nodes_table.Y, zeros(num_nodes, 1)];

%% 3. Parse Connectivity (Elementos)
% STABIL elements format: [ElementID, Node_left, Node_right]
elements = [elements_table.Element, elements_table.Node_left, elements_table.Node_right];

%% 4. Parse Boundary Conditions (Apoyos)
% STABIL supports format: [NodeID, Direction, Value] (1=X, 2=Y)
supports = [];
for i = 1:num_nodes
    n_id = nodes_table.Node(i);
    
    if nodes_table.restricted_X(i) == 1
        supports = [supports; n_id, 1, 0.0];
    end
    if nodes_table.restricted_Y(i) == 1
        supports = [supports; n_id, 2, 0.0];
    end
end

%% 5. Parse Loads (Cargas)
% STABIL loads format: [NodeID, Direction, Value]
loads = [];
for i = 1:num_nodes
    n_id = nodes_table.Node(i);
    
    if nodes_table.Load_x(i) ~= 0
        loads = [loads; n_id, 1, nodes_table.Load_x(i)];
    end
    if nodes_table.Load_y(i) ~= 0
        loads = [loads; n_id, 2, nodes_table.Load_y(i)];
    end
end

disp('Datos importados correctamente. Ejecutando solver STABIL...');

%% 6. STABIL Properties
Types = {1,'truss'};
ElementTypes = ones(size(elements, 1), 1); 

A = 0.01;      % Area (m^2)
E = 210e9;     % Young's Modulus (Pa)
Sections = [1, A];
Materials = [1, E];

ElementSections = ones(size(elements, 1), 1);
ElementMaterials = ones(size(elements, 1), 1);

%% 7. STABIL Solver Engine
[K, M] = asmkm(nodes, elements, Types, ElementTypes, Sections, ElementSections, Materials, ElementMaterials);
P_global = asmloads(nodes, elements, Types, ElementTypes, loads);

[u, reactions] = solveq(K, P_global, supports);

Forces = elemf(nodes, elements, Types, ElementTypes, Sections, ElementSections, Materials, ElementMaterials, u);

disp('Cálculo finalizado con éxito.');

%% 8. Visualization using STABIL Native Plots
figure('Name', ['Análisis STABIL - ', truss_name], 'Color', 'w', 'Position', [100, 100, 800, 800]);

% Plot 1: Geometry and Boundary Conditions
subplot(2, 1, 1);
plotelem(nodes, elements, Types, ElementTypes, supports);
title(['Geometría y Apoyos: ', truss_name]);
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;

% Plot 2: Internal Forces (Axials)
subplot(2, 1, 2);
plotforces(nodes, elements, Types, ElementTypes, Forces);
title('Diagrama de Esfuerzos Axiles');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;