"""
RTD Core Animation — Reachability-based Trajectory Design
=========================================================

Visualises the central pipeline of RTD on a single (x, y) position plane:

    1. X_0  — initial-condition set with state uncertainty.
    2. FRS  — Forward Reachable Set propagated forward in time, swept over a
              trajectory parameter k in [-1, 1].
    3. Slice — fix k = k*; the FRS collapses to a parameterized sub-tube.
    4. COM  — black line through the centre of the slice = planning-model
              centre-of-mass trajectory at k*.
    5. Body — dark tube around the COM = robot's physical footprint.
    6. Bloat — slightly lighter outer ring around the body tube = epsilon
               inflation that absorbs worst-case tracking error between the
               planning model and the true closed-loop dynamics.

The five layers stack via z-order so the bloat reads as a halo around the
body, the body as a band on the COM, and both as inhabitants of the slice.

------------------------------------------------------------
Install + render
------------------------------------------------------------
Install Manim Community Edition (one-time):

    python -m venv .venv && source .venv/bin/activate
    pip install manim

Render at high quality (1080p, 60fps):

    manim -pqh rtd_core.py RTDCoreAnimation

Render a fast preview (480p, 15fps) while iterating:

    manim -pql rtd_core.py RTDCoreAnimation

Output goes to ./media/videos/rtd_core/<quality>/RTDCoreAnimation.mp4 by
default; change with `--media_dir <path>`.
"""

from manim import *
import numpy as np


# ----- Parameterised trajectory family --------------------------------------
# y(t; k) = k * tanh(t / TAU) * AMP
TAU = 2.5
AMP = 1.4


def y_of_t(t: float, k: float) -> float:
    """Centre-of-mass y-position at time t for trajectory parameter k."""
    return k * np.tanh(t / TAU) * AMP


def frs_radius(t: float) -> float:
    """Half-width of the FRS at time t — initial uncertainty + growth."""
    return 0.30 + 0.06 * t


def slice_radius(t: float) -> float:
    """Half-width of a single-k slice — tighter than the full FRS."""
    return 0.28 + 0.045 * t


# ----- Colours --------------------------------------------------------------
COLOR_IC = YELLOW
COLOR_IC_EDGE = YELLOW_E
COLOR_FRS = BLUE_D
COLOR_FRS_HAIR = BLUE_C
COLOR_SLICE_FILL = PURPLE_C
COLOR_SLICE_EDGE = PURPLE_D
COLOR_COM = BLACK
COLOR_BODY_FILL = "#3a3a3a"  # dark grey — robot footprint
COLOR_BODY_EDGE = GREY_E
COLOR_BLOAT_FILL = "#9a9a9a"  # lighter grey — epsilon inflation halo
COLOR_BLOAT_EDGE = "#7a7a7a"
COLOR_CAPTION_BLOAT = "#7a4a00"  # warm tone to call attention to inflation


