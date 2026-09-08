% Load required libraries into workspace
load_system('simulink');
load_system('fl_lib');
load_system('nesl_utility');

% Initialize new model
modelName = 'Duct_Thermofluid_Flow';
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end
new_system(modelName);
open_system(modelName);

% Add Simulink, Simscape, and Converter Blocks
add_block('simulink/Sources/Constant',                            [modelName '/Flow_Val']);
add_block('nesl_utility/Simulink-PS Converter',                   [modelName '/S2P_Flow']);
add_block('fl_lib/Gas/Sources/Flow Rate Source (G)',         [modelName '/Mass_Flow_Source']);

% Gas Elements and Utilities
add_block('fl_lib/Gas/Elements/Reservoir (G)',                     [modelName '/Inlet_Reservoir']);
add_block('fl_lib/Gas/Elements/Pipe (G)',                         [modelName '/Duct']);
add_block('fl_lib/Gas/Elements/Reservoir (G)',                     [modelName '/Outlet_Reservoir']);
add_block('fl_lib/Gas/Utilities/Gas Properties (G)',          [modelName '/Gas_Properties']);
add_block('fl_lib/Gas/Sensors/Pressure & Temperature Sensor (G)', [modelName '/Pressure_Sensor']);
add_block('fl_lib/Gas/Sensors/Pressure & Temperature Sensor (G)', [modelName '/Pressure_Sensor_2']);
add_block('nesl_utility/Solver Configuration',                     [modelName '/Solver_Config']);
add_block('nesl_utility/PS-Simulink Converter',                    [modelName '/P2S_Press']);
add_block('nesl_utility/PS-Simulink Converter',                    [modelName '/P2S_Press_2']);
add_block('simulink/Sinks/Scope',                                 [modelName '/Scope']);
add_block('simulink/Sinks/Out1',                                  [modelName '/Out1']);
add_block('simulink/Sinks/Out1',                                  [modelName '/Out2']);

% Set Block Parameters
set_param([modelName '/Flow_Val'], 'Value', '0.02');               % 0.02 kg/s mass flow rate
set_param([modelName '/P2S_Press'], 'Unit', 'Pa');                % Pressure signal output in Pascals
set_param([modelName '/P2S_Press_2'], 'Unit', 'Pa');                % Pressure signal output in Pascals
set_param([modelName '/Scope'], 'NumInputPorts', '2');
set_param([modelName '/Duct'], 'length', '0.5', 'area', '0.0025'); % 0.5m length, 50mm x 50mm duct

% Create Handles
h_S2P_Flow         = get_param([modelName '/S2P_Flow'], 'PortHandles');
h_Mass_Flow_Source = get_param([modelName '/Mass_Flow_Source'], 'PortHandles');
h_Inlet_Reservoir  = get_param([modelName '/Inlet_Reservoir'], 'PortHandles');
h_Duct             = get_param([modelName '/Duct'], 'PortHandles');
h_Outlet_Reservoir = get_param([modelName '/Outlet_Reservoir'], 'PortHandles');
h_Gas_Properties   = get_param([modelName '/Gas_Properties'], 'PortHandles');
h_Pressure_Sensor  = get_param([modelName '/Pressure_Sensor'], 'PortHandles');
h_Pressure_Sensor_2  = get_param([modelName '/Pressure_Sensor_2'], 'PortHandles');
h_P2S_Press        = get_param([modelName '/P2S_Press'], 'PortHandles');
h_P2S_Press_2      = get_param([modelName '/P2S_Press_2'], 'PortHandles');
h_Solver_Config    = get_param([modelName '/Solver_Config'], 'PortHandles');

% Connect Physical & Signal Lines via Port Handles
add_line(modelName, 'Flow_Val/1',   'S2P_Flow/1',   'autorouting', 'on');
add_line(modelName, h_S2P_Flow.RConn(1), h_Mass_Flow_Source.LConn(2), 'autorouting', 'on');
add_line(modelName, h_Inlet_Reservoir.LConn(1), h_Mass_Flow_Source.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Mass_Flow_Source.RConn(1), h_Duct.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Duct.RConn(1), h_Outlet_Reservoir.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Duct.LConn(1), h_Pressure_Sensor.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Duct.RConn(1), h_Pressure_Sensor_2.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Pressure_Sensor.RConn(1), h_P2S_Press.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Pressure_Sensor_2.RConn(1), h_P2S_Press_2.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Solver_Config.RConn(1), h_Duct.LConn(1), 'autorouting', 'on');
add_line(modelName, h_Gas_Properties.RConn(1), h_Duct.LConn(1), 'autorouting', 'on');
% Connect Signal Outputs
add_line(modelName, 'P2S_Press/1', 'Scope/1', 'autorouting', 'on');
add_line(modelName, 'P2S_Press_2/1', 'Scope/2', 'autorouting', 'on');
add_line(modelName, 'P2S_Press/1', 'Out1/1',  'autorouting', 'on');
add_line(modelName, 'P2S_Press_2/1', 'Out2/1',  'autorouting', 'on');

% Auto-arrange model diagram layout
Simulink.BlockDiagram.arrangeSystem(modelName);

% Save and simulate model
save_system(modelName);
simOut = sim(modelName, 'StopTime', '10');

% Extract data
pressData1 = simOut.yout.get(1).Values;

% Pressure differential
deltaP = simOut.yout.get(1).Values.Data - simOut.yout.get(2).Values.Data;

% Plot pressure drop across duct
figure;
% plot(pressData1.Time, pressData1.Data, 'LineWidth', 1.5);
plot(pressData1.Time, deltaP, 'LineWidth', 1.5);
grid on;
xlabel('Time (s)');
ylabel('Duct Pressure Drop (Pa)');