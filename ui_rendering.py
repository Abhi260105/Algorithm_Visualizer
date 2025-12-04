"""
UI Rendering Module - Static backgrounds, layered drawing, animation system
Separates rendering logic from algorithm execution
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from core_algorithms import AlgorithmEvent, EventType


# Enhanced color theme with animation colors
THEME = {
    "bg": "#f8f8f6",           # off-white background
    "fg": "#000000",           # pure black text
    "border": "#000000",       # black borders
    "grid": "#c0c0c0",         # light gray for graph grid
    "canvas_bg": "#ffffff",    # pure white background for graph
    "highlight": "#4CAF50",    # GREEN for all animation highlights
    "comparing": "#4CAF50",    # GREEN for comparing
    "swapping": "#4CAF50",     # GREEN for swapping
    "sorted": "#90EE90",       # light green for sorted
    "found": "#2E7D32",        # dark green for found
    "searching": "#4CAF50",    # GREEN for searching
    "button_hover": "#e0e0e0", # hover color for buttons
    "button_active": "#333333" # active button color
}


class GraphPaperBackground:
    """Static graph paper background generator - 1cm square boxes"""
    
    @staticmethod
    def create_background(ax, width: int = 100, height: int = 100):
        """
        Create a static graph paper background
        1cm square boxes with neutral colors
        
        Args:
            ax: matplotlib axis object
            width: width in units
            height: height in units
        """
        # Set background color
        ax.set_facecolor(THEME["canvas_bg"])
        
        # Configure grid - 1cm square boxes
        ax.set_axisbelow(True)  # Grid behind all content
        
        # Major grid lines (1 unit = 1cm)
        ax.grid(True, which='major', 
                color=THEME["grid"], 
                linestyle='-', 
                linewidth=0.8, 
                alpha=0.5)
        
        # Set tick positions for 1cm squares
        ax.set_xticks(np.arange(0, width, 1))
        ax.set_yticks(np.arange(0, height, 1))
        
        # Hide tick labels to keep it clean
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        # Set borders
        for spine in ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
            spine.set_visible(True)
        
        # Remove minor ticks
        ax.tick_params(which='minor', length=0)
        ax.tick_params(which='major', length=0)
    
    @staticmethod
    def apply_to_axis(ax):
        """Apply graph paper theme to existing axis"""
        GraphPaperBackground.create_background(ax)


class LayeredRenderer:
    """
    Layered rendering system
    Layer order: background → grid → elements → highlights → text
    """
    
    def __init__(self, ax):
        self.ax = ax
        self.cached_background = None
        
    def clear_layers(self):
        """Clear all drawing layers (except cached background)"""
        self.ax.clear()
        # Reapply background
        GraphPaperBackground.apply_to_axis(self.ax)
    
    def draw_bars(self, data: List[int], colors: List[str], 
                  edgecolor: str = None, linewidth: int = 2):
        """
        Layer 1: Draw bar chart elements
        
        Args:
            data: list of values
            colors: list of colors for each bar
            edgecolor: edge color for bars
            linewidth: width of bar edges
        """
        if not data:
            return
        
        n = len(data)
        x = range(n)
        
        # Draw bars
        bars = self.ax.bar(x, data, color=colors, 
                          edgecolor=edgecolor or THEME["border"],
                          linewidth=linewidth,
                          zorder=2)  # Above grid, below highlights
        
        # Set proper limits to center content
        self.ax.set_xlim(-0.5, n - 0.5)
        max_val = max(data) if data else 100
        self.ax.set_ylim(0, max_val * 1.1)
        
        return bars
    
    def add_highlights(self, indices: List[int], data_length: int, 
                      highlight_color: str = None):
        """
        Layer 2: Add highlight rectangles over specific bars
        
        Args:
            indices: list of indices to highlight
            data_length: total number of data points
            highlight_color: color for highlights
        """
        color = highlight_color or THEME["highlight"]
        
        for idx in indices:
            if 0 <= idx < data_length:
                # Draw highlight rectangle
                rect = Rectangle(
                    (idx - 0.4, 0), 0.8, 1,
                    transform=self.ax.get_xaxis_transform(),
                    facecolor=color,
                    alpha=0.3,
                    zorder=3  # Above bars
                )
                self.ax.add_patch(rect)
    
    def add_text_overlay(self, text: str, position: str = 'top'):
        """
        Layer 3: Add text overlay
        
        Args:
            text: text to display
            position: 'top', 'bottom', 'center'
        """
        if position == 'top':
            y = 0.95
        elif position == 'bottom':
            y = 0.05
        else:
            y = 0.5
        
        self.ax.text(0.5, y, text,
                    transform=self.ax.transAxes,
                    ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    color=THEME["fg"],
                    family='Courier',
                    bbox=dict(boxstyle='round,pad=0.5', 
                             facecolor=THEME["bg"], 
                             alpha=0.8),
                    zorder=4)  # Above everything
    
    def set_title(self, title: str):
        """Set chart title with consistent styling"""
        self.ax.set_title(title, 
                         color=THEME["fg"],
                         fontsize=12, 
                         fontweight='bold', 
                         family='Courier',
                         pad=15)
    
    def set_labels(self, xlabel: str = "", ylabel: str = ""):
        """Set axis labels with consistent styling"""
        if xlabel:
            self.ax.set_xlabel(xlabel, 
                             color=THEME["fg"], 
                             family='Courier', 
                             fontsize=10,
                             fontweight='bold')
        if ylabel:
            self.ax.set_ylabel(ylabel, 
                             color=THEME["fg"], 
                             family='Courier', 
                             fontsize=10,
                             fontweight='bold')


class SortingVisualizer:
    """Visualization handler for sorting algorithms"""
    
    def __init__(self, fig, ax, canvas):
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        self.renderer = LayeredRenderer(ax)
        
        # Initialize with background
        self._setup_canvas()
    
    def _setup_canvas(self):
        """Setup canvas with theme"""
        self.fig.patch.set_facecolor(THEME["canvas_bg"])
        GraphPaperBackground.apply_to_axis(self.ax)
    
    def draw_state(self, data: List[int], event: AlgorithmEvent = None):
        """
        Draw current state based on algorithm event
        
        Args:
            data: current data array
            event: algorithm event describing what to visualize
        """
        if not data:
            self._draw_empty_state("NO DATA")
            return
        
        # Clear and reapply background
        self.renderer.clear_layers()
        
        # Determine colors based on event
        colors = self._get_colors_for_event(data, event)
        
        # Layer 1: Draw bars
        self.renderer.draw_bars(data, colors)
        
        # Layer 2: Add highlights if event specifies
        if event and event.indices:
            self.renderer.add_highlights(event.indices, len(data))
        
        # Layer 3: Set title and labels
        self.renderer.set_title("SORTING VISUALIZATION")
        self.renderer.set_labels("INDEX", "VALUE")
        
        # Layer 4: Add message if present
        if event and event.message:
            self.renderer.add_text_overlay(event.message, 'top')
        
        # Render
        self.canvas.draw_idle()
    
    def _get_colors_for_event(self, data: List[int], 
                              event: AlgorithmEvent = None) -> List[str]:
        """
        Determine bar colors based on event type
        All active operations use GREEN
        """
        n = len(data)
        colors = [THEME["bg"]] * n  # Default: neutral
        
        if not event:
            return colors
        
        # GREEN for all active operations
        if event.event_type in [EventType.COMPARE, EventType.SWAP, 
                                EventType.HIGHLIGHT, EventType.DIVIDE,
                                EventType.PIVOT]:
            for idx in event.indices:
                if 0 <= idx < n:
                    colors[idx] = THEME["highlight"]  # GREEN
        
        elif event.event_type == EventType.MERGE:
            for idx in event.indices:
                if 0 <= idx < n:
                    colors[idx] = THEME["highlight"]  # GREEN
        
        elif event.event_type == EventType.SORTED:
            # Light green for sorted elements
            for idx in event.indices:
                if 0 <= idx < n:
                    colors[idx] = THEME["sorted"]
        
        return colors
    
    def _draw_empty_state(self, message: str):
        """Draw empty state with message"""
        self.renderer.clear_layers()
        self.renderer.set_title("SORTING VISUALIZATION")
        self.renderer.add_text_overlay(message, 'center')
        self.canvas.draw_idle()


class SearchVisualizer:
    """Visualization handler for search algorithms"""
    
    def __init__(self, fig, ax, canvas):
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        self.renderer = LayeredRenderer(ax)
        
        # Initialize with background
        self._setup_canvas()
    
    def _setup_canvas(self):
        """Setup canvas with theme"""
        self.fig.patch.set_facecolor(THEME["canvas_bg"])
        GraphPaperBackground.apply_to_axis(self.ax)
    
    def draw_state(self, data: List[int], event: AlgorithmEvent = None):
        """
        Draw current search state
        
        Args:
            data: current data array
            event: algorithm event describing what to visualize
        """
        if not data:
            self._draw_empty_state("NO DATA")
            return
        
        # Clear and reapply background
        self.renderer.clear_layers()
        
        # Determine colors based on event
        colors = self._get_colors_for_event(data, event)
        
        # Layer 1: Draw bars
        self.renderer.draw_bars(data, colors)
        
        # Layer 2: Add highlights
        if event and event.indices:
            if event.event_type == EventType.FOUND:
                # Dark green for found element
                self.renderer.add_highlights(event.indices, len(data), 
                                            THEME["found"])
            else:
                # Regular green for searching
                self.renderer.add_highlights(event.indices, len(data))
        
        # Layer 3: Set title and labels
        self.renderer.set_title("SEARCH VISUALIZATION")
        self.renderer.set_labels("INDEX", "VALUE")
        
        # Show index labels for search
        self.ax.set_xticks(range(len(data)))
        self.ax.set_xticklabels(range(len(data)), 
                               family='Courier', 
                               fontsize=8,
                               color=THEME["fg"])
        
        # Layer 4: Add message if present
        if event and event.message:
            self.renderer.add_text_overlay(event.message, 'top')
        
        # Render
        self.canvas.draw_idle()
    
    def _get_colors_for_event(self, data: List[int], 
                              event: AlgorithmEvent = None) -> List[str]:
        """Determine bar colors based on event type"""
        n = len(data)
        colors = [THEME["bg"]] * n  # Default: neutral
        
        if not event:
            return colors
        
        # GREEN for searching
        if event.event_type in [EventType.COMPARE, EventType.HIGHLIGHT]:
            for idx in event.indices:
                if 0 <= idx < n:
                    colors[idx] = THEME["searching"]  # GREEN
        
        # Dark green for found
        elif event.event_type == EventType.FOUND:
            for idx in event.indices:
                if 0 <= idx < n:
                    colors[idx] = THEME["found"]
        
        return colors
    
    def _draw_empty_state(self, message: str):
        """Draw empty state with message"""
        self.renderer.clear_layers()
        self.renderer.set_title("SEARCH VISUALIZATION")
        self.renderer.add_text_overlay(message, 'center')
        self.canvas.draw_idle()


class TreeVisualizer:
    """Visualization handler for tree structures"""
    
    def __init__(self, fig, ax, canvas):
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        
        # Initialize with background
        self._setup_canvas()
    
    def _setup_canvas(self):
        """Setup canvas with theme"""
        self.fig.patch.set_facecolor(THEME["canvas_bg"])
        self.ax.set_facecolor(THEME["canvas_bg"])
        self.ax.set_aspect('equal')
        self.ax.axis('off')
    
    def draw_tree(self, root, highlight_nodes: List[int] = None):
        """
        Draw binary tree with improved layout
        
        Args:
            root: TreeNode root
            highlight_nodes: list of values to highlight in GREEN
        """
        self.ax.clear()
        self._setup_canvas()
        
        if root is None:
            self._draw_empty_tree()
            return
        
        # Calculate positions with improved spacing
        positions = {}
        self._calculate_positions_improved(root, 0, 0, 8, positions)
        
        # Layer 1: Draw edges
        self._draw_edges(root, positions)
        
        # Layer 2: Draw nodes
        self._draw_nodes(positions, highlight_nodes or [])
        
        # Auto-adjust view
        self._auto_adjust_view(positions)
        
        # Render
        self.canvas.draw_idle()
    
    def _calculate_positions_improved(self, node, x: float, y: float, 
                                     width: float, positions: dict):
        """
        Calculate node positions with better spacing
        Uses exponential width reduction for better layout
        """
        if node is not None:
            positions[node] = (x, y)
            
            # Exponential width reduction for deeper levels
            new_width = width * 0.6
            vertical_spacing = 1.5  # Increased vertical spacing
            
            if node.left:
                self._calculate_positions_improved(
                    node.left, 
                    x - width, 
                    y - vertical_spacing, 
                    new_width, 
                    positions
                )
            
            if node.right:
                self._calculate_positions_improved(
                    node.right, 
                    x + width, 
                    y - vertical_spacing, 
                    new_width, 
                    positions
                )
    
    def _draw_edges(self, node, positions: dict):
        """Draw edges between nodes with consistent styling"""
        if node is not None:
            x, y = positions[node]
            
            if node.left:
                left_x, left_y = positions[node.left]
                self.ax.plot([x, left_x], [y, left_y], 
                           '-', 
                           color=THEME["border"],
                           linewidth=2.5,
                           zorder=1)  # Behind nodes
                self._draw_edges(node.left, positions)
            
            if node.right:
                right_x, right_y = positions[node.right]
                self.ax.plot([x, right_x], [y, right_y], 
                           '-', 
                           color=THEME["border"],
                           linewidth=2.5,
                           zorder=1)  # Behind nodes
                self._draw_edges(node.right, positions)
    
    def _draw_nodes(self, positions: dict, highlight_values: List[int]):
        """Draw tree nodes with consistent styling and highlights"""
        for node, (x, y) in positions.items():
            # Determine if node should be highlighted
            is_highlighted = node.value in highlight_values
            
            # Node background color
            node_color = THEME["highlight"] if is_highlighted else THEME["bg"]
            
            # Draw node rectangle
            node_width = 0.6
            node_height = 0.4
            rect = Rectangle(
                (x - node_width/2, y - node_height/2),
                node_width, node_height,
                facecolor=node_color,
                edgecolor=THEME["border"],
                linewidth=2.5,
                zorder=2  # Above edges
            )
            self.ax.add_patch(rect)
            
            # Draw node value
            text_color = THEME["bg"] if is_highlighted else THEME["fg"]
            self.ax.text(x, y, str(node.value),
                        ha='center', va='center',
                        color=text_color,
                        fontsize=12,
                        fontweight='bold',
                        family='Courier',
                        zorder=3)  # Above rectangle
    
    def _auto_adjust_view(self, positions: dict):
        """Auto-adjust view to fit all nodes"""
        if not positions:
            return
        
        x_coords = [pos[0] for pos in positions.values()]
        y_coords = [pos[1] for pos in positions.values()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Add padding
        padding = 1.5
        self.ax.set_xlim(x_min - padding, x_max + padding)
        self.ax.set_ylim(y_min - padding, y_max + padding)
    
    def _draw_empty_tree(self):
        """Draw empty tree state"""
        self.ax.text(0, 0, "EMPTY TREE",
                    ha='center', va='center',
                    color=THEME["fg"],
                    fontsize=14,
                    fontweight='bold',
                    family='Courier')
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)


class AnimationPlayer:
    """
    Event-driven animation player
    Plays back algorithm events with timing control
    """
    
    def __init__(self, visualizer, update_callback=None):
        """
        Args:
            visualizer: SortingVisualizer or SearchVisualizer instance
            update_callback: function called after each frame
        """
        self.visualizer = visualizer
        self.update_callback = update_callback
        self.is_playing = False
        self.current_event_index = 0
        
    def play_events(self, events: List[AlgorithmEvent], speed: float = 0.1):
        """
        Play algorithm events with animation
        
        Args:
            events: list of AlgorithmEvent objects
            speed: delay between frames in seconds
        """
        self.is_playing = True
        self.current_event_index = 0
        
        for i, event in enumerate(events):
            if not self.is_playing:
                break
            
            self.current_event_index = i
            
            # Draw current event state
            if event.data_snapshot:
                self.visualizer.draw_state(event.data_snapshot, event)
            
            # Callback for status updates
            if self.update_callback:
                self.update_callback(event, i, len(events))
            
            # Timing delay
            import time
            time.sleep(speed)
        
        self.is_playing = False
    
    def stop(self):
        """Stop animation playback"""
        self.is_playing = False
    
    def is_running(self) -> bool:
        """Check if animation is running"""
        return self.is_playing