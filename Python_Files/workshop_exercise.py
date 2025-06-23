# =====================================================
# SKYLINE 2D PACKING ALGORITHM
# Step-by-Step Implementation
# =====================================================

# Import libraries for visualization
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# =====================================================
# STEP 1: Basic Skyline Class 
# =====================================================


class Skyline:
    """
    Skyline data structure for 2D rectangle packing.
    
    The skyline tracks the upper boundary (horizon) of all placed rectangles.
    Think of it like a city skyline - we track the height at different X positions.
    
    """
    
    def __init__(self):
        """
        Initialize skyline with single point at origin.
        
        We start with one point (0,0) representing the bottom-left corner
        of our empty container. As rectangles are added, this list grows
        to track the changing skyline profile.
        """
        self.points = [(0, 0)]  # Start with origin point (x=0, y=0)
    
    def get_height_at(self, x):
        """
        Get the skyline height at any X position.
        
        This is the key query operation when we want to place a rectangle,
        we need to know how high the skyline is at that X position.
        The rectangle's bottom edge will touch the skyline.
        
        Args:
            x: X coordinate where we want to know the height
            
        Returns:
            Y coordinate (height) of skyline at position x
        """
        # Loop through consecutive pairs of skyline points
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]      # Left point of current segment
            x2, y2 = self.points[i + 1]  # Right point of current segment
            
            # If x falls within this segment's X range
            if x1 <= x <= x2:
                # Return the higher of the two Y values
                # This ensures we don't place rectangles inside existing ones
                return max(y1, y2)
        
        # If x is outside all segments, height is 0 (ground level)
        return 0
    
    def add_rectangle(self, x, y, width, height):
        """
        Add a rectangle and update the skyline profile.
        
        This is the core operation that changes the skyline. When we place
        a rectangle, it creates a new step in the skyline profile.
        
        The algorithm:
        1. Remove any skyline points that fall inside the new rectangle
        2. Add two new points: left edge (goes up) and right edge (goes down)
        3. Sort all points to maintain left-to-right order
        
        Args:
            x, y: Bottom-left corner of the rectangle
            width, height: Dimensions of the rectangle
        """
        print("Adding rectangle: position=({0},{1}), size={2}x{3}".format(x, y, width, height))
        
        # Calculate the edges of the new rectangle
        left_x = x              # Left edge X coordinate
        right_x = x + width     # Right edge X coordinate  
        top_y = y + height      # Top edge Y coordinate (new skyline height)
        
        # STEP 1: Keep only skyline points that are outside the new rectangle
        # Points that fall within the rectangle's X range get "covered up"
        new_points = []
        for sx, sy in self.points:
            # Keep point if it's to the left OR to the right of the rectangle
            if sx < left_x or sx > right_x:
                new_points.append((sx, sy))
        
        # STEP 2: Add the new skyline segment created by this rectangle
        # The rectangle creates a flat-topped segment between left_x and right_x
        new_points.extend([
            (left_x, top_y),    # Left edge: skyline jumps UP to top of rectangle
            (right_x, y)        # Right edge: skyline drops DOWN to original level
        ])
        
        # STEP 3: Sort all points by X coordinate to maintain proper order
        # The skyline must always be ordered from left to right
        self.points = sorted(new_points)
        
        print("New skyline points: {0}".format(self.points))

# =====================================================
# VISUALIZATION FUNCTION
# =====================================================

