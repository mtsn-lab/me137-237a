% Load required libraries into workspace
load_system('simulink');
load_system('fl_lib');
load_system('nesl_utility');

% Initialize new model
modelName = 'CPU_Thermal_Conduction';
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end
new_system(modelName);
open_system(modelName);

% Add Simulink, Simscape, and Converter Blocks
add_block('simulink/Sources/Constant',                            [modelName '/Power_Val']);
add_block('nesl_utility/Simulink-PS Converter',                   [modelName '/S2P_Power']);
add_block('fl_lib/Thermal/Thermal Sources/Ideal Heat Flow Source',   [modelName '/CPU_Power']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Mass',          [modelName '/Silicon_Die']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Resistance',    [modelName '/TIM_Spreader']);
add_block('simulink/Sources/Constant',                            [modelName '/Amb_Val']);
add_block('nesl_utility/Simulink-PS Converter',                   [modelName '/S2P_Amb']);
add_block('fl_lib/Thermal/Thermal Sources/Ideal Temperature Source', [modelName '/Ambient_Air']);
add_block('fl_lib/Thermal/Thermal Elements/Thermal Reference',    [modelName '/Thermal_Ref']);
add_block('fl_lib/Thermal/Thermal Sensors/Temperature Sensor',    [modelName '/Temp_Sensor']);
add_block('nesl_utility/Solver Configuration',                     [modelName '/Solver_Config']);
add_block('nesl_utility/PS-Simulink Converter',                    [modelName '/P2S_Temp']);
add_block('simulink/Sinks/Scope',                                 [modelName '/Scope']);
add_block('simulink/Sinks/Out1', [modelName '/Out1']);

% Set Parameters
set_param([modelName '/Power_Val'], 'Value', '65');                      % 65 W heat input
set_param([modelName '/Silicon_Die'], 'mass', '0.015', 'sp_heat', '710');  % Mass & specific heat
set_param([modelName '/TIM_Spreader'], 'resistance', '0.5');             % Thermal resistance (K/W)
set_param([modelName '/Amb_Val'], 'Value', '298.15');                    % 25 degC ambient (298.15 K)
set_param([modelName '/P2S_Temp'], 'Unit', 'degC');                      % Physical unit output

% Create Handles
h_S2P_Power = get_param([modelName '/S2P_Power'], 'PortHandles');
h_CPU_Power  = get_param([modelName '/CPU_Power'], 'PortHandles');
h_S2P_Amb = get_param([modelName '/S2P_Amb'], 'PortHandles');
h_Ambient_Air = get_param([modelName '/Ambient_Air'], 'PortHandles');
h_Thermal_Ref = get_param([modelName '/Thermal_Ref'], 'PortHandles');
h_Silicon_Die = get_param([modelName '/Silicon_Die'], 'PortHandles');
h_TIM_Spreader = get_param([modelName '/TIM_Spreader'], 'PortHandles');
h_Temp_Sensor = get_param([modelName '/Temp_Sensor'], 'PortHandles');
h_P2S_Temp = get_param([modelName '/P2S_Temp'], 'PortHandles');
h_Solver_Config = get_param([modelName '/Solver_Config'], 'PortHandles');

% Connect Physical & Signal Lines directly by Port Names
add_line(modelName, 'Power_Val/1',   'S2P_Power/1',   'autorouting', 'on');
add_line(modelName, h_S2P_Power.RConn(1), h_CPU_Power.RConn(1), 'autorouting', 'on');
add_line(modelName, 'Amb_Val/1',     'S2P_Amb/1',     'autorouting', 'on');
add_line(modelName, h_S2P_Amb.RConn(1), h_Ambient_Air.RConn(1), 'autorouting', 'on');
add_line(modelName, h_Thermal_Ref.LConn(1), h_CPU_Power.RConn(2), 'autorouting', 'on');
add_line(modelName, h_CPU_Power.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_TIM_Spreader.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_TIM_Spreader.RConn(1), h_Ambient_Air.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Thermal_Ref.LConn(1), h_Ambient_Air.RConn(2), 'autorouting', 'on');
add_line(modelName, h_Temp_Sensor.LConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Thermal_Ref.LConn(1), h_Temp_Sensor.RConn(1), 'autorouting', 'on');
add_line(modelName, h_Temp_Sensor.RConn(2), h_P2S_Temp.LConn(1), 'autorouting', 'on');
add_line(modelName, 'P2S_Temp/1',     'Scope/1',        'autorouting', 'on');
add_line(modelName, h_Solver_Config.RConn(1), h_Silicon_Die.LConn(1), 'autorouting', 'on');
add_line(modelName, 'P2S_Temp/1', 'Out1/1', 'autorouting', 'on');

% Auto-arrange model diagram layout
Simulink.BlockDiagram.arrangeSystem(modelName);

% Save and simulate model
save_system(modelName);
simOut = sim(modelName, 'StopTime', '30');

% Extract data from Outport (yout)
tempData = simOut.yout.get(1).Values;

% Plot junction temperature
figure;
plot(tempData.Time, tempData.Data, 'LineWidth', 1.5);
grid on;
xlabel('Time (s)');
ylabel('Die Temperature (°C)');