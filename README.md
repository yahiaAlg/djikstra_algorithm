# Dijkstra's Algorithm: A Python Implementation with Logging and Error Handling

This documentation provides a detailed explanation of the Python code that implements Dijkstra's algorithm for finding the shortest paths in a weighted graph. The code is designed with a focus on clarity, robustness, and best practices, incorporating logging and error handling for a smooth developer experience.

## Table of Contents

- [Dijkstra's Algorithm: A Python Implementation with Logging and Error Handling](#dijkstras-algorithm-a-python-implementation-with-logging-and-error-handling)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Code Structure](#code-structure)
    - [1. Logging Setup](#1-logging-setup)
    - [2. Graph Class](#2-graph-class)
      - [2.1. Attributes](#21-attributes)
      - [2.2. Methods](#22-methods)
        - [2.2.1. `__init__`](#221-__init__)
        - [2.2.2. `add_vertex`](#222-add_vertex)
        - [2.2.3. `add_edge`](#223-add_edge)
        - [2.2.4. `get_neighbors`](#224-get_neighbors)
    - [3. `dijkstra` Function](#3-dijkstra-function)
    - [4. Main Driver Code](#4-main-driver-code)
  - [Example Usage](#example-usage)
  - [Logging](#logging)
  - [Error Handling](#error-handling)
  - [Key Features and Best Practices](#key-features-and-best-practices)
  - [Contributing](#contributing)
- [Utility Graph Drawing code](#utility-graph-drawing-code)
- [Graph Visualization with Tkinter](#graph-visualization-with-tkinter)
  - [Features:](#features)
  - [Installation:](#installation)
  - [Usage:](#usage)
  - [Code Explanation:](#code-explanation)
    - [1. `visualize_graph(graph_filepath, distances=None)`:](#1-visualize_graphgraph_filepath-distancesnone)
      - [1.1. Loading the Graph Data](#11-loading-the-graph-data)
      - [1.2. Input Validation](#12-input-validation)
      - [1.3 Tkinter Setup](#13-tkinter-setup)
      - [1.4. Node and Edge Drawing](#14-node-and-edge-drawing)
  - [Logging:](#logging-1)
  - [Conclusion:](#conclusion)

## Introduction

Dijkstra's algorithm is a classic graph search algorithm that finds the shortest paths from a single source vertex to all other vertices in a weighted graph. This implementation uses an adjacency list representation of the graph and incorporates logging and error handling for enhanced functionality and robustness.

## Code Structure

The code is structured into four main parts:

### 1. Logging Setup

```python
import logging

# Configure logging to write to a file
logging.basicConfig(filename='dijkstra.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
```

- This section sets up the logging system using the `logging` module.
- It configures logging to write log messages to a file named `dijkstra.log`.
- The `level=logging.DEBUG` setting ensures that log messages of all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) are recorded.
- The `format` argument defines the structure of each log message, including the timestamp, logging level, and message content.

### 2. Graph Class

```python
class Graph:
    """
    Represents a weighted graph using an adjacency list.

    Attributes:
        vertices (dict): A dictionary where keys are vertices and values are 
                        dictionaries representing neighbors and edge weights.
    """

    # ... (Methods are explained in the following sections)
```

- The `Graph` class provides an object-oriented representation of the graph.
- It encapsulates the data structure and operations related to the graph.

#### 2.1. Attributes

- `vertices (dict)`: A dictionary that stores the vertices and their connections.
   - Keys: Vertices of the graph.
   - Values: Dictionaries representing the neighbors of each vertex.
     - Keys: Neighboring vertices.
     - Values: Weights of the edges connecting the vertex to its neighbors.

#### 2.2. Methods

##### 2.2.1. `__init__`

```python
    def __init__(self):
        """Initializes a new Graph object."""
        self.vertices = {}
        logging.info("Created an empty graph.")
```

- The constructor (`__init__`) initializes a new `Graph` object.
- It creates an empty dictionary `self.vertices` to store the vertices and their connections.
- It logs an informational message indicating that an empty graph has been created.

##### 2.2.2. `add_vertex`

```python
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
```

- `add_vertex(self, vertex)`: Adds a vertex to the graph if it doesn't already exist.
  - It takes the vertex to be added as an argument.
  - If the vertex is not already present, it's added to the `self.vertices` dictionary, and an empty dictionary is assigned as its value (representing no initial neighbors).
  - A debug message is logged to record the addition of the vertex.
  - If the vertex already exists, a warning message is logged, and no action is taken.
  - The method includes error handling (`try-except` block) to catch `TypeError` exceptions, which might occur if the provided vertex is not hashable (cannot be used as a dictionary key). In case of an error, it logs the error message along with the vertex type and re-raises the exception.

##### 2.2.3. `add_edge`

```python
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
```

- `add_edge(self, u, v, weight)`: Adds an edge connecting vertices `u` and `v` with the specified `weight`.
  - It ensures that both vertices `u` and `v` exist in the graph by calling `self.add_vertex()` for each.
  - It then adds the edge by updating the adjacency list (`self.vertices`) for both vertices, reflecting the undirected nature of the graph.
  - A debug message is logged to record the addition of the edge.
  - Similar to `add_vertex`, it incorporates error handling to catch `TypeError` exceptions, logging the error and re-raising the exception if an invalid vertex type is encountered.

##### 2.2.4. `get_neighbors`

```python
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
```

- `get_neighbors(self, vertex)`: Retrieves the neighbors of a given `vertex`.
  - It uses the `get()` method on the `self.vertices` dictionary to safely access the neighbors of the vertex. 
  - If the vertex doesn't exist, it returns an empty dictionary to avoid raising a `KeyError`.
  - The method logs a debug message indicating the neighbors retrieved for the given vertex.

### 3. `dijkstra` Function

```python
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

    distances = {vertex: float('inf') for vertex in graph.vertices}
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
            if new_distance &lt; distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex
                logging.debug(f"Updated distance to {neighbor} via {current_vertex} to {new_distance}")

    logging.info("Dijkstra's algorithm completed.")
    return distances, predecessors
```

- `dijkstra(graph, source)`: Implements Dijkstra's algorithm to calculate shortest paths.
  - It takes a `Graph` object and a `source` vertex as input.
  - **Error Handling**:
    - It first checks if the provided `graph` is indeed a `Graph` object using `isinstance`. If not, it raises a `TypeError` with a descriptive error message.
    - It also ensures that the `source` vertex exists in the graph. If not, a `ValueError` is raised.
  - **Initialization**:
    - Two dictionaries, `distances` and `predecessors`, are initialized:
      - `distances`: Stores the shortest distance from the source to each vertex, initially set to infinity for all vertices except the source (set to 0).
      - `predecessors`: Stores the predecessor vertex in the shortest path from the source to each vertex. Initially, all predecessors are set to `None`.
    - A list `unvisited` is created, initially containing all vertices of the graph.
  - **Dijkstra's Algorithm Loop**:
    - The algorithm iterates as long as there are unvisited vertices.
    - In each iteration:
      - It selects the `current_vertex` with the minimum distance from the source among the `unvisited` vertices.
      - The `current_vertex` is removed from the `unvisited` list.
      - For each `neighbor` of the `current_vertex`, it calculates the `new_distance` from the source to the `neighbor` through the `current_vertex`.
      - If the `new_distance` is shorter than the current `distances[neighbor]`, it updates `distances[neighbor]` and sets the `predecessor` of the `neighbor` to the `current_vertex`.
 - **Return Values**:
   - After processing all vertices, the function returns two dictionaries: 
      - `distances`: containing the shortest distances from the source to all other vertices in the graph.
      - `predecessors`: storing the predecessor node that leads to the shortest path from the source node to each vertex.

### 4. Main Driver Code

```python
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
```

- The code within the `if __name__ == "__main__":` block is executed only when the script is run directly (not when imported as a module).
- It demonstrates an example usage of the `Graph` class and the `dijkstra` function.
- A `Graph` object is created, and edges with their corresponding weights are added to the graph, defining its structure.
- The `dijkstra` function is then called with the graph and the source vertex (`"A"` in this case).
- Finally, the calculated shortest `distances` from the source vertex 'A' to all other vertices and the `predecessors` are printed to the console.

## Example Usage

The "Main Driver Code" section demonstrates a basic use case. You can modify the graph structure and the source vertex to experiment with different scenarios.

## Logging

The code extensively uses the `logging` module to record messages about the program's execution. These messages are categorized into different levels:

- **DEBUG**: Detailed information, typically useful for debugging purposes (e.g., logging each step of the algorithm).
- **INFO**:  Confirms that things are working as expected (e.g., indicating the start and completion of Dijkstra's algorithm).
- **WARNING**: Indicates potential issues that don't necessarily halt execution (e.g., attempting to add a duplicate vertex).
- **ERROR**: Records errors that may cause the program to malfunction (e.g., invalid input types).

The log messages are written to the `dijkstra.log` file, providing valuable insights into the code's behavior, especially during debugging or when analyzing the algorithm's execution path.

## Error Handling

The code implements robust error handling using `try-except` blocks to catch potential exceptions and prevent abrupt program termination. The primary exception handled is the `TypeError`, which is raised if an invalid vertex type is used.

- **Catching `TypeError`**: This ensures that the graph structure is maintained with valid vertex types, and any attempt to use an unsupported type is caught and logged.
- **Re-raising Exceptions**: In the current implementation, after logging the error, the exceptions are re-raised to halt the program's execution. This is a common practice in scenarios where the program cannot recover from the error, and continuing execution might lead to unexpected behavior. 
- **Other Error Handling**: The `dijkstra` function also includes checks to ensure that the input `graph` is a `Graph` object and that the `source` vertex exists in the graph, raising `TypeError` and `ValueError`, respectively, if these conditions are not met. 

## Key Features and Best Practices

- **Object-Oriented Approach**: The use of the `Graph` class promotes code organization and encapsulation of graph-related operations.
- **Clear Documentation**: Detailed docstrings enhance code readability and understanding.
- **Descriptive Naming**:  Meaningful variable and method names improve code clarity.
- **Logging for Debugging**:  Logging provides a detailed record of the program's execution flow and helps in identifying and resolving issues.
- **Error Handling**: Implementing error handling makes the code more robust and reliable by gracefully handling potential errors.
- **Type Hinting**: The use of type hinting further improves code readability and allows for better static analysis.

## Contributing

Contributions to this code are welcome. Please feel free to fork the repository and submit pull requests for any improvements or bug fixes.

# Utility Graph Drawing code
# Graph Visualization with Tkinter

This Python script provides a visual representation of a graph, leveraging the Tkinter library for the graphical user interface. 

## Features:

- **Visualizes Graphs:** Renders graph data stored in a JSON file.
- **Adjacency List Format:**  Supports graphs represented using the adjacency list format.
- **Node Highlighting:** Optionally highlights nodes based on provided distances from a source vertex.
- **Error Handling:** Includes robust error handling to gracefully manage invalid input or file errors.
- **Detailed Logging:**  Logs key events and potential issues to a file for debugging and monitoring.

## Installation:

1. **Python and Tkinter:** Ensure you have Python installed on your system. Tkinter is usually included in standard Python distributions.
2. **Required Packages:**  No external packages beyond the Python standard library are required.

## Usage:

1. **Prepare Your Graph Data:**
   - Create a JSON file representing your graph as an adjacency list. For example:

     ```json
     {
       "A": {"B": 4, "C": 2},
       "B": {"C": 1, "D": 5},
       "C": {"D": 8, "E": 10},
       "D": {"E": 2, "F": 6},
       "E": {"F": 3},
       "F": {}
     }
     ```

     - In this format, each key in the JSON object represents a vertex in the graph.
     - The corresponding value is another dictionary representing its adjacent vertices and edge weights.
2. **Run the Script:**
   - Replace `"graph.json"` in the `if __name__ == "__main__":` block with the actual path to your JSON graph file.
   - Run the script using `python graph_visualization.py` (or your preferred method of executing Python scripts).
   - A Tkinter window will appear, displaying the visualized graph.

## Code Explanation:

The code is organized into functions for clarity and reusability:

### 1. `visualize_graph(graph_filepath, distances=None)`:

This function is responsible for loading graph data, creating the visualization, and handling errors.

```python
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
    
    # ... (Code implementation - see the next sections for explanations)
```

- **Arguments**:
   - `graph_filepath (str)`: The path to the JSON file containing the graph data.
   - `distances (dict, optional)`:  An optional dictionary where keys are vertices, and values are their distances from a source vertex (used for node highlighting).
- **Error Handling**: 
  - Uses `try...except` blocks to handle potential errors during file loading (`FileNotFoundError`, `json.JSONDecodeError`), data type validation (`TypeError`), and unexpected errors during visualization (`Exception`). 
  - Logs error messages using the `logging` module to provide debugging information.

#### 1.1. Loading the Graph Data

```python
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
```

- This section attempts to load the graph data from the specified JSON file.
- It uses a `with open(...)` block to ensure the file is properly closed, even if errors occur.
- The `json.load(file)` function parses the JSON data into a Python dictionary.
- Error handling is in place to catch `FileNotFoundError` and `json.JSONDecodeError`. If caught, the errors are logged, and the exceptions are re-raised.

#### 1.2. Input Validation

```python
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
```

- Before proceeding, the code validates the input data:
  - **Graph Type Check:** It verifies if the loaded `graph` is a dictionary-like object (which is expected for an adjacency list representation).
  - **Distances Type and Consistency Check:** If `distances` are provided:
    - It checks if it's a dictionary.
    - It verifies that every vertex in the `distances` dictionary also exists in the loaded `graph`. 

#### 1.3 Tkinter Setup

```python
    window = tk.Tk()
    window.title("Graph Visualization")

    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()
```

- **Window Creation**: A main window (`window`) is created using `tk.Tk()`, and its title is set.
- **Canvas Setup**: A `tk.Canvas` widget is created. The canvas serves as the drawing area for the graph visualization. It is initialized with a specified width, height, and a white background color. 

#### 1.4. Node and Edge Drawing

```python
    node_radius = 20
    node_positions = {}  # Store node positions to draw edges

    # ... (Helper functions draw_node and get_node_color)

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
```

- **Node Positioning:**
  - The code calculates node positions to arrange them in a circular layout on the canvas.
  - It uses trigonometry (`math.cos` and `math.sin`) to determine the `(x, y)` coordinates of each node on the circle's circumference.
- **Node and Edge Drawing**:
  - It iterates through the vertices and edges of the graph.
  - The `draw_node` helper function (explained below) is called to draw each node on the canvas at its calculated position.
  - Edges are drawn as lines between nodes using `canvas.create_line`.
  - Edge weights are displayed as text labels near the midpoint of each edge using `canvas.create_text`.
- **Node Highlighting (Optional):**
  - If the `distances` dictionary is provided, nodes are highlighted based on their distances.
  - The `get_node_color` helper function (explained below) calculates a color along a gradient (from green to red) based on the normalized distance of each node.

**Helper Functions:**

- **`draw_node(vertex, x, y)`:**  Draws a single node (represented as a circle) with its label on the canvas. It uses `canvas.create_oval` to draw the circle and `canvas.create_text` to place the vertex label at its center. 

- **`get_node_color(distance, max_distance)`:** Calculates a color along a green-to-red gradient based on the provided `distance` and the `max_distance`. This is used to visually represent the relative distances of nodes from a source vertex (if distance information is provided). 

## Logging:

This script utilizes the `logging` module to record informative messages during its execution. This is beneficial for:

- **Debugging:** Quickly identifying and resolving any errors or issues.
- **Monitoring:** Understanding the script's execution flow and behavior.

You can customize the logging level and format in the `logging.basicConfig()` call.

## Conclusion:

This documentation provides a comprehensive overview of the provided Python script for graph visualization. With its support for loading graph data from JSON files, optional node highlighting based on distances, error handling, and informative logging, this script is a useful tool for visually exploring and presenting graph structures. Remember to customize the code and experiment with your own graph data for various use cases. 
