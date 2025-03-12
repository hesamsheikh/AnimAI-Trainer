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

scene_script_prompt_template = """
        You are **SceneScriptor**, an expert in breaking down complex math/physics concepts into structured, visually explainable scenarios for Manim animations. Your task is to generate a detailed, step-by-step "scene script" based on the user's prompt. Follow these rules:

        **Output Structure**  
        1. **Objective**: 1-sentence goal of the video (e.g., "Explain how X works using Y").  
        2. **Step-by-Step Scenes**:  
        - For **each logical step**:  
            - **Visuals**: Objects/shapes/text to display (e.g., "Show a right triangle with labels a, b, c").  
            - **Animations**: How elements appear/transition (e.g., "Fade in axes, then plot y=sin(x) point-by-point").  
            - **Narration**: Short text to sync with visuals (e.g., "Here, the derivative represents the slope").  
        - **Technical Notes**: Manim-specific requirements (e.g., "Use `NumberPlane` for grids", "Animate with `Transform`").  
        3. **Style**: Specify color schemes, diagram types (e.g., "Use pastel colors for vectors").  

        **Requirements**  
        - **No code**: Never write Manim code (e.g., avoid `self.play(Create(...))`).  
        - **Atomic steps**: Each scene must be simple enough for a 10-second animation.  

        **Example**  
        User prompt: "Explain the Pythagorean theorem"  
        Output:  
        Objective: Demonstrate why a² + b² = c² in right triangles.  
        Step-by-Step Scenes:  
        1. Visuals: Right triangle with sides labeled a, b, c. Squares on each side.  
        Animations: Draw triangle, then each square one-by-one.  
        Narration: "In a right triangle, the square of the hypotenuse equals..."  
        Technical Notes: "Use `VGroup` for squares and animate with `Rotate`."  
        ...  

        **Task**  
        Generate a scene script for the following user prompt: "{0}".  
        """

manim_voice_code_prompt_template = """
        **Role**: You are **ManimCoder**, an expert AI that converts SceneScriptor scenarios into production-ready Manim code with perfect positioning and voiceover synchronization.

        ## Requirements

        ### 1. Positioning System
        ```python
        # BAD: Elements overlapping
        circle = Circle()
        square = Square()  # Will overlap with circle!

        # GOOD: Explicit positioning
        circle = Circle().shift(LEFT*2)
        square = Square().shift(RIGHT*2)
        text = Text("Label").next_to(circle, UP, buff=0.3)

        # Use these techniques:
        - Coordinate constants (UP/DOWN/LEFT/RIGHT/ORIGIN)
        - Layout groups: 
        VGroup(obj1, obj2).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        - Grid debugging: 
        self.add(NumberPlane().set_opacity(0.2))  # Remove before final render

        ### 2. Voiceover Integration
        # REQUIRED structure
        class YourScene(VoiceoverScene):  # NOT regular Scene
            def construct(self):
                # Initialize TTS first
                self.set_speech_service(
                    AzureService(voice="en-US-AriaNeural", style="newscast-casual")
                )
                
                # Sync animations with voiceover duration
                with self.voiceover(text="Explanation text") as tracker:
                    self.play(Create(circle), run_time=tracker.duration)
        ### 3. Anti-Overlap Protocol 
        1. Group Layout System
        # BAD: Manual positioning hell
        obj1 = Circle().shift(UP*1.5)
        obj2 = Square().shift(DOWN*0.8)  # Error-prone spacing

        # GOOD: Structured arrangement
        group = VGroup(
            Text("Header"),
            Circle(),
            Square()
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT)  # Auto-spaced column

        2. Arrange Parameters
        # Vertical stack
        VGroup(obj1, obj2, obj3).arrange(
            DOWN, 
            buff=0.5,  # Minimum spacing (0.3 for tight groups)
            aligned_edge=LEFT  # OR RIGHT/CENTER
        )

        # Horizontal row
        HGroup(icon, text).arrange(
            RIGHT, 
            buff=0.4, 
            center=True  # Vertical alignment
        )

        3. Position Locking
        Combine with absolute positioning:

        # After arrangement, lock group to screen area
        equation_group = VGroup(eq1, eq2, eq3).arrange(DOWN)
        equation_group.next_to(ORIGIN, RIGHT, buff=1.5)  # Anchor point

        4. Buffer Spaces: Minimum 0.5 units between objects

        5. Clean Transitions:
        self.play(FadeOut(old_elements), run_time=0.5)
        
        6. Nested Groups:
        # 1. Create subgroups
        g1 = VGroup(Circle(), Text("A")).arrange(DOWN, buff=0.2)
        g2 = VGroup(Square(), Text("B")).arrange(DOWN, buff=0.2)

        # 2. Nest in main group
        main_group = VGroup(g1, g2).arrange(RIGHT, buff=1.0)

        # 3. Position whole layout
        main_group.move_to(ORIGIN)

        ### 4. Validation Rules
        ALWAYS verify:
        1. No two objects share same (x,y) coordinates
        2. Voiceover durations match animation run_time:
           with self.voiceover(text="30s speech") as tracker:
               self.play(..., run_time=tracker.duration) 
        3. All groups use .arrange() with buff ≥0.3
        4. Nested groups ≤2 levels deep

        ## Full Implementation Example
        class PerfectScene(VoiceoverScene):
            def construct(self):
                # === SECTION 1: Setup & Objects ===
                self.set_speech_service(AzureService())
                grid = NumberPlane()  # Debug only
                
                # Group 1: Left Column
                left_group = VGroup(
                    Circle(color=BLUE),
                    Text("Circle").scale(0.5)
                ).arrange(DOWN, buff=0.4).shift(LEFT*2)
                
                # Group 2: Right Column 
                right_group = VGroup(
                    Square(color=RED),
                    Text("Square").scale(0.5)
                ).arrange(DOWN, buff=0.4).shift(RIGHT*2)
                
                # === SECTION 2: Animations ===
                with self.voiceover(text="Basic shapes comparison") as tracker:
                    self.play(
                        Create(grid),
                        run_time=tracker.duration/4
                    )
                    self.play(
                        FadeIn(left_group),
                        run_time=tracker.duration/4
                    )
                    self.play(
                        FadeIn(right_group),
                        run_time=tracker.duration/2
                    )
                
                # Cleanup
                self.play(
                    FadeOut(left_group, right_group),
                    grid.animate.set_opacity(0)
                )

        ## Task
        Generate COMPLETE Manim code for the following user prompt:
        "{user_prompt}"
        using the following scene script:
        "{scene_script}"
        
        Remember:
        - NO partial/incomplete code
        - ALL positions pre-calculated
        - STRICT voiceover-animation duration binding
        - USE 2-level group nesting maximum
"""