class RTDCoreAnimation(Scene):
    """Six-stage build-up of an RTD plan on a single position plane."""

    def construct(self):
        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------
        title = Text(
            "RTD Core: FRS → Slice → Body Tube → Tracking-Error Inflation",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ------------------------------------------------------------------
        # Axes — top-down (x, y) position plane
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[-0.5, 7.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=11,
            y_length=4.5,
            tips=True,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).next_to(title, DOWN, buff=0.3)

        x_lab = axes.get_x_axis_label("x").scale(0.85)
        y_lab = axes.get_y_axis_label("y").scale(0.85)

        self.play(Create(axes), Write(x_lab), Write(y_lab))
        self.wait(0.3)

        # Caption anchor — every step's caption swaps in here so the layout
        # stays stable as the build-up progresses.
        cap_anchor = (
            Rectangle(width=11.5, height=0.55, stroke_opacity=0, fill_opacity=0)
            .next_to(axes, DOWN, buff=0.25)
        )

        # Time samples used by every layer
        ts = np.linspace(0, 7, 140)

        # ------------------------------------------------------------------
        # 1) Initial-condition set X_0
        # ------------------------------------------------------------------
        ic_set = Ellipse(
            width=0.42, height=0.78,
            stroke_color=COLOR_IC_EDGE, stroke_width=2,
            fill_color=COLOR_IC, fill_opacity=0.65,
        ).move_to(axes.c2p(0, 0))

        cap_ic = Tex(
            r"$X_0$: initial-condition set with state uncertainty",
            font_size=34, color=COLOR_IC_EDGE,
        ).move_to(cap_anchor)

        self.play(GrowFromCenter(ic_set), FadeIn(cap_ic))
        self.wait(0.7)

        # ------------------------------------------------------------------
        # 2) Full FRS over k in [-1, 1] — fan-shaped tube
        # ------------------------------------------------------------------
        frs_top = [axes.c2p(t, y_of_t(t, +1.0) + frs_radius(t)) for t in ts]
        frs_bot = [axes.c2p(t, y_of_t(t, -1.0) - frs_radius(t)) for t in reversed(ts)]
        frs_region = Polygon(
            *(frs_top + frs_bot),
            stroke_color=COLOR_FRS, stroke_width=2,
            fill_color=COLOR_FRS, fill_opacity=0.18,
        ).set_z_index(-4)

        # Sample trajectory hairs to advertise that the FRS is a *family*
        sample_ks = np.linspace(-0.9, 0.9, 9)
        sample_trajs = VGroup(*[
            axes.plot(
                lambda t, k=k: y_of_t(t, k),
                x_range=[0, 7],
                stroke_color=COLOR_FRS_HAIR,
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            for k in sample_ks
        ]).set_z_index(-3)

        cap_frs = Tex(
            r"FRS: $\bigcup_{k \in [-1,\,1]} \mathrm{Reach}(X_0,\,k,\,t)$",
            font_size=34, color=COLOR_FRS,
        ).move_to(cap_anchor)

        self.play(
            FadeIn(frs_region),
            *[Create(tr) for tr in sample_trajs],
            FadeOut(cap_ic),
            FadeIn(cap_frs),
            run_time=2.2,
        )
        self.wait(0.9)

        # ------------------------------------------------------------------
        # 3) Slice the FRS at a specific k* — sub-tube
        # ------------------------------------------------------------------
        k_star = 0.45

        def slice_center(t):
            return y_of_t(t, k_star)

        slice_top = [axes.c2p(t, slice_center(t) + slice_radius(t)) for t in ts]
        slice_bot = [axes.c2p(t, slice_center(t) - slice_radius(t)) for t in reversed(ts)]
        slice_region = Polygon(
            *(slice_top + slice_bot),
            stroke_color=COLOR_SLICE_EDGE, stroke_width=2,
            fill_color=COLOR_SLICE_FILL, fill_opacity=0.55,
        ).set_z_index(-2)

        cap_slice = Tex(
            rf"Slice at $k^* = {k_star}$: parameterised sub-tube of the FRS",
            font_size=34, color=COLOR_SLICE_EDGE,
        ).move_to(cap_anchor)

        self.play(
            FadeOut(sample_trajs),
            FadeIn(slice_region),
            FadeOut(cap_frs),
            FadeIn(cap_slice),
            run_time=1.6,
        )
        self.wait(0.9)

        # ------------------------------------------------------------------
        # 4) COM trajectory inside the slice (black line)
        # ------------------------------------------------------------------
        com_curve = axes.plot(
            slice_center, x_range=[0, 7],
            color=COLOR_COM, stroke_width=4,
        ).set_z_index(2)

        cap_com = Tex(
            r"Black line: planning-model COM trajectory at $k^*$",
            font_size=34, color=COLOR_COM,
        ).move_to(cap_anchor)

        self.play(
            Create(com_curve),
            FadeOut(cap_slice),
            FadeIn(cap_com),
            run_time=1.4,
        )
        self.wait(0.7)

        # ------------------------------------------------------------------
        # 5) Body footprint tube around the COM (dark shade)
        # ------------------------------------------------------------------
        body_r = 0.13
        body_top = [axes.c2p(t, slice_center(t) + body_r) for t in ts]
        body_bot = [axes.c2p(t, slice_center(t) - body_r) for t in reversed(ts)]
        body_tube = Polygon(
            *(body_top + body_bot),
            stroke_color=COLOR_BODY_EDGE, stroke_width=1.5,
            fill_color=COLOR_BODY_FILL, fill_opacity=0.85,
        ).set_z_index(1)

        cap_body = Tex(
            r"Body-footprint tube around the COM (vehicle's physical extent)",
            font_size=34, color=COLOR_BODY_FILL,
        ).move_to(cap_anchor)

        self.play(
            FadeIn(body_tube),
            FadeOut(cap_com),
            FadeIn(cap_body),
            run_time=1.4,
        )
        self.wait(0.7)

        # ------------------------------------------------------------------
        # 6) epsilon-inflation: lighter halo around the body tube absorbs
        #    worst-case tracking error between planning model and true system.
        #    Bloat sits *behind* the body so the viewer reads it as a margin
        #    extending past the dark band on both sides.
        # ------------------------------------------------------------------
        epsilon = 0.10
        bloat_r = body_r + epsilon
        bloat_top = [axes.c2p(t, slice_center(t) + bloat_r) for t in ts]
        bloat_bot = [axes.c2p(t, slice_center(t) - bloat_r) for t in reversed(ts)]
        bloat_tube = Polygon(
            *(bloat_top + bloat_bot),
            stroke_color=COLOR_BLOAT_EDGE, stroke_width=1.5,
            fill_color=COLOR_BLOAT_FILL, fill_opacity=0.55,
        ).set_z_index(0)  # behind body tube, above slice

        cap_bloat = Tex(
            r"$\varepsilon$-inflation: worst-case tracking-error margin"
            r" \quad (planning model $\not\equiv$ true dynamics)",
            font_size=32, color=COLOR_CAPTION_BLOAT,
        ).move_to(cap_anchor)

        self.play(
            FadeIn(bloat_tube),
            FadeOut(cap_body),
            FadeIn(cap_bloat),
            run_time=2.0,
        )
        self.wait(0.6)

        # ------------------------------------------------------------------
        # Brief "pulse" on the inflation: nudge the bloat radius up and back
        # to emphasise that this is the tunable safety margin.
        # ------------------------------------------------------------------
        bloat_r_big = body_r + epsilon * 1.45
        big_top = [axes.c2p(t, slice_center(t) + bloat_r_big) for t in ts]
        big_bot = [axes.c2p(t, slice_center(t) - bloat_r_big) for t in reversed(ts)]
        bloat_tube_big = Polygon(
            *(big_top + big_bot),
            stroke_color=COLOR_BLOAT_EDGE, stroke_width=1.5,
            fill_color=COLOR_BLOAT_FILL, fill_opacity=0.55,
        ).set_z_index(0)

        # Grow then shrink — pulse twice to drive the point home
        bloat_back = Polygon(
            *(bloat_top + bloat_bot),
            stroke_color=COLOR_BLOAT_EDGE, stroke_width=1.5,
            fill_color=COLOR_BLOAT_FILL, fill_opacity=0.55,
        ).set_z_index(0)

        self.play(Transform(bloat_tube, bloat_tube_big), run_time=0.7)
        self.play(Transform(bloat_tube, bloat_back), run_time=0.7)

        self.wait(2.5)
