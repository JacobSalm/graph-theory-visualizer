# =========================================================
# ALGORITHM 1
# =========================================================


def is_path(walk):
    """
    A walk is a path if no vertex
    appears more than once.
    """

    return (
        len(walk)
        ==
        len(set(walk))
    )


# =========================================================
# CYCLE
# =========================================================

def is_cycle(walk):
    """
    A cycle starts and ends at the
    same vertex and has no repeated
    interior vertices.
    """

    if len(walk) < 4:
        return False

    if (
        walk[0]
        !=
        walk[-1]
    ):
        return False

    vertices = (
        walk[:-1]
    )

    return (
        len(vertices)
        ==
        len(set(vertices))
    )


# =========================================================
# FIND SHORTEST CLOSED SUBWALK
# =========================================================

def find_shortest_closed_subwalk(
    walk
):

    shortest = None

    for start in range(
        len(walk)
    ):

        for end in range(
            start + 1,
            len(walk)
        ):

            if (
                walk[start]
                ==
                walk[end]
            ):

                closed_walk = (
                    walk[
                        start:end + 1
                    ]
                )

                if (
                    shortest is None
                    or
                    len(closed_walk)
                    <
                    len(
                        shortest[
                            "walk"
                        ]
                    )
                ):

                    shortest = {

                        "start": start,
                        "end": end,
                        "walk": closed_walk
                    }

    return shortest


# =========================================================
# REMOVE CLOSED SUBWALK
# =========================================================

def remove_closed_subwalk(
    walk,
    start,
    end
):

    return (
        walk[
            :start + 1
        ]
        +
        walk[
            end + 1:
        ]
    )


# =========================================================
# RUN WHOLE ALGORITHM
# =========================================================

def run_algorithm(walk):

    path = walk.copy()

    while not (
        is_path(path)
        or
        is_cycle(path)
    ):

        closed = (
            find_shortest_closed_subwalk(
                path
            )
        )

        if closed is None:
            break

        path = (
            remove_closed_subwalk(
                path,
                closed["start"],
                closed["end"]
            )
        )

    return path


# =========================================================
# STEP-BY-STEP SESSION
# =========================================================

class Algorithm1Session:

    def __init__(self):
        self.reset()


    def reset(self):

        self.path = []

        self.path_edges = []

        self.closed = None

        self.closed_edges = []

        self.phase = "IDLE"

        self.message = ""


    # =====================================================
    # START
    # =====================================================

    def start(
        self,
        vertex_ids,
        edge_ids
    ):

        self.path = (
            vertex_ids.copy()
        )

        self.path_edges = (
            edge_ids.copy()
        )

        self.closed = None

        self.closed_edges = []

        if not self.path:

            self.phase = "IDLE"

            self.message = (
                "Build a walk first."
            )

            return False

        self.phase = "CHECK"

        self.message = (
            "P := W    "
            "Press SPACE to continue."
        )

        return True


    # =====================================================
    # NEXT STEP
    # =====================================================

    def step(self):

        if not self.path:

            self.message = (
                "No walk loaded."
            )

            return


        # =================================================
        # CHECK P
        # =================================================

        if self.phase == "CHECK":

            if is_path(
                self.path
            ):

                self.phase = (
                    "FINISHED"
                )

                self.closed = None
                self.closed_edges = []

                self.message = (
                    "P is a path. "
                    "Algorithm finished."
                )

                return


            if is_cycle(
                self.path
            ):

                self.phase = (
                    "FINISHED"
                )

                self.closed = None
                self.closed_edges = []

                self.message = (
                    "P is a cycle. "
                    "Algorithm finished."
                )

                return


            self.closed = (
                find_shortest_closed_subwalk(
                    self.path
                )
            )

            if self.closed is None:

                self.phase = (
                    "FINISHED"
                )

                self.closed_edges = []

                self.message = (
                    "No closed subwalk found."
                )

                return


            start = (
                self.closed[
                    "start"
                ]
            )

            end = (
                self.closed[
                    "end"
                ]
            )

            self.closed_edges = (
                self.path_edges[
                    start:end
                ].copy()
            )

            self.phase = (
                "SHOW_C"
            )

            self.message = (
                "Found shortest closed "
                "subwalk C. "
                "Press SPACE to remove it."
            )

            return


        # =================================================
        # REMOVE C
        # =================================================

        if (
            self.phase
            ==
            "SHOW_C"
        ):

            start = (
                self.closed[
                    "start"
                ]
            )

            end = (
                self.closed[
                    "end"
                ]
            )

            self.path_edges = (
                self.path_edges[
                    :start
                ]
                +
                self.path_edges[
                    end:
                ]
            )

            self.path = (
                remove_closed_subwalk(
                    self.path,
                    start,
                    end
                )
            )

            self.closed = None

            self.closed_edges = []

            self.phase = (
                "CHECK"
            )

            self.message = (
                "P := P minus C. "
                "Press SPACE to continue."
            )

            return


        if (
            self.phase
            ==
            "FINISHED"
        ):

            self.message = (
                "Algorithm already finished."
            )