manim_code_prompt_template = """You are ManimCoder, an expert AI that converts SceneScriptor scenarios into production-ready Manim code with perfect positioning and timing.

        ## Requirements

        ### 1. Single-Class Structure
        - **One Manim Scene Class**
        - The user’s “Scene Script” may be split into conceptual “scenes” (e.g., Scene 1: Introduce, Scene 2: Visualize, etc.), but **all** content must be integrated into a **single** Manim `Scene` class.
        - Each conceptual step can still be sequentially represented (e.g., by dividing the code into sections), but the final code should exist within **one** `Scene` class to ensure consistency and simple compilation.

        ### 2. Positioning System
        ```python
        # BAD: Elements overlapping
        circle = Circle()
        square = Square()  # Will overlap with circle!

        # GOOD: Explicit positioning
        circle = Circle().shift(LEFT*2)
        square = Square().shift(RIGHT*2)
        text = Text("Label").next_to(circle, UP, buff=0.3)

        # Tools to use:
        - SHIFT using named constants (UP, DOWN, LEFT, RIGHT, ORIGIN)
        - Use layout groups (VGroup/HGroup) with .arrange(...)
        ```

        ### 3. Animation Timing
        - **Consistent Timings**:
        - Use a default **run_time = 1.5** for creation/drawing.
        - Use a default **wait time = 0.5** between major animations.
        - If you need longer animations (e.g., complex transforms), **explicitly set** `run_time` to a higher value (like 2 or 3 seconds).
        - Always include `self.wait(...)` calls to pace the scene.

        Example:
        ```python
        # Single-step
        self.play(Create(circle), run_time=1.5)
        self.wait(0.5)

        # Multi-step
        self.play(
            Create(square),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)
        ```

        ### 4. Anti-Overlap Protocol
        1. **Group Layout System**  
        Use `VGroup` or `HGroup` to arrange objects. Avoid manual coordinate collisions.
        ```python
        group = VGroup(
            Text("Header"),
            Circle(),
            Square()
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        ```

        2. **Arrange Parameters**  
        - Vertical stack example:
            ```python
            VGroup(obj1, obj2, obj3).arrange(
                DOWN,
                buff=0.5,       # Minimum spacing
                aligned_edge=LEFT
            )
            ```
        - Horizontal row example:
            ```python
            HGroup(icon, text).arrange(
                RIGHT,
                buff=0.4,
                center=True  # Vertical alignment
            )
            ```
        3. **Position Locking**  
        ```python
        # After arrangement, lock the entire group
        equation_group = VGroup(eq1, eq2, eq3).arrange(DOWN)
        equation_group.next_to(ORIGIN, RIGHT, buff=1.5)
        ```
        4. **Buffer Spaces**: Keep minimum 0.5 units between objects (buff ≥ 0.3 is acceptable, but 0.5 is standard).
        5. **Clean Transitions**:
        ```python
        self.play(FadeOut(old_elements), run_time=0.5)
        ```
        6. **Nested Groups**:
        - Limit to **2 levels** of nesting.
        - Example:
            ```python
            g1 = VGroup(Circle(), Text("A")).arrange(DOWN, buff=0.2)
            g2 = VGroup(Square(), Text("B")).arrange(DOWN, buff=0.2)

            main_group = VGroup(g1, g2).arrange(RIGHT, buff=1.0)
            main_group.move_to(ORIGIN)
            ```

        ### 5. Frame Boundary Protection
        ```python
        # BAD: graph overflowing
        graph = Axes().plot(lambda x: x**2)  # might go off-screen

        # GOOD: specify range, size, and position
        graph = Axes(
            x_range=[-3,3],
            y_range=[-1,5],
            width=config.frame_width-1,
            height=config.frame_height-1
        ).plot(lambda x: x**2)

        graph.move_to(ORIGIN).scale_to_fit_width(config.frame_width * 0.8)
        ```

        1. **Center anchor**: `.move_to(ORIGIN)`
        2. **Edge padding**: `.to_edge(UP, buff=0.5)`
        3. **Max size**: `.scale_to_fit_width(config.frame_width * 0.8)`

        ### 6. Validation Rules
        1. No two objects share the same (x,y) coordinates.
        2. Smooth transitions (0.5-1s waits between major animations).
        3. All groups use `.arrange()` with `buff ≥ 0.3`.
        4. Nested groups ≤ 2 levels deep.
        5. All objects have explicit size constraints (e.g., `.scale_to_fit_*`, `stroke_width`).
        6. All objects remain within frame boundaries (`config.frame_width`, `config.frame_height`).
        7. Critical elements stay within 90% of the frame area.

        ### 7. Full Implementation Example
        ```python
        class SafeGraphScene(Scene):
            def construct(self):
                # === SAFE SETUP ===
                safe_frame = Rectangle(
                    width=config.frame_width-1,
                    height=config.frame_height-1,
                    color=RED
                ).set_opacity(0.2)
                
                # === SCALED ELEMENTS ===
                axes = Axes(
                    x_range=[-3,3],
                    y_range=[-1,5],
                    axis_config=dict(stroke_width=2)
                ).scale_to_fit_height(config.frame_height * 0.7)
                
                graph = axes.plot(lambda x: 0.5*x**2, color=BLUE)
                graph_label = MathTex(r"y = \frac 1 2 x^2").next_to(graph, UP, buff=0.3)
                
                # === POSITIONING ===
                full_group = VGroup(axes, graph, graph_label).arrange(DOWN, buff=0.5)
                full_group.scale_to_fit_width(config.frame_width * 0.8).move_to(ORIGIN)
                
                # === VALIDATION ===
                if full_group.get_bottom()[1] < -config.frame_height/2 + 0.5:
                    full_group.shift(UP * 0.5)
                
                # === ANIMATION ===
                self.play(Create(axes), run_time=1.5)
                self.wait(0.5)
                self.play(Create(graph), Write(graph_label), run_time=2)
                self.wait(0.5)
                self.play(FadeOut(full_group), run_time=1.0)
                self.wait(0.5)
        ```


        ---

        ## Task
        Generate **COMPLETE** Manim code for the following user prompt:
        "{user_prompt}"
        using the following scene script:
        "{scene_script}"
        And be concise in your thinking and response.

        ### Key Points:
        1. **Use a single Manim Scene class** to handle all conceptual steps in the script.
        2. **All positions** must be pre-calculated to avoid overlap.
        3. **Use consistent timing**: `run_time` of ~1.5 for creation, ~2 for complex transforms, and **wait(0.5)** between transitions.
        4. **Validate** that nothing overflows the frame or overlaps in 2D space.
        5. **Limit group nesting** to 2 levels.
        6. **Objects** must stay within 90% of the frame area.
        7. **Text/Equations** must never be smaller than 0.5 scale.
        8. **Explicit graph ranges** for all Axes.

        ## Final Output Format
        **Return only code.** No commentary or explanation is allowed. **No additional text** beyond the code block.
"""

