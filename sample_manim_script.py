from manim import *

class SquareToCircle(Scene):
    def construct(self):
        # Create a square
        square = Square(color=BLUE, fill_opacity=0.5)
        
        # Display the square
        self.play(Create(square))
        
        # Transform the square into a circle
        self.play(Transform(square, Circle(color=RED, fill_opacity=0.5)))
        
        # Wait for 1 second
        self.wait(1)


class MathExample(Scene):
    def construct(self):
        # Create a mathematical equation
        equation = MathTex("e^{i\\pi} + 1 = 0")
        
        # Display the equation with a fade in animation
        self.play(FadeIn(equation))
        
        # Scale the equation
        self.play(equation.animate.scale(2))
        
        # Move the equation
        self.play(equation.animate.shift(UP * 2))
        
        # Wait for 2 seconds
        self.wait(2)


# To run this script using the Manim CLI:
# manim -pql sample_manim_script.py SquareToCircle
# manim -pql sample_manim_script.py MathExample 