def show_skyline_evolution():
    """
    Visualize how the skyline evolves step by step.
    
    Each panel shows both the rectangles and the resulting skyline.
    """
    
    # Create figure with 3 subplots side by side
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Create a fresh skyline for the demonstration
    skyline = Skyline()
    
    # Define three rectangles
    # Format: (x, y, width, height)
    rectangles = [
        (0, 0, 2.5, 1.5),      # Rectangle 1: wide base rectangle
        (2.5, 0, 1.5, 2.0),    # Rectangle 2: tall rectangle to the right
        (1.0, 1.5, 1.5, 1.0)   # Rectangle 3: small rectangle on top of first one
    ]
    
    # Colors for visual distinction
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
    
    # Process each rectangle and create a visualization for each step
    for step, (x, y, w, h) in enumerate(rectangles):
        # Get the current subplot
        ax = axes[step]
        
        # Add this rectangle to our skyline
        skyline.add_rectangle(x, y, w, h)
        
        # Setup the plot area
        ax.set_xlim(-0.2, 5)     # X axis from -0.2 to 5
        ax.set_ylim(-0.2, 3)     # Y axis from -0.2 to 3
        ax.set_aspect('equal')    # Equal scaling on both axes
        ax.grid(True, alpha=0.3)  # Light grid for reference
        
        # Draw all rectangles
        for i, (rx, ry, rw, rh) in enumerate(rectangles[:step+1]):
            # Create rectangle patch for matplotlib
            rect = patches.Rectangle(
                (rx, ry),           # Bottom-left corner
                rw, rh,             # Width and height
                facecolor=colors[i], # Fill color
                edgecolor='black',   # Border color
                linewidth=2          # Border thickness
            )
            ax.add_patch(rect)  # Add rectangle to plot
            
            # Add number label in center of rectangle
            center_x = rx + rw/2
            center_y = ry + rh/2
            ax.text(center_x, center_y, str(i+1), 
                   ha='center', va='center',           # Center alignment
                   fontsize=12, fontweight='bold',     # Font styling
                   color='white')                      # White text for visibility
        
        # Draw the skyline as a redline
        # Build arrays of X and Y coordinates for the skyline line
        skyline_x = [0]  # Start from left edge
        skyline_y = [skyline.points[0][1]]  # Start height
        
        # Add all skyline points
        for sx, sy in skyline.points:
            skyline_x.append(sx)
            skyline_y.append(sy)
        
        # Extend line to right edge of plot
        skyline_x.append(5)
        skyline_y.append(skyline_y[-1])  # Same height as last point
        
        # Draw the skyline line
        ax.plot(skyline_x, skyline_y, 'r-',    # Red solid line
               linewidth=3)                    # Thick line for visibility
        
        # Mark each skyline point with a red dot
        for sx, sy in skyline.points:
            ax.plot(sx, sy, 'ro', markersize=6)  # Red circle marker
        
        # Add title
        ax.set_title("Step {0}".format(step+1), 
                    fontsize=14, fontweight='bold')
        
        # Show skyline point as text
        points_text = "Skyline: {0}".format(skyline.points)
        ax.text(0.02, 0.98, points_text,        # Position: top-left corner
               transform=ax.transAxes,           # Use axis coordinates (0-1 range)
               fontsize=9,                       # Small font
               bbox=dict(boxstyle='round',       # Rounded text box
                        facecolor='white',       # White background
                        alpha=0.8),              # Semi-transparent
               verticalalignment='top')          # Align to top
    
    # Adjust layout and show the plot
    plt.tight_layout()  # Optimize spacing between subplots
    plt.show()          # Display the visualization

# =====================================================
# DEMONSTRATION: TEST THE SKYLINE STEP BY STEP
# =====================================================

print("=" * 50)
print("SKYLINE ALGORITHM DEMONSTRATION")
print("=" * 50)

# Create a new skyline instance for testing
skyline = Skyline()
print("Step 0 - Initial skyline: {0}".format(skyline.points))
print("  (This represents an empty container)")

# Add first rectangle at bottom-left
print("\nStep 1 - Adding first rectangle...")
skyline.add_rectangle(0, 0, 2.5, 1.5)
print("  Skyline after first rectangle: {0}".format(skyline.points))
print("  Height at x=1.0: {0}".format(skyline.get_height_at(1.0)))

# Add second rectangle to the right
print("\nStep 2 - Adding second rectangle...")
skyline.add_rectangle(2.5, 0, 1.5, 2.0)
print("  Skyline after second rectangle: {0}".format(skyline.points))
print("  Height at x=3.0: {0}".format(skyline.get_height_at(3.0)))

# Add third rectangle on top of the first one
print("\nStep 3 - Adding third rectangle on top...")
skyline.add_rectangle(1.0, 1.5, 1.5, 1.0)
print("  Final skyline: {0}".format(skyline.points))
print("  Height at x=1.5: {0}".format(skyline.get_height_at(1.5)))

print("\n" + "=" * 50)
print("Now showing visual representation...")
print("=" * 50)

# Show the step-by-step visualization
show_skyline_evolution()
