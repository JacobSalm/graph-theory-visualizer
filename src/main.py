import math
import pygame

from algorithm1 import (
    is_path,
    is_cycle,
    find_shortest_closed_subwalk,
    remove_closed_subwalk,
)

from bipartite import get_bipartite_coloring


# =========================================================
# SETUP
# =========================================================

pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Graph Theory Visualizer"
)

clock = pygame.time.Clock()

vertex_font = pygame.font.SysFont(
    None,
    30
)

ui_font = pygame.font.SysFont(
    None,
    26
)

menu_font = pygame.font.SysFont(
    None,
    25
)


# =========================================================
# COLORS
# =========================================================

BACKGROUND = (30, 30, 30)

GRID_COLOR = (50, 50, 50)

VERTEX_COLOR = (230, 230, 230)

TEXT_COLOR = (20, 20, 20)

WHITE = (240, 240, 240)

BORDER_COLOR = (255, 255, 255)

EDGE_COLOR = (180, 180, 180)

SELECTED_COLOR = (255, 220, 0)

HOVER_COLOR = (255, 110, 110)

MENU_BACKGROUND = (45, 45, 45)

MENU_HOVER = (75, 75, 75)

MENU_BORDER = (180, 180, 180)

WALK_EDGE_COLOR = (70, 150, 255)

WALK_VERTEX_COLOR = (100, 180, 255)

ALGORITHM_PATH_COLOR = (180, 100, 255)

CLOSED_WALK_COLOR = (255, 90, 70)

BIPARTITE_COLOR_0 = (90, 170, 255)

BIPARTITE_COLOR_1 = (255, 150, 90)

POPUP_BACKGROUND = (20, 20, 20)

POPUP_BORDER = (230, 230, 230)

SUCCESS_COLOR = (100, 230, 130)

FAIL_COLOR = (255, 100, 100)


# =========================================================
# SETTINGS
# =========================================================

GRID_SIZE = 50

VERTEX_RADIUS = 22

MENU_WIDTH = 220

MENU_ITEM_HEIGHT = 42

MAX_PARALLEL_EDGES = 4

EDGE_HOVER_DISTANCE = 10


# =========================================================
# MODES
# =========================================================

EDIT_MODE = "EDIT GRAPH"

WALK_MODE = "BUILD WALK"

ALGORITHM_MODE = "RUN ALGORITHM"

CHECK_BIPARTITE_MODE = "CHECK IF BIPARTITE"

current_mode = EDIT_MODE


# =========================================================
# GRAPH DATA
# =========================================================

vertices = []

# Every tuple is one REAL edge.
#
# Example:
#
# (0, 1)
# (0, 1)
# (0, 1)
#
# means three separate parallel edges.
edges = []

selected_vertex = None

next_vertex_number = 0


# =========================================================
# WALK DATA
# =========================================================

# Exact vertices visited.
#
# Example:
# [a, b, c]
walk_vertices = []

# Exact edges used.
#
# If:
#
# walk_vertices = [a, b, c]
#
# then:
#
# walk_edges[0] connects a -> b
# walk_edges[1] connects b -> c
#
# This is important for multigraphs.
walk_edges = []


# =========================================================
# ALGORITHM 1 DATA
# =========================================================

algorithm_path = []

algorithm_path_edges = []

algorithm_closed = None

algorithm_closed_edges = []

algorithm_phase = "IDLE"

algorithm_message = ""


# =========================================================
# BIPARTITE DATA
# =========================================================

bipartite_colors = {}

bipartite_message = ""

bipartite_message_color = WHITE

bipartite_message_until = 0


# =========================================================
# CONTEXT MENU
# =========================================================

menu_open = False

menu_x = 0

menu_y = 0

menu_items = [
    "EDIT GRAPH",
    "BUILD WALK",
    "RUN ALGORITHM",
    "CHECK IF BIPARTITE",
    "RESET GRAPH",
]


# =========================================================
# VERTEX LABELS
# =========================================================

def get_vertex_label(index):

    if index < 26:

        return chr(
            ord("a") + index
        )

    if index < 52:

        return chr(
            ord("A") + (index - 26)
        )

    return f"V{index + 1}"


# =========================================================
# GRID / POSITION HELPERS
# =========================================================

def snap_to_grid(value):

    return round(
        value / GRID_SIZE
    ) * GRID_SIZE


def position_is_valid(x, y):

    for vertex in vertices:

        if (
            vertex["x"] == x
            and
            vertex["y"] == y
        ):

            return False

    return True


def get_vertex_at_position(x, y):

    for index, vertex in enumerate(
        vertices
    ):

        dx = x - vertex["x"]

        dy = y - vertex["y"]

        distance_squared = (
            dx * dx
            +
            dy * dy
        )

        if (
            distance_squared
            <= VERTEX_RADIUS ** 2
        ):

            return index

    return None


def get_vertex_index_by_label(label):

    for index, vertex in enumerate(
        vertices
    ):

        if vertex["label"] == label:

            return index

    return None


# =========================================================
# RESET HELPERS
# =========================================================

def reset_algorithm_state():

    global algorithm_path
    global algorithm_path_edges

    global algorithm_closed
    global algorithm_closed_edges

    global algorithm_phase
    global algorithm_message

    algorithm_path = []

    algorithm_path_edges = []

    algorithm_closed = None

    algorithm_closed_edges = []

    algorithm_phase = "IDLE"

    algorithm_message = ""


