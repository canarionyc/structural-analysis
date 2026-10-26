%% STABIL 3.1 + Excel Importer: Automated Truss Solver
clear; clc;

% Define the Excel filename
filename = 'Cerchas_Data2.xlsx'; 
truss_name = 'Cercha 2 (Desde Excel)';

disp(['--- IMPORTANDO DATOS DE: ', filename, ' ---']);

%% 1. Import Data from Excel
nodes_table = readtable(filename, 'Sheet', 'Nodes');
elements_table = readtable(filename, 'Sheet', 'Elements');

%% 2. Parse Geometry (Nodos)
% STABIL nodes format: [NodeID, X, Y, Z]
num_nodes = height(nodes_table);
nodes = [nodes_table.Node, nodes_table.X, nodes_table.Y, zeros(num_nodes, 1)];

%% 3. Parse Connectivity & STABIL format
% Formato requerido por STABIL:
% [ID_Elem, ID_Tipo, ID_Seccion, ID_Material, Nodo_Left, Nodo_Right]
elements = [elements_table.Element, ...
            elements_table.Type, ... 
            elements_table.Section, ... 
            elements_table.Material, ... 
            elements_table.Node_left, ...
            elements_table.Node_right];

%% 4. Parse Boundary Conditions (Apoyos)
% STABIL supports format: [NodeID, Direction, Value] (1=X, 2=Y, 3=Z)
supports = [];
for i = 1:num_nodes
    n_id = nodes_table.Node(i);
    if nodes_table.restricted_X(i) == 1
        supports = [supports; n_id, 1, 0.0]; % Bloquear X
    end
    if nodes_table.restricted_Y(i) == 1
        supports = [supports; n_id, 2, 0.0]; % Bloquear Y
    end
    
    % CRÍTICO: Bloquear el Eje Z en todos los nodos para evitar matriz singular en 2D
    supports = [supports; n_id, 3, 0.0]; 
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

%% 6. STABIL Properties (Requerido por el Método de Rigidez)
Types = {1, 'truss'};

% Format Material: [MatID, E (Young), nu (Poisson), rho (Densidad)]
Materials = [1, 210e9, 0.3, 7850]; 

% Format Section: [SecID, A (Área), Iyy, Izz, J]
% Añadimos inercias ficticias (1e-5) para evitar divisiones por cero internas
Sections = [1, 0.01, 1e-5, 1e-5, 1e-5]; 
%% 7. STABIL Solver Engine
% Assemble global stiffness matrix K
K = asmkm(nodes, elements, Types, Materials, Sections);

% Assemble global load vector P manually (3 DOFs per node: X, Y, Z)
num_dofs = num_nodes * 3;
P = zeros(num_dofs, 1);

for i = 1:size(loads, 1)
    nodo_id = loads(i, 1);
    dir = loads(i, 2); % 1=X, 2=Y, 3=Z
    val = loads(i, 3);
    
    % Find the actual row index of the node in the 'nodes' matrix
    nodo_idx = find(nodes(:,1) == nodo_id);
    
    % Map to the correct global Degree of Freedom (DOF)
    % DOF = 3 * (Node_Index - 1) + Direction
    dof_index = 3 * (nodo_idx - 1) + dir;
    P(dof_index) = val;
end

% Solve for displacements (u) and reactions
[u, reactions] = solveq(K, P, supports);

% Compute internal forces (Axials)
Forces = elemf(nodes, elements, Types, Materials, Sections, u);

disp('Cálculo finalizado con éxito.');

%% 7. STABIL Solver Engine (Native Matrix Partitioning)
% Assemble global stiffness matrix K
K = asmkm(nodes, elements, Types, Materials, Sections);

% Assemble global load vector P manually (3 DOFs per node: X, Y, Z)
num_dofs = num_nodes * 3;
P = zeros(num_dofs, 1);

for i = 1:size(loads, 1)
    nodo_id = loads(i, 1);
    dir = loads(i, 2); 
    val = loads(i, 3);
    
    nodo_idx = find(nodes(:,1) == nodo_id);
    dof_index = 3 * (nodo_idx - 1) + dir;
    P(dof_index) = val;
end

% --- NATIVE FEM SOLVER ---
% Identify Constrained DOFs (c_dofs) and Free DOFs (f_dofs)
c_dofs = []; 
u_known = []; 
for i = 1:size(supports, 1)
    nodo_id = supports(i, 1);
    dir = supports(i, 2);
    val = supports(i, 3);
    
    nodo_idx = find(nodes(:,1) == nodo_id);
    c_dofs = [c_dofs; 3 * (nodo_idx - 1) + dir];
    u_known = [u_known; val];
end

% All DOFs that are not constrained are free
f_dofs = setdiff(1:num_dofs, c_dofs)'; 

% Initialize displacement vector
u = zeros(num_dofs, 1);
u(c_dofs) = u_known;

% Solve for unknown displacements: K_ff * u_f = P_f - K_fc * u_c
u(f_dofs) = K(f_dofs, f_dofs) \ (P(f_dofs) - K(f_dofs, c_dofs) * u(c_dofs));

% Calculate Global Reactions: R = K * u - P
reactions_global = K * u - P;

% Compute internal forces (Axials) using STABIL's native function
Forces = elemf(nodes, elements, Types, Materials, Sections, u);

disp('Cálculo finalizado con éxito.');

% Imprimir Reacciones en consola para verificación
disp('--- REACCIONES EN LOS APOYOS ---');
for i = 1:length(c_dofs)
    dof = c_dofs(i);
    nodo_idx = ceil(dof / 3);
    nodo_id = nodes(nodo_idx, 1);
    dir = mod(dof - 1, 3) + 1; % 1=X, 2=Y, 3=Z
    
    if dir == 1; dir_str = 'X'; elseif dir == 2; dir_str = 'Y'; else; dir_str = 'Z'; end
    
    % Filtrar Eje Z ya que es ficticio para 2D
    if dir ~= 3
        fprintf('Nodo %d (Eje %s): %8.2f\n', nodo_id, dir_str, reactions_global(dof));
    end
end
%% 8. Visualization using STABIL Native Plots
figure('Name', ['Análisis STABIL - ', truss_name], 'Color', 'w', 'Position', [100, 100, 800, 800]);

% Plot 1: Geometry and Boundary Conditions
subplot(2, 1, 1);
plotelem(nodes, elements, Types, supports);
title(['Geometría y Apoyos: ', truss_name]);
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;

% Plot 2: Internal Forces (Axials)
subplot(2, 1, 2);
plotforces(nodes, elements, Types, Forces);
title('Diagrama de Esfuerzos Axiles');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;