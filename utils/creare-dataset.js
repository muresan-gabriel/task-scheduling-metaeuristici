import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { uniqueNamesGenerator, adjectives, animals } from 'unique-names-generator';


// Parameters for dataset
const numTasks = 100; // Number of tasks
const numMachines = 10; // Number of machines (VMs)

// Utility functions
const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const getRandomFloat = (min, max, decimals = 2) => {
  const factor = Math.pow(10, decimals);
  return Math.round((Math.random() * (max - min) + min) * factor) / factor;
};

// Get current directory for output files
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Generate tasks
const tasks = Array.from({ length: numTasks }, (_, i) => ({
  Task_ID: i + 1,
  Processing_Time: getRandomInt(1, 1000),
  Required_RAM: getRandomInt(128, 8192),
  Required_CPU: getRandomFloat(0.1, 4.0),
  Required_Storage: getRandomInt(1, 500),
}));

// Generate machines
const machines = Array.from({ length: numMachines }, (_, i) => {
  const machineName = uniqueNamesGenerator({
    dictionaries: [adjectives, animals],
    length: 2,
    style: 'capital', // Capitalize first letter of each word
    separator: '', // No separator
  });
  return {
    Machine_ID: i + 1,
    Machine_Name: machineName.charAt(0).toUpperCase() + machineName.slice(1),
    Total_RAM: getRandomInt(8192, 65536),
    Total_CPU: getRandomFloat(4, 64),
    Total_Storage: getRandomInt(500, 2000),
  };
});

// Save datasets to CSV
const tasksCsv = tasks.map(task => Object.values(task).join(',')).join('\n');
const machinesCsv = machines.map(machine => Object.values(machine).join(',')).join('\n');

// Add headers
const tasksCsvWithHeader = `Task_ID,Processing_Time,Required_RAM,Required_CPU,Required_Storage\n${tasksCsv}`;
const machinesCsvWithHeader = `Machine_ID,Machine_Name,Total_RAM,Total_CPU,Total_Storage\n${machinesCsv}`;

// File paths
const tasksFilePath = path.join(__dirname, '../data/Cloud_Task_Scheduling_Tasks.csv');
const machinesFilePath = path.join(__dirname, '../data/Cloud_Task_Scheduling_Machines.csv');

// Write files
fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });
fs.writeFileSync(tasksFilePath, tasksCsvWithHeader, 'utf8');
fs.writeFileSync(machinesFilePath, machinesCsvWithHeader, 'utf8');

console.log(`Dataset-uri create:`);
console.log(`- Sarcini: ${tasksFilePath}`);
console.log(`- VM-uri: ${machinesFilePath}`);
