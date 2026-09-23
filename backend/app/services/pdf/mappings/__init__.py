"""One module per form: only coordinates, no logic.

Coordinates are PDF points (A4 = 595 x 842), origin top-left, measured from the dotted
leaders of the original templates (see docs/FORM_ANALYSIS.md, Appendix A).
"""

# Text sits slightly above the dotted leader instead of on top of the dots.
LIFT = 3.0


def on_dots(dot_baseline: float) -> float:
    return dot_baseline - LIFT
