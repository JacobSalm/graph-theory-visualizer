import pygame

from algorithm1 import (
    is_path,
    is_cycle,
    find_shortest_closed_subwalk,
    remove_closed_subwalk
)

from bipartite import (
    get_bipartite_coloring
)


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


# =========================================================
# BIPARTITE COLORS
# =========================================================

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

edges = []

selected_vertex = None

next_vertex_number = 0


# =========================================================
# WALK DATA
# =========================================================

walk = []


# =========================================================
# ALGORITHM 1 DATA
# =========================================================

algorithm_path = []

algorithm_closed = None

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
    "RESET GRAPH"
]


# =========================================================
# VERTEX LABELS
# =========================================================

def get_vertex_label(index):

    # a through z
    if index < 26:

        return chr(
            ord("a") + index
        )

    # A through Z
    if index < 52:

        return chr(
            ord("A") + (index - 26)
        )

    return f"V{index + 1}"


# =========================================================
# GRID
# =========================================================

def snap_to_grid(value):

    return round(
        value / GRID_SIZE
    ) * GRID_SIZE


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
# VERTEX HELPERS
# =========================================================

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
# RESET ALGORITHM STATE
# =========================================================

def reset_algorithm_state():

    global algorithm_path
    global algorithm_closed
    global algorithm_phase
    global algorithm_message

    algorithm_path = []

    algorithm_closed = None

    algorithm_phase = "IDLE"

    algorithm_message = ""


# =========================================================
# RESET BIPARTITE STATE
# =========================================================

def reset_bipartite_state():

    global bipartite_colors
    global bipartite_message
    global bipartite_message_until

    bipartite_colors = {}

    bipartite_message = ""

    bipartite_message_until = 0


# =========================================================
# ADD VERTEX
# =========================================================

def add_vertex(x, y):

    global next_vertex_number

    x = snap_to_grid(x)

    y = snap_to_grid(y)

    if not position_is_valid(x, y):

        print(
            "A vertex already exists here."
        )

        return

    label = get_vertex_label(
        next_vertex_number
    )

    next_vertex_number += 1

    vertex = {
        "x": x,
        "y": y,
        "label": label
    }

    vertices.append(
        vertex
    )

    reset_bipartite_state()

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

    # ---------------------------------
    # Remove attached edges
    # and fix remaining indexes
    # ---------------------------------

    for vertex1, vertex2 in edges:

        if (
            vertex1 == vertex_index
            or
            vertex2 == vertex_index
        ):

            continue

        if vertex1 > vertex_index:

            vertex1 -= 1

        if vertex2 > vertex_index:

            vertex2 -= 1

        remaining_edges.append(
            (vertex1, vertex2)
        )

    edges.clear()

    edges.extend(
        remaining_edges
    )

    vertices.pop(
        vertex_index
    )

    walk.clear()

    reset_algorithm_state()

    reset_bipartite_state()

    selected_vertex = None

    print(
        f"Deleted vertex {label} "
        f"and all attached edges."
    )

    print(
        "Existing walk cleared "
        "because the graph changed."
    )


# =========================================================
# EDGE FUNCTIONS
# =========================================================

def edge_exists(vertex1, vertex2):

    for edge in edges:

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

            return True

    return False


def vertices_are_connected(
    vertex1,
    vertex2
):

    return edge_exists(
        vertex1,
        vertex2
    )


def toggle_edge(vertex1, vertex2):

    if vertex1 == vertex2:

        print(
            "Cannot connect a vertex "
            "to itself."
        )

        return

    # ---------------------------------
    # Remove existing edge
    # ---------------------------------

    for edge in edges:

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

            edges.remove(
                edge
            )

            walk.clear()

            reset_algorithm_state()

            reset_bipartite_state()

            label1 = vertices[
                vertex1
            ]["label"]

            label2 = vertices[
                vertex2
            ]["label"]

            print(
                f"Removed edge "
                f"{label1} -- {label2}"
            )

            print(
                "Existing walk cleared "
                "because the graph changed."
            )

            return

    # ---------------------------------
    # Otherwise create edge
    # ---------------------------------

    edges.append(
        (vertex1, vertex2)
    )

    walk.clear()

    reset_algorithm_state()

    reset_bipartite_state()

    label1 = vertices[
        vertex1
    ]["label"]

    label2 = vertices[
        vertex2
    ]["label"]

    print(
        f"Created edge "
        f"{label1} -- {label2}"
    )

    print(
        "Existing walk cleared "
        "because the graph changed."
    )


