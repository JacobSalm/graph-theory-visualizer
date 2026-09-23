# =========================================================
# WALK SYSTEM
# =========================================================


class WalkSystem:

    def __init__(self):

        self.vertex_ids = []

        self.edge_ids = []


    # =====================================================
    # RESET
    # =====================================================

    def clear(self):

        self.vertex_ids.clear()

        self.edge_ids.clear()


    # =====================================================
    # INFORMATION
    # =====================================================

    def is_empty(self):

        return (
            len(self.vertex_ids)
            ==
            0
        )


    def current_vertex(self):

        if self.is_empty():

            return None

        return self.vertex_ids[
            -1
        ]


    def get_labels(
        self,
        graph
    ):

        return [

            graph.get_vertex_label_by_id(
                vertex_id
            )

            for vertex_id
            in self.vertex_ids
        ]


    # =====================================================
    # ADD VERTEX
    # =====================================================

    def add_vertex(
        self,
        graph,
        vertex_id
    ):

        # First vertex starts the walk.

        if self.is_empty():

            self.vertex_ids.append(
                vertex_id
            )

            label = (
                graph.get_vertex_label_by_id(
                    vertex_id
                )
            )

            return (
                True,
                f"Walk started at {label}"
            )

        previous_vertex = (
            self.current_vertex()
        )

        # If user chooses vertex -> vertex,
        # automatically use bridge #1.

        edge_id = (
            graph.get_default_edge_between(
                previous_vertex,
                vertex_id
            )
        )

        if edge_id is None:

            previous_label = (
                graph.get_vertex_label_by_id(
                    previous_vertex
                )
            )

            next_label = (
                graph.get_vertex_label_by_id(
                    vertex_id
                )
            )

            return (
                False,
                f"INVALID WALK MOVE: "
                f"No edge between "
                f"{previous_label} "
                f"and {next_label}"
            )

        self.edge_ids.append(
            edge_id
        )

        self.vertex_ids.append(
            vertex_id
        )

        number, total = (
            graph.get_parallel_edge_number(
                edge_id
            )
        )

        if (
            total is not None
            and
            total > 1
        ):

            message = (
                f"Used default bridge "
                f"{number}/{total}."
            )

        else:

            message = (
                "Walk extended."
            )

        return (
            True,
            message
        )


    # =====================================================
    # ADD EXACT EDGE
    # =====================================================

    def add_edge(
        self,
        graph,
        edge_id
    ):

        if self.is_empty():

            return (
                False,
                "Start the walk by "
                "clicking a vertex first."
            )

        current_vertex = (
            self.current_vertex()
        )

        next_vertex = (
            graph.get_other_endpoint(
                edge_id,
                current_vertex
            )
        )

        if next_vertex is None:

            current_label = (
                graph.get_vertex_label_by_id(
                    current_vertex
                )
            )

            return (
                False,
                f"That edge is not connected "
                f"to the current vertex "
                f"{current_label}."
            )

        self.edge_ids.append(
            edge_id
        )

        self.vertex_ids.append(
            next_vertex
        )

        number, total = (
            graph.get_parallel_edge_number(
                edge_id
            )
        )

        current_label = (
            graph.get_vertex_label_by_id(
                current_vertex
            )
        )

        next_label = (
            graph.get_vertex_label_by_id(
                next_vertex
            )
        )

        return (
            True,
            f"Used bridge "
            f"{number}/{total} from "
            f"{current_label} to "
            f"{next_label}."
        )


    # =====================================================
    # UNDO
    # =====================================================

    def undo(self):

        if self.is_empty():

            return None

        removed_vertex = (
            self.vertex_ids.pop()
        )

        if self.edge_ids:

            self.edge_ids.pop()

        return removed_vertex