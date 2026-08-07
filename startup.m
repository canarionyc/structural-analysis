% Dark Mode Plotting Setup (Corrected)
% Add this to your startup.m file

% % 1. Set the Figure Background to Dark Gray
% set(groot, 'defaultFigureColor', [0.15 0.15 0.15]);
% 
% % 2. Set Axes Background and Spines
% set(groot, 'defaultAxesColor', [0.15 0.15 0.15]);
% set(groot, 'defaultAxesXColor', [0.9 0.9 0.9]); % Affects X-axis line AND X-Label
% set(groot, 'defaultAxesYColor', [0.9 0.9 0.9]); % Affects Y-axis line AND Y-Label
% set(groot, 'defaultAxesZColor', [0.9 0.9 0.9]); % Affects Z-axis line AND Z-Label
% set(groot, 'defaultAxesGridColor', [0.4 0.4 0.4]);
% 
% % 3. Set Default Text Color (This fixes Title and arbitrary Text)
% set(groot, 'defaultTextColor', [1 1 1]);
% 
% % 4. Optional: Color Order
% bright_colors = [0 1 1; 1 0 1; 1 1 0; 0 1 0; 0.5 0.5 1; 1 0.5 0];
% set(groot, 'defaultAxesColorOrder', bright_colors);

% Force Light Theme for Plots (Paper-friendly)
% Even if MATLAB is in Dark Mode

% 1. Equivalent to figure.facecolor : white
set(groot, 'defaultFigureColor', 'w');

% 2. Equivalent to axes.facecolor : white
set(groot, 'defaultAxesColor', 'w');

% 3. Ensure Text and Axis Lines are Black (Crucial for visibility on white)
% If your system is dark, MATLAB might try to make these white/light gray
set(groot, 'defaultAxesXColor', 'k');
set(groot, 'defaultAxesYColor', 'k');
set(groot, 'defaultAxesZColor', 'k');
set(groot, 'defaultTextColor', 'k');  % Forces titles and labels to black

% 4. Optional: Set default grid to a soft gray (standard look)
set(groot, 'defaultAxesGridColor', [0.15 0.15 0.15]);
set(groot, 'defaultAxesGridAlpha', 0.15);

%% added by matlab copilot

% startup.m — ensure legend background = white, text = black

% Function to update legend appearance
function updateAllLegends()
    lg = findall(0,'Type','legend');
    for k = 1:numel(lg)
        try
            % text color
            lg(k).TextColor = [0 0 0];
        catch
            try, set(lg(k),'TextColor',[0 0 0]); end
        end
        try
            % New graphics: BoxFace controls legend patch
            lg(k).BoxFace.ColorType = 'truecoloralpha';
            lg(k).BoxFace.Color = [1 1 1];
            lg(k).BoxFace.FaceAlpha = 1;
            lg(k).EdgeColor = [0 0 0];
        catch
            % Fallback for older releases
            try, set(lg(k),'Color',[1 1 1],'EdgeColor',[0 0 0]); end
        end
    end
end

% Update any existing legends now
updateAllLegends();

% Ensure legends in newly created figures get fixed:
set(groot,'DefaultFigureCreateFcn',@(f,~) onFigureCreate(f));

function onFigureCreate(fig)
    % When a new figure is created, update any current legends and
    % attach listener to update legends whenever children change.
    updateAllLegends();
    addlistener(fig,'ObjectChildAdded',@(src,ev) updateAllLegends());
end