# =========================================================
# WALK FUNCTIONS
# =========================================================

def add_vertex_to_walk(vertex_index):

    # ---------------------------------
    # First vertex
    # ---------------------------------

    if len(walk) == 0:

        walk.append(
            vertex_index
        )

        print(
            f"Walk started at "
            f"{vertices[vertex_index]['label']}"
        )

        return

    # ---------------------------------
    # Every next vertex must have edge
    # ---------------------------------

    previous_vertex = walk[-1]

    if vertices_are_connected(
        previous_vertex,
        vertex_index
    ):

        walk.append(
            vertex_index
        )

        print(
            "Walk: "
            +
            " -> ".join(
                vertices[index]["label"]
                for index in walk
            )
        )

    else:

        print(
            f"INVALID WALK MOVE: "
            f"No edge between "
            f"{vertices[previous_vertex]['label']} "
            f"and "
            f"{vertices[vertex_index]['label']}"
        )


# =========================================================
# ALGORITHM 1 CONTROLS
# =========================================================

def start_algorithm():

    global algorithm_path
    global algorithm_closed
    global algorithm_phase
    global algorithm_message

    if len(walk) == 0:

        algorithm_path = []

        algorithm_closed = None

        algorithm_phase = "IDLE"

        algorithm_message = (
            "Build a walk first."
        )

        print(
            "Cannot run Algorithm 1: "
            "no walk exists."
        )

        return

    # ---------------------------------
    # P := W
    # ---------------------------------

    algorithm_path = [

        vertices[index]["label"]

        for index in walk
    ]

    algorithm_closed = None

    algorithm_phase = "CHECK"

    algorithm_message = (
        "P := W    Press SPACE to continue."
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
    global algorithm_closed
    global algorithm_phase
    global algorithm_message

    if len(algorithm_path) == 0:

        algorithm_message = (
            "No walk loaded."
        )

        return


    # =====================================================
    # CHECK WHETHER P IS A PATH OR CYCLE
    # =====================================================

    if algorithm_phase == "CHECK":

        # ---------------------------------
        # Stop if P is a path
        # ---------------------------------

        if is_path(
            algorithm_path
        ):

            algorithm_phase = (
                "FINISHED"
            )

            algorithm_closed = None

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
        # Stop if P is a cycle
        # ---------------------------------

        if is_cycle(
            algorithm_path
        ):

            algorithm_phase = (
                "FINISHED"
            )

            algorithm_closed = None

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
        # Find shortest closed subwalk
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

            algorithm_message = (
                "No closed subwalk found."
            )

            return

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
                algorithm_closed["walk"]
            )
        )


    # =====================================================
    # REMOVE C
    # =====================================================

    elif algorithm_phase == "SHOW_C":

        algorithm_path = (
            remove_closed_subwalk(
                algorithm_path,
                algorithm_closed["start"],
                algorithm_closed["end"]
            )
        )

        algorithm_closed = None

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
# ALGORITHM 2: BIPARTITE CHECK
# =========================================================

def build_adjacency_graph():

    graph = {}

    for index, vertex in enumerate(
        vertices
    ):

        label = vertex["label"]

        graph[label] = []

        for neighbor in range(
            len(vertices)
        ):

            if edge_exists(
                index,
                neighbor
            ):

                graph[label].append(
                    vertices[neighbor]["label"]
                )

    return graph


