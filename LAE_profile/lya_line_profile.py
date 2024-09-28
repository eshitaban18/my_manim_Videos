from manim import *
import numpy as np


def make_particles(num, cenx, ceny, radius=.5):
    seed = 7
    r = radius * np.sqrt(np.random.rand(num))
    seed = 143
    theta = np.random.rand(num) * 2 * np.pi
    x = cenx + r * np.cos(theta)
    y = ceny + r * np.sin(theta)
    mini_circ = VGroup(*[Dot().shift(x[i] * LEFT + y[i] * UP)
                         for i in range(num)])
    return mini_circ


def make_particles_fly(num, cenx, ceny, radius):
    r = radius
    theta = np.linspace(0, 2, num) * np.pi
    x = cenx + r * np.cos(theta)
    y = ceny + r * np.sin(theta)
    mini_circ = VGroup(*[Dot().shift(x[i] * LEFT + y[i] * UP)
                         for i in range(num)])
    return mini_circ


def show_arrow(num, cenx, ceny, length=2, inflow=False):

    if inflow:
        r2 = 1
        theta = np.linspace(0, 2, num) * np.pi
        x2 = cenx + r2 * np.cos(theta)
        y2 = ceny + r2 * np.sin(theta)

        r1 = length
        x1 = cenx + r1 * np.cos(theta)
        y1 = ceny + r1 * np.sin(theta)
        arrows = VGroup(*[Arrow(start=x1[i] * LEFT + y1[i] * UP,
                                end=x2[i] * LEFT + y2[i] * UP,
                                buff=.7, color=GOLD) for i in range(num)])
    else:
        r2 = length
        theta = np.linspace(0, 2, num) * np.pi
        x2 = cenx + r2 * np.cos(theta)
        y2 = ceny + r2 * np.sin(theta)

        r1 = 1
        x1 = cenx + r1 * np.cos(theta)
        y1 = ceny + r1 * np.sin(theta)
        arrows = VGroup(*[Arrow(start=x1[i] * LEFT + y1[i] * UP,
                                end=x2[i] * LEFT + y2[i] * UP,
                                buff=.7, color=GOLD) for i in range(num)])
    return arrows


def read_data(filename):
    lamb, flux = np.loadtxt(filename).T
    return lamb, flux


class Lya(Scene):

    def construct(self):

        # write my Name
        name = Text("Made by Eshita Banerjee", color=WHITE).scale(.2).to_edge(DR)
        self.add(name)

        # make the galaxy
        cenx = 4
        circle = Circle(color=DARK_BROWN, fill_opacity=.4,
                        radius=1.5).shift(cenx * LEFT)
        self.play(Create(circle), run_time=2)

        # plot_line_profile
        ax = Axes()
        l1, f1 = read_data("./1D_gauss_again.txt")
        line_gauss = ax.plot_line_graph(
            l1, f1*14, add_vertex_dots=False, stroke_width=8).shift(RIGHT * 4 + DOWN * 1)
        self.add(line_gauss)
        self.wait(1)

        # add dots and 2D gaussian
        mini_circ = make_particles(num=30, cenx=cenx, ceny=0)
        # these will in/out flow
        cen_circ = make_particles(num=20, cenx=cenx, ceny=0, radius=0)
        l2, f2 = read_data("./2D_gauss.txt")
        line_2dgauss = ax.plot_line_graph(
            l2, f2*5, add_vertex_dots=False, stroke_width=6,
        ).set_sheen_direction(LEFT).shift(RIGHT * 4 + DOWN * 1).set_color(color=[PURE_RED, PURE_BLUE])
        self.add(mini_circ, cen_circ)
        self.wait(1)
        self.play(Transform(line_gauss, line_2dgauss))
        self.wait(2)

        # -----------------------------------------------
        # outflow
        # -----------------------------------------------
        out_circ = make_particles_fly(num=20, cenx=cenx, ceny=0, radius=3)
        arrow_out = show_arrow(num=5, cenx=cenx, ceny=0)
        outvelo_text = Text('[0, V]', color=PURE_GREEN).next_to(circle, 2.7*UP)
        outflow_text = Text('Outflow').next_to(circle, 6.6 *UP)
        self.play(Transform(cen_circ, out_circ),
                  FadeIn(arrow_out, run_time=.5))
        self.add(outvelo_text, outflow_text)
        self.wait(1)

        # show arrow
        arrow_show1 = Arrow(start=3*RIGHT + 3*DOWN, end=3 *
                            RIGHT + DOWN, color=YELLOW)
        self.add(arrow_show1)
        self.wait(1)

        # show red peak
        l3, f3 = read_data("./red_peak.txt")
        red_peak = ax.plot_line_graph(
            l3, f3*5, add_vertex_dots=False, stroke_width=6
        ).set_sheen_direction(LEFT).shift(RIGHT * 4 + DOWN * 1).set_color(color=[PURE_RED, PURE_BLUE])
        self.play(Transform(line_2dgauss, red_peak), FadeOut(line_gauss))

        # show Title
        title1 = Text('Red-peak LAE ', color=RED).next_to(red_peak, UP)
        self.add(title1)

        self.wait(3)
        self.remove(outvelo_text, outflow_text, arrow_out)

        # -----------------------------------------------
        # inflow
        # -----------------------------------------------
        in_circ = make_particles_fly(num=20, cenx=cenx, ceny=0, radius=1)
        arrow_in = show_arrow(num=5, cenx=cenx, ceny=0, inflow=True)
        invelo_text = Text('[-V, 0]', color=PURE_GREEN).next_to(circle, 3*DOWN)
        inflow_text = Text('Inflow').next_to(circle, 6.6 * UP)
        self.play(FadeOut(cen_circ), Transform(
            out_circ, in_circ), FadeIn(arrow_in, run_time=.5))
        self.add(invelo_text, inflow_text)
        self.wait(1)

        # show arrow
        arrow_show2 = Arrow(start=5*RIGHT + 3*DOWN, end=5 *
                            RIGHT + DOWN, color=YELLOW)
        self.play(Transform(arrow_show1, arrow_show2))
        self.wait(1)

        # show red peak
        l4, f4 = read_data("./blue_peak.txt")
        blue_peak = ax.plot_line_graph(
            l4, f4*5, add_vertex_dots=False, stroke_width=6
        ).set_sheen_direction(LEFT).shift(RIGHT * 4 + DOWN * 1).set_color(color=[PURE_RED, PURE_BLUE])
        self.play(Transform(red_peak, blue_peak), FadeOut(line_2dgauss))

        # show Title
        title2 = Text('Blue-peak LAE ', color=BLUE).next_to(blue_peak, UP)
        self.play(Transform(title1, title2))
        self.wait(3)
