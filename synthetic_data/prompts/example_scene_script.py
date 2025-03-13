"""
Example scene script for a Manim animation explaining derivatives using geometric intuition.
This serves as a reference for the expected output format from the SceneScriptor.
"""

exmaple_scene_script = """
### Scene Script: Explaining Derivatives Using Geometric Intuition

---

#### **Objective**:
Demonstrate how the derivative of a function represents the slope of its tangent line at any point, using geometric visualization.

---

#### **Step-by-Step Scenes**:

---

### **Scene 1: Introduce the Function and Its Graph**
- **Visuals**:
  - A coordinate plane (`NumberPlane`) with x and y axes.
  - A smooth curve representing a function \( f(x) \) (e.g., \( f(x) = x^2 \)).
  - A point \( P \) on the curve labeled \( (x, f(x)) \).
- **Animations**:
  - Fade in the coordinate plane.
  - Draw the curve \( f(x) \) smoothly from left to right.
  - Highlight point \( P \) with a dot and label it.
- **Narration**:
  "Consider a function \( f(x) \). At any point \( P \) on its graph, we can explore how the function changes."
- **Technical Notes**:
  - Use `NumberPlane` for the grid.
  - Animate the curve with `Create`.
  - Use `Dot` and `MathTex` for point \( P \).

---

### **Scene 2: Introduce a Nearby Point**
- **Visuals**:
  - A second point \( Q \) on the curve, close to \( P \), labeled \( (x + h, f(x + h)) \).
  - A dashed line connecting \( P \) and \( Q \).
- **Animations**:
  - Fade in point \( Q \) and the dashed line.
  - Animate \( Q \) moving closer to \( P \) along the curve.
- **Narration**:
  "To understand the rate of change at \( P \), we look at a nearby point \( Q \). As \( Q \) gets closer to \( P \), the line between them approximates the tangent."
- **Technical Notes**:
  - Use `DashedLine` for the connecting line.
  - Animate \( Q \) with `MoveAlongPath`.

---

### **Scene 3: Calculate the Slope of the Secant Line**
- **Visuals**:
  - A right triangle formed by the horizontal distance \( h \) and vertical distance \( f(x + h) - f(x) \).
  - Label the horizontal side \( h \) and the vertical side \( \Delta f \).
- **Animations**:
  - Draw the triangle beneath the dashed line.
  - Label the sides with `MathTex`.
- **Narration**:
  "The slope of the line between \( P \) and \( Q \) is the ratio of the vertical change \( \Delta f \) to the horizontal change \( h \)."
- **Technical Notes**:
  - Use `Polygon` for the triangle.
  - Animate labels with `Write`.

---

### **Scene 4: Shrink \( h \) to Approach the Tangent Line**
- **Visuals**:
  - Animate \( Q \) moving closer to \( P \), shrinking \( h \) and \( \Delta f \).
  - The dashed line becomes the tangent line at \( P \).
- **Animations**:
  - Smoothly move \( Q \) toward \( P \).
  - Transform the dashed line into a solid tangent line.
- **Narration**:
  "As \( h \) approaches zero, the secant line becomes the tangent line, and the slope represents the derivative \( f'(x) \)."
- **Technical Notes**:
  - Use `Transform` to morph the dashed line into the tangent line.
  - Use `ValueTracker` to animate \( h \) shrinking.

---

### **Scene 5: Highlight the Derivative as the Slope**
- **Visuals**:
  - The tangent line at \( P \) with its slope labeled \( f'(x) \).
  - A small slope triangle on the tangent line with labels \( \Delta x \) and \( \Delta y \).
- **Animations**:
  - Fade in the slope triangle and label.
  - Highlight the tangent line and its slope.
- **Narration**:
  "The derivative \( f'(x) \) is the slope of the tangent line at \( P \), representing the instantaneous rate of change of the function."
- **Technical Notes**:
  - Use `MathTex` for \( f'(x) \).
  - Animate the slope triangle with `Create`.

---

### **Scene 6: Generalize the Concept**
- **Visuals**:
  - Multiple points on the curve, each with its own tangent line and slope label.
  - A graph of the derivative \( f'(x) \) below the original function.
- **Animations**:
  - Fade in tangent lines and slopes at multiple points.
  - Plot \( f'(x) \) point-by-point below \( f(x) \).
- **Narration**:
  "By repeating this process for every point on the curve, we can construct the derivative function \( f'(x) \), which describes how \( f(x) \) changes at every point."
- **Technical Notes**:
  - Use `VGroup` for tangent lines and slopes.
  - Animate \( f'(x) \) with `Plot`.

---

#### **Style**:
- **Color Scheme**:
  - Use pastel colors: light blue for the curve, orange for tangent lines, and green for labels.
- **Diagram Types**:
  - Use smooth curves for \( f(x) \) and straight lines for tangents.
  - Keep labels minimal and clear.

---

This script provides a clear, step-by-step breakdown of the geometric intuition behind derivatives, suitable for a Manim animation.
""" 