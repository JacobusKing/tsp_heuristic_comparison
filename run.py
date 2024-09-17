from scipy.spatial import distance_matrix
from import_data import parse_tsplib, parse_tour_file
from solver import solve
from evaluate import calculate_tour_distance

file = 'test'
coords = parse_tsplib(file)
dist_matrix = distance_matrix(coords, coords)

optimal_tour = parse_tour_file(file)
optimal_total_distance = calculate_tour_distance(optimal_tour, dist_matrix)

tour = solve(dist_matrix, 60)
total_distance = calculate_tour_distance(tour, dist_matrix)

print()
print(f"Tour: {tour}")
print(f"Total distance for the tour: {total_distance}")

print()
print(f"Optimal tour: {optimal_tour}")
print(f"Total distance for the optimal tour: {optimal_total_distance}")




