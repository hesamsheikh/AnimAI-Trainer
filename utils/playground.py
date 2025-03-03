from manim import *
import numpy as np
from utils.bounding_box import create_bounding_box, get_bounding_box, check_mobject_overlap

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
        cosine_label = MathTex(r"y = \cos(x)").next_to(axes, UP, buff=0.5)

        # Explanation text
        explanation = MathTex(r"\text{Derivative of } \cos(x) \text{ is } -\sin(x)")
        explanation.to_edge(UP, buff=1)

        # Tangent line at a given point
        x0 = 1  # Initial point
        tan_slope = -np.sin(x0)  # Derivative of cos(x) is -sin(x)
        tangent_line = axes.plot(lambda x: tan_slope * (x - x0) + np.cos(x0), color=YELLOW)

        # Moving dot on cosine curve
        dot = Dot(point=axes.c2p(x0, np.cos(x0)), color=RED)

        # Slope text
        slope_text = MathTex(r"\text{Slope} = -\sin(x)").to_edge(DOWN)

        # Create bounding boxes for all objects
        axes_with_box = create_bounding_box(axes)
        labels_with_box = create_bounding_box(labels)
        cosine_graph_with_box = create_bounding_box(cosine_graph)
        cosine_label_with_box = create_bounding_box(cosine_label)
        explanation_with_box = create_bounding_box(explanation)
        tangent_line_with_box = create_bounding_box(tangent_line)
        dot_with_box = create_bounding_box(dot)
        slope_text_with_box = create_bounding_box(slope_text)

        # Add elements with their bounding boxes
        self.play(Create(axes_with_box), Write(labels_with_box))
        self.play(Create(cosine_graph_with_box), Write(cosine_label_with_box))
        self.play(Write(explanation_with_box))
        self.play(Create(dot_with_box))
        self.play(Create(tangent_line_with_box), Write(slope_text_with_box))

        # Check for potential overlaps between elements
        # Use check_mobject_overlap to detect overlaps between mobjects
        overlap_detected = False
        overlap_message = ""
        
        # Check all possible pairs of objects for overlaps
        objects = [dot, tangent_line, cosine_graph, cosine_label, explanation, slope_text]
        object_names = ["dot", "tangent_line", "cosine_graph", "cosine_label", "explanation", "slope_text"]
        
        for i in range(len(objects)):
            for j in range(i+1, len(objects)):
                if check_mobject_overlap(objects[i], objects[j]):
                    overlap_detected = True
                    if overlap_message:
                        overlap_message += ", "
                    overlap_message += f"{object_names[i]} & {object_names[j]}"
        
        # Create an overlap status indicator
        if overlap_detected:
            overlap_status = Text(f"Overlapping: {overlap_message}", color=YELLOW).scale(0.5)
        else:
            overlap_status = Text("Elements properly positioned", color=GREEN).scale(0.5)
        
        overlap_status.to_edge(UP+RIGHT)
        self.play(FadeIn(overlap_status))
        self.wait(1)
        
        # Animate the dot and tangent line moving along the curve
        for x_val in np.linspace(-PI, PI, 30):
            new_slope = -np.sin(x_val)
            new_tangent = axes.plot(lambda x: new_slope * (x - x_val) + np.cos(x_val), color=YELLOW)
            new_dot = Dot(point=axes.c2p(x_val, np.cos(x_val)), color=RED)
            
            # Create bounding boxes for the new objects
            new_tangent_with_box = create_bounding_box(new_tangent)
            new_dot_with_box = create_bounding_box(new_dot)
            
            slope_update = MathTex(f"\text{{Slope}} = {-np.sin(x_val):.2f}").to_edge(DOWN)
            slope_update_with_box = create_bounding_box(slope_update)
            
            self.play(
                Transform(tangent_line_with_box, new_tangent_with_box),
                Transform(dot_with_box, new_dot_with_box),
                Transform(slope_text_with_box, slope_update_with_box),
                run_time=0.2
            )
        
        self.wait(2)


# Example usage
class OverlapExampleScene(Scene):
    def construct(self):
        # Create objects
        circle = Circle(radius=1).shift(LEFT*4)  # Start far left
        text = Text("Testing overlap detection").scale(0.8).shift(RIGHT*2)  # Place text on the right
        
        # Create groups with bounding boxes
        circle_group = create_bounding_box(circle, color=RED)
        text_group = create_bounding_box(text, color=BLUE)
        
        # Add objects to scene
        self.add(circle_group, text_group)

        # Animate the objects appearing
        self.play(Create(circle_group), run_time=1)
        self.play(Create(text_group), run_time=1)
        # Create status text that will be updated
        status_text = Text("No overlap detected", color=GREEN).scale(0.7)
        status_text.to_edge(DOWN)
        
        # Check for overlaps initially
        if check_mobject_overlap(circle, text):
            status_text.become(Text("Objects are overlapping!", color=YELLOW).scale(0.7).to_edge(DOWN))
        
        self.play(FadeIn(status_text))
        self.wait(1)
        
        # Gradually move circle toward text to demonstrate overlap detection
        self.play(circle_group.animate.shift(RIGHT*3), run_time=3)
        
        # Check for overlaps after animation and update the text
        if check_mobject_overlap(circle, text):
            status_text.become(Text("Objects are overlapping!", color=YELLOW).scale(0.7).to_edge(DOWN))
        else:
            status_text.become(Text("No overlap detected", color=GREEN).scale(0.7).to_edge(DOWN))
        
        self.wait(1)
        self.play(FadeOut(status_text))
        
        # Fade out all objects
        self.play(
            FadeOut(circle_group),
            FadeOut(text_group),
            run_time=1
        )
        
        self.wait(1)
