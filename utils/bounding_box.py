from manim import Rectangle, VGroup, RED, Mobject 
from manim import Text, MathTex, Tex, SingleStringMathTex
import inspect


# Helper function for creating bounding boxes
def create_bounding_box(obj, color=RED):
    """
    Make a bounding box around an object and 
    return a VGroup containing the object and its bounding box
    """
    center = obj.get_center()
    width = obj.width
    height = obj.height
    
    # Create rectangle based on object dimensions
    rect = Rectangle(
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2,
        fill_opacity=0
    ).move_to(center)
    
    # Group the object with its bounding box
    return VGroup(obj, rect)


def get_bounding_box(obj):
    """
    Get the coordinates of the bounding box of an object
    """
    center = obj.get_center()
    width = obj.width
    height = obj.height
    return center, width, height


def if_box_overlap(bbox1, bbox2):
    """
    Check if two bounding boxes overlap.
    
    Args:
        bbox1 (tuple): First bounding box in format (center, width, height)
                      where center is a numpy array or Point with x,y coordinates
        bbox2 (tuple): Second bounding box in format (center, width, height)
                      where center is a numpy array or Point with x,y coordinates
    
    Returns:
        bool: True if the bounding boxes overlap, False otherwise
    """
    center1, width1, height1 = bbox1
    center2, width2, height2 = bbox2
    
    # Calculate half-dimensions
    half_width1, half_height1 = width1/2, height1/2
    half_width2, half_height2 = width2/2, height2/2
    
    # Calculate the x and y distances between centers
    dx = abs(center1[0] - center2[0])
    dy = abs(center1[1] - center2[1])
    
    # Check for overlap
    if dx < (half_width1 + half_width2) and dy < (half_height1 + half_height2):
        return True
    
    return False

def check_two_mobjects_overlap(mobject1: Mobject, mobject2: Mobject):
    """
    Check if two Manim mobjects overlap using their bounding boxes.
    
    Args:
        mobject1 (Mobject): First Manim mobject
        mobject2 (Mobject): Second Manim mobject
    
    Returns:
        bool: True if the mobjects overlap, False otherwise
    """
    # Get bounding boxes for both mobjects
    bbox1 = get_bounding_box(mobject1)
    bbox2 = get_bounding_box(mobject2)
    
    # Check for overlap
    return if_box_overlap(bbox1, bbox2)


def get_mobject_name(mobject, frame=None):
    """
    Dynamically find the variable name of a mobject by inspecting the caller's scope.
    
    Args:
        mobject: The mobject to find the name for
        frame: Optional frame to inspect (defaults to caller's frame)
        
    Returns:
        str: The variable name, or repr(mobject) if name not found
    """
    if frame is None:
        # Get the caller's frame (skip this function's frame)
        frame = inspect.currentframe().f_back
    
    # Look through local and global variables
    for name, obj in frame.f_locals.items():
        if obj is mobject:  # Use 'is' for identity comparison
            return name
            
    for name, obj in frame.f_globals.items():
        if obj is mobject:
            return name
    
    # If we can't find the name, return None
    return None


def check_mobject_overlaps(scene):
    """
    Check for overlaps between all pairs of mobjects in a list.
    
    Args:
        mobjects (list): List of Manim mobjects to check for overlaps
        
    Returns:
        list: List of tuples containing pairs of overlapping mobjects
    """
    overlapping_pairs = []

    # Get the caller's frame for variable name lookup
    caller_frame = inspect.currentframe().f_back
    
    mobjects = scene.mobjects
    # Check all possible pairs, but only for text-like mobjects
    for i in range(len(mobjects)):
        # Skip if not a text-like or group mobject
        if not isinstance(mobjects[i], (Text, MathTex, Tex, SingleStringMathTex, VGroup)):
            continue

        for j in range(i + 1, len(mobjects)):
            if check_two_mobjects_overlap(mobjects[i], mobjects[j]):
                name_i = get_mobject_name(mobjects[i], caller_frame)
                name_j = get_mobject_name(mobjects[j], caller_frame)
                if name_i and name_j:
                    overlapping_pairs.append((name_i, name_j))
    return overlapping_pairs