def reset_bipartite_state():

    global bipartite_colors

    global bipartite_message

    global bipartite_message_until

    bipartite_colors = {}

    bipartite_message = ""

    bipartite_message_until = 0


def clear_walk():

    walk_vertices.clear()

    walk_edges.clear()

    reset_algorithm_state()


def graph_changed():

    # If the actual graph changes,
    # old edge IDs in a walk might no
    # longer be valid.

    clear_walk()

    reset_bipartite_state()


# =========================================================
# ADD VERTEX
# =========================================================

def add_vertex(x, y):

    global next_vertex_number

    x = snap_to_grid(x)

    y = snap_to_grid(y)

    if not position_is_valid(
        x,
        y
    ):

        print(
            "A vertex already exists here."
        )

        return

    label = get_vertex_label(
        next_vertex_number
    )

    next_vertex_number += 1

    vertices.append(
        {
            "x": x,
            "y": y,
            "label": label,
        }
    )

    graph_changed()

    print(
        f"Created vertex {label} "
        f"at ({x}, {y})"
    )


# =========================================================
# DELETE VERTEX
# =========================================================

def delete_vertex(vertex_index):

    global selected_vertex

    label = vertices[
        vertex_index
    ]["label"]

    remaining_edges = []

    for vertex1, vertex2 in edges:

        # Delete edges attached to
        # the removed vertex.

        if (
            vertex1 == vertex_index
            or
            vertex2 == vertex_index
        ):

            continue

        # Vertex indexes shift down
        # after deleting a vertex.

        if vertex1 > vertex_index:

            vertex1 -= 1

        if vertex2 > vertex_index:

            vertex2 -= 1

        remaining_edges.append(
            (
                vertex1,
                vertex2,
            )
        )

    edges.clear()

    edges.extend(
        remaining_edges
    )

    vertices.pop(
        vertex_index
    )

    selected_vertex = None

    graph_changed()

    print(
        f"Deleted vertex {label} "
        f"and all attached edges."
    )


# =========================================================
# EDGE HELPERS
# =========================================================

def get_parallel_edge_indices(
    vertex1,
    vertex2
):

    result = []

    for edge_index, edge in enumerate(
        edges
    ):

        a, b = edge

        if (
            (
                a == vertex1
                and
                b == vertex2
            )
            or
            (
                a == vertex2
                and
                b == vertex1
            )
        ):

            result.append(
                edge_index
            )

    return result


def count_edges_between(
    vertex1,
    vertex2
):

    return len(
        get_parallel_edge_indices(
            vertex1,
            vertex2
        )
    )


def edge_exists(
    vertex1,
    vertex2
):

    return (
        count_edges_between(
            vertex1,
            vertex2
        )
        > 0
    )


def vertices_are_connected(
    vertex1,
    vertex2
):

    return edge_exists(
        vertex1,
        vertex2
    )


def edge_is_incident_to_vertex(
    edge_index,
    vertex_index
):

    if not (
        0
        <=
        edge_index
        <
        len(edges)
    ):

        return False

    a, b = edges[
        edge_index
    ]

    return (
        a == vertex_index
        or
        b == vertex_index
    )


def get_other_endpoint(
    edge_index,
    vertex_index
):

    if not edge_is_incident_to_vertex(
        edge_index,
        vertex_index
    ):

        return None

    a, b = edges[
        edge_index
    ]

    if a == vertex_index:

        return b

    return a


def get_parallel_edge_number(
    edge_index
):

    if not (
        0
        <=
        edge_index
        <
        len(edges)
    ):

        return None, None

    a, b = edges[
        edge_index
    ]

    group = (
        get_parallel_edge_indices(
            a,
            b
        )
    )

    return (
        group.index(edge_index) + 1,
        len(group),
    )


def get_default_edge_between(
    vertex1,
    vertex2
):

    """
    If the user clicks vertex -> vertex
    instead of choosing a specific curve,
    use bridge #1 / the first-created edge.
    """

    group = (
        get_parallel_edge_indices(
            vertex1,
            vertex2
        )
    )

    if not group:

        return None

    return group[0]


# =========================================================
# ADD EDGE
# =========================================================

def add_edge(
    vertex1,
    vertex2
):

    if vertex1 == vertex2:

        print(
            "Self-loops are not enabled."
        )

        return

    current_count = (
        count_edges_between(
            vertex1,
            vertex2
        )
    )

    if (
        current_count
        >=
        MAX_PARALLEL_EDGES
    ):

        label1 = vertices[
            vertex1
        ]["label"]

        label2 = vertices[
            vertex2
        ]["label"]

        print(
            f"Maximum of "
            f"{MAX_PARALLEL_EDGES} edges "
            f"between {label1} and {label2}."
        )

        return

    edges.append(
        (
            vertex1,
            vertex2,
        )
    )

    graph_changed()

    label1 = vertices[
        vertex1
    ]["label"]

    label2 = vertices[
        vertex2
    ]["label"]

    print(
        f"Created edge "
        f"{label1} -- {label2} "
        f"({current_count + 1}/"
        f"{MAX_PARALLEL_EDGES})"
    )


# =========================================================
# DELETE ONE EDGE
# =========================================================

def delete_edge(
    edge_index
):

    if not (
        0
        <=
        edge_index
        <
        len(edges)
    ):

        return

    vertex1, vertex2 = (
        edges[
            edge_index
        ]
    )

    label1 = vertices[
        vertex1
    ]["label"]

    label2 = vertices[
        vertex2
    ]["label"]

    edges.pop(
        edge_index
    )

    graph_changed()

    remaining = (
        count_edges_between(
            vertex1,
            vertex2
        )
    )

    print(
        f"Deleted one edge "
        f"{label1} -- {label2}. "
        f"{remaining} remaining."
    )


