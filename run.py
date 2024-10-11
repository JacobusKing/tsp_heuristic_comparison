from scipy.spatial import distance_matrix
from import_data import parse_tsplib, parse_tour_file
from solver import exact_solver, jk_solver, full_two_opt
from evaluate import calculate_tour_distance, plot_tour

name = "Jacobus_King"
time_limit = 60 # Specify the time limit in seconds that will be provided to the solver
file = 'tsp225' # Specify the file name containing the instance to be run

# Import instance
coords = parse_tsplib(file) # Obtain the coordinates of cities in the instance
dist_matrix = distance_matrix(coords, coords) # Generate the distance matrix

# Call your solver here to take the distance matrix and time limit in seconds as input and provide a tour with 0-based indexing as output
tour = jk_solver(dist_matrix, time_limit, nit = 0.00001)
# print('Starting full 2-opt.')
# tour = full_two_opt(tour, dist_matrix, time_limit*0.1)

# Evaluate your solution
total_distance = calculate_tour_distance(tour, dist_matrix) # Evaluate your solution

# Import an optimal solution
optimal_tour = parse_tour_file(file)
optimal_tour = [city - 1 for city in optimal_tour] + [0] # Convert 1-based index from the .opt.tour file to 0-based index for the distance matrix
optimal_total_distance = calculate_tour_distance(optimal_tour, dist_matrix)

# Plot both solutions
plot_tour(coords, tour, filename = f'{name}_{file}_{time_limit}.pdf', heading = f"Tour of {name}: {round(total_distance, 2)}")
plot_tour(coords, optimal_tour, filename = f'Optimal_{file}_{time_limit}.pdf', heading = f"Optimal tour: {round(optimal_total_distance, 2)}")

print()
print(f"Tour: {tour}")
print(f"Total distance for the tour: {total_distance}")

print()
print(f"Optimal tour: {optimal_tour}")
print(f"Total distance for the optimal tour: {optimal_total_distance}")

print(f"You are {round((total_distance - optimal_total_distance)/optimal_total_distance*100, 2)}% away from optimality.")