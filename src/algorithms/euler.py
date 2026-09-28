# =========================================================
# ALGORITHM 3: EULER PROPERTY
# =========================================================


# =========================================================
# DEGREE
# =========================================================

def get_degree(
    graph,
    vertex_id
):
    """
    Return the degree of one vertex.

    Every parallel edge counts separately.
    """

    degree = 0

    for edge_id in (
        graph.get_edge_ids()
    ):

        edge = graph.get_edge(
            edge_id
        )

        if edge is None:
            continue

        if (
            edge["u"] == vertex_id
            or
            edge["v"] == vertex_id
        ):

            degree += 1

    return degree


# =========================================================
# CONNECTED
# =========================================================

def is_connected(graph):
    """
    Return True if every vertex belongs
    to one connected component.
    """

    vertex_ids = (
        graph.get_vertex_ids()
    )

    # Empty graph or a graph containing
    # one vertex is treated as connected.
    if len(vertex_ids) <= 1:

        return True


    # ---------------------------------
    # DFS
    # ---------------------------------

    start = vertex_ids[0]

    visited = set()

    stack = [
        start
    ]


    while stack:

        current = (
            stack.pop()
        )

        if current in visited:
            continue

        visited.add(
            current
        )


        # Check every edge attached
        # to current vertex.

        for edge_id in (
            graph.get_edge_ids()
        ):

            edge = graph.get_edge(
                edge_id
            )

            if edge is None:
                continue

            neighbor = None


            if (
                edge["u"]
                ==
                current
            ):

                neighbor = (
                    edge["v"]
                )


            elif (
                edge["v"]
                ==
                current
            ):

                neighbor = (
                    edge["u"]
                )


            if (
                neighbor is not None
                and
                neighbor not in visited
            ):

                stack.append(
                    neighbor
                )


    return (
        len(visited)
        ==
        len(vertex_ids)
    )


# =========================================================
# EULER PROPERTY
# =========================================================

def is_eulerian(graph):
    """
    A graph is Eulerian when:

    1. The graph is connected.
    2. Every vertex has even degree.
    """

    if not is_connected(
        graph
    ):

        return False


    for vertex_id in (
        graph.get_vertex_ids()
    ):

        degree = get_degree(
            graph,
            vertex_id
        )

        if (
            degree % 2
            !=
            0
        ):

            return False


    return True


# =========================================================
# FIND EULER CYCLE
# =========================================================

def find_euler_cycle(graph):
    """
    Find an actual Euler cycle using
    Hierholzer's algorithm.

    Returns:

    {
        "vertices": [vertex IDs...],
        "edges": [edge IDs...]
    }

    or None if the graph is not Eulerian.
    """

    if not is_eulerian(
        graph
    ):

        return None


    vertex_ids = (
        graph.get_vertex_ids()
    )

    edge_ids = (
        graph.get_edge_ids()
    )


    # ---------------------------------
    # Empty graph
    # ---------------------------------

    if not vertex_ids:

        return {
            "vertices": [],
            "edges": []
        }


    # ---------------------------------
    # Graph with no edges
    # ---------------------------------

    if not edge_ids:

        return {
            "vertices": [
                vertex_ids[0]
            ],
            "edges": []
        }


    # =====================================================
    # BUILD EDGE-ID ADJACENCY
    # =====================================================

    adjacency = {

        vertex_id: []

        for vertex_id
        in vertex_ids
    }


    for edge_id in edge_ids:

        edge = graph.get_edge(
            edge_id
        )

        u = edge["u"]

        v = edge["v"]

        adjacency[u].append(
            edge_id
        )

        adjacency[v].append(
            edge_id
        )


    # =====================================================
    # CHOOSE START
    # =====================================================

    start = None

    for vertex_id in vertex_ids:

        if (
            get_degree(
                graph,
                vertex_id
            )
            > 0
        ):

            start = vertex_id

            break


    if start is None:

        start = vertex_ids[0]


    # =====================================================
    # HIERHOLZER'S ALGORITHM
    # =====================================================

    used_edges = set()

    vertex_stack = [
        start
    ]

    # edge_stack[i] is the edge that
    # entered the corresponding vertex.
    edge_stack = []


    reversed_vertices = []

    reversed_edges = []


    while vertex_stack:

        current = (
            vertex_stack[-1]
        )


        # ---------------------------------
        # Remove already-used candidates
        # ---------------------------------

        while (
            adjacency[current]
            and
            adjacency[current][-1]
            in used_edges
        ):

            adjacency[current].pop()


        # ---------------------------------
        # Unused edge exists
        # ---------------------------------

        if adjacency[current]:

            edge_id = (
                adjacency[current].pop()
            )

            if edge_id in used_edges:
                continue

            used_edges.add(
                edge_id
            )


            next_vertex = (
                graph.get_other_endpoint(
                    edge_id,
                    current
                )
            )


            if next_vertex is None:

                return None


            vertex_stack.append(
                next_vertex
            )

            edge_stack.append(
                edge_id
            )


        # ---------------------------------
        # Dead end
        # Add to final circuit backwards
        # ---------------------------------

        else:

            vertex = (
                vertex_stack.pop()
            )

            reversed_vertices.append(
                vertex
            )


            if edge_stack:

                edge_id = (
                    edge_stack.pop()
                )

                reversed_edges.append(
                    edge_id
                )


    # =====================================================
    # REVERSE INTO TRAVERSAL ORDER
    # =====================================================

    cycle_vertices = list(
        reversed(
            reversed_vertices
        )
    )

    cycle_edges = list(
        reversed(
            reversed_edges
        )
    )


    # =====================================================
    # SAFETY CHECKS
    # =====================================================

    # Every edge must have been used.
    if (
        len(cycle_edges)
        !=
        len(edge_ids)
    ):

        return None


    # If edges exist, cycle must end
    # where it started.
    if (
        cycle_edges
        and
        cycle_vertices[0]
        !=
        cycle_vertices[-1]
    ):

        return None


    return {

        "vertices": cycle_vertices,

        "edges": cycle_edges
    }