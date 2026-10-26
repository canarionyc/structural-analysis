%% Automated Truss Solver (Excel + STABIL 3.1 Native Partitioning)
clear; clc;

filename = 'Cerchas_Data2.xlsx'; 
truss_name = 'Cercha 2 (Desde Excel)';

disp(['--- IMPORTANDO DATOS DE: ', filename, ' ---']);

%% 1. Import Data from Excel
nodes_table = readtable(filename, 'Sheet', 'Nodes');
elements_table = readtable(filename, 'Sheet', 'Elements');

%% 2. Parse Geometry
% [NodeID, X, Y, Z]
num_nodes = height(nodes_table);
nodes = [nodes_table.Node, nodes_table.X, nodes_table.Y, zeros(num_nodes, 1)];

%% 3. Parse Connectivity
% [ID_Elem, ID_Tipo, ID_Seccion, ID_Material, Nodo_Left, Nodo_Right]
elements = [elements_table.Element, ...
            elements_table.Type, ... 
            elements_table.Section, ... 
            elements_table.Material, ... 
            elements_table.Node_left, ...
            elements_table.Node_right];

%% 4. Parse Boundary Conditions
% [NodeID, Direction, Value] (1=X, 2=Y, 3=Z)
supports = [];
for i = 1:num_nodes
    n_id = nodes_table.Node(i);
    if nodes_table.restricted_X(i) == 1
        supports = [supports; n_id, 1, 0.0]; 
    end
    if nodes_table.restricted_Y(i) == 1
        supports = [supports; n_id, 2, 0.0]; 
    end
    % Lock Z-axis for 2D analysis
    supports = [supports; n_id, 3, 0.0]; 
end

%% 5. Parse Loads
% [NodeID, Direction, Value]
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

disp('Datos importados correctamente. Ensamblando matrices...');

%% 6. STABIL Properties
Types = {1, 'truss'};
Materials = [1, 210e9, 0.3, 7850]; 
Sections = [1, 0.01, 1e-5, 1e-5, 1e-5]; 

%% 7. Assemble Global Matrices
% K: Global Stiffness Matrix
K = asmkm(nodes, elements, Types, Materials, Sections);

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

%% 8. Native FEM Solver (mldivide \ Partitioning)
disp('Resolviendo sistema de ecuaciones...');

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

f_dofs = setdiff(1:num_dofs, c_dofs)'; 

u = zeros(num_dofs, 1);
u(c_dofs) = u_known;

% Use MATLAB's built-in mldivide (\) to solve the linear system
u(f_dofs) = K(f_dofs, f_dofs) \ (P(f_dofs) - K(f_dofs, c_dofs) * u(c_dofs));

% Global reactions
reactions_global = K * u - P;

%% 9. Compute Element Forces
% Generate the DOF mapping required by elemforces using STABIL's built-in getdof
[DOF, ~] = getdof(elements, Types);

% Calculate internal forces (using empty arrays for DLoads and TLoads)
ForcesLCS = elemforces(nodes, elements, Types, Sections, Materials, DOF, u, [], []);

disp('Cálculo finalizado con éxito.');

%% 10. Console Output
disp('--- REACCIONES EN LOS APOYOS ---');
for i = 1:length(c_dofs)
    dof = c_dofs(i);
    nodo_idx = ceil(dof / 3);
    nodo_id = nodes(nodo_idx, 1);
    dir = mod(dof - 1, 3) + 1; 
    
    if dir == 1; dir_str = 'X'; elseif dir == 2; dir_str = 'Y'; else; dir_str = 'Z'; end
    
    if dir ~= 3
        fprintf('Nodo %d (Eje %s): %8.2f\n', nodo_id, dir_str, reactions_global(dof));
    end
end

%% 11. Visualization
figure('Name', ['Análisis Estructural - ', truss_name], 'Color', 'w', 'Position', [100, 100, 800, 800]);

% Plot Geometry and Supports
subplot(2, 1, 1);
plotelem(nodes, elements, Types); % <- Eliminado el argumento 'supports'
hold on;

% Draw supports natively over the STABIL plot
for i = 1:size(nodes, 1)
    nodo_id = nodes(i, 1);
    nx = nodes(i, 2);
    ny = nodes(i, 3);
    
    % Find restrictions for this node
    is_fixed_x = any(supports(:,1) == nodo_id & supports(:,2) == 1);
    is_fixed_y = any(supports(:,1) == nodo_id & supports(:,2) == 2);
    
    if is_fixed_x && is_fixed_y
        % Apoyo Fijo (Cuadrado rojo)
        plot(nx, ny, 'ks', 'MarkerFaceColor', 'r', 'MarkerSize', 10);
    elseif is_fixed_x || is_fixed_y
        % Apoyo Móvil (Triángulo azul)
        plot(nx, ny, 'k^', 'MarkerFaceColor', 'b', 'MarkerSize', 10);
    end
end
hold off;

title(['Geometría y Apoyos: ', truss_name]);
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;

% Plot Internal Axials
subplot(2, 1, 2);
plotforc(nodes, elements, Types, ForcesLCS);
title('Diagrama de Esfuerzos Axiles');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;