import fs from "fs";
import React, { useState } from "react";
import { render, Text, Box } from "ink";
import SelectInput from "ink-select-input";
import { useInput, Key } from "ink";

interface Machine {
  Machine_ID: number;
  Machine_Name: string;
  Total_RAM: number;
  Total_CPU: number;
  Total_Storage: number;
}

interface Task {
  Task_ID: number;
  Processing_Time: number;
  Required_RAM: number;
  Required_CPU: number;
  Required_Storage: number;
}

interface Assignment {
  Task_ID: number;
  Assigned_Machine_ID: number;
}

interface MachineScreenProps {
  machine: Machine;
  tasks: Task[];
  onBack: () => void;
}

const MachineScreen: React.FC<MachineScreenProps> = ({
  machine,
  tasks,
  onBack,
}) => {
  useInput((input, key: Key) => {
    if (key.backspace) {
      onBack();
    } else if (key.ctrl && input === "q") {
      process.exit();
    }
  });

  return (
    <Box flexDirection="column">
      <Text>
        <Text bold>VM:</Text> {machine.Machine_Name} (ID::{machine.Machine_ID})
      </Text>
      <Text>Total RAM: {machine.Total_RAM}</Text>
      <Text>Total CPU: {machine.Total_CPU}</Text>
      <Text>Total Stocare: {machine.Total_Storage}</Text>
      <Text>Sarcini Alocate:</Text>
      <Box marginLeft={2} flexDirection="column">
        {tasks.map((task) => (
          <Text key={task.Task_ID}>
            Task {task.Task_ID} - Timp de Procesare: {task.Processing_Time}, RAM:{" "}
            {task.Required_RAM}, CPU: {task.Required_CPU}, Stocare:{" "}
            {task.Required_Storage}
          </Text>
        ))}
      </Box>
      <Text color="cyan">Apăsați Backspace pentru a merge înapoi</Text>
    </Box>
  );
};

const Main = () => {
  const results = JSON.parse(fs.readFileSync("results.json", "utf8"));
  const machines: Machine[] = results.machines;
  const tasks: Task[] = results.tasks;
  const assignments: Assignment[] = results.assignments;

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedMachine, setSelectedMachine] = useState<Machine | null>(null);
  const [currentPage, setCurrentPage] = useState(0);

  const itemsPerPage = 15;

  const filteredMachines = machines.filter(
    (machine) =>
      machine.Machine_Name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(machine.Machine_ID).includes(searchQuery)
  );

  const paginatedMachines = filteredMachines.slice(
    currentPage * itemsPerPage,
    (currentPage + 1) * itemsPerPage
  );

  const machineOptions = paginatedMachines.map((machine) => ({
    label: machine.Machine_Name,
    value: machine,
    key: String(machine.Machine_ID),
  }));

  const totalPages = Math.ceil(filteredMachines.length / itemsPerPage);

  useInput((input, key) => {
    if (key.backspace) {
      setSearchQuery((query) => query.slice(0, -1));
    } else if (!key.return && !key.escape && !key.tab && !key.ctrl) {
      setSearchQuery((query) => query + input);
      setCurrentPage(0);
    } else if (key.rightArrow && input === "" && currentPage < totalPages - 1) {
      setCurrentPage((page) => page + 1); // Go to next page
    } else if (key.leftArrow && input === "" && currentPage > 0) {
      setCurrentPage((page) => page - 1); // Go to previous page
    }
  });

  if (selectedMachine) {
    const assignedTasks = assignments
      .filter((a) => a.Assigned_Machine_ID === selectedMachine.Machine_ID)
      .map((a) => tasks.find((t) => t.Task_ID === a.Task_ID)!);

    return (
      <MachineScreen
        machine={selectedMachine}
        tasks={assignedTasks}
        onBack={() => setSelectedMachine(null)}
      />
    );
  }

  return (
    <Box flexDirection="column">
      <Text bold>
        Selectați o mașină virtuală pentru a vizualiza sarcinile alocate
      </Text>
      <Box>
        <Text>Căutare: </Text>
        <Text color="green">
          {searchQuery || "Începeți să scrieți pentru a căuta..."}
        </Text>
      </Box>
      <SelectInput
        items={machineOptions}
        onSelect={(item) => setSelectedMachine(item.value)}
      />
      <Box marginTop={1}>
        <Text color="yellow">
          Pagina {currentPage + 1} din {totalPages}
        </Text>
      </Box>
      <Text color="cyan">Folosiți CTRL + ArrowLeft / ArrowRight pentru a schimba paginile</Text>
    </Box>
  );
};

console.clear();
render(<Main />);
