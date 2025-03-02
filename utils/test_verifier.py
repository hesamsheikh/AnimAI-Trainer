import time
import os

# Import from utils directly since it's at the project root level
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

test_code_1 = """
from manim import * class MyScene(Scene): def construct(self): polygon = RegularPolygon(n=8, radius=2, color=PINK) self.add(polygon)
"""

def test_code(description, code):
    print(f"Testing {description}:")
    is_valid, error_message = syntax_checker(code)
    print(f"Valid: {is_valid}")
    if not is_valid:
        # Print only first 30 characters of error message
        truncated_error = error_message[:30] + "..." if len(error_message) > 30 else error_message
        print(f"Error: {truncated_error}")
    print()

def test_verifier():
    test_code("valid Manim code", valid_code)
    start_time = time.time()
    
    test_code("valid Manim code", valid_code)
    test_code("invalid code (missing Scene subclass)", invalid_code_1)
    test_code("invalid code (syntax error)", invalid_code_2)
    test_code("invalid code (missing import)", invalid_code_3)
    test_code("test_code", test_code_1)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    test_verifier() 