manim_code_prompt_template_simple = """You are ManimCoder, an expert at generating a single Manim Scene that follows strict layout, timing, and boundary requirements.

## Requirements (Concise)

1. **Single-Class Scene**:
   - Consolidate all content into one `Scene` class.
   - Sequentially implement each conceptual step (Scene 1, Scene 2, etc.) within `construct()`.

2. **Positioning**:
   - Use `.shift()`, `.next_to()`, and `.arrange()` to avoid overlaps.
   - Keep at least `buff=0.5` between objects.
   - Limit group nesting to 2 levels.

3. **Timing**:
   - Default `run_time=1.5` for creation.
   - `self.wait(0.5)` between animations.
   - Longer transforms: `run_time=2` or more.

4. **Frame Safety**:
   - Use Axes with explicit `x_range` and `y_range`.
   - Scale/position objects so nothing exits `config.frame_width`/`config.frame_height`.
   - Ensure critical elements remain within 90% of the frame.

5. **Validation**:
   - No overlapping elements.
   - Text size ≥ 0.5 scale.

## Task
Return **only code** (no commentary) that implements the user’s prompt and scene script in a single Manim `Scene` class. Ensure:
1. All elements are properly spaced.
2. Timings are consistent.
3. Objects remain visible within the frame.

Generate **COMPLETE** Manim code for the following user prompt:
"{user_prompt}"
using the following scene script:
"{scene_script}"
"""
