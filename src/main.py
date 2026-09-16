import pygame


# -------------------------
# Setup
# -------------------------

pygame.init()

WIDTH = 900
HEIGHT = 600

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

VERTEX_COLOR = (230, 230, 230)

TEXT_COLOR = (20, 20, 20)

BORDER_COLOR = (255, 255, 255)


# -------------------------
# Graph data
# -------------------------

vertices = []

VERTEX_RADIUS = 22


# -------------------------
# Helper functions
# -------------------------

def get_vertex_label(index):
    return chr(ord("A") + index)


def draw_vertices():

    for vertex in vertices:

        x = vertex["x"]
        y = vertex["y"]
        label = vertex["label"]

        # Draw circle
        pygame.draw.circle(
            screen,
            VERTEX_COLOR,
            (x, y),
            VERTEX_RADIUS
        )

        # Draw border
        pygame.draw.circle(
            screen,
            BORDER_COLOR,
            (x, y),
            VERTEX_RADIUS,
            2
        )

        # Draw label
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


def add_vertex(x, y):

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


# -------------------------
# Main loop
# -------------------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Left mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_x, mouse_y = event.pos

                add_vertex(
                    mouse_x,
                    mouse_y
                )

    # Clear screen
    screen.fill(BACKGROUND)

    # Draw graph
    draw_vertices()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()