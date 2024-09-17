import numpy as np

def calculate_tour_distance(tour, dist_matrix):
    """
    Calculate the total distance for a given tour using the provided distance matrix.

    Parameters:
    - tour: List of city indices representing the tour (1-based index from the .opt.tour file).
    - dist_matrix: 2D NumPy array representing the distance between cities (0-based index).

    Returns:
    - total_distance: The total distance traveled in the tour.
    """
    n = len(tour)
    total_distance = 0

    # Convert 1-based index from the .opt.tour file to 0-based index for the distance matrix
    tour = [city - 1 for city in tour]

    # Calculate the total distance by summing up the distances between consecutive cities
    for i in range(n - 1):
        total_distance += dist_matrix[tour[i], tour[i + 1]]

    # Add the distance to return to the starting city to complete the cycle
    total_distance += dist_matrix[tour[-1], tour[0]]

    return total_distance
