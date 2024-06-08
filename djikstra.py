import logging
import json

# Configure logging to write to a file
logging.basicConfig(
    filename="dijkstra.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Graph:
    """
    Represents a weighted graph using an adjacency list.

    Attributes:
        vertices (dict): A dictionary where keys are vertices and values are
                        dictionaries representing neighbors and edge weights.
    """

    def __init__(self):
        """Initializes a new Graph object."""
        self.vertices = {}
        logging.info("Created an empty graph.")

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.

        Args:
            vertex: The vertex to be added.

        Raises:
            TypeError: If the vertex is not hashable (cannot be used as a key).
        """
        try:
            if vertex not in self.vertices:
                self.vertices[vertex] = {}
                logging.debug(f"Added vertex: {vertex}")
            else:
                logging.warning(f"Vertex {vertex} already exists. Skipping.")
        except TypeError as e:
            logging.error(f"Invalid vertex type: {type(vertex)}. Error: {e}")
            raise

    def add_edge(self, u, v, weight):
        """
        Adds an edge to the graph with the given weight.

        Args:
            u: The starting vertex of the edge.
            v: The ending vertex of the edge.
            weight: The weight of the edge.

        Raises:
            TypeError: If any of the vertices are not hashable.
        """
        try:
            self.add_vertex(u)  # Ensure both vertices exist
            self.add_vertex(v)
            self.vertices[u][v] = weight
            self.vertices[v][u] = weight  # For undirected graph
            logging.debug(f"Added edge: ({u}, {v}, weight={weight})")
        except TypeError as e:
            logging.error(f"Invalid vertex type. Error: {e}")
            raise

    def get_neighbors(self, vertex):
        """
        Returns the neighbors of a vertex and their edge weights.

        Args:
            vertex: The vertex to get neighbors for.

        Returns:
            dict: A dictionary where keys are neighboring vertices and values are edge weights.
                  Returns an empty dictionary if the vertex does not exist.
        """
        neighbors = self.vertices.get(vertex, {})  # Safe access using get()
        logging.debug(f"Retrieved neighbors for vertex {vertex}: {neighbors}")
        return neighbors


def dijkstra(graph, source):
    """
    Implements Dijkstra's algorithm to find the shortest paths from a source vertex.

    Args:
        graph (Graph): The graph to search.
        source: The source vertex.

    Returns:
        tuple: A tuple containing two dictionaries:
               - distances: shortest distances from the source to all vertices.
               - predecessors: a dictionary mapping each vertex to its predecessor in the shortest path.

    Raises:
        ValueError: If the source vertex is not in the graph.
        TypeError: If the graph is not an instance of the Graph class.
    """
    if not isinstance(graph, Graph):
        logging.error("Invalid graph type provided to Dijkstra's algorithm.")
        raise TypeError("graph must be an instance of the Graph class")

    if source not in graph.vertices:
        logging.error(f"Source vertex {source} not found in the graph.")
        raise ValueError(f"Source vertex {source} not in graph")

    distances = {vertex: float("inf") for vertex in graph.vertices}
    predecessors = {vertex: None for vertex in graph.vertices}
    distances[source] = 0
    unvisited = list(graph.vertices)

    logging.info(f"Starting Dijkstra's algorithm from source vertex: {source}")

    while unvisited:
        # Find vertex with min distance in unvisited
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
        unvisited.remove(current_vertex)

        logging.debug(f"Visiting current vertex: {current_vertex}")

        for neighbor, weight in graph.get_neighbors(current_vertex).items():
            new_distance = distances[current_vertex] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex
                logging.debug(
                    f"Updated distance to {neighbor} via {current_vertex} to {new_distance}"
                )

    logging.info("Dijkstra's algorithm completed.")
    return distances, predecessors


if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)
    g.add_edge("D", "F", 6)
    g.add_edge("E", "F", 3)

    distances, predecessors = dijkstra(g, "A")

    print("Distances from source 'A':", distances)
    print("Predecessors:", predecessors)

    # --- Save Graph to JSON ---
    graph_data = g.vertices  # Get the graph data (adjacency list)
    try:
        with open("graph.json", "w") as file:
            json.dump(graph_data, file, indent=4)
        logging.info("Graph data saved to graph.json")
    except Exception as e:
        logging.error(f"An error occurred while saving the graph: {e}")
