%% STABIL 3.1 Solver Script: Cercha 2
clear; clc;

%% 1. Geometry Definition (Nodos)
% Por favor, actualiza estas coordenadas con las medidas exactas de CERCHA 2.jpg
% Format: nodes = [NodeID, X, Y, Z] (STABIL requires Z even for 2D, set Z=0)
nodes = [
    1, 0.0, 0.0, 0.0;  % Nodo 1
    2, 2.5, 0.0, 0.0;  % Nodo 2 
    3, 2.5, 3.0, 0.0;  % Nodo 3 (Ejemplo)
    % ... [!] AÑADE EL RESTO DE NODOS AQUÍ
];

%% 2. Connectivity (Elementos)
% Format: elements = [ElementID, Node1, Node2]
elements = [
    1, 1, 2; % Barra 1
    2, 2, 3; % Barra 2
    % ... [!] AÑADE EL RESTO DE BARRAS AQUÍ
];

%% 3. STABIL Properties
% STABIL needs Types, Sections (Area), and Materials (Young's Modulus) 
% to assemble the global stiffness matrix (ke_truss), even for pure statics.
Types = {'truss'};
ElementTypes = ones(size(elements, 1), 1); % All elements are type 1 ('truss')

A = 0.01;      % Cross-sectional area / Área de la sección (m^2)
E = 210e9;     % Young's Modulus / Módulo de Young (Pa) - Acero
Sections = [1, A];
Materials = [1, E];

ElementSections = ones(size(elements, 1), 1);
ElementMaterials = ones(size(elements, 1), 1);

%% 4. Boundary Conditions (Apoyos)
% Format: supports = [NodeID, Direction, Value]
% Directions for 2D truss: 1 = X-axis, 2 = Y-axis
supports = [
    1, 1, 0.0; % Nodo 1 bloqueado en X
    1, 2, 0.0; % Nodo 1 bloqueado en Y
    % ... [!] DEFINE TUS APOYOS REALES AQUÍ
];

%% 5. Loads (Cargas)
% Format: loads = [NodeID, Direction, Value]
loads = [
    3, 2, -500; % Ejemplo: 500 N hacia abajo en el Nodo 3
    % ... [!] DEFINE TUS CARGAS REALES AQUÍ
];

%% 6. STABIL Solver Engine
% This automatically calls: ke_truss, loads_truss, etc.
[K, M] = asmkm(nodes, elements, Types, ElementTypes, Sections, ElementSections, Materials, ElementMaterials);
P_global = asmloads(nodes, elements, Types, ElementTypes, loads);

% Solve for displacements (u) and reactions
[u, reactions] = solveq(K, P_global, supports);

% Compute internal forces (Calls forces_truss and forceslcs_truss)
Forces = elemf(nodes, elements, Types, ElementTypes, Sections, ElementSections, Materials, ElementMaterials, u);

%% 7. Visualization using STABIL Native Plots
figure('Name', 'Análisis STABIL - Cercha 2', 'Color', 'w');

% Plot 1: Geometry and Boundary Conditions
% Internally uses coord_truss
subplot(2, 1, 1);
plotelem(nodes, elements, Types, ElementTypes, supports);
title('Geometría y Apoyos (Cercha 2)');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;

% Plot 2: Internal Forces (Axials)
% Internally uses fdiagrgcs_truss to plot the structural diagrams
subplot(2, 1, 2);
plotforces(nodes, elements, Types, ElementTypes, Forces);
title('Diagrama de Esfuerzos Axiles');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');
grid on; axis equal;