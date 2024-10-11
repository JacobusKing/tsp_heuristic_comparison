import pulp
import numpy as np
from evaluate import calculate_tour_distance
import time
import math
import random
import matplotlib.pyplot as plt

def exact_solver(dist_matrix, time_limit):
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


def plot_improvement(data):
    # Separate keys and values for plotting
    x = list(data.keys())
    y = list(data.values())

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')  # Line plot with markers
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Improvement of best solution found')
    plt.grid(True)
    plt.savefig("output/improvement.png")
    plt.show()
    return

def jk_solver(dist_matrix, time_limit, nit):
    start_time = time.time() # Start the "timer"
    n = len(dist_matrix) # Get the number of cities in the instance

    current_route = [i for i in range(n)]
    random.shuffle(current_route) # Generate a random solution
    current_obj = calculate_tour_distance(current_route, dist_matrix)
    print(f"Initial random solution: {current_obj}")
    
    best_obj = current_obj # Start out with a best objective function value
    best_route = current_route[:] # Variable where we will store the solution corresponding to the best objective function value

    iteration = 1
    iterations_since_improvement = 0
    plot = {}
    while time.time() - start_time < time_limit: # Make sure that we stick to our time limit
        plot[iteration] = best_obj

        i = random.choice(range(1, n - 2))
        k = random.choice(range(i + 1, n))

        test_route = two_opt(current_route, i, k)
        test_obj = calculate_tour_distance(test_route, dist_matrix) # Get the objective function value of the randomly generated solution
        if test_obj < current_obj: # Check whether the new random solution is better than the incumbent solution
            current_route = test_route
            current_obj = test_obj
            if current_obj < best_obj:
                iterations_since_improvement = 0
                best_route = current_route
                best_obj = current_obj
                print(f"New best feasible solution at iteration {iteration} ({round(time.time() - start_time, 0)}s): {best_obj}")
        elif random.random() < nit:
            current_route = test_route
            current_obj = test_obj
            print("Accepting non-improving move.")

        iteration += 1
        iterations_since_improvement += 1

    plot_improvement(plot)
    return best_route

def two_opt(route, i, k):
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route

def full_two_opt(route, distance_matrix, time_limit):
    """Solve TSP using 2-opt moves.

    Args:
        cities (list): List of city names or identifiers.
        distance_matrix (np.array): Matrix where distance_matrix[i][j] represents the distance between city i and city j.
        max_iterations (int): Maximum number of iterations for optimization.

    Returns:
        tuple: (optimal route, minimum distance)
    """
    start_time = time.time() # Start the "timer"

    # Initial route (ordered list of cities)
    n = len(distance_matrix)
    # route = list(range(n))
    min_distance = calculate_tour_distance(route, distance_matrix)
    iteration = 0
    print(f"New best feasible solution at iteration {iteration}: {min_distance}")
    
    while time.time() - start_time < time_limit: # Make sure that we stick to our time limit
        improved = False
        iteration += 1
        
        # Loop through all pairs (i, k) where i < k
        for i in range(1, n - 2):
            for k in range(i + 1, n):
                # Apply 2-opt by reversing route between i and k
                new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
                new_distance = calculate_tour_distance(new_route, distance_matrix)
                
                # Check if this new route is better
                if new_distance < min_distance:
                    route = new_route
                    min_distance = new_distance
                    improved = True
                    print(f"New best feasible solution at iteration {iteration} ({round(time.time() - start_time, 0)}s): {min_distance}")
                    break

                if time.time() - start_time > time_limit:
                    break
            if time.time() - start_time > time_limit:
                    break
            if improved:
                break
        
        # Stop if no improvement was found in the last iteration
        if not improved:
            print("No improvement!")
            break
    
    return route