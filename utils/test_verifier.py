from verifier import syntax_checker

# Example of valid Manim code
valid_code = """
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
"""

# Example of invalid Manim code (missing Scene subclass)
invalid_code_1 = """
from manim import *

def create_animation():
    square = Square(color=BLUE)
    # This won't work because it's not in a Scene subclass
    self.play(Create(square))
"""

# Example of invalid Manim code (syntax error)
invalid_code_2 = """
from manim import *

class BrokenScene(Scene):
    def construct(self)
        # Missing colon after function definition
        square = Square(color=BLUE)
        self.play(Create(square))
"""

# Example of invalid Manim code (missing import)
invalid_code_3 = """
class SimpleScene(Scene):
    def construct(self):
        square = Square()
        self.play(Create(square))
"""

def test_verifier():
    print("Testing valid Manim code:")
    is_valid, error_message = syntax_checker(valid_code)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error_message}")
    print()

    print("Testing invalid code (missing Scene subclass):")
    is_valid, error_message = syntax_checker(invalid_code_1)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error_message}")
    print()

    print("Testing invalid code (syntax error):")
    is_valid, error_message = syntax_checker(invalid_code_2)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error_message}")
    print()

    print("Testing invalid code (missing import):")
    is_valid, error_message = syntax_checker(invalid_code_3)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error_message}")

if __name__ == "__main__":
    test_verifier() 