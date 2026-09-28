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
    EULER_MODE,
    RESET_ACTION
)

from algorithms.algorithm1 import (
    Algorithm1Session
)

from algorithms.bipartite import (
    get_bipartite_coloring
)

from algorithms.euler import (
    find_euler_cycle
)


# =========================================================
# SETUP
# =========================================================

pygame.init()

WIDTH = 1200

HEIGHT = 700

GRID_SIZE = 50

VERTEX_RADIUS = 22

DOUBLE_CLICK_TIME = 350


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


# Holds:

# {
#     "vertices": [...],
#     "edges": [...]
# }

euler_result = None


# =========================================================
# RENAME STATE
# =========================================================

last_vertex_click = None

last_vertex_click_time = 0

renaming_vertex = None


# =========================================================
# HELPERS
# =========================================================

def get_names(
    vertex_ids
):

    return [

        graph.get_vertex_label_by_id(
            vertex_id
        )

        for vertex_id
        in vertex_ids
    ]


# =========================================================
# GRAPH CHANGED
# =========================================================

def graph_changed():

    global bipartite_colors

    global euler_result


    # Structural graph changes make
    # old walk edge IDs invalid.

    walk.clear()

    algorithm1.reset()

    bipartite_colors = {}

    euler_result = None

    ui.clear_popup()


# =========================================================
# PRINT WALK
# =========================================================

def print_walk():

    names = (
        walk.get_labels(
            graph
        )
    )


    if names:

        print(
            "Walk: "
            +
            " -> ".join(
                names
            )
        )


# =========================================================
# RESET GRAPH
# =========================================================

def reset_graph():

    global selected_vertex

    global bipartite_colors

    global euler_result

    global last_vertex_click


    graph.reset()

    walk.clear()

    algorithm1.reset()


    bipartite_colors = {}

    euler_result = None


    selected_vertex = None

    last_vertex_click = None


    ui.clear_popup()


    print(
        "Graph reset."
    )


# =========================================================
# BIPARTITE CHECK
# =========================================================

