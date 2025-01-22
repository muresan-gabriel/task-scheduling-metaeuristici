import numpy as np
import random
from datetime import datetime
from tqdm import tqdm
import json

class Machine:
    def __init__(self, id, total_ram, total_cpu, total_storage, name=None):
        self.id = id
        self.total_ram = total_ram
        self.total_cpu = total_cpu
        self.total_storage = total_storage
        self.name = name or f"Machine_{id}"


class Task:
    def __init__(self, id, processing_time, required_ram, required_cpu, required_storage):
        self.id = id
        self.processing_time = processing_time
        self.required_ram = required_ram
        self.required_cpu = required_cpu
        self.required_storage = required_storage


class Solution:
    def __init__(self, assignments=None):
        self.assignments = assignments if assignments else []

    def crossover(self, other, machines, tasks):
        point = random.randint(0, len(self.assignments) - 1)
        child1_assignments = self.assignments[:point] + other.assignments[point:]
        child2_assignments = other.assignments[:point] + self.assignments[point:]
        
        child1 = Solution(child1_assignments)
        child2 = Solution(child2_assignments)
        
        validate_and_repair(child1, machines, tasks)
        validate_and_repair(child2, machines, tasks)
        
        return child1, child2

    def mutate(self, mutation_rate, machines, tasks):
        for i in range(len(self.assignments)):
            if random.random() < mutation_rate:
                self.assignments[i] = random.choice(machines).id
        validate_and_repair(self, machines, tasks)


def fitness(solution, machines, tasks):
    penalties = 0
    machine_usage = {machine.id: {"RAM": 0, "CPU": 0, "Storage": 0} for machine in machines}

    for task, machine_id in zip(tasks, solution.assignments):
        machine = next((m for m in machines if m.id == machine_id), None)
        
        if not machine:
            # Penalize heavily for invalid assignments
            penalties += 1000  # Arbitrary high penalty for unassigned tasks
            continue
        
        machine_usage[machine.id]["RAM"] += task.required_ram
        machine_usage[machine.id]["CPU"] += task.required_cpu
        machine_usage[machine.id]["Storage"] += task.required_storage

        # Check for resource overflow and add penalties
        for resource, limit in [("RAM", machine.total_ram), ("CPU", machine.total_cpu), ("Storage", machine.total_storage)]:
            if machine_usage[machine.id][resource] > limit:
                penalties += (machine_usage[machine.id][resource] - limit)  # Penalize based on overflow

    return -penalties


def load_machines(file_path):
    machines = []
    with open(file_path, "r") as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split(",")
            machine_id = int(parts[0])
            name = parts[1]
            ram = int(parts[2])
            cpu = float(parts[3])
            storage = int(parts[4])
            machines.append(Machine(machine_id, ram, cpu, storage, name))
    return machines


def load_tasks(file_path):
    tasks = []
    with open(file_path, "r") as file:
        next(file)
        for line in file:
            task_id, time, ram, cpu, storage = map(float, line.strip().split(","))
            tasks.append(Task(int(task_id), int(time), int(ram), cpu, int(storage)))
    return tasks


def validate_and_repair(solution, machines, tasks):
    # Initialize usage for each machine
    machine_usage = {machine.id: {"RAM": 0, "CPU": 0, "Storage": 0} for machine in machines}
    
    for i, (task, machine_id) in enumerate(zip(tasks, solution.assignments)):
        # Ensure machine_id is valid
        machine = next((m for m in machines if m.id == machine_id), None)
        
        if not machine:
            # Invalid machine_id, reassign task to a valid machine
            valid_machines = [
                m.id for m in machines if
                m.total_ram >= task.required_ram and
                m.total_cpu >= task.required_cpu and
                m.total_storage >= task.required_storage
            ]
            if valid_machines:
                solution.assignments[i] = random.choice(valid_machines)
                machine_id = solution.assignments[i]
                machine = next(m for m in machines if m.id == machine_id)
            else:
                # If no valid machine is found, mark task as unassigned
                solution.assignments[i] = -1
                continue
        
        # Check if the task fits on the assigned machine
        usage = machine_usage[machine.id]
        if (
            usage["RAM"] + task.required_ram > machine.total_ram or
            usage["CPU"] + task.required_cpu > machine.total_cpu or
            usage["Storage"] + task.required_storage > machine.total_storage
        ):
            # Reassign task to a valid machine
            valid_machines = [
                m.id for m in machines if
                machine_usage[m.id]["RAM"] + task.required_ram <= m.total_ram and
                machine_usage[m.id]["CPU"] + task.required_cpu <= m.total_cpu and
                machine_usage[m.id]["Storage"] + task.required_storage <= m.total_storage
            ]
            if valid_machines:
                solution.assignments[i] = random.choice(valid_machines)
                machine_id = solution.assignments[i]
                machine = next(m for m in machines if m.id == machine_id)
            else:
                # If no valid machine is found, mark task as unassigned
                solution.assignments[i] = -1
                continue

        # Update the machine's usage
        machine_usage[machine.id]["RAM"] += task.required_ram
        machine_usage[machine.id]["CPU"] += task.required_cpu
        machine_usage[machine.id]["Storage"] += task.required_storage


def genetic_algorithm(machines, tasks, population_size, generations, mutation_rate):
    # Initialize the population
    population = [Solution([random.choice(machines).id for _ in tasks]) for _ in range(population_size)]

    for _ in tqdm(range(generations), desc="Alocare Sarcini"):
        # Sort population by fitness
        population = sorted(population, key=lambda sol: fitness(sol, machines, tasks), reverse=True)

        next_generation = []
        while len(next_generation) < population_size:
            # Select parents
            parent1 = random.choice(population[:10])  # Select top solutions for crossover
            parent2 = random.choice(population[:10])
            
            # Perform crossover
            child1, child2 = parent1.crossover(parent2, machines, tasks)

            # Mutate and ensure valid solutions
            child1.mutate(mutation_rate, machines, tasks)
            child2.mutate(mutation_rate, machines, tasks)

            next_generation.extend([child1, child2])

        # Prepare the next generation
        population = next_generation[:population_size]

    # Return the best solution in the final generation
    return max(population, key=lambda sol: fitness(sol, machines, tasks))


def save_results(machines, tasks, solution, output_file="results.json"):
    results = {
        "machines": [
            {
                "Machine_ID": machine.id,
                "Machine_Name": machine.name,
                "Total_RAM": machine.total_ram,
                "Total_CPU": machine.total_cpu,
                "Total_Storage": machine.total_storage
            }
            for machine in machines
        ],
        "tasks": [
            {
                "Task_ID": task.id,
                "Processing_Time": task.processing_time,
                "Required_RAM": task.required_ram,
                "Required_CPU": task.required_cpu,
                "Required_Storage": task.required_storage
            }
            for task in tasks
        ],
        "assignments": [
            {"Task_ID": tasks[i].id, "Assigned_Machine_ID": machine_id}
            for i, machine_id in enumerate(solution.assignments)
        ]
    }

    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)


def main():
    machines = load_machines("data/Cloud_Task_Scheduling_Machines.csv")
    tasks = load_tasks("data/Cloud_Task_Scheduling_Tasks.csv")

    print("Se alocă sarcinile pe VM-uri. Vă rugăm așteptați...")
    best_solution = genetic_algorithm(machines, tasks, population_size=100, generations=500, mutation_rate=0.1)

    save_results(machines, tasks, best_solution)

    print("Alocarea a fost realizată cu succes!")


if __name__ == "__main__":
    main()
