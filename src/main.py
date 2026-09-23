# =========================================================
# GRAPH THEORY VISUALIZER
# =========================================================

import pygame

from graph_model import GraphModel

from walk_system import WalkSystem

from rendering import Renderer

from ui import (
    UI,
    EDIT_MODE,
    WALK_MODE,
    ALGORITHM_MODE,
    BIPARTITE_MODE,
    RESET_ACTION
)

from algorithms.algorithm1 import (
    Algorithm1Session
)

from algorithms.bipartite import (
    get_bipartite_coloring
)


# =========================================================
# SETUP
# =========================================================

pygame.init()

WIDTH = 1200

HEIGHT = 700

GRID_SIZE = 50

VERTEX_RADIUS = 22


screen = pygame.display.set_mode(
    (
        WIDTH,
        HEIGHT
    )
)

pygame.display.set_caption(
    "Graph Theory Visualizer"
)

clock = pygame.time.Clock()


# =========================================================
# SYSTEMS
# =========================================================

graph = GraphModel(
    grid_size=GRID_SIZE,
    max_parallel_edges=4
)

walk = WalkSystem()

renderer = Renderer(
    screen,
    WIDTH,
    HEIGHT,
    grid_size=GRID_SIZE,
    vertex_radius=VERTEX_RADIUS
)

ui = UI(
    screen,
    WIDTH,
    HEIGHT
)

algorithm1 = (
    Algorithm1Session()
)


# =========================================================
# APP STATE
# =========================================================

current_mode = (
    EDIT_MODE
)

selected_vertex = None

bipartite_colors = {}


# =========================================================
# RESET DERIVED DATA
# =========================================================

def graph_changed():

    global bipartite_colors

    walk.clear()

    algorithm1.reset()

    bipartite_colors = {}

    ui.clear_popup()


# =========================================================
# PRINT WALK
# =========================================================

def print_walk():

    labels = (
        walk.get_labels(
            graph
        )
    )

    if labels:

        print(
            "Walk: "
            +
            " -> ".join(
                labels
            )
        )


# =========================================================
# RESET GRAPH
# =========================================================

def reset_graph():

    global selected_vertex

    global bipartite_colors

    graph.reset()

    walk.clear()

    algorithm1.reset()

    bipartite_colors = {}

    selected_vertex = None

    ui.clear_popup()

    print(
        "Graph reset."
    )


# =========================================================
# CHECK BIPARTITE
# =========================================================

def run_bipartite_check():

    global bipartite_colors

    adjacency = (
        graph.to_adjacency_labels()
    )

    result, coloring = (
        get_bipartite_coloring(
            adjacency
        )
    )

    if result:

        bipartite_colors = (
            coloring
        )

        ui.show_popup(
            "Graph is BIPARTITE",
            success=True
        )

        print(
            "The graph IS bipartite."
        )

    else:

        # No coloring if graph fails.

        bipartite_colors = {}

        ui.show_popup(
            "Graph is NOT bipartite",
            success=False
        )

        print(
            "The graph is NOT bipartite."
        )


# =========================================================
# START ALGORITHM 1
# =========================================================

def start_algorithm1():

    labels = (
        walk.get_labels(
            graph
        )
    )

    started = (
        algorithm1.start(
            labels,
            walk.edge_ids
        )
    )

    if started:

        print(
            "Algorithm 1 started."
        )

        print(
            "P = "
            +
            " -> ".join(
                algorithm1.path
            )
        )

    else:

        print(
            "Cannot run Algorithm 1: "
            "build a walk first."
        )


# =========================================================
# MODE CONTROL
# =========================================================

def set_mode(new_mode):

    global current_mode

    global selected_vertex

    current_mode = (
        new_mode
    )

    selected_vertex = None

    ui.close_menu()

    print(
        f"Mode changed to: "
        f"{current_mode}"
    )

    if (
        current_mode
        ==
        ALGORITHM_MODE
    ):

        start_algorithm1()

    elif (
        current_mode
        ==
        BIPARTITE_MODE
    ):

        run_bipartite_check()


# =========================================================
# MENU ACTION
# =========================================================

def handle_menu_action(
    action
):

    if action is None:

        return

    if (
        action
        ==
        RESET_ACTION
    ):

        reset_graph()

        return

    set_mode(
        action
    )


# =========================================================
# ADD VERTEX
# =========================================================

def create_vertex(
    x,
    y
):

    vertex_id, message = (
        graph.add_vertex(
            x,
            y
        )
    )

    print(
        message
    )

    if vertex_id is not None:

        graph_changed()


# =========================================================
# ADD EDGE
# =========================================================

def create_edge(
    vertex1,
    vertex2
):

    edge_id, message = (
        graph.add_edge(
            vertex1,
            vertex2
        )
    )

    print(
        message
    )

    if edge_id is not None:

        graph_changed()


