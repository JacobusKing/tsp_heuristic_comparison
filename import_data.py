import numpy as np

def parse_tsplib(file):
    with open(f"instances/{file}.tsp", 'r') as f:
        lines = f.readlines()

    node_coord_section = False
    dimension = 0
    coords = []

    for line in lines:
        line = line.strip()
        
        if line.startswith('DIMENSION'):
            dimension = int(line.split()[-1])

        elif line.startswith('NODE_COORD_SECTION'):
            node_coord_section = True

        elif node_coord_section:
            if line == 'EOF':
                break
            _, x, y = line.split()
            coords.append((float(x), float(y)))

        

    return np.array(coords)

def parse_tour_file(file):
    """
    Parse the tour from a TSPLIB .tour or .opt.tour file.

    Parameters:
    - file_path: Path to the .tour file.

    Returns:
    - tour: List of city indices in the order they are visited (1-based indexing).
    """
    tour = []
    in_tour_section = False

    with open(f"instances/{file}.opt.tour", 'r') as f:
        for line in f:
            line = line.strip()

            # Start reading tour section
            if line == "TOUR_SECTION":
                in_tour_section = True
                continue

            # End of tour section
            if line == "-1" or line == "EOF":
                break

            # Add city index to the tour
            if in_tour_section:
                city = int(line)
                tour.append(city)

    return tour