# =========================================================
# MULTI-EDGE CURVE OFFSETS
# =========================================================

def get_parallel_offsets(count):

    if count == 1:

        return [
            0
        ]

    if count == 2:

        return [
            -24,
            24,
        ]

    if count == 3:

        return [
            -36,
            0,
            36,
        ]

    if count == 4:

        return [
            -48,
            -16,
            16,
            48,
        ]

    return []


# =========================================================
# CREATE CURVED EDGE
# =========================================================

def make_curve_points(
    start,
    end,
    offset
):

    # Straight center edge.

    if offset == 0:

        return [
            start,
            end,
        ]

    x1, y1 = start

    x2, y2 = end

    dx = x2 - x1

    dy = y2 - y1

    length = math.hypot(
        dx,
        dy
    )

    if length == 0:

        return [
            start,
            end,
        ]

    # Perpendicular direction.

    perpendicular_x = (
        -dy / length
    )

    perpendicular_y = (
        dx / length
    )

    midpoint_x = (
        x1 + x2
    ) / 2

    midpoint_y = (
        y1 + y2
    ) / 2

    # Bezier control point.

    control_x = (
        midpoint_x
        +
        perpendicular_x
        *
        offset
        *
        2
    )

    control_y = (
        midpoint_y
        +
        perpendicular_y
        *
        offset
        *
        2
    )

    points = []

    for step in range(
        31
    ):

        t = step / 30

        one_minus_t = (
            1 - t
        )

        x = (
            one_minus_t ** 2
            * x1

            +

            2
            * one_minus_t
            * t
            * control_x

            +

            t ** 2
            * x2
        )

        y = (
            one_minus_t ** 2
            * y1

            +

            2
            * one_minus_t
            * t
            * control_y

            +

            t ** 2
            * y2
        )

        points.append(
            (
                x,
                y,
            )
        )

    return points


# =========================================================
# EDGE RENDER DATA
# =========================================================

def get_edge_render_data():

    groups = {}

    # Group parallel edges.

    for edge_index, edge in enumerate(
        edges
    ):

        vertex1, vertex2 = edge

        key = tuple(
            sorted(
                (
                    vertex1,
                    vertex2,
                )
            )
        )

        if key not in groups:

            groups[key] = []

        groups[key].append(
            edge_index
        )

    render_data = []

    for key, edge_indexes in (
        groups.items()
    ):

        offsets = (
            get_parallel_offsets(
                len(edge_indexes)
            )
        )

        vertex1 = key[0]

        vertex2 = key[1]

        start = (
            vertices[
                vertex1
            ]["x"],
            vertices[
                vertex1
            ]["y"],
        )

        end = (
            vertices[
                vertex2
            ]["x"],
            vertices[
                vertex2
            ]["y"],
        )

        for (
            edge_index,
            offset
        ) in zip(
            edge_indexes,
            offsets
        ):

            points = (
                make_curve_points(
                    start,
                    end,
                    offset
                )
            )

            render_data.append(
                (
                    edge_index,
                    points,
                )
            )

    return render_data


def get_edge_render_map():

    return {
        edge_index: points

        for edge_index, points

        in get_edge_render_data()
    }


# =========================================================
# EDGE HOVER DETECTION
# =========================================================

def point_to_segment_distance(
    px,
    py,
    x1,
    y1,
    x2,
    y2
):

    dx = x2 - x1

    dy = y2 - y1

    if (
        dx == 0
        and
        dy == 0
    ):

        return math.hypot(
            px - x1,
            py - y1
        )

    t = (
        (
            (px - x1) * dx
            +
            (py - y1) * dy
        )
        /
        (
            dx * dx
            +
            dy * dy
        )
    )

    t = max(
        0,
        min(
            1,
            t
        )
    )

    nearest_x = (
        x1 + t * dx
    )

    nearest_y = (
        y1 + t * dy
    )

    return math.hypot(
        px - nearest_x,
        py - nearest_y
    )


def get_hovered_edge(
    mouse_x,
    mouse_y
):

    best_edge = None

    best_distance = (
        EDGE_HOVER_DISTANCE
    )

    for edge_index, points in (
        get_edge_render_data()
    ):

        for point_index in range(
            len(points) - 1
        ):

            x1, y1 = (
                points[
                    point_index
                ]
            )

            x2, y2 = (
                points[
                    point_index + 1
                ]
            )

            distance = (
                point_to_segment_distance(
                    mouse_x,
                    mouse_y,
                    x1,
                    y1,
                    x2,
                    y2
                )
            )

            if (
                distance
                <
                best_distance
            ):

                best_distance = (
                    distance
                )

                best_edge = (
                    edge_index
                )

    return best_edge


# =========================================================
# WALK FUNCTIONS
# =========================================================

def print_walk():

    print(
        "Walk: "
        +
        " -> ".join(
            vertices[index]["label"]

            for index in walk_vertices
        )
    )


def start_walk_at_vertex(
    vertex_index
):

    walk_vertices.append(
        vertex_index
    )

    print(
        f"Walk started at "
        f"{vertices[vertex_index]['label']}"
    )


