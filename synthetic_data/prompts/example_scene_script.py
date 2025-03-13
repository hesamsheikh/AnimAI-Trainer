"""
Example scene script for a Manim animation explaining derivatives using geometric intuition.
This serves as a reference for the expected output format from the SceneScriptor.
"""

exmaple_scene_script = """## Scene Script: Geometric Intuition of Derivatives

**Objective:** Explain how the derivative represents the instantaneous rate of change (slope of the tangent line) of a function.

**Step-by-Step Scenes:**

1. **Visuals:** Cartesian plane with axes. A simple curve (e.g., y = x^2) plotted on the plane.
   **Animations:** Fade in axes, then draw the curve.
   **Narration:** "Let's consider a function, a curve on a graph."

2. **Visuals:** Same curve. A specific point 'P' marked on the curve.
   **Animations:** Highlight the point P on the curve.
   **Narration:** "We want to understand how the function changes *at* this specific point."

3. **Visuals:** Curve, point P, and a secant line drawn through P and another nearby point 'Q'. 'Q' should be draggable. Label the points P and Q.
   **Animations:** Draw the secant line PQ. Animate point Q moving along the curve.
   **Narration:** "We can approximate this change by drawing a secant line."

4. **Visuals:** Curve, point P, secant line PQ, and labels for the rise and run of the secant line. Show the slope calculation (rise/run) as text.
   **Animations:** Highlight the 'rise' and 'run' of the secant line. Display "Slope = Δy/Δx".
   **Narration:** "The slope of this line gives us the average rate of change between the two points."

5. **Visuals:** Curve, point P, secant line PQ. Animate point Q moving *closer* to point P. The secant line rotates, becoming less and less slanted.
   **Animations:** Point Q smoothly approaches P. The secant line rotates correspondingly.
   **Narration:** "As point Q gets closer and closer to P…"

6. **Visuals:** Curve, point P, and the tangent line at point P.
   **Animations:** As Q reaches P, the secant line transforms into the tangent line.
   **Narration:** "...the secant line becomes the tangent line."

7. **Visuals:** Curve, point P, tangent line. Highlight the slope of the tangent line.  Display the derivative notation: dy/dx.
   **Animations:** Highlight the slope of the tangent line. Display "dy/dx".
   **Narration:** "The slope of the tangent line is the *instantaneous* rate of change – the derivative."

8. **Visuals:**  A series of curves, each with a tangent line at a specific point. Show the varying slopes of the tangent lines.
   **Animations:** Cycle through different curves and points, highlighting how the tangent line (and therefore the derivative) changes.
   **Narration:** "The derivative is different at every point on the curve, representing the rate of change at that specific location."

**Style:**

*   Use a clean, modern aesthetic.
*   Color scheme: Blue for the curve, green for the secant line, red for the tangent line.
*   Use smooth transitions between animations.
*   Highlight important elements with a subtle glow effect.
*   Keep text concise and easy to read.
""" 