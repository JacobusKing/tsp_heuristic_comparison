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

    # Calculate the total distance by summing up the distances between consecutive cities
    for i in range(n - 1):
        total_distance += dist_matrix[tour[i], tour[i + 1]]

    # Add the distance to return to the starting city to complete the cycle
    total_distance += dist_matrix[tour[-1], tour[0]]

    return total_distance

import matplotlib.pyplot as plt

def plot_tour(coordinates, tour, filename, heading):
    """
    Plots the given coordinates and connects them based on the tour.

    Parameters:
    - coordinates: A 2D array of shape (n, 2) where n is the number of points.
    - tour: A list of indices representing the order in which to connect the points.
    """
    # Convert the coordinates to a NumPy array for easier indexing
    coords = np.array(coordinates)

    # Extract x and y coordinates
    x = coords[:, 0]
    y = coords[:, 1]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', label='Coordinates')

    # Plot the tour
    for i in range(len(tour) - 1):
        start = tour[i]
        end = tour[i + 1]
        plt.plot([x[start], x[end]], [y[start], y[end]], color='orange')

    # Add labels and title
    plt.title(heading)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid()
    plt.legend()

    # Save the plot
    plt.savefig(f'output/{filename}', format='pdf')

    return