def add_vertex_to_walk(
    vertex_index
):

    """
    Normal vertex -> vertex selection.

    If multiple edges exist,
    automatically use bridge #1.
    """

    if not walk_vertices:

        start_walk_at_vertex(
            vertex_index
        )

        return

    previous_vertex = (
        walk_vertices[-1]
    )

    edge_index = (
        get_default_edge_between(
            previous_vertex,
            vertex_index
        )
    )

    if edge_index is None:

        print(
            f"INVALID WALK MOVE: "
            f"No edge between "
            f"{vertices[previous_vertex]['label']} "
            f"and "
            f"{vertices[vertex_index]['label']}"
        )

        return

    walk_edges.append(
        edge_index
    )

    walk_vertices.append(
        vertex_index
    )

    bridge_number, bridge_total = (
        get_parallel_edge_number(
            edge_index
        )
    )

    if (
        bridge_total is not None
        and
        bridge_total > 1
    ):

        print(
            f"Defaulted to bridge "
            f"{bridge_number}/"
            f"{bridge_total} between "
            f"{vertices[previous_vertex]['label']} "
            f"and "
            f"{vertices[vertex_index]['label']}."
        )

    print_walk()


def add_edge_to_walk(
    edge_index
):

    """
    Clicking a specific curved edge
    uses that exact bridge.
    """

    if not walk_vertices:

        print(
            "Start the walk by "
            "clicking a vertex first."
        )

        return

    current_vertex = (
        walk_vertices[-1]
    )

    next_vertex = (
        get_other_endpoint(
            edge_index,
            current_vertex
        )
    )

    if next_vertex is None:

        print(
            f"That edge is not connected "
            f"to the current walk vertex "
            f"{vertices[current_vertex]['label']}."
        )

        return

    walk_edges.append(
        edge_index
    )

    walk_vertices.append(
        next_vertex
    )

    bridge_number, bridge_total = (
        get_parallel_edge_number(
            edge_index
        )
    )

    print(
        f"Used bridge "
        f"{bridge_number}/"
        f"{bridge_total} from "
        f"{vertices[current_vertex]['label']} "
        f"to "
        f"{vertices[next_vertex]['label']}."
    )

    print_walk()


def undo_walk_step():

    if not walk_vertices:

        return

    removed_vertex = (
        walk_vertices.pop()
    )

    # One fewer vertex means one fewer
    # traversed edge, except when deleting
    # the very first/start vertex.

    if walk_edges:

        walk_edges.pop()

    reset_algorithm_state()

    print(
        f"Removed "
        f"{vertices[removed_vertex]['label']} "
        f"from walk."
    )


# =========================================================
# ALGORITHM 1
# =========================================================

def start_algorithm():

    global algorithm_path
    global algorithm_path_edges

    global algorithm_closed
    global algorithm_closed_edges

    global algorithm_phase
    global algorithm_message

    if not walk_vertices:

        algorithm_path = []

        algorithm_path_edges = []

        algorithm_closed = None

        algorithm_closed_edges = []

        algorithm_phase = "IDLE"

        algorithm_message = (
            "Build a walk first."
        )

        print(
            "Cannot run Algorithm 1: "
            "no walk exists."
        )

        return

    algorithm_path = [

        vertices[index]["label"]

        for index in walk_vertices
    ]

    # IMPORTANT:
    #
    # Keep the exact bridges used by W.

    algorithm_path_edges = (
        walk_edges.copy()
    )

    algorithm_closed = None

    algorithm_closed_edges = []

    algorithm_phase = "CHECK"

    algorithm_message = (
        "P := W    "
        "Press SPACE to continue."
    )

    print(
        "Algorithm 1 started."
    )

    print(
        "P = "
        +
        " -> ".join(
            algorithm_path
        )
    )


def next_algorithm_step():

    global algorithm_path
    global algorithm_path_edges

    global algorithm_closed
    global algorithm_closed_edges

    global algorithm_phase
    global algorithm_message

    if not algorithm_path:

        algorithm_message = (
            "No walk loaded."
        )

        return


    # =====================================================
    # CHECK
    # =====================================================

    if algorithm_phase == "CHECK":

        # ---------------------------------
        # Path
        # ---------------------------------

        if is_path(
            algorithm_path
        ):

            algorithm_phase = (
                "FINISHED"
            )

            algorithm_closed = None

            algorithm_closed_edges = []

            algorithm_message = (
                "P is a path. "
                "Algorithm finished."
            )

            print(
                "Algorithm finished: "
                "P is a path."
            )

            print(
                "Output P = "
                +
                " -> ".join(
                    algorithm_path
                )
            )

            return


        # ---------------------------------
        # Cycle
        # ---------------------------------

        if is_cycle(
            algorithm_path
        ):

            algorithm_phase = (
                "FINISHED"
            )

            algorithm_closed = None

            algorithm_closed_edges = []

            algorithm_message = (
                "P is a cycle. "
                "Algorithm finished."
            )

            print(
                "Algorithm finished: "
                "P is a cycle."
            )

            print(
                "Output P = "
                +
                " -> ".join(
                    algorithm_path
                )
            )

            return


        # ---------------------------------
        # Find C
        # ---------------------------------

        algorithm_closed = (
            find_shortest_closed_subwalk(
                algorithm_path
            )
        )

        if algorithm_closed is None:

            algorithm_phase = (
                "FINISHED"
            )

            algorithm_closed_edges = []

            algorithm_message = (
                "No closed subwalk found."
            )

            return

        start = (
            algorithm_closed[
                "start"
            ]
        )

        end = (
            algorithm_closed[
                "end"
            ]
        )

        # Example:
        #
        # vertices:
        # b -> c -> d -> b
        #
        # uses three edges:
        #
        # edge[start:end]

        algorithm_closed_edges = (
            algorithm_path_edges[
                start:end
            ].copy()
        )

        algorithm_phase = (
            "SHOW_C"
        )

        algorithm_message = (
            "Found shortest closed "
            "subwalk C. "
            "Press SPACE to remove it."
        )

        print(
            "C = "
            +
            " -> ".join(
                algorithm_closed[
                    "walk"
                ]
            )
        )


    # =====================================================
    # REMOVE C
    # =====================================================

    elif algorithm_phase == "SHOW_C":

        start = (
            algorithm_closed[
                "start"
            ]
        )

        end = (
            algorithm_closed[
                "end"
            ]
        )

        # Remove the exact bridges
        # belonging to C.

        algorithm_path_edges = (
            algorithm_path_edges[
                :start
            ]
            +
            algorithm_path_edges[
                end:
            ]
        )

        algorithm_path = (
            remove_closed_subwalk(
                algorithm_path,
                start,
                end
            )
        )

        algorithm_closed = None

        algorithm_closed_edges = []

        algorithm_phase = "CHECK"

        algorithm_message = (
            "P := P minus C. "
            "Press SPACE to continue."
        )

        print(
            "New P = "
            +
            " -> ".join(
                algorithm_path
            )
        )


    # =====================================================
    # FINISHED
    # =====================================================

    elif algorithm_phase == "FINISHED":

        algorithm_message = (
            "Algorithm already finished."
        )


