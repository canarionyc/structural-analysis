%% Master Plot: Geometry, Supports, and Axial Forces
figure('Name', 'Análisis de Cercha (Geometría y Esfuerzos)', 'Color', 'w');
hold on; grid on; axis equal;

title('Cercha: Geometría, Apoyos y Esfuerzos Axiles');
xlabel('Eje X (m)');
ylabel('Eje Y (m)');

% Dummy plots to generate a clean legend
plot(NaN, NaN, 'b-', 'LineWidth', 2, 'DisplayName', 'Tracción (+)');
plot(NaN, NaN, 'r-', 'LineWidth', 2, 'DisplayName', 'Compresión (-)');
plot(NaN, NaN, 'k-', 'LineWidth', 1, 'DisplayName', 'Nulo (0)');

% Plot elements with color-coded forces and text labels
for i = 1:num_bars
    n1 = bars(i, 1); 
    n2 = bars(i, 2);
    x_coords = [nodes(n1,1), nodes(n2,1)];
    y_coords = [nodes(n1,2), nodes(n2,2)];
    
    % Determine color and line weight based on the axial force
    if axiles(i) > 1e-5
        c = 'b'; lw = 2.5; % Tension
    elseif axiles(i) < -1e-5
        c = 'r'; lw = 2.5; % Compression
    else
        c = 'k'; lw = 1.0; % Zero force
    end
    
    % Draw the bar (HandleVisibility off prevents duplicating legend entries)
    plot(x_coords, y_coords, '-', 'Color', c, 'LineWidth', lw, 'HandleVisibility', 'off');
    
    % Add text label with the exact axial value at the midpoint
    mid_x = mean(x_coords);
    mid_y = mean(y_coords);
    text(mid_x, mid_y, sprintf('%.1f', axiles(i)), ...
        'Color', c, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom', 'BackgroundColor', 'w', 'Margin', 1);
end

% Plot Nodes
plot(nodes(:,1), nodes(:,2), 'ko', 'MarkerFaceColor', 'w', 'MarkerSize', 6, 'DisplayName', 'Nodos');

% Plot Supports (Triangles shifted slightly down for clarity)
plot(nodes(1,1), nodes(1,2)-0.2, '^', 'Color', [0 0.5 0], 'MarkerFaceColor', [0 0.8 0], 'MarkerSize', 10, 'DisplayName', 'Apoyo Móvil');
plot(nodes(4,1), nodes(4,2)-0.2, '^', 'Color', [0.5 0 0.5], 'MarkerFaceColor', [0.8 0 0.8], 'MarkerSize', 10, 'DisplayName', 'Apoyo Fijo');

legend('Location', 'bestoutside');
set(gca, 'FontSize', 11);
hold off;

%% 
?plotforc
