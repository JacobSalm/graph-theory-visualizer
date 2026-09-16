# =========================================================
# ALGORITHM 1
# =========================================================


def is_path(walk):
    """
    A walk is a path if no vertex
    appears more than once.
    """

    return len(walk) == len(set(walk))


# =========================================================
# CHECK FOR CYCLE
# =========================================================

def is_cycle(walk):
    """
    A cycle starts and ends at the same vertex
    and has no repeated vertices in between.
    """

    # Need at least:
    # a -> b -> c -> a
    if len(walk) < 4:
        return False

    # First and last must match
    if walk[0] != walk[-1]:
        return False

    # Ignore the final repeated vertex
    cycle_vertices = walk[:-1]

    # All other vertices must be unique
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
    Find the shortest closed subwalk C
    inside P.

    Returns:

        {
            "start": index,
            "end": index,
            "walk": [...]
        }

    or None.
    """

    shortest = None

    for start in range(len(walk)):

        for end in range(
            start + 1,
            len(walk)
        ):

            # A closed subwalk begins and
            # ends at the same vertex
            if walk[start] == walk[end]:

                closed_walk = walk[
                    start:end + 1
                ]

                if (
                    shortest is None
                    or
                    len(closed_walk)
                    <
                    len(shortest["walk"])
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
    """
    Perform:

        P := P ⊖ C

    Keep one copy of the repeated vertex
    while removing the closed section.
    """

    return (
        walk[:start + 1]
        +
        walk[end + 1:]
    )


# =========================================================
# RUN WHOLE ALGORITHM
# =========================================================

def run_algorithm(walk):
    """
    Run Algorithm 1 until P
    is either a path or a cycle.
    """

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

        # Safety check
        if closed is None:
            break

        path = remove_closed_subwalk(
            path,
            closed["start"],
            closed["end"]
        )

    return path