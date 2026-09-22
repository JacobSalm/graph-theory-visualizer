# =========================================================
# ALGORITHM 2: BIPARTITE CHECK
# =========================================================

from collections import deque


def get_bipartite_coloring(graph):
    """
    Check whether a graph is bipartite.

    Returns:

        (True, color_map)

    if bipartite.

    Returns:

        (False, {})

    otherwise.
    """

    color = {}

    for vertex in graph:

        if vertex in color:

            continue

        color[vertex] = 0

        queue = deque([
            vertex
        ])

        while queue:

            current = (
                queue.popleft()
            )

            for neighbor in graph[
                current
            ]:

                if neighbor not in color:

                    color[neighbor] = (
                        1
                        -
                        color[current]
                    )

                    queue.append(
                        neighbor
                    )

                elif (
                    color[neighbor]
                    ==
                    color[current]
                ):

                    return (
                        False,
                        {}
                    )

    return (
        True,
        color
    )


def is_bipartite(graph):

    result, _ = (
        get_bipartite_coloring(
            graph
        )
    )

    return result