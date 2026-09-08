% Load required libraries into workspace
load_system('simulink');
load_system('fl_lib');
load_system('nesl_utility');

% Initialize new model
modelName = 'Forced_Convective_Cooling';
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end
new_system(modelName);
open_system(modelName);

% Add Simulink, Simscape, and Converter Blocks
% --- Thermal Domain Blocks ---
add_block('simulink/Sources/Constant',                            [modelName '/Power_Val']);
add_block('nesl_utility/Simulink-PS Converter',                   [modelName '/S2P_Power']);
add_block('fl_lib/Thermal/Thermal Sources/Ideal Heat Flow Source',   [modelName '/CPU_Power']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Mass',          [modelName '/Silicon_Die']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Resistance',    [modelName '/TIM_Spreader']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Reference',    [modelName '/Thermal_Ref']);
add_block('fl_lib/Thermal/Thermal Sensors/Temperature Sensor',    [modelName '/Die_Temp_Sensor']);
add_block('nesl_utility/PS-Simulink Converter',                    [modelName '/P2S_Die_Temp']);

% --- Thermofluid (Gas) Domain Blocks ---
add_block('simulink/Sources/Constant',                            [modelName '/Flow_Val']);
add_block('nesl_utility/Simulink-PS Converter',                   [modelName '/S2P_Flow']);
add_block('fl_lib/Gas/Sources/Flow Rate Source (G)',         [modelName '/Mass_Flow_Source']);
add_block('fl_lib/Gas/Elements/Reservoir (G)',                     [modelName '/Inlet_Reservoir']);
add_block('fl_lib/Gas/Elements/Pipe (G)',                         [modelName '/Duct']);
add_block('fl_lib/Gas/Elements/Reservoir (G)',                     [modelName '/Outlet_Reservoir']);
add_block('fl_lib/Gas/Utilities/Gas Properties (G)',          [modelName '/Gas_Properties']);
add_block('fl_lib/Gas/Sensors/Pressure & Temperature Sensor (G)', [modelName '/Air_Temp_Sensor']);
add_block('nesl_utility/PS-Simulink Converter',                    [modelName '/P2S_Air_Temp']);

% --- Utilities & Sinks ---
add_block('nesl_utility/Solver Configuration',                     [modelName '/Solver_Config']);
add_block('simulink/Sinks/Scope',                                 [modelName '/Scope']);
add_block('simulink/Sinks/Out1',                                  [modelName '/Out1']);
add_block('simulink/Sinks/Out1',                                  [modelName '/Out2']);

% Set Block Parameters
% Thermal Parameters
set_param([modelName '/Power_Val'], 'Value', '65');                      % 65 W CPU power
set_param([modelName '/Silicon_Die'], 'mass', '0.015', 'sp_heat', '710');  % 15g silicon die
set_param([modelName '/TIM_Spreader'], 'resistance', '0.2');             % Thermal resistance (K/W)
set_param([modelName '/P2S_Die_Temp'], 'Unit', 'degC');                  % Output in degC

% Gas & Flow Parameters
set_param([modelName '/Flow_Val'], 'Value', '0.02');               % 0.02 kg/s forced mass flow
set_param([modelName '/Duct'], 'length', '0.5', 'area', '0.0025'); % 0.5m length, 50mm x 50mm duct
set_param([modelName '/P2S_Air_Temp'], 'Unit', 'degC');            % Output in degC
set_param([modelName '/Scope'], 'NumInputPorts', '2');

% Create Handles
h_S2P_Power        = get_param([modelName '/S2P_Power'], 'PortHandles');
h_CPU_Power        = get_param([modelName '/CPU_Power'], 'PortHandles');
h_Thermal_Ref      = get_param([modelName '/Thermal_Ref'], 'PortHandles');
h_Silicon_Die      = get_param([modelName '/Silicon_Die'], 'PortHandles');
h_TIM_Spreader     = get_param([modelName '/TIM_Spreader'], 'PortHandles');
h_Die_Temp_Sensor  = get_param([modelName '/Die_Temp_Sensor'], 'PortHandles');
h_P2S_Die_Temp     = get_param([modelName '/P2S_Die_Temp'], 'PortHandles');

h_S2P_Flow         = get_param([modelName '/S2P_Flow'], 'PortHandles');
h_Mass_Flow_Source = get_param([modelName '/Mass_Flow_Source'], 'PortHandles');
h_Inlet_Reservoir  = get_param([modelName '/Inlet_Reservoir'], 'PortHandles');
h_Duct             = get_param([modelName '/Duct'], 'PortHandles');
h_Outlet_Reservoir = get_param([modelName '/Outlet_Reservoir'], 'PortHandles');
h_Gas_Properties   = get_param([modelName '/Gas_Properties'], 'PortHandles');
h_Air_Temp_Sensor  = get_param([modelName '/Air_Temp_Sensor'], 'PortHandles');
h_P2S_Air_Temp     = get_param([modelName '/P2S_Air_Temp'], 'PortHandles');
h_Solver_Config    = get_param([modelName '/Solver_Config'], 'PortHandles');

% Connect Physical & Signal Lines via Port Handles
% 1. Thermal Domain Wiring
add_line(modelName, 'Power_Val/1',   'S2P_Power/1',   'autorouting', 'on');
add_line(modelName, h_S2P_Power.RConn(1), h_CPU_Power.RConn(1), 'autorouting', 'on');
add_line(modelName, h_Thermal_Ref.LConn(1), h_CPU_Power.RConn(2), 'autorouting', 'on');
add_line(modelName, h_CPU_Power.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_TIM_Spreader.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');

% Die Temperature Sensing
add_line(modelName, h_Die_Temp_Sensor.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Thermal_Ref.LConn(1), h_Die_Temp_Sensor.RConn(1), 'autorouting', 'on');
add_line(modelName, h_Die_Temp_Sensor.RConn(2), h_P2S_Die_Temp.LConn(1), 'autorouting', 'on');

% 2. Thermofluid Domain Wiring
add_line(modelName, 'Flow_Val/1',   'S2P_Flow/1',   'autorouting', 'on');
add_line(modelName, h_S2P_Flow.RConn(1), h_Mass_Flow_Source.LConn(2), 'autorouting', 'on');
add_line(modelName, h_Inlet_Reservoir.LConn(1), h_Mass_Flow_Source.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Mass_Flow_Source.RConn(1), h_Duct.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Duct.RConn(1), h_Outlet_Reservoir.LConn(1), 'autorouting', 'on');

% Air Outlet Temperature Sensing
add_line(modelName, h_Duct.RConn(1), h_Air_Temp_Sensor.LConn(1), 'autorouting', 'on');


%% Manually change the pressure/temperature sensor to read temperature only.
% manually connect everything...

%{
add_line(modelName, h_Air_Temp_Sensor.RConn(1), h_P2S_Air_Temp.LConn(1), 'autorouting', 'on');

% 3. Multi-Domain Coupling: Connect Spreader (Thermal) to Duct Surface Thermal Port H (Thermofluid)
add_line(modelName, h_TIM_Spreader.RConn(1), h_Duct.LConn(2), 'autorouting', 'on');

% Solver & Gas Property Setup
add_line(modelName, h_Solver_Config.RConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Gas_Properties.RConn(1), h_Duct.LConn(1), 'autorouting', 'on');

% Connect Signal Outputs to Scope and Outports
add_line(modelName, 'P2S_Die_Temp/1', 'Scope/1', 'autorouting', 'on');
add_line(modelName, 'P2S_Air_Temp/1', 'Scope/2', 'autorouting', 'on');
add_line(modelName, 'P2S_Die_Temp/1', 'Out1/1',  'autorouting', 'on');
add_line(modelName, 'P2S_Air_Temp/1', 'Out2/1',  'autorouting', 'on');

% Auto-arrange model diagram layout
Simulink.BlockDiagram.arrangeSystem(modelName);

% Save and simulate model
save_system(modelName);
simOut = sim(modelName, 'StopTime', '30');

% Extract logged data
dieTempData = simOut.yout.get(1).Values;
airTempData = simOut.yout.get(2).Values;

% Plot transient temperature response
figure;
plot(dieTempData.Time, dieTempData.Data, 'r-', 'LineWidth', 1.5); hold on;
plot(airTempData.Time, airTempData.Data, 'b--', 'LineWidth', 1.5);
grid on;
xlabel('Time (s)');
ylabel('Temperature (°C)');
legend('CPU Die Temperature', 'Air Outlet Temperature', 'Location', 'best');
title('Coupled Forced Convective Cooling Response');
%}