# =========================================================
# DELETE VERTEX
# =========================================================

def remove_vertex(
    vertex_id
):

    message = (
        graph.delete_vertex(
            vertex_id
        )
    )

    if message is None:

        return

    print(
        message
    )

    graph_changed()


# =========================================================
# DELETE EDGE
# =========================================================

def remove_edge(
    edge_id
):

    message = (
        graph.delete_edge(
            edge_id
        )
    )

    if message is None:

        return

    print(
        message
    )

    graph_changed()


# =========================================================
# WALK VERTEX CLICK
# =========================================================

def walk_vertex_click(
    vertex_id
):

    success, message = (
        walk.add_vertex(
            graph,
            vertex_id
        )
    )

    print(
        message
    )

    if success:

        print_walk()

        algorithm1.reset()


# =========================================================
# WALK EDGE CLICK
# =========================================================

def walk_edge_click(
    edge_id
):

    success, message = (
        walk.add_edge(
            graph,
            edge_id
        )
    )

    print(
        message
    )

    if success:

        print_walk()

        algorithm1.reset()


# =========================================================
# MAIN LOOP
# =========================================================

running = True


while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():


        # =================================================
        # QUIT
        # =================================================

        if (
            event.type
            ==
            pygame.QUIT
        ):

            running = False


        # =================================================
        # KEYBOARD
        # =================================================

        elif (
            event.type
            ==
            pygame.KEYDOWN
        ):


            # ---------------------------------------------
            # MODE 1
            # ---------------------------------------------

            if (
                event.key
                ==
                pygame.K_1
            ):

                set_mode(
                    EDIT_MODE
                )


            # ---------------------------------------------
            # MODE 2
            # ---------------------------------------------

            elif (
                event.key
                ==
                pygame.K_2
            ):

                set_mode(
                    WALK_MODE
                )


            # ---------------------------------------------
            # MODE 3
            # ---------------------------------------------

            elif (
                event.key
                ==
                pygame.K_3
            ):

                set_mode(
                    ALGORITHM_MODE
                )


            # ---------------------------------------------
            # SPACE
            # ---------------------------------------------

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

                    algorithm1.step()

                    print(
                        algorithm1.message
                    )


            # ---------------------------------------------
            # DELETE WITH X
            # ---------------------------------------------

            elif (
                event.key
                ==
                pygame.K_x
            ):

                if (
                    current_mode
                    ==
                    EDIT_MODE
                ):

                    mouse_x, mouse_y = (
                        pygame.mouse.get_pos()
                    )

                    hovered_vertex = (
                        graph.vertex_at_position(
                            mouse_x,
                            mouse_y,
                            VERTEX_RADIUS
                        )
                    )

                    # Vertex always gets priority.

                    if (
                        hovered_vertex
                        is not None
                    ):

                        remove_vertex(
                            hovered_vertex
                        )

                    else:

                        hovered_edge = (
                            renderer.get_hovered_edge(
                                graph,
                                mouse_x,
                                mouse_y
                            )
                        )

                        if (
                            hovered_edge
                            is not None
                        ):

                            remove_edge(
                                hovered_edge
                            )


            # ---------------------------------------------
            # WALK UNDO
            # ---------------------------------------------

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

                    removed = (
                        walk.undo()
                    )

                    if (
                        removed
                        is not None
                    ):

                        algorithm1.reset()

                        print(
                            "Removed last "
                            "walk step."
                        )


            # ---------------------------------------------
            # CLEAR WALK
            # ---------------------------------------------

            elif (
                event.key
                ==
                pygame.K_c
            ):

                if (
                    current_mode
                    ==
                    WALK_MODE
                ):

                    walk.clear()

                    algorithm1.reset()

                    print(
                        "Walk cleared."
                    )


            # ---------------------------------------------
            # ESC
            # ---------------------------------------------

            elif (
                event.key
                ==
                pygame.K_ESCAPE
            ):

                selected_vertex = None

                ui.close_menu()


        # =================================================
        # MOUSE
        # =================================================

        elif (
            event.type
            ==
            pygame.MOUSEBUTTONDOWN
        ):

            mouse_x, mouse_y = (
                event.pos
            )


            # ---------------------------------------------
            # RIGHT CLICK
            # ---------------------------------------------

            if event.button == 3:

                ui.open_menu(
                    mouse_x,
                    mouse_y
                )

                continue


            # ---------------------------------------------
            # LEFT CLICK
            # ---------------------------------------------

            if event.button != 1:

                continue


            # ---------------------------------------------
            # MENU HAS PRIORITY
            # ---------------------------------------------

            if ui.menu_open:

                action = (
                    ui.handle_menu_click(
                        mouse_x,
                        mouse_y
                    )
                )

                handle_menu_action(
                    action
                )

                continue


            # =================================================
            # EDIT MODE
            # =================================================

            if (
                current_mode
                ==
                EDIT_MODE
            ):

                clicked_vertex = (
                    graph.vertex_at_position(
                        mouse_x,
                        mouse_y,
                        VERTEX_RADIUS
                    )
                )

                # -----------------------------------------
                # CLICKED VERTEX
                # -----------------------------------------

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

                        label = (
                            graph.get_vertex_label_by_id(
                                selected_vertex
                            )
                        )

                        print(
                            f"Selected vertex "
                            f"{label}"
                        )

                    else:

                        create_edge(
                            selected_vertex,
                            clicked_vertex
                        )

                        selected_vertex = None


                # -----------------------------------------
                # EMPTY SPACE
                # -----------------------------------------

                else:

                    selected_vertex = None

                    create_vertex(
                        mouse_x,
                        mouse_y
                    )


            # =================================================
            # WALK MODE
            # =================================================

            elif (
                current_mode
                ==
                WALK_MODE
            ):

                # Vertex has priority.

                clicked_vertex = (
                    graph.vertex_at_position(
                        mouse_x,
                        mouse_y,
                        VERTEX_RADIUS
                    )
                )

                if (
                    clicked_vertex
                    is not None
                ):

                    walk_vertex_click(
                        clicked_vertex
                    )

                else:

                    clicked_edge = (
                        renderer.get_hovered_edge(
                            graph,
                            mouse_x,
                            mouse_y
                        )
                    )

                    if (
                        clicked_edge
                        is not None
                    ):

                        walk_edge_click(
                            clicked_edge
                        )


    # =====================================================
    # CURRENT HOVER
    # =====================================================

    mouse_x, mouse_y = (
        pygame.mouse.get_pos()
    )

    hovered_vertex = None

    hovered_edge = None


    if (
        current_mode
        in
        (
            EDIT_MODE,
            WALK_MODE
        )
    ):

        hovered_vertex = (
            graph.vertex_at_position(
                mouse_x,
                mouse_y,
                VERTEX_RADIUS
            )
        )


    # Vertex takes priority over edge.

    if (
        hovered_vertex
        is None
        and
        current_mode
        in
        (
            EDIT_MODE,
            WALK_MODE
        )
    ):

        candidate_edge = (
            renderer.get_hovered_edge(
                graph,
                mouse_x,
                mouse_y
            )
        )

        if (
            current_mode
            ==
            EDIT_MODE
        ):

            hovered_edge = (
                candidate_edge
            )

        elif (
            current_mode
            ==
            WALK_MODE
            and
            candidate_edge
            is not None
            and
            not walk.is_empty()
            and
            graph.edge_is_incident_to_vertex(
                candidate_edge,
                walk.current_vertex()
            )
        ):

            # Only glow an edge in Walk Mode
            # when it is actually usable from
            # the current walk position.

            hovered_edge = (
                candidate_edge
            )


    # =====================================================
    # DRAW
    # =====================================================

    renderer.clear()

    renderer.draw_grid()


    # -----------------------------------------------------
    # BASE GRAPH
    # -----------------------------------------------------

    renderer.draw_edges(
        graph,
        hovered_edge
    )


    # -----------------------------------------------------
    # WALK
    # -----------------------------------------------------

    if (
        current_mode
        not in
        (
            ALGORITHM_MODE,
            BIPARTITE_MODE
        )
    ):

        renderer.draw_walk(
            graph,
            walk
        )


    # -----------------------------------------------------
    # ALGORITHM 1
    # -----------------------------------------------------

    if (
        current_mode
        ==
        ALGORITHM_MODE
    ):

        renderer.draw_algorithm(
            graph,
            algorithm1
        )


    # -----------------------------------------------------
    # VERTICES
    # -----------------------------------------------------

    if (
        current_mode
        ==
        BIPARTITE_MODE
    ):

        colors_to_draw = (
            bipartite_colors
        )

    else:

        colors_to_draw = {}


    renderer.draw_vertices(
        graph,
        selected_vertex=selected_vertex,
        hovered_vertex=hovered_vertex,
        bipartite_colors=colors_to_draw
    )


    # =====================================================
    # UI
    # =====================================================

    ui.draw_mode(
        current_mode
    )


    if (
        current_mode
        !=
        BIPARTITE_MODE
    ):

        ui.draw_walk(
            walk.get_labels(
                graph
            )
        )


    if (
        current_mode
        ==
        ALGORITHM_MODE
    ):

        ui.draw_algorithm(
            algorithm1
        )


    ui.draw_popup()

    ui.draw_context_menu()


    # =====================================================
    # FRAME
    # =====================================================

    pygame.display.flip()

    clock.tick(
        60
    )


pygame.quit()