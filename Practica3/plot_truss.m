function plot_truss(nodes, bars, axiles, supports, loads, reactions, truss_name)
%% Post-Processing and Visualization Engine
% Includes elements, axial forces, supports, applied loads, and reactions

figure('Name', ['Análisis de ', truss_name], 'Color', 'w');
hold on; grid on; axis equal;

title(['Esquema Estático y Esfuerzos: ', truss_name]);
xlabel('Eje X (m)');
ylabel('Eje Y (m)');

%% 1. Calculate Visual Scaling for Force Vectors
% Find the maximum dimension of the truss to scale arrows to 15% of its size
max_dim = max(range(nodes(:,1)), range(nodes(:,2)));
if max_dim == 0; max_dim = 10; end % Fallback

% Find the maximum force (either applied or reaction)
max_load = max(abs(loads(:, 2:3)), [], 'all');
max_rxn = max(abs(reactions));
max_force = max(max_load, max_rxn);
if max_force == 0; max_force = 1; end % Avoid division by zero

scale_factor = (0.15 * max_dim) / max_force;

%% 2. Unpack Reactions mapping them to specific nodes
rxn_vectors = zeros(size(nodes, 1), 2);
r_idx = 1;
for i = 1:size(supports, 1)
    n = supports(i, 1);
    if supports(i, 2) == 1 % X-fixed
        rxn_vectors(n, 1) = reactions(r_idx);
        r_idx = r_idx + 1;
    end
    if supports(i, 3) == 1 % Y-fixed
        rxn_vectors(n, 2) = reactions(r_idx);
        r_idx = r_idx + 1;
    end
end

%% 3. Draw Legend Dummies (For clean legend generation)
plot(NaN, NaN, 'b-', 'LineWidth', 2, 'DisplayName', 'Tracción (+)');
plot(NaN, NaN, 'r-', 'LineWidth', 2, 'DisplayName', 'Compresión (-)');
plot(NaN, NaN, 'k-', 'LineWidth', 1, 'DisplayName', 'Nulo (0)');
plot(NaN, NaN, 'ks', 'MarkerFaceColor', [0.8 0.8 0.8], 'MarkerSize', 10, 'DisplayName', 'Apoyos');
quiver(NaN, NaN, 0, 0, 'Color', 'm', 'LineWidth', 1.5, 'DisplayName', 'Cargas');
quiver(NaN, NaN, 0, 0, 'Color', [0 0.6 0], 'LineWidth', 1.5, 'DisplayName', 'Reacciones');

%% 4. Draw Bars and Axial Forces
num_bars = size(bars, 1);
for i = 1:num_bars
    n1 = bars(i, 1); 
    n2 = bars(i, 2);
    x_coords = [nodes(n1,1), nodes(n2,1)];
    y_coords = [nodes(n1,2), nodes(n2,2)];
    
    if axiles(i) > 1e-5
        c = 'b'; lw = 2.5; 
    elseif axiles(i) < -1e-5
        c = 'r'; lw = 2.5; 
    else
        c = 'k'; lw = 1.0; 
    end
    
    plot(x_coords, y_coords, '-', 'Color', c, 'LineWidth', lw, 'HandleVisibility', 'off');
    
    mid_x = mean(x_coords);
    mid_y = mean(y_coords);
    text(mid_x, mid_y, sprintf('%.1f', axiles(i)), ...
        'Color', c, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom', 'BackgroundColor', 'w', 'Margin', 1);
end

%% 5. Draw Supports
for i = 1:size(supports, 1)
    n = supports(i, 1);
    nx = nodes(n, 1);
    ny = nodes(n, 2);
    
    % Draw a square for fixed, triangle for others, to keep it simple
    if supports(i, 2) == 1 && supports(i, 3) == 1
        plot(nx, ny, 'ks', 'MarkerFaceColor', [0.8 0.8 0.8], 'MarkerSize', 12, 'HandleVisibility', 'off');
    else
        plot(nx, ny, 'k^', 'MarkerFaceColor', [0.8 0.8 0.8], 'MarkerSize', 10, 'HandleVisibility', 'off');
    end
end

%% 6. Draw Nodes
plot(nodes(:,1), nodes(:,2), 'ko', 'MarkerFaceColor', 'w', 'MarkerSize', 5, 'HandleVisibility', 'off');

%% 7. Draw Applied Loads (Magenta)
for i = 1:size(loads, 1)
    n = loads(i, 1);
    nx = nodes(n, 1);
    ny = nodes(n, 2);
    Fx = loads(i, 2);
    Fy = loads(i, 3);
    
    if abs(Fx) > 0 || abs(Fy) > 0
        u = Fx * scale_factor;
        v = Fy * scale_factor;
        % Draw arrow pointing TO the node
        quiver(nx - u, ny - v, u, v, 0, 'Color', 'm', 'LineWidth', 1.5, 'MaxHeadSize', 0.5, 'HandleVisibility', 'off');
        % Text label
        text(nx - u, ny - v, sprintf('%.1f', norm([Fx, Fy])), 'Color', 'm', 'VerticalAlignment', 'bottom', 'FontWeight', 'bold');
    end
end

%% 8. Draw Reactions (Green)
for n = 1:size(nodes, 1)
    Rx = rxn_vectors(n, 1);
    Ry = rxn_vectors(n, 2);
    nx = nodes(n, 1);
    ny = nodes(n, 2);
    
    if abs(Rx) > 1e-5 || abs(Ry) > 1e-5
        u = Rx * scale_factor;
        v = Ry * scale_factor;
        % Draw arrow pointing AWAY from the node
        quiver(nx, ny, u, v, 0, 'Color', [0 0.6 0], 'LineWidth', 2, 'MaxHeadSize', 0.5, 'HandleVisibility', 'off');
        % Text label
        text(nx + u, ny + v, sprintf('%.1f', norm([Rx, Ry])), 'Color', [0 0.5 0], 'VerticalAlignment', 'bottom', 'FontWeight', 'bold');
    end
end

legend('Location', 'bestoutside');
set(gca, 'FontSize', 11);
hold off;
%%
ts = datestr(now, 'yyyymmdd_HHMMSS');        
truss_name_png = truss_name + "_" + ts + ".png";
exportgraphics(gca,truss_name_png,'Resolution',300)
end