# =========================================================
# ALGORITHM 2: BIPARTITE
# =========================================================

def build_adjacency_graph():

    graph = {}

    for index, vertex in enumerate(
        vertices
    ):

        label = vertex[
            "label"
        ]

        graph[label] = []

        # Parallel edges do not change
        # whether a graph is bipartite.
        #
        # So each neighbor only needs
        # to appear once.

        for neighbor in range(
            len(vertices)
        ):

            if edge_exists(
                index,
                neighbor
            ):

                graph[label].append(
                    vertices[
                        neighbor
                    ]["label"]
                )

    return graph


def check_current_graph_bipartite():

    global bipartite_colors

    global bipartite_message

    global bipartite_message_color

    global bipartite_message_until

    graph = (
        build_adjacency_graph()
    )

    result, coloring = (
        get_bipartite_coloring(
            graph
        )
    )

    if result:

        bipartite_colors = (
            coloring
        )

        bipartite_message = (
            "Graph is BIPARTITE"
        )

        bipartite_message_color = (
            SUCCESS_COLOR
        )

        print(
            "The graph IS bipartite."
        )

    else:

        bipartite_colors = {}

        bipartite_message = (
            "Graph is NOT bipartite"
        )

        bipartite_message_color = (
            FAIL_COLOR
        )

        print(
            "The graph is NOT bipartite."
        )

    bipartite_message_until = (
        pygame.time.get_ticks()
        +
        3000
    )


# =========================================================
# RESET GRAPH
# =========================================================

def reset_graph():

    global selected_vertex

    global next_vertex_number

    vertices.clear()

    edges.clear()

    walk_vertices.clear()

    walk_edges.clear()

    selected_vertex = None

    next_vertex_number = 0

    reset_algorithm_state()

    reset_bipartite_state()

    print(
        "Graph reset."
    )


# =========================================================
# MODE CONTROL
# =========================================================

def set_mode(new_mode):

    global current_mode

    global selected_vertex

    global menu_open

    current_mode = new_mode

    selected_vertex = None

    menu_open = False

    print(
        f"Mode changed to: "
        f"{current_mode}"
    )

    if (
        new_mode
        ==
        ALGORITHM_MODE
    ):

        start_algorithm()

    elif (
        new_mode
        ==
        CHECK_BIPARTITE_MODE
    ):

        check_current_graph_bipartite()


# =========================================================
# DRAW GRID
# =========================================================

