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
# CHECK FOR CYCLE
# =========================================================

def is_cycle(walk):
    """
    A cycle starts and ends at the same vertex
    and has no repeated vertices in between.
    """

    if len(walk) < 4:

        return False

    if walk[0] != walk[-1]:

        return False

    cycle_vertices = (
        walk[:-1]
    )

    return (
        len(cycle_vertices)
        ==
        len(set(cycle_vertices))
    )


# =========================================================
# FIND SHORTEST CLOSED SUBWALK
# =========================================================

def find_shortest_closed_subwalk(walk):
    """
    Find the shortest closed subwalk C.

    Returns:

        {
            "start": start_index,
            "end": end_index,
            "walk": [...]
        }

    or None.
    """

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
                        shortest["walk"]
                    )
                ):

                    shortest = {
                        "start": start,
                        "end": end,
                        "walk": closed_walk,
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
    """
    Perform:

        P := P - C

    Keep one copy of the repeated vertex.
    """

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
    """
    Run Algorithm 1 until P
    becomes a path or cycle.
    """

    path = (
        walk.copy()
    )

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