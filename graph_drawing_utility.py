import tkinter as tk
import logging
import math
import json

# Configure logging
logging.basicConfig(
    filename="graph_visualization.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def visualize_graph(graph_filepath, distances=None):
    """
    Visualizes a graph from a JSON file using Tkinter Canvas.

    Args:
        graph_filepath (str): The path to the JSON file containing the graph data.
                              The JSON should represent the graph as an adjacency list.
        distances (dict, optional): A dictionary mapping vertices to their
                                    shortest distances from a source vertex.
                                    If provided, node colors will reflect distances.

    Raises:
        FileNotFoundError: If the specified graph file is not found.
        json.JSONDecodeError: If the JSON file is not valid JSON or does not have the correct format.
        TypeError: If `distances` is provided and is not a dictionary.
        ValueError: If any vertex in `distances` is not found in the graph.
        Exception: For any other unexpected errors during visualization.
    """

    logging.info("Starting graph visualization.")

    try:
        # Load graph data from JSON file
        with open(graph_filepath, "r") as file:
            graph = json.load(file)
    except FileNotFoundError:
        logging.error(f"Graph file not found: {graph_filepath}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {graph_filepath}")
        raise

    # Error Handling: Input Validation
    if not isinstance(graph, dict):
        logging.error("Invalid graph type provided. Must be a dictionary-like object.")
        raise TypeError("Graph must be a dictionary-like object.")
    if distances is not None:
        if not isinstance(distances, dict):
            logging.error("Distances must be provided as a dictionary.")
            raise TypeError("Distances must be a dictionary.")
        for vertex in distances:
            if vertex not in graph:
                logging.error(f"Vertex {vertex} in 'distances' not found in the graph.")
                raise ValueError(
                    f"Vertex {vertex} in 'distances' not found in the graph."
                )

    window = tk.Tk()
    window.title("Graph Visualization")

    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    node_radius = 20
    node_positions = {}  # Store node positions to draw edges

    # --- Helper Functions ---
    def draw_node(vertex, x, y):
        """Draws a single node (circle) with its label on the canvas."""
        try:
            node_id = canvas.create_oval(
                x - node_radius,
                y - node_radius,
                x + node_radius,
                y + node_radius,
                fill="lightblue",
            )
            canvas.create_text(x, y, text=vertex, font=("Arial", 12))
            node_positions[vertex] = (x, y, node_id)  # Store node ID
            logging.debug(f"Drew node: {vertex} at ({x}, {y})")
        except Exception as e:
            logging.error(f"Error drawing node {vertex}: {e}")

    def get_node_color(distance, max_distance):
        """Calculates a color along a green-to-red gradient based on distance."""
        try:
            # Normalized distance for color calculation
            normalized_distance = distance / max_distance if max_distance else 0
            red = int(255 * normalized_distance)
            green = int(255 * (1 - normalized_distance))
            color = f"#{red:02x}{green:02x}00"  # Hex color string
            return color
        except Exception as e:
            logging.error(f"Error calculating node color: {e}")
            return "lightblue"  # Default color on error

    # --- Node and Edge Drawing Logic ---
    try:
        num_vertices = len(graph)
        angle_increment = 2 * math.pi / num_vertices

        # Calculate node positions before drawing
        for i, vertex in enumerate(graph):
            angle = i * angle_increment
            x = canvas_width / 2 + 200 * math.cos(angle)
            y = canvas_height / 2 + 200 * math.sin(angle)
            node_positions[vertex] = (x, y)  # Store position only

        # Draw nodes and edges
        for u in graph:
            draw_node(u, node_positions[u][0], node_positions[u][1])
            for v, weight in graph[u].items():
                if v in node_positions:
                    x1, y1 = node_positions[u][:2]  # Unpack only x, y
                    x2, y2 = node_positions[v][:2]  # Unpack only x, y
                    canvas.create_line(x1, y1, x2, y2)
                    canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(weight),
                        font=("Arial", 10),
                    )
                    logging.debug(f"Drew edge: ({u}, {v}), Weight: {weight}")

        # Highlight nodes based on distances (if provided)
        if distances:
            max_distance = max(distances.values())
            for vertex, dist in distances.items():
                if vertex in node_positions:  # Ensure the node is in the graph
                    x, y, node_id = node_positions[vertex]
                    color = get_node_color(dist, max_distance)
                    canvas.itemconfig(node_id, fill=color)

    except Exception as e:
        logging.error(f"An error occurred during visualization: {e}")

    window.mainloop()


# Example usage:
if __name__ == "__main__":
    graph_file = "graph.json"  # Replace with your graph file
    visualize_graph(graph_file)
