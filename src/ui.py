# =========================================================
# USER INTERFACE
# =========================================================

import pygame


# =========================================================
# MODES
# =========================================================

EDIT_MODE = "EDIT GRAPH"

WALK_MODE = "BUILD WALK"

ALGORITHM_MODE = "RUN ALGORITHM"

BIPARTITE_MODE = (
    "CHECK IF BIPARTITE"
)

RESET_ACTION = "RESET GRAPH"


# =========================================================
# UI
# =========================================================

class UI:

    WHITE = (
        240,
        240,
        240
    )

    SECONDARY_TEXT = (
        170,
        170,
        170
    )

    MENU_BACKGROUND = (
        45,
        45,
        45
    )

    MENU_HOVER = (
        75,
        75,
        75
    )

    MENU_BORDER = (
        180,
        180,
        180
    )

    POPUP_BACKGROUND = (
        20,
        20,
        20
    )

    POPUP_BORDER = (
        230,
        230,
        230
    )

    SUCCESS_COLOR = (
        100,
        230,
        130
    )

    FAIL_COLOR = (
        255,
        100,
        100
    )

    INPUT_BACKGROUND = (
        40,
        40,
        40
    )

    INPUT_FIELD = (
        65,
        65,
        65
    )

    INPUT_BORDER = (
        210,
        210,
        210
    )

    SELECTION_COLOR = (
        80,
        110,
        170
    )


    def __init__(
        self,
        screen,
        width,
        height
    ):

        self.screen = screen

        self.width = width

        self.height = height

        self.ui_font = (
            pygame.font.SysFont(
                None,
                26
            )
        )

        self.menu_font = (
            pygame.font.SysFont(
                None,
                25
            )
        )

        self.small_font = (
            pygame.font.SysFont(
                None,
                21
            )
        )

        self.input_font = (
            pygame.font.SysFont(
                None,
                30
            )
        )


        # =================================================
        # CONTEXT MENU
        # =================================================

        self.menu_width = 220

        self.menu_item_height = 42

        self.menu_open = False

        self.menu_x = 0

        self.menu_y = 0

        self.menu_items = [

            (
                "EDIT GRAPH",
                EDIT_MODE
            ),

            (
                "BUILD WALK",
                WALK_MODE
            ),

            (
                "RUN ALGORITHM",
                ALGORITHM_MODE
            ),

            (
                "CHECK IF BIPARTITE",
                BIPARTITE_MODE
            ),

            (
                "RESET GRAPH",
                RESET_ACTION
            )
        ]


        # =================================================
        # POPUP
        # =================================================

        self.popup_message = ""

        self.popup_color = (
            self.WHITE
        )

        self.popup_until = 0


        # =================================================
        # TEXT INPUT
        # =================================================

        self.text_input_active = False

        self.text_input_title = ""

        self.text_input_value = ""

        self.text_input_select_all = False

        self.max_input_length = 40


    # =====================================================
    # HELPER - FIT TEXT
    # =====================================================

    def fit_text(
        self,
        text,
        font,
        maximum_width
    ):

        text = str(
            text
        )

        if (
            font.size(text)[0]
            <=
            maximum_width
        ):

            return text

        shortened = text

        while (
            shortened
            and
            font.size(
                shortened + "…"
            )[0]
            >
            maximum_width
        ):

            shortened = (
                shortened[:-1]
            )

        return (
            shortened
            +
            "…"
        )


    # =====================================================
    # CONTEXT MENU
    # =====================================================

    def open_menu(
        self,
        x,
        y
    ):

        self.menu_open = True

        self.menu_x = min(
            x,
            self.width
            -
            self.menu_width
        )

        total_height = (
            len(self.menu_items)
            *
            self.menu_item_height
        )

        self.menu_y = min(
            y,
            self.height
            -
            total_height
        )


    def close_menu(self):

        self.menu_open = False


    def handle_menu_click(
        self,
        x,
        y
    ):

        if not self.menu_open:
            return None

        for index, (
            text,
            action
        ) in enumerate(
            self.menu_items
        ):

            item_rect = (
                pygame.Rect(
                    self.menu_x,
                    self.menu_y
                    +
                    index
                    *
                    self.menu_item_height,
                    self.menu_width,
                    self.menu_item_height
                )
            )

            if item_rect.collidepoint(
                x,
                y
            ):

                self.menu_open = False

                return action

        self.menu_open = False

        return None


    def draw_context_menu(self):

        if not self.menu_open:
            return

        mouse_x, mouse_y = (
            pygame.mouse.get_pos()
        )

        total_height = (
            len(self.menu_items)
            *
            self.menu_item_height
        )

        pygame.draw.rect(
            self.screen,
            self.MENU_BACKGROUND,
            (
                self.menu_x,
                self.menu_y,
                self.menu_width,
                total_height
            )
        )

        pygame.draw.rect(
            self.screen,
            self.MENU_BORDER,
            (
                self.menu_x,
                self.menu_y,
                self.menu_width,
                total_height
            ),
            2
        )

        for index, (
            text,
            action
        ) in enumerate(
            self.menu_items
        ):

            item_y = (
                self.menu_y
                +
                index
                *
                self.menu_item_height
            )

            item_rect = (
                pygame.Rect(
                    self.menu_x,
                    item_y,
                    self.menu_width,
                    self.menu_item_height
                )
            )

            if item_rect.collidepoint(
                mouse_x,
                mouse_y
            ):

                pygame.draw.rect(
                    self.screen,
                    self.MENU_HOVER,
                    item_rect
                )

            rendered = (
                self.menu_font.render(
                    text,
                    True,
                    self.WHITE
                )
            )

            self.screen.blit(
                rendered,
                (
                    self.menu_x + 12,
                    item_y + 10
                )
            )


    # =====================================================
    # MODE
    # =====================================================

    def draw_mode(
        self,
        current_mode
    ):

        mode_text = (
            self.ui_font.render(
                f"MODE: {current_mode}",
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            mode_text,
            (
                15,
                15
            )
        )

        if (
            current_mode
            ==
            EDIT_MODE
        ):

            instructions = (
                "Double Click Vertex = Rename"
                "   |   Click Pair = Add Edge"
                "   |   Hover + X Delete"
                "   |   Right Click Menu"
            )

        elif (
            current_mode
            ==
            WALK_MODE
        ):

            instructions = (
                "Vertex -> Vertex = Bridge #1"
                "   |   Click Exact Edge = Use It"
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
            BIPARTITE_MODE
        ):

            instructions = (
                "Algorithm 2: Bipartite Check"
                "   |   1 Edit"
                "   |   Right Click Menu"
            )

        else:

            instructions = ""

        help_text = (
            self.small_font.render(
                instructions,
                True,
                self.SECONDARY_TEXT
            )
        )

        self.screen.blit(
            help_text,
            (
                15,
                45
            )
        )


    # =====================================================
    # WALK SUMMARY
    # =====================================================

    def draw_walk(
        self,
        graph,
        walk,
        show_steps=False
    ):

        labels = (
            walk.get_labels(
                graph
            )
        )

        if labels:

            walk_text = (
                "W = "
                +
                " -> ".join(
                    labels
                )
            )

        else:

            walk_text = (
                "W = empty"
            )

        walk_text = (
            self.fit_text(
                walk_text,
                self.ui_font,
                760
            )
        )

        text = (
            self.ui_font.render(
                walk_text,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            text,
            (
                15,
                75
            )
        )

        if show_steps:

            self.draw_walk_steps(
                graph,
                walk
            )


    # =====================================================
    # WALK STEP PANEL
    # =====================================================

    def draw_walk_steps(
        self,
        graph,
        walk
    ):

        panel_width = 350

        panel_x = (
            self.width
            -
            panel_width
            -
            15
        )

        panel_y = 85

        max_steps = 12

        number_of_steps = (
            len(
                walk.edge_ids
            )
        )

        visible_steps = min(
            number_of_steps,
            max_steps
        )

        extra_rows = 2

        if (
            number_of_steps
            >
            max_steps
        ):

            extra_rows += 1

        panel_height = (
            48
            +
            (
                visible_steps
                +
                extra_rows
            )
            *
            25
        )

        panel_rect = (
            pygame.Rect(
                panel_x,
                panel_y,
                panel_width,
                panel_height
            )
        )

        pygame.draw.rect(
            self.screen,
            self.POPUP_BACKGROUND,
            panel_rect
        )

        pygame.draw.rect(
            self.screen,
            self.MENU_BORDER,
            panel_rect,
            2
        )


        title = (
            self.ui_font.render(
                "WALK STEPS",
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            title,
            (
                panel_x + 12,
                panel_y + 10
            )
        )


        # ---------------------------------
        # No walk
        # ---------------------------------

        if walk.is_empty():

            empty = (
                self.small_font.render(
                    "No walk started.",
                    True,
                    self.SECONDARY_TEXT
                )
            )

            self.screen.blit(
                empty,
                (
                    panel_x + 12,
                    panel_y + 44
                )
            )

            return


        # ---------------------------------
        # Start vertex
        # ---------------------------------

        start_name = (
            graph.get_vertex_label_by_id(
                walk.vertex_ids[0]
            )
        )

        start_line = (
            "Start: "
            +
            str(start_name)
        )

        start_line = (
            self.fit_text(
                start_line,
                self.small_font,
                panel_width - 24
            )
        )

        rendered_start = (
            self.small_font.render(
                start_line,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            rendered_start,
            (
                panel_x + 12,
                panel_y + 44
            )
        )


        # ---------------------------------
        # Decide which steps to show
        # ---------------------------------

        start_step = max(
            0,
            number_of_steps
            -
            max_steps
        )

        current_y = (
            panel_y + 70
        )


        if start_step > 0:

            earlier = (
                self.small_font.render(
                    f"... {start_step} earlier "
                    f"step(s)",
                    True,
                    self.SECONDARY_TEXT
                )
            )

            self.screen.blit(
                earlier,
                (
                    panel_x + 12,
                    current_y
                )
            )

            current_y += 25


        # ---------------------------------
        # Individual steps
        # ---------------------------------

        for step_index in range(
            start_step,
            number_of_steps
        ):

            from_vertex = (
                walk.vertex_ids[
                    step_index
                ]
            )

            to_vertex = (
                walk.vertex_ids[
                    step_index + 1
                ]
            )

            edge_id = (
                walk.edge_ids[
                    step_index
                ]
            )

            from_name = (
                graph.get_vertex_label_by_id(
                    from_vertex
                )
            )

            to_name = (
                graph.get_vertex_label_by_id(
                    to_vertex
                )
            )

            bridge_number, bridge_total = (
                graph.get_parallel_edge_number(
                    edge_id
                )
            )

            step_text = (
                f"{step_index + 1}. "
                f"{from_name} -> {to_name} "
                f"[bridge "
                f"{bridge_number}/"
                f"{bridge_total}]"
            )

            step_text = (
                self.fit_text(
                    step_text,
                    self.small_font,
                    panel_width - 24
                )
            )

            rendered = (
                self.small_font.render(
                    step_text,
                    True,
                    self.WHITE
                )
            )

            self.screen.blit(
                rendered,
                (
                    panel_x + 12,
                    current_y
                )
            )

            current_y += 25


    # =====================================================
    # ALGORITHM DISPLAY
    # =====================================================

    def draw_algorithm(
        self,
        graph,
        algorithm
    ):

        path_labels = [

            graph.get_vertex_label_by_id(
                vertex_id
            )

            for vertex_id
            in algorithm.path
        ]

        if path_labels:

            path_text = (
                "P = "
                +
                " -> ".join(
                    path_labels
                )
            )

        else:

            path_text = (
                "P = empty"
            )

        path_text = (
            self.fit_text(
                path_text,
                self.ui_font,
                900
            )
        )

        rendered_path = (
            self.ui_font.render(
                path_text,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            rendered_path,
            (
                15,
                105
            )
        )


        if (
            algorithm.closed
            is not None
        ):

            closed_labels = [

                graph.get_vertex_label_by_id(
                    vertex_id
                )

                for vertex_id
                in algorithm.closed[
                    "walk"
                ]
            ]

            closed_text = (
                "C = "
                +
                " -> ".join(
                    closed_labels
                )
            )

        else:

            closed_text = (
                "C = none"
            )

        closed_text = (
            self.fit_text(
                closed_text,
                self.ui_font,
                900
            )
        )

        rendered_closed = (
            self.ui_font.render(
                closed_text,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            rendered_closed,
            (
                15,
                135
            )
        )


        rendered_message = (
            self.ui_font.render(
                algorithm.message,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            rendered_message,
            (
                15,
                165
            )
        )


    # =====================================================
    # POPUP
    # =====================================================

    def show_popup(
        self,
        message,
        success=True,
        duration=3000
    ):

        self.popup_message = (
            message
        )

        if success:

            self.popup_color = (
                self.SUCCESS_COLOR
            )

        else:

            self.popup_color = (
                self.FAIL_COLOR
            )

        self.popup_until = (
            pygame.time.get_ticks()
            +
            duration
        )


    def clear_popup(self):

        self.popup_message = ""

        self.popup_until = 0


    def draw_popup(self):

        if (
            self.popup_message
            ==
            ""
        ):

            return

        if (
            pygame.time.get_ticks()
            >
            self.popup_until
        ):

            return

        text = (
            self.ui_font.render(
                self.popup_message,
                True,
                self.popup_color
            )
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
            self.width // 2
            -
            box_width // 2
        )

        box_y = 100

        popup_rect = (
            pygame.Rect(
                box_x,
                box_y,
                box_width,
                box_height
            )
        )

        pygame.draw.rect(
            self.screen,
            self.POPUP_BACKGROUND,
            popup_rect
        )

        pygame.draw.rect(
            self.screen,
            self.POPUP_BORDER,
            popup_rect,
            2
        )

        text_rect = (
            text.get_rect(
                center=(
                    popup_rect.center
                )
            )
        )

        self.screen.blit(
            text,
            text_rect
        )


    # =====================================================
    # RENAME TEXT INPUT
    # =====================================================

    def open_text_input(
        self,
        title,
        initial_value=""
    ):

        self.close_menu()

        self.text_input_active = True

        self.text_input_title = (
            title
        )

        self.text_input_value = str(
            initial_value
        )

        # Typing immediately replaces
        # the current/default name.
        self.text_input_select_all = True


    def close_text_input(self):

        self.text_input_active = False

        self.text_input_title = ""

        self.text_input_value = ""

        self.text_input_select_all = False


    def handle_text_input_event(
        self,
        event
    ):

        if not self.text_input_active:

            return None


        # ---------------------------------
        # ENTER = SAVE
        # ---------------------------------

        if (
            event.key
            in
            (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            )
        ):

            value = (
                self.text_input_value
            )

            self.close_text_input()

            return (
                "submit",
                value
            )


        # ---------------------------------
        # ESC = CANCEL
        # ---------------------------------

        if (
            event.key
            ==
            pygame.K_ESCAPE
        ):

            self.close_text_input()

            return (
                "cancel",
                None
            )


        # ---------------------------------
        # CTRL + A
        # ---------------------------------

        if (
            event.key
            ==
            pygame.K_a
            and
            (
                event.mod
                &
                pygame.KMOD_CTRL
            )
        ):

            self.text_input_select_all = True

            return None


        # ---------------------------------
        # BACKSPACE
        # ---------------------------------

        if (
            event.key
            ==
            pygame.K_BACKSPACE
        ):

            if self.text_input_select_all:

                self.text_input_value = ""

                self.text_input_select_all = False

            else:

                self.text_input_value = (
                    self.text_input_value[
                        :-1
                    ]
                )

            return None


        # ---------------------------------
        # PRINTABLE CHARACTERS
        # ---------------------------------

        character = (
            event.unicode
        )

        if (
            character
            and
            character.isprintable()
        ):

            if (
                self.text_input_select_all
            ):

                self.text_input_value = ""

                self.text_input_select_all = False

            if (
                len(
                    self.text_input_value
                )
                <
                self.max_input_length
            ):

                self.text_input_value += (
                    character
                )

        return None


    def draw_text_input(self):

        if not self.text_input_active:

            return


        # ---------------------------------
        # Dark modal overlay
        # ---------------------------------

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                0,
                0,
                0,
                150
            )
        )

        self.screen.blit(
            overlay,
            (
                0,
                0
            )
        )


        # ---------------------------------
        # Main box
        # ---------------------------------

        box_width = 620

        box_height = 190

        box_x = (
            self.width // 2
            -
            box_width // 2
        )

        box_y = (
            self.height // 2
            -
            box_height // 2
        )

        box_rect = pygame.Rect(
            box_x,
            box_y,
            box_width,
            box_height
        )

        pygame.draw.rect(
            self.screen,
            self.INPUT_BACKGROUND,
            box_rect
        )

        pygame.draw.rect(
            self.screen,
            self.INPUT_BORDER,
            box_rect,
            2
        )


        # ---------------------------------
        # Title
        # ---------------------------------

        title = (
            self.ui_font.render(
                self.text_input_title,
                True,
                self.WHITE
            )
        )

        self.screen.blit(
            title,
            (
                box_x + 25,
                box_y + 20
            )
        )


        # ---------------------------------
        # Text field
        # ---------------------------------

        field_rect = pygame.Rect(
            box_x + 25,
            box_y + 62,
            box_width - 50,
            48
        )

        pygame.draw.rect(
            self.screen,
            self.INPUT_FIELD,
            field_rect
        )

        pygame.draw.rect(
            self.screen,
            self.INPUT_BORDER,
            field_rect,
            2
        )


        visible_value = (
            self.fit_text(
                self.text_input_value,
                self.input_font,
                field_rect.width - 24
            )
        )

        text_surface = (
            self.input_font.render(
                visible_value,
                True,
                self.WHITE
            )
        )

        text_x = (
            field_rect.x + 10
        )

        text_y = (
            field_rect.centery
            -
            text_surface.get_height()
            // 2
        )


        # ---------------------------------
        # Selected default/current text
        # ---------------------------------

        if (
            self.text_input_select_all
            and
            visible_value
        ):

            selection_rect = (
                text_surface.get_rect(
                    topleft=(
                        text_x,
                        text_y
                    )
                )
            )

            pygame.draw.rect(
                self.screen,
                self.SELECTION_COLOR,
                selection_rect
            )


        self.screen.blit(
            text_surface,
            (
                text_x,
                text_y
            )
        )


        # ---------------------------------
        # Cursor
        # ---------------------------------

        if (
            not self.text_input_select_all
            and
            (
                pygame.time.get_ticks()
                // 500
            )
            %
            2
            ==
            0
        ):

            cursor_x = (
                text_x
                +
                text_surface.get_width()
                +
                2
            )

            pygame.draw.line(
                self.screen,
                self.WHITE,
                (
                    cursor_x,
                    field_rect.y + 9
                ),
                (
                    cursor_x,
                    field_rect.bottom - 9
                ),
                2
            )


        # ---------------------------------
        # Instructions
        # ---------------------------------

        instructions = (
            self.small_font.render(
                "Enter = Save    Esc = Cancel"
                "    Ctrl+A = Select All",
                True,
                self.SECONDARY_TEXT
            )
        )

        self.screen.blit(
            instructions,
            (
                box_x + 25,
                box_y + 130
            )
        )