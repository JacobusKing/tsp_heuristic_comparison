import pulp
import numpy as np

def example_solver(dist_matrix, time_limit):
    # Number of cities
    n = len(dist_matrix)
    
    # Create the model
    tsp_model = pulp.LpProblem("TSP", pulp.LpMinimize)

    # Decision variables: x[i][j] = 1 if we travel from city i to city j, otherwise 0
    x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(n)] for i in range(n)]

    # Auxiliary variables for subtour elimination (MTZ constraints)
    u = [pulp.LpVariable(f"u_{i}", lowBound=0, upBound=n-1, cat="Continuous") for i in range(n)]

    # Objective function: Minimize the total travel distance
    tsp_model += pulp.lpSum(dist_matrix[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j)

    # Constraints: Every city is entered exactly once
    for j in range(n):
        tsp_model += pulp.lpSum(x[i][j] for i in range(n) if i != j) == 1

    # Constraints: Every city is exited exactly once
    for i in range(n):
        tsp_model += pulp.lpSum(x[i][j] for j in range(n) if i != j) == 1

    # Subtour elimination constraints (MTZ formulation)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                tsp_model += u[i] - u[j] + (n * x[i][j]) <= n - 1

    # Solve the problem
    tsp_model.solve(pulp.PULP_CBC_CMD(timeLimit=time_limit))

    # Extract the solution
    x_vars = []
    if pulp.LpStatus[tsp_model.status] == 'Optimal':
        print(f"Optimal tour cost: {pulp.value(tsp_model.objective)}")
        for i in range(n):
            for j in range(n):
                if pulp.value(x[i][j]) == 1:
                    x_vars.append((i,j))
    else:
        print("No optimal solution found.")

    # Convert the decision variables into a list representing the order in which cities are visited
    tour = [0]
    current_city = 0
    while len(x_vars) > 0:
        for i in range(n):
            if (current_city, i) in x_vars:
                x_vars.remove((current_city, i))
                current_city = i
                tour.append(current_city)
                break

    return tour