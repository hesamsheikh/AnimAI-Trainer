from manim import *
import numpy as np

class CosineDerivative(Scene):
    def construct(self):
        # Set up the axes
        axes = Axes(
            x_range=[-PI, PI, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=7,
            y_length=5,
            axis_config={"color": BLUE},
        )

        # Labels for the axes
        labels = axes.get_axis_labels(x_label=MathTex("x"), y_label=MathTex("y"))
        
        # Cosine function graph
        cosine_graph = axes.plot(lambda x: np.cos(x), color=WHITE)
        cosine_label = MathTex("y = \cos(x)").next_to(axes, UP, buff=0.5)

        # Explanation text
        explanation = MathTex("\text{Derivative of } \cos(x) \text{ is } -\sin(x)")
        explanation.to_edge(UP, buff=1)

        # Tangent line at a given point
        x0 = 1  # Initial point
        tan_slope = -np.sin(x0)  # Derivative of cos(x) is -sin(x)
        tangent_line = axes.plot(lambda x: tan_slope * (x - x0) + np.cos(x0), color=YELLOW)

        # Moving dot on cosine curve
        dot = Dot(point=axes.c2p(x0, np.cos(x0)), color=RED)

        # Slope text
        slope_text = MathTex("\text{Slope} = -\sin(x)").to_edge(DOWN)

        self.play(Create(axes), Write(labels))
        self.play(Create(cosine_graph), Write(cosine_label))
        self.play(Write(explanation))
        self.play(Create(dot))
        self.play(Create(tangent_line), Write(slope_text))
        
        # Animate the dot and tangent line moving along the curve
        for x_val in np.linspace(-PI, PI, 30):
            new_slope = -np.sin(x_val)
            new_tangent = axes.plot(lambda x: new_slope * (x - x_val) + np.cos(x_val), color=YELLOW)
            new_dot = Dot(point=axes.c2p(x_val, np.cos(x_val)), color=RED)
            slope_update = MathTex(f"\text{{Slope}} = {-np.sin(x_val):.2f}").to_edge(DOWN)
            
            self.play(Transform(tangent_line, new_tangent), Transform(dot, new_dot), Transform(slope_text, slope_update), run_time=0.2)
        
        self.wait(2)