def check_current_graph_bipartite():

    global bipartite_colors
    global bipartite_message
    global bipartite_message_color
    global bipartite_message_until

    graph = build_adjacency_graph()

    result, coloring = (
        get_bipartite_coloring(
            graph
        )
    )

    if result:

        # ---------------------------------
        # Save the two-set coloring
        # ---------------------------------

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

        # ---------------------------------
        # IMPORTANT:
        # No coloring for failed graph
        # ---------------------------------

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

    # Popup stays visible for 3 seconds
    bipartite_message_until = (
        pygame.time.get_ticks()
        + 3000
    )


# =========================================================
# RESET GRAPH
# =========================================================

def reset_graph():

    global selected_vertex
    global next_vertex_number

    vertices.clear()

    edges.clear()

    walk.clear()

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

    # ---------------------------------
    # Algorithm 1
    # ---------------------------------

    if new_mode == ALGORITHM_MODE:

        start_algorithm()

    # ---------------------------------
    # Algorithm 2
    # ---------------------------------

    elif (
        new_mode
        ==
        CHECK_BIPARTITE_MODE
    ):

        check_current_graph_bipartite()


# =========================================================
# DRAW NORMAL EDGES
# =========================================================

def draw_edges():

    for vertex1, vertex2 in edges:

        start = (
            vertices[vertex1]["x"],
            vertices[vertex1]["y"]
        )

        end = (
            vertices[vertex2]["x"],
            vertices[vertex2]["y"]
        )

        pygame.draw.line(
            screen,
            EDGE_COLOR,
            start,
            end,
            4
        )


# =========================================================
# DRAW WALK
# =========================================================

def draw_walk():

    if len(walk) == 0:

        return

    # ---------------------------------
    # Walk edges
    # ---------------------------------

    for index in range(
        len(walk) - 1
    ):

        vertex1 = walk[index]

        vertex2 = walk[
            index + 1
        ]

        start = (
            vertices[vertex1]["x"],
            vertices[vertex1]["y"]
        )

        end = (
            vertices[vertex2]["x"],
            vertices[vertex2]["y"]
        )

        pygame.draw.line(
            screen,
            WALK_EDGE_COLOR,
            start,
            end,
            7
        )

    # ---------------------------------
    # Walk vertices
    # ---------------------------------

    for vertex_index in walk:

        vertex = vertices[
            vertex_index
        ]

        pygame.draw.circle(
            screen,
            WALK_VERTEX_COLOR,
            (
                vertex["x"],
                vertex["y"]
            ),
            VERTEX_RADIUS + 5,
            4
        )


# =========================================================
# DRAW CURRENT ALGORITHM PATH P
# =========================================================

