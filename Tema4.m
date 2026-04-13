%% StaBIL manual
% Example 1.1: static analysis of a frame
% Units: m, kN

% Nodes=[NodID X  Y  Z]
Nodes=  [1     0  0  0;
         2     1.5  1.5  0;
         3     3  1.5  0;
         4     4  4  0;
         5     4  0  0;
         6     1  5  0];          % reference node

% Check the node coordinates as follows:     
figure
plotnodes(Nodes,'w.');

%% Element types -> {EltTypID EltName}
Types=  {1        'beam';
         2        'truss'};

b=0.10;
h=0.25;
r=0.004;

% Sections=[SecID A      ky   kz   Ixx Iyy Izz       yt   yb   zt   zb]
Sections=  [1     b*h    Inf  Inf  0   0   b*h^3/12  h/2  h/2  b/2  b/2;
            2     pi*r^2 NaN  NaN  NaN NaN NaN       NaN  NaN  NaN  NaN];

% Materials=[MatID     E nu];
Materials=  [1      30e6 0.2;               % concrete
             2     210e6 0.3];              % steel

% Elements=[EltID TypID SecID MatID n1 n2 n3]
Elements=  [1     1     1     1     1  2  6;              
            2     1     1     1     3  4  6;
            3     1     1     1     5  4  6;
            4     2     2     2     1  4  NaN];

%% Check node and element definitions as follows:
hold('on');
plotelem(Nodes,Elements,Types);
title('Nodes and elements');

%% Degrees of freedom 
% Assemble a column matrix containing all DOFs at which stiffness is
% present in the model:
DOF=getdof(Elements,Types);

% Remove all DOFs equal to zero from the vector:
%  - 2D analysis: select only UX,UY,ROTZ
%  - clamp node 1
%  - hinge at node 5
seldof=[0.03; 0.04; 0.05; 1.00; 5.01; 5.02];
DOF=removedof(DOF,seldof);

% Assembly of stiffness matrix K 
K=asmkm(Nodes,Elements,Types,Sections,Materials,DOF);

% Nodal loads: 5 kN horizontally on node 4.
seldof=[4.01];
PLoad=    [5];

%% Assembly of the load vectors:
P=nodalvalues(DOF,seldof,PLoad)

% Distributed loads are specified in the global coordinate system
% DLoads=[EltID n1globalX n1globalY n1globalZ ...]
DLoads=  [1     2 0 0 2 0 0];

P=P+elemloads(DLoads,Nodes,Elements,Types,DOF)

% Constraint equations: Constant=Coef1*DOF1+Coef2*DOF2+ ...
% Constraints=[Constant  Coef1 DOF1  Coef2 DOF2 ...]
Constr=       [0         1     2.01  -1    3.01;
               0         1     2.02  -1    3.02];
 
%% Add constraint equations
[K,P]=addconstr(Constr,DOF,K,P)

%% Solve K * U = P 
U=K\P

%% Plot displacements
figure
plotdisp(Nodes,Elements,Types,DOF,U,DLoads,Sections,Materials)

%% The displacements can be displayed as follows:
printdisp(Nodes,DOF,U);

%% Compute element forces
Forces=elemforces(Nodes,Elements,Types,Sections,Materials,DOF,U,DLoads);

% The element forces can be displayed in a orderly table:
printforc(Elements,Forces);

%% Plot element forces
figure
plotforc('norm',Nodes,Elements,Types,Forces,DLoads)
title('Normal forces')

figure
plotforc('sheary',Nodes,Elements,Types,Forces,DLoads)
title('Shear forces')

figure
plotforc('momz',Nodes,Elements,Types,Forces,DLoads)
title('Bending moments')

%% Plot stresses
figure
plotstress('snorm',Nodes,Elements,Types,Sections,Forces,DLoads)
title('Normal stresses due to normal forces')

figure
plotstress('smomzt',Nodes,Elements,Types,Sections,Forces,DLoads)
title('Normal stresses due to bending moments around z: top')

figure
plotstress('smomzb',Nodes,Elements,Types,Sections,Forces,DLoads)
title('Normal stresses due to bending moments around z: bottom')

figure
plotstress('smax',Nodes,Elements,Types,Sections,Forces,DLoads)
title('Maximal normal stresses')

figure
plotstress('smin',Nodes,Elements,Types,Sections,Forces,DLoads)
title('Minimal normal stresses')
