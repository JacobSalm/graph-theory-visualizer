# =========================================================
# RENDERING
# =========================================================

import math

import pygame


class Renderer:

    # =====================================================
    # COLORS
    # =====================================================

    BACKGROUND = (
        30,
        30,
        30
    )

    GRID_COLOR = (
        50,
        50,
        50
    )

    VERTEX_COLOR = (
        230,
        230,
        230
    )

    TEXT_COLOR = (
        20,
        20,
        20
    )

    BORDER_COLOR = (
        255,
        255,
        255
    )

    EDGE_COLOR = (
        180,
        180,
        180
    )

    SELECTED_COLOR = (
        255,
        220,
        0
    )

    HOVER_COLOR = (
        255,
        110,
        110
    )

    WALK_EDGE_COLOR = (
        70,
        150,
        255
    )

    WALK_VERTEX_COLOR = (
        100,
        180,
        255
    )

    ALGORITHM_PATH_COLOR = (
        180,
        100,
        255
    )

    CLOSED_WALK_COLOR = (
        255,
        90,
        70
    )

    BIPARTITE_COLOR_0 = (
        90,
        170,
        255
    )

    BIPARTITE_COLOR_1 = (
        255,
        150,
        90
    )


    # =====================================================
    # SETUP
    # =====================================================

    def __init__(
        self,
        screen,
        width,
        height,
        grid_size=50,
        vertex_radius=22
    ):

        self.screen = screen

        self.width = width

        self.height = height

        self.grid_size = (
            grid_size
        )

        self.vertex_radius = (
            vertex_radius
        )

        self.edge_hover_distance = 10

        self.vertex_font = (
            pygame.font.SysFont(
                None,
                30
            )
        )


    # =====================================================
    # BACKGROUND
    # =====================================================

    def clear(self):

        self.screen.fill(
            self.BACKGROUND
        )


    # =====================================================
    # GRID
    # =====================================================

    def draw_grid(self):

        for x in range(
            0,
            self.width,
            self.grid_size
        ):

            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                (x, 0),
                (x, self.height)
            )

        for y in range(
            0,
            self.height,
            self.grid_size
        ):

            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                (0, y),
                (self.width, y)
            )


    # =====================================================
    # PARALLEL EDGE OFFSETS
    # =====================================================

    def get_parallel_offsets(
        self,
        count
    ):

        if count == 1:

            return [
                0
            ]

        if count == 2:

            return [
                -24,
                24
            ]

        if count == 3:

            return [
                -36,
                0,
                36
            ]

        if count == 4:

            return [
                -48,
                -16,
                16,
                48
            ]

        return []


    # =====================================================
    # CURVE CREATION
    # =====================================================

    def make_curve_points(
        self,
        start,
        end,
        offset
    ):

        if offset == 0:

            return [
                start,
                end
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
                end
            ]

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
                    y
                )
            )

        return points


    # =====================================================
    # EDGE RENDER INFORMATION
    # =====================================================

    def get_edge_render_data(
        self,
        graph
    ):

        groups = {}

        for edge_id in (
            graph.get_edge_ids()
        ):

            edge = (
                graph.get_edge(
                    edge_id
                )
            )

            key = tuple(
                sorted(
                    (
                        edge["u"],
                        edge["v"]
                    )
                )
            )

            if key not in groups:

                groups[key] = []

            groups[
                key
            ].append(
                edge_id
            )

        render_data = []

        for (
            key,
            edge_ids
        ) in groups.items():

            offsets = (
                self.get_parallel_offsets(
                    len(edge_ids)
                )
            )

            vertex1 = (
                graph.get_vertex(
                    key[0]
                )
            )

            vertex2 = (
                graph.get_vertex(
                    key[1]
                )
            )

            if (
                vertex1 is None
                or
                vertex2 is None
            ):

                continue

            start = (
                vertex1["x"],
                vertex1["y"]
            )

            end = (
                vertex2["x"],
                vertex2["y"]
            )

            for (
                edge_id,
                offset
            ) in zip(
                edge_ids,
                offsets
            ):

                points = (
                    self.make_curve_points(
                        start,
                        end,
                        offset
                    )
                )

                render_data.append(
                    (
                        edge_id,
                        points
                    )
                )

        return render_data


    def get_edge_render_map(
        self,
        graph
    ):

        return {

            edge_id: points

            for edge_id, points
            in self.get_edge_render_data(
                graph
            )
        }


    # =====================================================
    # EDGE HOVER DISTANCE
    # =====================================================

    def point_to_segment_distance(
        self,
        px,
        py,
        x1,
        y1,
        x2,
        y2
    ):

        dx = (
            x2 - x1
        )

        dy = (
            y2 - y1
        )

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
            x1
            +
            t * dx
        )

        nearest_y = (
            y1
            +
            t * dy
        )

        return math.hypot(
            px - nearest_x,
            py - nearest_y
        )


    def get_hovered_edge(
        self,
        graph,
        mouse_x,
        mouse_y
    ):

        best_edge = None

        best_distance = (
            self.edge_hover_distance
        )

        for (
            edge_id,
            points
        ) in self.get_edge_render_data(
            graph
        ):

            for index in range(
                len(points) - 1
            ):

                x1, y1 = (
                    points[index]
                )

                x2, y2 = (
                    points[
                        index + 1
                    ]
                )

                distance = (
                    self.point_to_segment_distance(
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
                        edge_id
                    )

        return best_edge


    # =====================================================
    # NORMAL EDGES
    # =====================================================

    def draw_edges(
        self,
        graph,
        hovered_edge=None
    ):

        for (
            edge_id,
            points
        ) in self.get_edge_render_data(
            graph
        ):

            if (
                edge_id
                ==
                hovered_edge
            ):

                color = (
                    self.HOVER_COLOR
                )

                width = 7

            else:

                color = (
                    self.EDGE_COLOR
                )

                width = 4

            pygame.draw.lines(
                self.screen,
                color,
                False,
                points,
                width
            )


    # =====================================================
    # EXACT EDGES
    # =====================================================

    def draw_exact_edges(
        self,
        graph,
        edge_ids,
        color,
        width
    ):

        render_map = (
            self.get_edge_render_map(
                graph
            )
        )

        for edge_id in edge_ids:

            points = (
                render_map.get(
                    edge_id
                )
            )

            if points is None:

                continue

            pygame.draw.lines(
                self.screen,
                color,
                False,
                points,
                width
            )


    # =====================================================
    # WALK
    # =====================================================

    def draw_walk(
        self,
        graph,
        walk
    ):

        self.draw_exact_edges(
            graph,
            walk.edge_ids,
            self.WALK_EDGE_COLOR,
            7
        )

        for vertex_id in (
            walk.vertex_ids
        ):

            vertex = (
                graph.get_vertex(
                    vertex_id
                )
            )

            if vertex is None:

                continue

            pygame.draw.circle(
                self.screen,
                self.WALK_VERTEX_COLOR,
                (
                    vertex["x"],
                    vertex["y"]
                ),
                self.vertex_radius + 5,
                4
            )


    # =====================================================
    # ALGORITHM 1
    # =====================================================

    def draw_algorithm(
        self,
        graph,
        algorithm
    ):

        self.draw_exact_edges(
            graph,
            algorithm.path_edges,
            self.ALGORITHM_PATH_COLOR,
            7
        )

        self.draw_exact_edges(
            graph,
            algorithm.closed_edges,
            self.CLOSED_WALK_COLOR,
            10
        )


    # =====================================================
    # VERTICES
    # =====================================================

    def draw_vertices(
        self,
        graph,
        selected_vertex=None,
        hovered_vertex=None,
        bipartite_colors=None
    ):

        if bipartite_colors is None:

            bipartite_colors = {}

        for vertex_id in (
            graph.get_vertex_ids()
        ):

            vertex = (
                graph.get_vertex(
                    vertex_id
                )
            )

            x = vertex["x"]

            y = vertex["y"]

            label = vertex[
                "label"
            ]

            fill_color = (
                self.VERTEX_COLOR
            )

            if (
                label
                in
                bipartite_colors
            ):

                if (
                    bipartite_colors[
                        label
                    ]
                    ==
                    0
                ):

                    fill_color = (
                        self.BIPARTITE_COLOR_0
                    )

                else:

                    fill_color = (
                        self.BIPARTITE_COLOR_1
                    )

            pygame.draw.circle(
                self.screen,
                fill_color,
                (x, y),
                self.vertex_radius
            )

            if (
                vertex_id
                ==
                selected_vertex
            ):

                border_color = (
                    self.SELECTED_COLOR
                )

                border_width = 5

            elif (
                vertex_id
                ==
                hovered_vertex
            ):

                border_color = (
                    self.HOVER_COLOR
                )

                border_width = 4

            else:

                border_color = (
                    self.BORDER_COLOR
                )

                border_width = 2

            pygame.draw.circle(
                self.screen,
                border_color,
                (x, y),
                self.vertex_radius,
                border_width
            )

            text = (
                self.vertex_font.render(
                    label,
                    True,
                    self.TEXT_COLOR
                )
            )

            text_rect = (
                text.get_rect(
                    center=(
                        x,
                        y
                    )
                )
            )

            self.screen.blit(
                text,
                text_rect
            )