def draw_grid():

    for x in range(
        0,
        WIDTH,
        GRID_SIZE
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(
        0,
        HEIGHT,
        GRID_SIZE
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
        )


# =========================================================
# DRAW NORMAL EDGES
# =========================================================

def draw_edges():

    mouse_x, mouse_y = (
        pygame.mouse.get_pos()
    )

    hovered_vertex = (
        get_vertex_at_position(
            mouse_x,
            mouse_y
        )
    )

    hovered_edge = None

    if (
        current_mode
        in
        (
            EDIT_MODE,
            WALK_MODE,
        )
        and
        hovered_vertex is None
    ):

        candidate = (
            get_hovered_edge(
                mouse_x,
                mouse_y
            )
        )

        if candidate is not None:

            # In Edit mode any edge
            # can glow for deletion.

            if (
                current_mode
                ==
                EDIT_MODE
            ):

                hovered_edge = (
                    candidate
                )

            # In Walk mode only an edge
            # connected to the current
            # vertex is a valid next step.

            elif (
                walk_vertices
                and
                edge_is_incident_to_vertex(
                    candidate,
                    walk_vertices[-1]
                )
            ):

                hovered_edge = (
                    candidate
                )

    for edge_index, points in (
        get_edge_render_data()
    ):

        if (
            edge_index
            ==
            hovered_edge
        ):

            color = (
                HOVER_COLOR
            )

            width = 7

        else:

            color = (
                EDGE_COLOR
            )

            width = 4

        pygame.draw.lines(
            screen,
            color,
            False,
            points,
            width
        )


# =========================================================
# DRAW EXACT EDGE IDS
# =========================================================

def draw_exact_edges(
    edge_indices,
    color,
    width
):

    render_map = (
        get_edge_render_map()
    )

    for edge_index in edge_indices:

        points = (
            render_map.get(
                edge_index
            )
        )

        if points:

            pygame.draw.lines(
                screen,
                color,
                False,
                points,
                width
            )


# =========================================================
# DRAW WALK
# =========================================================

def draw_walk():

    if not walk_vertices:

        return

    # IMPORTANT:
    #
    # Draw the actual bridge used.
    #
    # We no longer invent a straight
    # line between two vertices.

    draw_exact_edges(
        walk_edges,
        WALK_EDGE_COLOR,
        7
    )

    for vertex_index in (
        walk_vertices
    ):

        vertex = vertices[
            vertex_index
        ]

        pygame.draw.circle(
            screen,
            WALK_VERTEX_COLOR,
            (
                vertex["x"],
                vertex["y"],
            ),
            VERTEX_RADIUS + 5,
            4
        )


# =========================================================
# DRAW ALGORITHM P
# =========================================================

def draw_algorithm_path():

    if (
        current_mode
        !=
        ALGORITHM_MODE
    ):

        return

    draw_exact_edges(
        algorithm_path_edges,
        ALGORITHM_PATH_COLOR,
        7
    )


# =========================================================
# DRAW CLOSED SUBWALK C
# =========================================================

def draw_closed_subwalk():

    if (
        current_mode
        !=
        ALGORITHM_MODE
    ):

        return

    if algorithm_closed is None:

        return

    draw_exact_edges(
        algorithm_closed_edges,
        CLOSED_WALK_COLOR,
        10
    )


# =========================================================
# DRAW VERTICES
# =========================================================

def draw_vertices():

    mouse_x, mouse_y = (
        pygame.mouse.get_pos()
    )

    hovered_vertex = (
        get_vertex_at_position(
            mouse_x,
            mouse_y
        )
    )

    for index, vertex in enumerate(
        vertices
    ):

        x = vertex["x"]

        y = vertex["y"]

        label = vertex[
            "label"
        ]

        fill_color = (
            VERTEX_COLOR
        )

        # ---------------------------------
        # Bipartite coloring
        # ---------------------------------

        if (
            current_mode
            ==
            CHECK_BIPARTITE_MODE
            and
            label in bipartite_colors
        ):

            if (
                bipartite_colors[
                    label
                ]
                == 0
            ):

                fill_color = (
                    BIPARTITE_COLOR_0
                )

            else:

                fill_color = (
                    BIPARTITE_COLOR_1
                )

        pygame.draw.circle(
            screen,
            fill_color,
            (x, y),
            VERTEX_RADIUS
        )


        # ---------------------------------
        # Border
        # ---------------------------------

        if (
            index
            ==
            selected_vertex
        ):

            border_color = (
                SELECTED_COLOR
            )

            border_width = 5

        elif (
            index
            ==
            hovered_vertex
            and
            current_mode
            in
            (
                EDIT_MODE,
                WALK_MODE,
            )
        ):

            border_color = (
                HOVER_COLOR
            )

            border_width = 4

        else:

            border_color = (
                BORDER_COLOR
            )

            border_width = 2

        pygame.draw.circle(
            screen,
            border_color,
            (x, y),
            VERTEX_RADIUS,
            border_width
        )


        # ---------------------------------
        # Label
        # ---------------------------------

        text = vertex_font.render(
            label,
            True,
            TEXT_COLOR
        )

        text_rect = text.get_rect(
            center=(x, y)
        )

        screen.blit(
            text,
            text_rect
        )


# =========================================================
# MODE DISPLAY
# =========================================================

def draw_mode_display():

    mode_text = ui_font.render(
        f"MODE: {current_mode}",
        True,
        WHITE
    )

    screen.blit(
        mode_text,
        (15, 15)
    )

    if current_mode == EDIT_MODE:

        instructions = (
            "1 Edit   2 Walk   3 Algorithm"
            "   |   Click pair = Add Edge"
            "   |   Hover + X Delete"
            "   |   Right Click Menu"
        )

    elif current_mode == WALK_MODE:

        instructions = (
            "Click vertex = default bridge"
            "   |   Click exact edge = that bridge"
            "   |   Backspace Undo"
            "   |   C Clear"
        )

    elif (
        current_mode
        ==
        ALGORITHM_MODE
    ):

        instructions = (
            "SPACE = Next Algorithm Step"
            "   |   1 Edit"
            "   |   2 Walk"
            "   |   Right Click Menu"
        )

    elif (
        current_mode
        ==
        CHECK_BIPARTITE_MODE
    ):

        instructions = (
            "Algorithm 2: Bipartite Check"
            "   |   Right Click Menu"
            "   |   1 Edit"
        )

    else:

        instructions = ""

    help_text = ui_font.render(
        instructions,
        True,
        (170, 170, 170)
    )

    screen.blit(
        help_text,
        (15, 45)
    )


# =========================================================
# WALK DISPLAY
# =========================================================

def draw_walk_display():

    if not walk_vertices:

        walk_string = (
            "W = empty"
        )

    else:

        labels = [

            vertices[index]["label"]

            for index in walk_vertices
        ]

        walk_string = (
            "W = "
            +
            " -> ".join(
                labels
            )
        )

    text = ui_font.render(
        walk_string,
        True,
        WHITE
    )

    screen.blit(
        text,
        (15, 75)
    )


# =========================================================
# ALGORITHM DISPLAY
# =========================================================

def draw_algorithm_display():

    if (
        current_mode
        !=
        ALGORITHM_MODE
    ):

        return

    if algorithm_path:

        path_text = (
            "P = "
            +
            " -> ".join(
                algorithm_path
            )
        )

    else:

        path_text = (
            "P = empty"
        )

    rendered_path = (
        ui_font.render(
            path_text,
            True,
            WHITE
        )
    )

    screen.blit(
        rendered_path,
        (15, 105)
    )


    if (
        algorithm_closed
        is not None
    ):

        closed_text = (
            "C = "
            +
            " -> ".join(
                algorithm_closed[
                    "walk"
                ]
            )
        )

    else:

        closed_text = (
            "C = none"
        )

    rendered_closed = (
        ui_font.render(
            closed_text,
            True,
            WHITE
        )
    )

    screen.blit(
        rendered_closed,
        (15, 135)
    )


    message = ui_font.render(
        algorithm_message,
        True,
        WHITE
    )

    screen.blit(
        message,
        (15, 165)
    )


# =========================================================
# BIPARTITE POPUP
# =========================================================

def draw_bipartite_popup():

    if (
        bipartite_message
        ==
        ""
    ):

        return

    if (
        pygame.time.get_ticks()
        >
        bipartite_message_until
    ):

        return

    text = ui_font.render(
        bipartite_message,
        True,
        bipartite_message_color
    )

    padding_x = 30

    padding_y = 18

    box_width = (
        text.get_width()
        +
        padding_x * 2
    )

    box_height = (
        text.get_height()
        +
        padding_y * 2
    )

    box_x = (
        WIDTH // 2
        -
        box_width // 2
    )

    box_y = 100

    popup_rect = pygame.Rect(
        box_x,
        box_y,
        box_width,
        box_height
    )

    pygame.draw.rect(
        screen,
        POPUP_BACKGROUND,
        popup_rect
    )

    pygame.draw.rect(
        screen,
        POPUP_BORDER,
        popup_rect,
        2
    )

    text_rect = text.get_rect(
        center=popup_rect.center
    )

    screen.blit(
        text,
        text_rect
    )


# =========================================================
# CONTEXT MENU
# =========================================================

def open_context_menu(
    x,
    y
):

    global menu_open

    global menu_x

    global menu_y

    menu_open = True

    menu_x = min(
        x,
        WIDTH - MENU_WIDTH
    )

    total_height = (
        len(menu_items)
        *
        MENU_ITEM_HEIGHT
    )

    menu_y = min(
        y,
        HEIGHT - total_height
    )


def draw_context_menu():

    if not menu_open:

        return

    mouse_x, mouse_y = (
        pygame.mouse.get_pos()
    )

    total_height = (
        len(menu_items)
        *
        MENU_ITEM_HEIGHT
    )

    pygame.draw.rect(
        screen,
        MENU_BACKGROUND,
        (
            menu_x,
            menu_y,
            MENU_WIDTH,
            total_height,
        )
    )

    pygame.draw.rect(
        screen,
        MENU_BORDER,
        (
            menu_x,
            menu_y,
            MENU_WIDTH,
            total_height,
        ),
        2
    )

    for index, item in enumerate(
        menu_items
    ):

        item_y = (
            menu_y
            +
            index
            *
            MENU_ITEM_HEIGHT
        )

        item_rect = pygame.Rect(
            menu_x,
            item_y,
            MENU_WIDTH,
            MENU_ITEM_HEIGHT
        )

        if item_rect.collidepoint(
            mouse_x,
            mouse_y
        ):

            pygame.draw.rect(
                screen,
                MENU_HOVER,
                item_rect
            )

        text = menu_font.render(
            item,
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                menu_x + 12,
                item_y + 10,
            )
        )


