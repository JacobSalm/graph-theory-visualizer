import pygame


# -------------------------
# Setup
# -------------------------

pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(
    "Graph Theory Visualizer"
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    None,
    30
)


# -------------------------
# Colors
# -------------------------

BACKGROUND = (30, 30, 30)

GRID_COLOR = (50, 50, 50)

VERTEX_COLOR = (230, 230, 230)

TEXT_COLOR = (20, 20, 20)

BORDER_COLOR = (255, 255, 255)

EDGE_COLOR = (180, 180, 180)

SELECTED_COLOR = (255, 220, 0)


# -------------------------
# Settings
# -------------------------

GRID_SIZE = 50

VERTEX_RADIUS = 22


# -------------------------
# Graph data
# -------------------------

vertices = []

edges = []

selected_vertex = None


# -------------------------
# Helper functions
# -------------------------

def get_vertex_label(index):

    # First 26 vertices:
    # a, b, c, ... z
    if index < 26:
        return chr(ord("a") + index)

    # Next 26 vertices:
    # A, B, C, ... Z
    if index < 52:
        return chr(ord("A") + (index - 26))

    # Backup if more than 52 vertices
    return f"V{index + 1}"


def snap_to_grid(value):

    return round(
        value / GRID_SIZE
    ) * GRID_SIZE


def position_is_valid(x, y):

    for vertex in vertices:

        if (
            vertex["x"] == x
            and vertex["y"] == y
        ):
            return False

    return True


def get_vertex_at_position(x, y):

    for index, vertex in enumerate(vertices):

        dx = x - vertex["x"]
        dy = y - vertex["y"]

        distance_squared = (
            dx * dx + dy * dy
        )

        if distance_squared <= VERTEX_RADIUS ** 2:
            return index

    return None


def edge_exists(vertex1, vertex2):

    for edge in edges:

        a, b = edge

        if (
            (a == vertex1 and b == vertex2)
            or
            (a == vertex2 and b == vertex1)
        ):
            return True

    return False


def add_vertex(x, y):

    x = snap_to_grid(x)
    y = snap_to_grid(y)

    if not position_is_valid(x, y):

        print(
            "A vertex already exists here."
        )

        return

    label = get_vertex_label(
        len(vertices)
    )

    vertex = {
        "x": x,
        "y": y,
        "label": label
    }

    vertices.append(vertex)

    print(
        f"Created vertex {label} "
        f"at ({x}, {y})"
    )


def toggle_edge(vertex1, vertex2):

    # No self-loop
    if vertex1 == vertex2:

        print(
            "Cannot connect a vertex "
            "to itself."
        )

        return

    # -------------------------
    # If edge exists, remove it
    # -------------------------

    for edge in edges:

        a, b = edge

        if (
            (a == vertex1 and b == vertex2)
            or
            (a == vertex2 and b == vertex1)
        ):

            edges.remove(edge)

            label1 = vertices[vertex1]["label"]
            label2 = vertices[vertex2]["label"]

            print(
                f"Removed edge "
                f"{label1} -- {label2}"
            )

            return

    # -------------------------
    # Otherwise create the edge
    # -------------------------

    edges.append(
        (vertex1, vertex2)
    )

    label1 = vertices[vertex1]["label"]
    label2 = vertices[vertex2]["label"]

    print(
        f"Created edge "
        f"{label1} -- {label2}"
    )


# -------------------------
# Drawing
# -------------------------

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


def draw_vertices():

    for index, vertex in enumerate(vertices):

        x = vertex["x"]
        y = vertex["y"]
        label = vertex["label"]

        pygame.draw.circle(
            screen,
            VERTEX_COLOR,
            (x, y),
            VERTEX_RADIUS
        )

        # Selected vertex gets yellow border
        if index == selected_vertex:

            border_color = SELECTED_COLOR
            border_width = 5

        else:

            border_color = BORDER_COLOR
            border_width = 2

        pygame.draw.circle(
            screen,
            border_color,
            (x, y),
            VERTEX_RADIUS,
            border_width
        )

        text = font.render(
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


# -------------------------
# Main loop
# -------------------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # -------------------------
        # Mouse clicks
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Left click
            if event.button == 1:

                mouse_x, mouse_y = event.pos

                clicked_vertex = (
                    get_vertex_at_position(
                        mouse_x,
                        mouse_y
                    )
                )


                # -------------------------
                # Clicked a vertex
                # -------------------------

                if clicked_vertex is not None:

                    if selected_vertex is None:

                        selected_vertex = clicked_vertex

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


                # -------------------------
                # Clicked empty space
                # -------------------------

                else:

                    selected_vertex = None

                    add_vertex(
                        mouse_x,
                        mouse_y
                    )


            # -------------------------
            # Right click cancels selection
            # -------------------------

            elif event.button == 3:

                selected_vertex = None

                print(
                    "Selection cancelled."
                )


    # -------------------------
    # Draw everything
    # -------------------------

    screen.fill(
        BACKGROUND
    )

    draw_grid()

    # Draw edges before vertices
    draw_edges()

    draw_vertices()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()