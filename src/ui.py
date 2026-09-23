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

        self.popup_message = ""

        self.popup_color = (
            self.WHITE
        )

        self.popup_until = 0


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
    # MODE DISPLAY
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
                "1 Edit   2 Walk   "
                "3 Algorithm"
                "   |   Click pair = Add Edge"
                "   |   Hover + X Delete"
                "   |   Right Click Menu"
            )

        elif (
            current_mode
            ==
            WALK_MODE
        ):

            instructions = (
                "Vertex -> Vertex = bridge #1"
                "   |   Click exact edge = "
                "use that bridge"
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
            self.ui_font.render(
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
    # WALK DISPLAY
    # =====================================================

    def draw_walk(
        self,
        labels
    ):

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


    # =====================================================
    # ALGORITHM DISPLAY
    # =====================================================

    def draw_algorithm(
        self,
        algorithm
    ):

        if algorithm.path:

            path_text = (
                "P = "
                +
                " -> ".join(
                    algorithm.path
                )
            )

        else:

            path_text = (
                "P = empty"
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

            closed_text = (
                "C = "
                +
                " -> ".join(
                    algorithm.closed[
                        "walk"
                    ]
                )
            )

        else:

            closed_text = (
                "C = none"
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