# =========================================================
# GRAPH MODEL
# =========================================================


class GraphModel:

    def __init__(
        self,
        grid_size=50,
        max_parallel_edges=4
    ):

        self.grid_size = grid_size
        self.max_parallel_edges = max_parallel_edges

        # Stable IDs.
        self.vertices = {}
        self.edges = {}

        self.next_vertex_id = 0
        self.next_edge_id = 0
        self.next_label_number = 0


    # =====================================================
    # DEFAULT LABELS
    # =====================================================

    def get_default_vertex_label(
        self,
        index
    ):

        # a-z
        if index < 26:
            return chr(
                ord("a") + index
            )

        # A-Z
        if index < 52:
            return chr(
                ord("A")
                +
                index - 26
            )

        return f"V{index + 1}"


    def get_next_available_default_label(self):

        existing_labels = {

            vertex["label"]

            for vertex
            in self.vertices.values()
        }

        while True:

            label = (
                self.get_default_vertex_label(
                    self.next_label_number
                )
            )

            self.next_label_number += 1

            if (
                label
                not in existing_labels
            ):

                return label


    # =====================================================
    # GRID
    # =====================================================

    def snap_to_grid(
        self,
        value
    ):

        return round(
            value / self.grid_size
        ) * self.grid_size


    # =====================================================
    # VERTEX ACCESS
    # =====================================================

    def get_vertex(
        self,
        vertex_id
    ):

        return self.vertices.get(
            vertex_id
        )


    def get_vertex_ids(self):

        return list(
            self.vertices.keys()
        )


    def get_vertex_label_by_id(
        self,
        vertex_id
    ):

        vertex = self.get_vertex(
            vertex_id
        )

        if vertex is None:
            return None

        return vertex["label"]


    # =====================================================
    # POSITION
    # =====================================================

    def position_is_valid(
        self,
        x,
        y
    ):

        for vertex in (
            self.vertices.values()
        ):

            if (
                vertex["x"] == x
                and
                vertex["y"] == y
            ):

                return False

        return True


    def vertex_at_position(
        self,
        x,
        y,
        radius
    ):

        for vertex_id, vertex in (
            self.vertices.items()
        ):

            dx = (
                x
                -
                vertex["x"]
            )

            dy = (
                y
                -
                vertex["y"]
            )

            distance_squared = (
                dx * dx
                +
                dy * dy
            )

            if (
                distance_squared
                <=
                radius ** 2
            ):

                return vertex_id

        return None


    # =====================================================
    # ADD VERTEX
    # =====================================================

    def add_vertex(
        self,
        x,
        y
    ):

        x = self.snap_to_grid(
            x
        )

        y = self.snap_to_grid(
            y
        )

        if not self.position_is_valid(
            x,
            y
        ):

            return (
                None,
                "A vertex already exists here."
            )

        vertex_id = (
            self.next_vertex_id
        )

        self.next_vertex_id += 1

        label = (
            self.get_next_available_default_label()
        )

        self.vertices[
            vertex_id
        ] = {

            "id": vertex_id,
            "x": x,
            "y": y,
            "label": label
        }

        return (
            vertex_id,
            f"Created vertex {label} "
            f"at ({x}, {y})"
        )


    # =====================================================
    # RENAME VERTEX
    # =====================================================

    def rename_vertex(
        self,
        vertex_id,
        new_label
    ):

        vertex = self.get_vertex(
            vertex_id
        )

        if vertex is None:

            return (
                False,
                "Vertex no longer exists."
            )

        new_label = (
            new_label.strip()
        )

        if new_label == "":

            return (
                False,
                "Vertex name cannot be empty."
            )

        # Keep names unique so the
        # displayed graph stays clear.

        for other_id, other_vertex in (
            self.vertices.items()
        ):

            if (
                other_id != vertex_id
                and
                other_vertex["label"]
                ==
                new_label
            ):

                return (
                    False,
                    f'A vertex named "{new_label}" '
                    f"already exists."
                )

        old_label = (
            vertex["label"]
        )

        vertex["label"] = (
            new_label
        )

        return (
            True,
            f'Renamed "{old_label}" '
            f'to "{new_label}".'
        )


    # =====================================================
    # DELETE VERTEX
    # =====================================================

    def delete_vertex(
        self,
        vertex_id
    ):

        if (
            vertex_id
            not in self.vertices
        ):

            return None

        label = (
            self.vertices[
                vertex_id
            ]["label"]
        )

        edge_ids_to_delete = [

            edge_id

            for edge_id, edge
            in self.edges.items()

            if (
                edge["u"] == vertex_id
                or
                edge["v"] == vertex_id
            )
        ]

        for edge_id in (
            edge_ids_to_delete
        ):

            del self.edges[
                edge_id
            ]

        del self.vertices[
            vertex_id
        ]

        return (
            f"Deleted vertex {label} "
            f"and all attached edges."
        )


    # =====================================================
    # EDGE ACCESS
    # =====================================================

    def get_edge(
        self,
        edge_id
    ):

        return self.edges.get(
            edge_id
        )


    def get_edge_ids(self):

        return list(
            self.edges.keys()
        )


    # =====================================================
    # PARALLEL EDGES
    # =====================================================

    def get_parallel_edge_ids(
        self,
        vertex1,
        vertex2
    ):

        result = []

        for edge_id, edge in (
            self.edges.items()
        ):

            u = edge["u"]
            v = edge["v"]

            if (
                (
                    u == vertex1
                    and
                    v == vertex2
                )
                or
                (
                    u == vertex2
                    and
                    v == vertex1
                )
            ):

                result.append(
                    edge_id
                )

        return result


    def count_edges_between(
        self,
        vertex1,
        vertex2
    ):

        return len(
            self.get_parallel_edge_ids(
                vertex1,
                vertex2
            )
        )


    def edge_exists(
        self,
        vertex1,
        vertex2
    ):

        return (
            self.count_edges_between(
                vertex1,
                vertex2
            )
            > 0
        )


    # =====================================================
    # ADD EDGE
    # =====================================================

    def add_edge(
        self,
        vertex1,
        vertex2
    ):

        if vertex1 == vertex2:

            return (
                None,
                "Self-loops are not enabled."
            )

        if (
            vertex1 not in self.vertices
            or
            vertex2 not in self.vertices
        ):

            return (
                None,
                "Invalid vertex."
            )

        current_count = (
            self.count_edges_between(
                vertex1,
                vertex2
            )
        )

        if (
            current_count
            >=
            self.max_parallel_edges
        ):

            label1 = (
                self.get_vertex_label_by_id(
                    vertex1
                )
            )

            label2 = (
                self.get_vertex_label_by_id(
                    vertex2
                )
            )

            return (
                None,
                f"Maximum of "
                f"{self.max_parallel_edges} "
                f"edges between "
                f"{label1} and {label2}."
            )

        edge_id = (
            self.next_edge_id
        )

        self.next_edge_id += 1

        self.edges[
            edge_id
        ] = {

            "id": edge_id,
            "u": vertex1,
            "v": vertex2
        }

        label1 = (
            self.get_vertex_label_by_id(
                vertex1
            )
        )

        label2 = (
            self.get_vertex_label_by_id(
                vertex2
            )
        )

        return (
            edge_id,
            f"Created edge "
            f"{label1} -- {label2} "
            f"({current_count + 1}/"
            f"{self.max_parallel_edges})"
        )


    # =====================================================
    # DELETE EDGE
    # =====================================================

    def delete_edge(
        self,
        edge_id
    ):

        edge = self.get_edge(
            edge_id
        )

        if edge is None:
            return None

        vertex1 = edge["u"]
        vertex2 = edge["v"]

        label1 = (
            self.get_vertex_label_by_id(
                vertex1
            )
        )

        label2 = (
            self.get_vertex_label_by_id(
                vertex2
            )
        )

        del self.edges[
            edge_id
        ]

        remaining = (
            self.count_edges_between(
                vertex1,
                vertex2
            )
        )

        return (
            f"Deleted one edge "
            f"{label1} -- {label2}. "
            f"{remaining} remaining."
        )


    # =====================================================
    # EDGE RELATIONSHIPS
    # =====================================================

    def edge_is_incident_to_vertex(
        self,
        edge_id,
        vertex_id
    ):

        edge = self.get_edge(
            edge_id
        )

        if edge is None:
            return False

        return (
            edge["u"] == vertex_id
            or
            edge["v"] == vertex_id
        )


    def get_other_endpoint(
        self,
        edge_id,
        vertex_id
    ):

        edge = self.get_edge(
            edge_id
        )

        if edge is None:
            return None

        if edge["u"] == vertex_id:
            return edge["v"]

        if edge["v"] == vertex_id:
            return edge["u"]

        return None


    def get_default_edge_between(
        self,
        vertex1,
        vertex2
    ):

        parallel_edges = (
            self.get_parallel_edge_ids(
                vertex1,
                vertex2
            )
        )

        if not parallel_edges:
            return None

        # Bridge #1
        return parallel_edges[0]


    def get_parallel_edge_number(
        self,
        edge_id
    ):

        edge = self.get_edge(
            edge_id
        )

        if edge is None:

            return (
                None,
                None
            )

        parallel_edges = (
            self.get_parallel_edge_ids(
                edge["u"],
                edge["v"]
            )
        )

        return (
            parallel_edges.index(
                edge_id
            )
            + 1,

            len(
                parallel_edges
            )
        )


    # =====================================================
    # ADJACENCY USING PERMANENT IDS
    # =====================================================

    def to_adjacency_ids(self):

        adjacency = {

            vertex_id: set()

            for vertex_id
            in self.vertices
        }

        for edge in (
            self.edges.values()
        ):

            u = edge["u"]
            v = edge["v"]

            adjacency[u].add(
                v
            )

            adjacency[v].add(
                u
            )

        return {

            vertex_id: list(
                neighbors
            )

            for vertex_id, neighbors
            in adjacency.items()
        }


    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.vertices.clear()
        self.edges.clear()

        self.next_vertex_id = 0
        self.next_edge_id = 0
        self.next_label_number = 0