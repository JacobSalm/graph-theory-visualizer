# =========================================================
# ALGORITHM 2: BIPARTITE CHECK
# =========================================================

from collections import deque


def get_bipartite_coloring(graph):
    """
    Check whether a graph is bipartite.

    Returns:
        (True, color_map)
            if graph is bipartite

        (False, {})
            if graph is not bipartite

    color_map assigns each vertex either:
        0 or 1
    """

    color = {}

    for vertex in graph:

        # Handle disconnected graphs
        if vertex not in color:

            color[vertex] = 0

            queue = deque([
                vertex
            ])

            while queue:

                current = queue.popleft()

                for neighbor in graph[current]:

                    # Not colored yet
                    if neighbor not in color:

                        color[neighbor] = (
                            1 - color[current]
                        )

                        queue.append(
                            neighbor
                        )

                    # Same color on both sides
                    # means NOT bipartite
                    elif (
                        color[neighbor]
                        ==
                        color[current]
                    ):

                        return False, {}

    return True, color


def is_bipartite(graph):
    """
    Simple True / False version.
    """

    result, _ = (
        get_bipartite_coloring(
            graph
        )
    )

    return result