def handle_menu_click(
    x,
    y
):

    global menu_open

    if not menu_open:

        return False

    for index, item in enumerate(
        menu_items
    ):

        item_rect = pygame.Rect(
            menu_x,
            menu_y
            +
            index
            *
            MENU_ITEM_HEIGHT,
            MENU_WIDTH,
            MENU_ITEM_HEIGHT
        )

        if item_rect.collidepoint(
            x,
            y
        ):

            if (
                item
                ==
                "EDIT GRAPH"
            ):

                set_mode(
                    EDIT_MODE
                )

            elif (
                item
                ==
                "BUILD WALK"
            ):

                set_mode(
                    WALK_MODE
                )

            elif (
                item
                ==
                "RUN ALGORITHM"
            ):

                set_mode(
                    ALGORITHM_MODE
                )

            elif (
                item
                ==
                "CHECK IF BIPARTITE"
            ):

                set_mode(
                    CHECK_BIPARTITE_MODE
                )

            elif (
                item
                ==
                "RESET GRAPH"
            ):

                reset_graph()

                menu_open = False

            return True

    menu_open = False

    return False


# =========================================================
# MAIN LOOP
# =========================================================

running = True


while running:

    for event in pygame.event.get():


        # =================================================
        # QUIT
        # =================================================

        if event.type == pygame.QUIT:

            running = False


        # =================================================
        # KEYBOARD
        # =================================================

        if event.type == pygame.KEYDOWN:


            # ---------------------------------
            # MODE SHORTCUTS
            # ---------------------------------

            if event.key == pygame.K_1:

                set_mode(
                    EDIT_MODE
                )


            elif event.key == pygame.K_2:

                set_mode(
                    WALK_MODE
                )


            elif event.key == pygame.K_3:

                set_mode(
                    ALGORITHM_MODE
                )


            # ---------------------------------
            # ALGORITHM STEP
            # ---------------------------------

            elif (
                event.key
                ==
                pygame.K_SPACE
            ):

                if (
                    current_mode
                    ==
                    ALGORITHM_MODE
                ):

                    next_algorithm_step()


            # ---------------------------------
            # X DELETE
            # ---------------------------------

            elif event.key == pygame.K_x:

                if (
                    current_mode
                    ==
                    EDIT_MODE
                ):

                    mouse_x, mouse_y = (
                        pygame.mouse.get_pos()
                    )

                    # Vertex has priority.

                    hovered_vertex = (
                        get_vertex_at_position(
                            mouse_x,
                            mouse_y
                        )
                    )

                    if (
                        hovered_vertex
                        is not None
                    ):

                        delete_vertex(
                            hovered_vertex
                        )

                    else:

                        hovered_edge = (
                            get_hovered_edge(
                                mouse_x,
                                mouse_y
                            )
                        )

                        if (
                            hovered_edge
                            is not None
                        ):

                            delete_edge(
                                hovered_edge
                            )


            # ---------------------------------
            # WALK UNDO
            # ---------------------------------

            elif (
                event.key
                ==
                pygame.K_BACKSPACE
            ):

                if (
                    current_mode
                    ==
                    WALK_MODE
                ):

                    undo_walk_step()


            # ---------------------------------
            # CLEAR WALK
            # ---------------------------------

            elif event.key == pygame.K_c:

                if (
                    current_mode
                    ==
                    WALK_MODE
                ):

                    clear_walk()

                    print(
                        "Walk cleared."
                    )


            # ---------------------------------
            # ESC
            # ---------------------------------

            elif (
                event.key
                ==
                pygame.K_ESCAPE
            ):

                menu_open = False

                selected_vertex = None


        # =================================================
        # MOUSE
        # =================================================

        if (
            event.type
            ==
            pygame.MOUSEBUTTONDOWN
        ):

            mouse_x, mouse_y = (
                event.pos
            )


            # ---------------------------------
            # RIGHT CLICK
            # ---------------------------------

            if event.button == 3:

                open_context_menu(
                    mouse_x,
                    mouse_y
                )

                continue


            # ---------------------------------
            # LEFT CLICK
            # ---------------------------------

            if event.button == 1:


                # Menu first.

                if menu_open:

                    handle_menu_click(
                        mouse_x,
                        mouse_y
                    )

                    continue


                # =================================
                # EDIT MODE
                # =================================

                if (
                    current_mode
                    ==
                    EDIT_MODE
                ):

                    clicked_vertex = (
                        get_vertex_at_position(
                            mouse_x,
                            mouse_y
                        )
                    )

                    if (
                        clicked_vertex
                        is not None
                    ):

                        if (
                            selected_vertex
                            is None
                        ):

                            selected_vertex = (
                                clicked_vertex
                            )

                            print(
                                f"Selected vertex "
                                f"{vertices[selected_vertex]['label']}"
                            )

                        else:

                            add_edge(
                                selected_vertex,
                                clicked_vertex
                            )

                            selected_vertex = None

                    else:

                        selected_vertex = None

                        add_vertex(
                            mouse_x,
                            mouse_y
                        )


                # =================================
                # WALK MODE
                # =================================

                elif (
                    current_mode
                    ==
                    WALK_MODE
                ):

                    # Vertex takes priority if
                    # cursor is actually on one.

                    clicked_vertex = (
                        get_vertex_at_position(
                            mouse_x,
                            mouse_y
                        )
                    )

                    if (
                        clicked_vertex
                        is not None
                    ):

                        # Clicking vertex -> vertex
                        # chooses default bridge #1.

                        add_vertex_to_walk(
                            clicked_vertex
                        )

                    else:

                        # Otherwise clicking the
                        # actual curved bridge
                        # selects THAT bridge.

                        clicked_edge = (
                            get_hovered_edge(
                                mouse_x,
                                mouse_y
                            )
                        )

                        if (
                            clicked_edge
                            is not None
                        ):

                            add_edge_to_walk(
                                clicked_edge
                            )

                    reset_algorithm_state()


                # =================================
                # ALGORITHM MODE
                # =================================

                elif (
                    current_mode
                    ==
                    ALGORITHM_MODE
                ):

                    pass


                # =================================
                # BIPARTITE MODE
                # =================================

                elif (
                    current_mode
                    ==
                    CHECK_BIPARTITE_MODE
                ):

                    pass


    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(
        BACKGROUND
    )

    draw_grid()

    draw_edges()


    # ---------------------------------
    # NORMAL WALK
    # ---------------------------------

    if (
        current_mode
        not in
        (
            ALGORITHM_MODE,
            CHECK_BIPARTITE_MODE,
        )
    ):

        draw_walk()


    # ---------------------------------
    # ALGORITHM 1
    # ---------------------------------

    draw_algorithm_path()

    draw_closed_subwalk()


    # ---------------------------------
    # VERTICES
    # ---------------------------------

    draw_vertices()


    # ---------------------------------
    # UI
    # ---------------------------------

    draw_mode_display()

    if (
        current_mode
        !=
        CHECK_BIPARTITE_MODE
    ):

        draw_walk_display()

    draw_algorithm_display()

    draw_bipartite_popup()

    draw_context_menu()


    pygame.display.flip()

    clock.tick(
        60
    )


pygame.quit()