def draw_algorithm_path():

    if (
        current_mode
        !=
        ALGORITHM_MODE
    ):

        return

    if len(algorithm_path) < 2:

        return

    for index in range(
        len(algorithm_path) - 1
    ):

        label1 = algorithm_path[
            index
        ]

        label2 = algorithm_path[
            index + 1
        ]

        vertex1 = (
            get_vertex_index_by_label(
                label1
            )
        )

        vertex2 = (
            get_vertex_index_by_label(
                label2
            )
        )

        if (
            vertex1 is None
            or
            vertex2 is None
        ):

            continue

        start = (
            vertices[vertex1]["x"],
            vertices[vertex1]["y"]
        )

        end = (
            vertices[vertex2]["x"],
            vertices[vertex2]["y"]
        )

        pygame.draw.line(
            screen,
            ALGORITHM_PATH_COLOR,
            start,
            end,
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

    closed_walk = (
        algorithm_closed["walk"]
    )

    for index in range(
        len(closed_walk) - 1
    ):

        label1 = closed_walk[
            index
        ]

        label2 = closed_walk[
            index + 1
        ]

        vertex1 = (
            get_vertex_index_by_label(
                label1
            )
        )

        vertex2 = (
            get_vertex_index_by_label(
                label2
            )
        )

        if (
            vertex1 is None
            or
            vertex2 is None
        ):

            continue

        start = (
            vertices[vertex1]["x"],
            vertices[vertex1]["y"]
        )

        end = (
            vertices[vertex2]["x"],
            vertices[vertex2]["y"]
        )

        pygame.draw.line(
            screen,
            CLOSED_WALK_COLOR,
            start,
            end,
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

        label = vertex["label"]


        # ---------------------------------
        # Determine fill color
        # ---------------------------------

        fill_color = (
            VERTEX_COLOR
        )

        if (
            current_mode
            ==
            CHECK_BIPARTITE_MODE
        ):

            if label in bipartite_colors:

                if (
                    bipartite_colors[label]
                    == 0
                ):

                    fill_color = (
                        BIPARTITE_COLOR_0
                    )

                else:

                    fill_color = (
                        BIPARTITE_COLOR_1
                    )


        # ---------------------------------
        # Draw vertex fill
        # ---------------------------------

        pygame.draw.circle(
            screen,
            fill_color,
            (x, y),
            VERTEX_RADIUS
        )


        # ---------------------------------
        # Border
        # ---------------------------------

        if index == selected_vertex:

            border_color = (
                SELECTED_COLOR
            )

            border_width = 5

        elif (
            index == hovered_vertex
            and
            current_mode == EDIT_MODE
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
# DRAW MODE DISPLAY
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


    # ---------------------------------
    # Edit Mode
    # ---------------------------------

    if current_mode == EDIT_MODE:

        instructions = (
            "1 Edit   2 Walk   3 Algorithm"
            "   |   Hover + X Delete"
            "   |   Right Click Menu"
        )


    # ---------------------------------
    # Walk Mode
    # ---------------------------------

    elif current_mode == WALK_MODE:

        instructions = (
            "Click vertices to build W"
            "   |   Backspace Undo"
            "   |   C Clear"
            "   |   1 Edit   3 Algorithm"
        )


    # ---------------------------------
    # Algorithm 1 Mode
    # ---------------------------------

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


    # ---------------------------------
    # Bipartite Mode
    # ---------------------------------

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
# DRAW WALK DISPLAY
# =========================================================

def draw_walk_display():

    if len(walk) == 0:

        walk_string = (
            "W = empty"
        )

    else:

        labels = [

            vertices[index]["label"]

            for index in walk
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
# DRAW ALGORITHM 1 DISPLAY
# =========================================================

def draw_algorithm_display():

    if (
        current_mode
        !=
        ALGORITHM_MODE
    ):

        return


    # ---------------------------------
    # P
    # ---------------------------------

    if len(algorithm_path) > 0:

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


    rendered_path = ui_font.render(
        path_text,
        True,
        WHITE
    )

    screen.blit(
        rendered_path,
        (15, 105)
    )


    # ---------------------------------
    # C
    # ---------------------------------

    if algorithm_closed is not None:

        closed_text = (
            "C = "
            +
            " -> ".join(
                algorithm_closed["walk"]
            )
        )

    else:

        closed_text = (
            "C = none"
        )


    rendered_closed = ui_font.render(
        closed_text,
        True,
        WHITE
    )

    screen.blit(
        rendered_closed,
        (15, 135)
    )


    # ---------------------------------
    # Explanation
    # ---------------------------------

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
# DRAW BIPARTITE POPUP
# =========================================================

def draw_bipartite_popup():

    if bipartite_message == "":

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


    # ---------------------------------
    # Popup background
    # ---------------------------------

    pygame.draw.rect(
        screen,
        POPUP_BACKGROUND,
        popup_rect
    )


    # ---------------------------------
    # Popup border
    # ---------------------------------

    pygame.draw.rect(
        screen,
        POPUP_BORDER,
        popup_rect,
        2
    )


    # ---------------------------------
    # Popup text
    # ---------------------------------

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

def open_context_menu(x, y):

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


    # ---------------------------------
    # Background
    # ---------------------------------

    pygame.draw.rect(
        screen,
        MENU_BACKGROUND,
        (
            menu_x,
            menu_y,
            MENU_WIDTH,
            total_height
        )
    )


    # ---------------------------------
    # Border
    # ---------------------------------

    pygame.draw.rect(
        screen,
        MENU_BORDER,
        (
            menu_x,
            menu_y,
            MENU_WIDTH,
            total_height
        ),
        2
    )


    # ---------------------------------
    # Menu items
    # ---------------------------------

    for index, item in enumerate(
        menu_items
    ):

        item_y = (
            menu_y
            +
            index * MENU_ITEM_HEIGHT
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
                item_y + 10
            )
        )


# =========================================================
# HANDLE CONTEXT MENU CLICK
# =========================================================

def handle_menu_click(x, y):

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
            index * MENU_ITEM_HEIGHT,
            MENU_WIDTH,
            MENU_ITEM_HEIGHT
        )


        if item_rect.collidepoint(
            x,
            y
        ):


            if item == "EDIT GRAPH":

                set_mode(
                    EDIT_MODE
                )


            elif item == "BUILD WALK":

                set_mode(
                    WALK_MODE
                )


            elif item == "RUN ALGORITHM":

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


            elif item == "RESET GRAPH":

                reset_graph()

                menu_open = False


            return True


    # Clicked outside menu
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
            # 1 = Edit Mode
            # ---------------------------------

            if event.key == pygame.K_1:

                set_mode(
                    EDIT_MODE
                )


            # ---------------------------------
            # 2 = Walk Mode
            # ---------------------------------

            elif event.key == pygame.K_2:

                set_mode(
                    WALK_MODE
                )


            # ---------------------------------
            # 3 = Algorithm 1 Mode
            # ---------------------------------

            elif event.key == pygame.K_3:

                set_mode(
                    ALGORITHM_MODE
                )


            # ---------------------------------
            # SPACE = next Algorithm 1 step
            # ---------------------------------

            elif event.key == pygame.K_SPACE:

                if (
                    current_mode
                    ==
                    ALGORITHM_MODE
                ):

                    next_algorithm_step()


            # ---------------------------------
            # X = delete hovered vertex
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


            # ---------------------------------
            # BACKSPACE = undo walk step
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
                    and
                    len(walk) > 0
                ):

                    removed_vertex = (
                        walk.pop()
                    )

                    reset_algorithm_state()

                    print(
                        f"Removed "
                        f"{vertices[removed_vertex]['label']} "
                        f"from walk."
                    )


            # ---------------------------------
            # C = clear walk
            # ---------------------------------

            elif event.key == pygame.K_c:

                if (
                    current_mode
                    ==
                    WALK_MODE
                ):

                    walk.clear()

                    reset_algorithm_state()

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


                # ---------------------------------
                # Context menu gets priority
                # ---------------------------------

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


                    # -----------------------------
                    # Clicked existing vertex
                    # -----------------------------

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

                            toggle_edge(
                                selected_vertex,
                                clicked_vertex
                            )

                            selected_vertex = None


                    # -----------------------------
                    # Clicked empty space
                    # -----------------------------

                    else:

                        selected_vertex = None

                        add_vertex(
                            mouse_x,
                            mouse_y
                        )


                # =================================
                # BUILD WALK MODE
                # =================================

                elif (
                    current_mode
                    ==
                    WALK_MODE
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

                        add_vertex_to_walk(
                            clicked_vertex
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

                    # Algorithm 1 uses SPACE
                    pass


                # =================================
                # BIPARTITE MODE
                # =================================

                elif (
                    current_mode
                    ==
                    CHECK_BIPARTITE_MODE
                ):

                    # Result is calculated as soon
                    # as this mode is selected.
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
    # Normal walk visualization
    # ---------------------------------

    if (
        current_mode
        !=
        ALGORITHM_MODE
        and
        current_mode
        !=
        CHECK_BIPARTITE_MODE
    ):

        draw_walk()


    # ---------------------------------
    # Algorithm 1 visualization
    # ---------------------------------

    draw_algorithm_path()

    draw_closed_subwalk()


    # ---------------------------------
    # Vertices
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


    # ---------------------------------
    # Bipartite popup
    # ---------------------------------

    draw_bipartite_popup()


    # ---------------------------------
    # Context menu always last
    # ---------------------------------

    draw_context_menu()


    pygame.display.flip()


    clock.tick(
        60
    )


pygame.quit()