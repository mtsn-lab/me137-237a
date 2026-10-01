% Implicit Finite Volume Method

clear all
close all

%% Inputs
L = 0.05; H = 0.01; 
U_inf = 1.0; T_inf = 300; T_wall = 350;
Pr = 0.6818;
nu = 1.5e-5; 
alpha = nu/Pr;
%nu = 1.5e-5; alpha = 2.2e-5;
% nu = 1.5e-5; alpha = 1.5e-5;

Pr = nu/alpha;

nx = 1600; ny = 960; 
% nx = 5000; ny = 2000; 
dx = L/nx; dy = H/ny;
y = linspace(0, H, ny)';

%% Initialization
u = U_inf * ones(ny, nx);
v = zeros(ny, nx);
T = T_inf * ones(ny, nx);

u(1,:) = 0;      % Wall
u(end,:) = U_inf; % Freestream
T(1,:) = T_wall;
T(end,:) = T_inf;

%% Calculations
for i = 1:nx-1
    % 1. SOLVE MOMENTUM (Implicit y, Marching x)
    A = zeros(ny, ny);
    B = zeros(ny, 1);
    for j = 2:ny-1
        u_old = u(j,i);
        v_old = v(j,i); % Using known v from prev station for linearization
        
        c_diff = nu / dy^2;
        c_adv_v = v_old / (2*dy); 
        
        A(j, j-1) = -c_diff - c_adv_v;
        A(j, j)   = (u_old / dx) + 2*c_diff;
        A(j, j+1) = -c_diff + c_adv_v;
        B(j)      = (u_old^2) / dx;
    end
    A(1,1) = 1; B(1) = 0;
    A(end,end) = 1; B(end) = U_inf;
    u(:, i+1) = A \ B;
    
    % 2. SOLVE CONTINUITY (Calculate v_{i+1} immediately)
    for j = 2:ny
        v(j, i+1) = v(j-1, i+1) - (dy/dx) * (u(j, i+1) - u(j, i));
    end
    
    % 3. SOLVE ENERGY (Match Momentum's numerical footprint)
    At = zeros(ny, ny);
    Bt = zeros(ny, 1);
    for j = 2:ny-1
        % To match u exactly at Pr=1, we must use the same velocities used in u's matrix
        u_star = u(j,i); % Use the same linearization velocity as used in u loop
        v_star = v(j,i); 
        
        c_diff_t = alpha / dy^2;
        c_adv_vt = v_star / (2*dy);
        
        At(j, j-1) = -c_diff_t - c_adv_vt;
        At(j, j)   = (u_star / dx) + 2*c_diff_t;
        At(j, j+1) = -c_diff_t + c_adv_vt;
        Bt(j)      = (u_star * T(j, i)) / dx;
    end
    At(1,1) = 1; Bt(1) = T_wall;
    At(end,end) = 1; Bt(end) = T_inf;
    T(:, i+1) = At \ Bt;
end

%{
for i = 1:nx-1
    % 1. SOLVE MOMENTUM (Implicit y, Marching x)
    % Equation: u_prev * (u_new - u_prev)/dx + v_prev * (du/dy)_new = nu * (d2u/dy2)_new
    A = zeros(ny, ny);
    B = zeros(ny, 1);
    
    for j = 2:ny-1
        u_old = u(j,i);
        v_old = v(j,i);
        
        % Finite Volume coefficients
        % Upwind for vertical advection for stability
        c_diff = nu / dy^2;
        c_adv_v = v_old / (2*dy);
        
        A(j, j-1) = -c_diff - c_adv_v;
        A(j, j)   = (u_old / dx) + 2*c_diff;
        A(j, j+1) = -c_diff + c_adv_v;
        
        B(j) = (u_old^2) / dx;
    end
    
    % Boundary Conditions for Momentum
    A(1,1) = 1; B(1) = 0;
    A(end,end) = 1; B(end) = U_inf;
    
    u(:, i+1) = A \ B;
    
    % 2. SOLVE CONTINUITY (for v)
    % dv/dy = -du/dx
    for j = 2:ny
        v(j, i+1) = v(j-1, i+1) - (dy/dx) * (u(j, i+1) - u(j, i));
    end
    
    % 3. SOLVE ENERGY (Implicit y, Marching x)
    At = zeros(ny, ny);
    Bt = zeros(ny, 1);
    for j = 2:ny-1
        c_diff_t = alpha / dy^2;
        At(j, j-1) = -c_diff_t - c_adv_v;
        At(j, j)   = (u(j, i+1) / dx) + 2*c_diff_t;
        At(j, j+1) = -c_diff_t + c_adv_v;
        Bt(j)      = (u(j, i+1) * T(j, i)) / dx;
    end
    At(1,1) = 1; Bt(1) = T_wall;
    At(end,end) = 1; Bt(end) = T_inf;
    
    T(:, i+1) = At \ Bt;
end
%}

%% Plotting 
[X, Y] = meshgrid(linspace(0, L, nx), y);
figure('Position', [100, 100, 1000, 400]);

subplot(1,2,1);
contourf(X, Y, u, 20, 'LineColor', 'none'); colorbar;
title('Velocity u (m/s)'); xlabel('x (m)'); ylabel('y (m)');

subplot(1,2,2);
contourf(X, Y, T, 20, 'LineColor', 'none'); colorbar;
colormap('hot');
title('Temperature (K)'); xlabel('x (m)'); ylabel('y (m)');

%% Dimensional analysis

% grid arrays (matching the solver)
x_coords = linspace(dx, L, nx); % Avoid x=0 to prevent division by zero
[X, Y] = meshgrid(x_coords, y);

% Similarity Variable (Eta)
Eta = Y .* sqrt(U_inf ./ (nu .* X));

% Non-dimensional Velocity (f') and Temperature (Theta)
f_prime = u ./ U_inf;
Theta = (T - T_wall) ./ (T_inf - T_wall);

figure('Name', 'Similarity Analysis', 'Position', [200, 200, 1000, 450]);

% Velocity
subplot(1,2,1); hold on; grid on;
stations_to_plot = round(linspace(nx*0.2, nx*0.8, 5)); 

for s = stations_to_plot
    plot(f_prime(:, s), Eta(:, s), 'LineWidth', 1.5, ...
         'DisplayName', sprintf('x = %.3f m', x_coords(s)));
end
xlabel('f'' (\eta) = u/U_\infty');
ylabel('\eta');
ylim([0 4]);
legend('Location', 'best');

subplot(1,2,2); hold on; grid on;
for s = stations_to_plot
    plot(Theta(:, s), Eta(:, s), 'LineWidth', 1.5, ...
         'DisplayName', sprintf('x = %.3f m', x_coords(s)));
end
xlabel('\theta(\eta) = (T-T_w)/(T_\infty-T_w)'); % (T - T_wall) ./ (T_inf - T_wall)
ylabel('\eta');
ylim([0 4]);
legend('Location', 'best');