def run_bipartite_check():

    global bipartite_colors


    adjacency = (
        graph.to_adjacency_ids()
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

        bipartite_colors = {}


        ui.show_popup(
            "Graph is NOT bipartite",
            success=False
        )


        print(
            "The graph is NOT bipartite."
        )


# =========================================================
# EULER CHECK
# =========================================================

def run_euler_check():

    global euler_result


    result = (
        find_euler_cycle(
            graph
        )
    )


    # ---------------------------------
    # NOT EULERIAN
    # ---------------------------------

    if result is None:

        euler_result = None


        ui.show_popup(
            "Graph is NOT EULERIAN",
            success=False
        )


        print(
            "The graph is NOT Eulerian."
        )


        return


    # ---------------------------------
    # EULERIAN
    # ---------------------------------

    euler_result = result


    ui.show_popup(
        "Graph is EULERIAN",
        success=True
    )


    print(
        "The graph IS Eulerian."
    )


    names = get_names(
        euler_result[
            "vertices"
        ]
    )


    if names:

        print(
            "Euler cycle:"
        )

        print(
            " -> ".join(
                names
            )
        )


# =========================================================
# ALGORITHM 1
# =========================================================

def start_algorithm1():

    started = (
        algorithm1.start(
            walk.vertex_ids,
            walk.edge_ids
        )
    )


    if started:

        names = get_names(
            algorithm1.path
        )


        print(
            "Algorithm 1 started."
        )


        print(
            "P = "
            +
            " -> ".join(
                names
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

def set_mode(
    new_mode
):

    global current_mode

    global selected_vertex

    global last_vertex_click


    current_mode = (
        new_mode
    )


    selected_vertex = None

    last_vertex_click = None


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


    elif (
        current_mode
        ==
        EULER_MODE
    ):

        run_euler_check()


# =========================================================
# MENU
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
# CREATE VERTEX
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


    if (
        vertex_id
        is not None
    ):

        graph_changed()


# =========================================================
# CREATE EDGE
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


    if (
        edge_id
        is not None
    ):

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
# WALK
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
# RENAME
# =========================================================

def begin_vertex_rename(
    vertex_id
):

    global renaming_vertex

    global selected_vertex


    renaming_vertex = (
        vertex_id
    )


    selected_vertex = None


    vertex = graph.get_vertex(
        vertex_id
    )


    if vertex is None:

        return


    ui.open_text_input(
        "Rename Vertex",
        vertex["label"]
    )


def save_vertex_rename(
    new_name
):

    global renaming_vertex


    if (
        renaming_vertex
        is None
    ):

        return


    success, message = (
        graph.rename_vertex(
            renaming_vertex,
            new_name
        )
    )


    print(
        message
    )


    if success:

        ui.show_popup(
            message,
            success=True,
            duration=1800
        )


        renaming_vertex = None


    else:

        ui.show_popup(
            message,
            success=False,
            duration=2200
        )


        current_vertex = (
            graph.get_vertex(
                renaming_vertex
            )
        )


        if (
            current_vertex
            is not None
        ):

            ui.open_text_input(
                "Rename Vertex",
                new_name
            )


# =========================================================
# DOUBLE CLICK
# =========================================================

def is_double_click(
    vertex_id
):

    global last_vertex_click

    global last_vertex_click_time


    now = (
        pygame.time.get_ticks()
    )


    double_clicked = (
        vertex_id
        ==
        last_vertex_click
        and
        now
        -
        last_vertex_click_time
        <=
        DOUBLE_CLICK_TIME
    )


    if double_clicked:

        last_vertex_click = None

        last_vertex_click_time = 0

        return True


    last_vertex_click = (
        vertex_id
    )


    last_vertex_click_time = (
        now
    )


    return False


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

            continue


        # =================================================
        # RENAME BOX HAS PRIORITY
        # =================================================

        if ui.text_input_active:

            if (
                event.type
                ==
                pygame.KEYDOWN
            ):

                result = (
                    ui.handle_text_input_event(
                        event
                    )
                )


                if result is not None:

                    action, value = (
                        result
                    )


                    if (
                        action
                        ==
                        "submit"
                    ):

                        save_vertex_rename(
                            value
                        )


                    elif (
                        action
                        ==
                        "cancel"
                    ):

                        renaming_vertex = None


            continue


        # =================================================
        # KEYBOARD
        # =================================================

        if (
            event.type
            ==
            pygame.KEYDOWN
        ):


            # ---------------------------------------------
            # MODES
            # ---------------------------------------------

            if (
                event.key
                ==
                pygame.K_1
            ):

                set_mode(
                    EDIT_MODE
                )


            elif (
                event.key
                ==
                pygame.K_2
            ):

                set_mode(
                    WALK_MODE
                )


            elif (
                event.key
                ==
                pygame.K_3
            ):

                set_mode(
                    ALGORITHM_MODE
                )


            # ---------------------------------------------
            # ALGORITHM STEP
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
            # DELETE
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
            # ESCAPE
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

            if (
                event.button
                ==
                3
            ):

                ui.open_menu(
                    mouse_x,
                    mouse_y
                )

                continue


            # ---------------------------------------------
            # LEFT CLICK ONLY
            # ---------------------------------------------

            if (
                event.button
                !=
                1
            ):

                continue


            # ---------------------------------------------
            # MENU
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


                if (
                    clicked_vertex
                    is not None
                ):


                    # -------------------------------------
                    # DOUBLE CLICK = RENAME
                    # -------------------------------------

                    if is_double_click(
                        clicked_vertex
                    ):

                        begin_vertex_rename(
                            clicked_vertex
                        )

                        continue


                    # -------------------------------------
                    # FIRST VERTEX
                    # -------------------------------------

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


                    # -------------------------------------
                    # SECOND VERTEX = ADD EDGE
                    # -------------------------------------

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

                    last_vertex_click = None


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
    # HOVER STATE
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


    if (
        hovered_vertex is None
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
            candidate_edge is not None
            and
            not walk.is_empty()
            and
            graph.edge_is_incident_to_vertex(
                candidate_edge,
                walk.current_vertex()
            )
        ):

            hovered_edge = (
                candidate_edge
            )


    # =====================================================
    # DRAW
    # =====================================================

    renderer.clear()

    renderer.draw_grid()


    # -----------------------------------------------------
    # BASE EDGES
    # -----------------------------------------------------

    renderer.draw_edges(
        graph,
        hovered_edge
    )


    # -----------------------------------------------------
    # NORMAL WALK
    # -----------------------------------------------------

    if (
        current_mode
        not in
        (
            ALGORITHM_MODE,
            BIPARTITE_MODE,
            EULER_MODE
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
    # EULER CYCLE
    # -----------------------------------------------------

    if (
        current_mode
        ==
        EULER_MODE
        and
        euler_result
        is not None
    ):

        renderer.draw_euler_cycle(
            graph,
            euler_result[
                "edges"
            ]
        )


    # -----------------------------------------------------
    # BIPARTITE COLORS
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


    # -----------------------------------------------------
    # VERTICES
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NORMAL WALK UI
    # -----------------------------------------------------

    if (
        current_mode
        not in
        (
            BIPARTITE_MODE,
            EULER_MODE
        )
    ):

        ui.draw_walk(
            graph,
            walk,
            show_steps=(
                current_mode
                ==
                WALK_MODE
            )
        )


    # -----------------------------------------------------
    # ALGORITHM 1 UI
    # -----------------------------------------------------

    if (
        current_mode
        ==
        ALGORITHM_MODE
    ):

        ui.draw_algorithm(
            graph,
            algorithm1
        )


    # -----------------------------------------------------
    # EULER UI
    # -----------------------------------------------------

    if (
        current_mode
        ==
        EULER_MODE
        and
        euler_result
        is not None
    ):

        ui.draw_euler_cycle(
            graph,
            euler_result
        )


    # -----------------------------------------------------
    # POPUPS
    # -----------------------------------------------------

    ui.draw_popup()


    # -----------------------------------------------------
    # RIGHT CLICK MENU
    # -----------------------------------------------------

    ui.draw_context_menu()


    # -----------------------------------------------------
    # RENAME MODAL
    # -----------------------------------------------------

    ui.draw_text_input()


    # =====================================================
    # FRAME
    # =====================================================

    pygame.display.flip()


    clock.tick(
        60
    )


pygame.quit()