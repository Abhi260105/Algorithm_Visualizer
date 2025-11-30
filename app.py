import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, colorchooser, filedialog
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle
from datetime import datetime
import json
import csv
import math
import threading
from PIL import Image
import io

# Global variables
data = []
sorting_history = []
search_history = []
tree_data = []
HISTORY_FILE = "sorting_history.json"
SEARCH_HISTORY_FILE = "search_history.json"
CONFIG_FILE = "config.json"
current_theme = "modern_dark"
execution_times = {}

# Speed presets
SPEED_PRESETS = {
    "Instant": 0.001,
    "Fast": 0.05,
    "Normal": 0.1,
    "Slow": 0.5,
    "Very Slow": 1.0
}

# Enhanced themes with modern design
themes = {
    "modern_dark": {
        "bg": "#1e1e2e",
        "fg": "#cdd6f4",
        "entry_bg": "#313244",
        "entry_fg": "#cdd6f4",
        "highlight": "#fab387",
        "button_bg": "#45475a",
        "active_bg": "#585b70",
        "accent": "#89b4fa",
        "success": "#a6e3a1",
        "warning": "#f9e2af",
        "error": "#f38ba8",
        "surface": "#181825"
    },
    "modern_light": {
        "bg": "#eff1f5",
        "fg": "#4c4f69",
        "entry_bg": "#ffffff",
        "entry_fg": "#4c4f69",
        "highlight": "#fe640b",
        "button_bg": "#e6e9ef",
        "active_bg": "#ccd0da",
        "accent": "#1e66f5",
        "success": "#40a02b",
        "warning": "#df8e1d",
        "error": "#d20f39",
        "surface": "#f5f5f5"
    },
    "cyberpunk": {
        "bg": "#0a0e27",
        "fg": "#00ff41",
        "entry_bg": "#1a1a2e",
        "entry_fg": "#00ff41",
        "highlight": "#ff0080",
        "button_bg": "#2a2a4a",
        "active_bg": "#3a3a5a",
        "accent": "#00ffff",
        "success": "#00ff00",
        "warning": "#ffff00",
        "error": "#ff0040",
        "surface": "#0f0f1e"
    }
}

bar_color = "#89b4fa"
highlight_color = "#fab387"

# Tree Node class for binary tree operations
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ToolTip class
class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Display tooltip"""
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=self.text, 
                            background="#ffffe0", foreground="black",
                            relief=tk.SOLID, borderwidth=1, 
                            font=("Arial", 9), padx=5, pady=3)
            label.pack()
        except:
            pass
    
    def hide_tooltip(self, event=None):
        """Hide tooltip"""
        try:
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
        except:
            pass

class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Algorithm Visualizer")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(bg=themes[current_theme]["bg"])
        
        # Control variables
        self.is_paused = False
        self.step_mode = False
        self.is_running = False
        self.capture_frames = False
        self.frames = []
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.setup_styles()
        
        # Create tabs
        self.sorting_tab = tk.Frame(self.notebook)
        self.search_tab = tk.Frame(self.notebook)
        self.tree_tab = tk.Frame(self.notebook)
        self.analysis_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.sorting_tab, text="Sorting Algorithms")
        self.notebook.add(self.search_tab, text="Search Algorithms")
        self.notebook.add(self.tree_tab, text="Tree Operations")
        self.notebook.add(self.analysis_tab, text="Performance Analysis")
        
        self.setup_sorting_tab()
        self.setup_search_tab()
        self.setup_tree_tab()
        self.setup_analysis_tab()
        
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize data
        self.data = []
        self.search_array = []
        self.binary_tree = None
        
        # Load configuration and history
        self.load_config()
        self.load_history()
        self.apply_theme()
        self.setup_keyboard_shortcuts()

    def setup_styles(self):
        """Setup custom ttk styles"""
        self.style = ttk.Style()
        theme = themes[current_theme]
        
        # Configure notebook style
        self.style.configure('TNotebook', background=theme["bg"])
        self.style.configure('TNotebook.Tab', background=theme["button_bg"], 
                           foreground=theme["fg"], padding=[20, 10])
        self.style.map('TNotebook.Tab', background=[('selected', theme["accent"])])

    def create_button(self, parent, text, command, style="default", width=None):
        """Create a styled button with consistent theming"""
        theme = themes[current_theme]
        styles = {
            "default": {"bg": theme["button_bg"], "fg": theme["fg"]},
            "accent": {"bg": theme["accent"], "fg": "white"},
            "success": {"bg": theme["success"], "fg": "white"},
            "warning": {"bg": theme["warning"], "fg": theme["bg"] if current_theme == "modern_light" else "white"},
            "error": {"bg": theme["error"], "fg": "white"}
        }
        
        btn_config = {
            "text": text,
            "command": command,
            "font": ("Arial", 10, "bold"),
            "relief": tk.FLAT,
            "activebackground": theme["active_bg"],
            "cursor": "hand2",
            **styles.get(style, styles["default"])
        }
        
        if width:
            btn_config["width"] = width
        
        return tk.Button(parent, **btn_config)

    def setup_sorting_tab(self):
        """Setup the sorting algorithms tab"""
        theme = themes[current_theme]
        
        # Main container
        main_frame = tk.Frame(self.sorting_tab, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=theme["surface"], relief=tk.RAISED, bd=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Create matplotlib figure for sorting
        self.sort_fig, self.sort_ax = plt.subplots(figsize=(12, 6))
        self.sort_fig.patch.set_facecolor(theme["surface"])
        self.sort_ax.set_facecolor(theme["surface"])
        self.sort_ax.tick_params(colors=theme["fg"])
        for spine in self.sort_ax.spines.values():
            spine.set_color(theme["fg"])
        
        self.sort_canvas = FigureCanvasTkAgg(self.sort_fig, viz_frame)
        self.sort_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Array display frame
        self.array_frame = tk.Frame(main_frame, bg=theme["bg"], height=50)
        self.array_frame.pack(fill=tk.X, padx=10, pady=5)
        self.array_frame.pack_propagate(False)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=theme["bg"])
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input section
        input_section = tk.LabelFrame(controls_frame, text="Data Input", 
                                    bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        input_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(input_section, text="Array:", bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.sort_entry = tk.Entry(input_section, width=30, bg=theme["entry_bg"], fg=theme["entry_fg"], 
                                 font=("Arial", 10), relief=tk.FLAT, bd=5)
        self.sort_entry.grid(row=0, column=1, padx=5, pady=2)
        ToolTip(self.sort_entry, "Enter comma-separated numbers (e.g., 5,2,8,1,9)")
        
        gen_btn = self.create_button(input_section, "Generate Random", self.generate_sort_data, "accent", 15)
        gen_btn.grid(row=0, column=2, padx=5, pady=2)
        ToolTip(gen_btn, "Generate random array of 10-30 elements")
        
        # Speed controls
        tk.Label(input_section, text="Speed:", bg=theme["bg"], fg=theme["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.sort_speed = tk.DoubleVar(value=0.1)
        
        # Speed preset frame
        speed_frame = tk.Frame(input_section, bg=theme["bg"])
        speed_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="w")
        
        self.speed_preset = tk.StringVar(value="Normal")
        for preset_name, preset_value in SPEED_PRESETS.items():
            rb = tk.Radiobutton(speed_frame, text=preset_name, variable=self.speed_preset, 
                               value=preset_name, bg=theme["bg"], fg=theme["fg"],
                               selectcolor=theme["accent"], activebackground=theme["bg"],
                               command=lambda v=preset_value: self.sort_speed.set(v))
            rb.pack(side=tk.LEFT, padx=2)
        ToolTip(speed_frame, "Select animation speed for visualization")
        
        # Algorithm buttons
        algo_section = tk.LabelFrame(controls_frame, text="Sorting Algorithms", 
                                   bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        algo_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        algorithms = [
            ("Bubble Sort", lambda: self.run_sorting_algorithm(self.bubble_sort, "Bubble Sort")),
            ("Selection Sort", lambda: self.run_sorting_algorithm(self.selection_sort, "Selection Sort")),
            ("Insertion Sort", lambda: self.run_sorting_algorithm(self.insertion_sort, "Insertion Sort")),
            ("Merge Sort", lambda: self.run_sorting_algorithm(self.merge_sort, "Merge Sort")),
            ("Quick Sort", lambda: self.run_sorting_algorithm(self.quick_sort, "Quick Sort")),
            ("Heap Sort", lambda: self.run_sorting_algorithm(self.heap_sort, "Heap Sort")),
            ("Radix Sort", lambda: self.run_sorting_algorithm(self.radix_sort, "Radix Sort")),
            ("Shell Sort", lambda: self.run_sorting_algorithm(self.shell_sort, "Shell Sort")),
            ("Cocktail Sort", lambda: self.run_sorting_algorithm(self.cocktail_sort, "Cocktail Sort")),
            ("Comb Sort", lambda: self.run_sorting_algorithm(self.comb_sort, "Comb Sort"))
        ]
        
        for i, (text, command) in enumerate(algorithms):
            row, col = i // 5, i % 5
            btn = self.create_button(algo_section, text, command, "default", 12)
            btn.grid(row=row, column=col, padx=3, pady=2)
            ToolTip(btn, f"Run {text} algorithm")
        
        # Control buttons
        control_section = tk.LabelFrame(controls_frame, text="Controls", 
                                      bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        control_section.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        control_buttons = [
            ("Pause/Resume", self.toggle_pause, "warning"),
            ("Step", self.step_forward, "warning"),
            ("Record", self.start_capture, "accent"),
            ("Export GIF", self.stop_and_export_gif, "accent"),
            ("Save Data", self.save_sorted_data, "success"),
            ("Load Data", self.load_data_from_file, "success"),
            ("Reset", self.reset_sort_visualization, "error"),
            ("Theme", self.cycle_theme, "default")
        ]
        
        for i, (text, command, style) in enumerate(control_buttons):
            btn = self.create_button(control_section, text, command, style, 12)
            btn.grid(row=i//2, column=i%2, padx=3, pady=2)
            
            # Add tooltips
            if text == "Pause/Resume":
                ToolTip(btn, "Pause or resume animation (Space)")
            elif text == "Step":
                ToolTip(btn, "Execute one step at a time")
            elif text == "Record":
                ToolTip(btn, "Start recording frames for GIF")
            elif text == "Export GIF":
                ToolTip(btn, "Export recorded animation as GIF")
        
        # Status bar
        self.sort_status = tk.Label(main_frame, text="Ready", bg=theme["surface"], 
                                  fg=theme["fg"], font=("Arial", 10), relief=tk.SUNKEN, bd=1)
        self.sort_status.pack(fill=tk.X, padx=10, pady=(0, 10))

    def setup_search_tab(self):
        """Setup the search algorithms tab"""
        theme = themes[current_theme]
        
        main_frame = tk.Frame(self.search_tab, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=theme["surface"], relief=tk.RAISED, bd=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Create matplotlib figure for search
        self.search_fig, self.search_ax = plt.subplots(figsize=(12, 6))
        self.search_fig.patch.set_facecolor(theme["surface"])
        self.search_ax.set_facecolor(theme["surface"])
        self.search_ax.tick_params(colors=theme["fg"])
        for spine in self.search_ax.spines.values():
            spine.set_color(theme["fg"])
        
        self.search_canvas = FigureCanvasTkAgg(self.search_fig, viz_frame)
        self.search_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=theme["bg"])
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input section
        input_section = tk.LabelFrame(controls_frame, text="Search Setup", 
                                    bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        input_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(input_section, text="Array:", bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.search_array_entry = tk.Entry(input_section, width=30, bg=theme["entry_bg"], 
                                         fg=theme["entry_fg"], font=("Arial", 10), relief=tk.FLAT, bd=5)
        self.search_array_entry.grid(row=0, column=1, padx=5, pady=2)
        ToolTip(self.search_array_entry, "Enter numbers (will be sorted automatically)")
        
        tk.Label(input_section, text="Target:", bg=theme["bg"], fg=theme["fg"]).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.search_target_entry = tk.Entry(input_section, width=10, bg=theme["entry_bg"], 
                                          fg=theme["entry_fg"], font=("Arial", 10), relief=tk.FLAT, bd=5)
        self.search_target_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ToolTip(self.search_target_entry, "Enter the value to search for")
        
        gen_btn = self.create_button(input_section, "Generate Sorted", self.generate_search_data, "accent", 15)
        gen_btn.grid(row=0, column=2, padx=5, pady=2)
        ToolTip(gen_btn, "Generate sorted array for searching")
        
        # Search algorithms
        search_section = tk.LabelFrame(controls_frame, text="Search Algorithms", 
                                     bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        search_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        search_algorithms = [
            ("Linear Search", lambda: self.run_search_algorithm(self.linear_search, "Linear Search")),
            ("Binary Search", lambda: self.run_search_algorithm(self.binary_search, "Binary Search")),
            ("Jump Search", lambda: self.run_search_algorithm(self.jump_search, "Jump Search")),
            ("Interpolation", lambda: self.run_search_algorithm(self.interpolation_search, "Interpolation Search")),
            ("Exponential", lambda: self.run_search_algorithm(self.exponential_search, "Exponential Search")),
            ("Fibonacci", lambda: self.run_search_algorithm(self.fibonacci_search, "Fibonacci Search"))
        ]
        
        for i, (text, command) in enumerate(search_algorithms):
            btn = self.create_button(search_section, text, command, "default", 15)
            btn.grid(row=i//3, column=i%3, padx=3, pady=2)
            ToolTip(btn, f"Run {text} algorithm")
        
        # Status
        self.search_status = tk.Label(main_frame, text="Ready", bg=theme["surface"], 
                                    fg=theme["fg"], font=("Arial", 10), relief=tk.SUNKEN, bd=1)
        self.search_status.pack(fill=tk.X, padx=10, pady=(0, 10))

    def setup_tree_tab(self):
        """Setup the tree operations tab"""
        theme = themes[current_theme]
        
        main_frame = tk.Frame(self.tree_tab, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=theme["surface"], relief=tk.RAISED, bd=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Create matplotlib figure for tree
        self.tree_fig, self.tree_ax = plt.subplots(figsize=(12, 8))
        self.tree_fig.patch.set_facecolor(theme["surface"])
        self.tree_ax.set_facecolor(theme["surface"])
        self.tree_ax.set_aspect('equal')
        self.tree_ax.axis('off')
        
        self.tree_canvas = FigureCanvasTkAgg(self.tree_fig, viz_frame)
        self.tree_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=theme["bg"])
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Tree operations
        tree_ops_section = tk.LabelFrame(controls_frame, text="Tree Operations", 
                                       bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        tree_ops_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(tree_ops_section, text="Value:", bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, padx=5, pady=2)
        self.tree_value_entry = tk.Entry(tree_ops_section, width=15, bg=theme["entry_bg"], 
                                       fg=theme["entry_fg"], font=("Arial", 10), relief=tk.FLAT, bd=5)
        self.tree_value_entry.grid(row=0, column=1, padx=5, pady=2)
        ToolTip(self.tree_value_entry, "Enter value (-1000 to 1000)")
        
        tree_buttons = [
            ("Insert", self.insert_node, "success"),
            ("Delete", self.delete_node, "error"),
            ("Search", self.search_tree, "accent"),
            ("Clear", self.clear_tree, "warning")
        ]
        
        for i, (text, command, style) in enumerate(tree_buttons):
            btn = self.create_button(tree_ops_section, text, command, style, 8)
            btn.grid(row=1, column=i, padx=3, pady=2)
        
        # Traversal operations
        traversal_section = tk.LabelFrame(controls_frame, text="Tree Traversals", 
                                        bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        traversal_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        traversal_buttons = [
            ("Inorder", lambda: self.traverse_tree("inorder")),
            ("Preorder", lambda: self.traverse_tree("preorder")),
            ("Postorder", lambda: self.traverse_tree("postorder")),
            ("Level Order", lambda: self.traverse_tree("level_order"))
        ]
        
        for i, (text, command) in enumerate(traversal_buttons):
            btn = self.create_button(traversal_section, text, command, "success", 10)
            btn.grid(row=i//2, column=i%2, padx=3, pady=2)
            ToolTip(btn, f"{text} traversal")
        
        # Tree info
        info_section = tk.LabelFrame(controls_frame, text="Tree Information", 
                                   bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        info_section.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        self.tree_info_text = tk.Text(info_section, width=30, height=4, bg=theme["entry_bg"], 
                                    fg=theme["entry_fg"], font=("Arial", 9), relief=tk.FLAT)
        self.tree_info_text.pack(padx=5, pady=5)
        
        # Status
        self.tree_status = tk.Label(main_frame, text="Ready", bg=theme["surface"], 
                                  fg=theme["fg"], font=("Arial", 10), relief=tk.SUNKEN, bd=1)
        self.tree_status.pack(fill=tk.X, padx=10, pady=(0, 10))

    def setup_analysis_tab(self):
        """Setup the performance analysis tab"""
        theme = themes[current_theme]
        
        main_frame = tk.Frame(self.analysis_tab, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Analysis visualization
        viz_frame = tk.Frame(main_frame, bg=theme["surface"], relief=tk.RAISED, bd=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.analysis_fig, (self.time_ax, self.space_ax) = plt.subplots(1, 2, figsize=(14, 6))
        self.analysis_fig.patch.set_facecolor(theme["surface"])
        
        for ax in [self.time_ax, self.space_ax]:
            ax.set_facecolor(theme["surface"])
            ax.tick_params(colors=theme["fg"])
            for spine in ax.spines.values():
                spine.set_color(theme["fg"])
        
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, viz_frame)
        self.analysis_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=theme["bg"])
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Analysis buttons
        analysis_section = tk.LabelFrame(controls_frame, text="Performance Analysis", 
                                       bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        analysis_section.pack(side=tk.LEFT, padx=(0, 10))
        
        analysis_buttons = [
            ("Compare Sorting", self.compare_sorting_algorithms, "warning"),
            ("Compare Searching", self.compare_search_algorithms, "warning"),
            ("Big O Analysis", self.show_complexity_analysis, "accent"),
            ("Export Results", self.export_analysis, "success")
        ]
        
        for i, (text, command, style) in enumerate(analysis_buttons):
            btn = self.create_button(analysis_section, text, command, style, 15)
            btn.grid(row=i//2, column=i%2, padx=3, pady=2)
        
        # History section
        history_section = tk.LabelFrame(controls_frame, text="History", 
                                      bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        history_section.pack(side=tk.RIGHT, padx=(10, 0))
        
        history_buttons = [
            ("View Sort History", self.view_sort_history, "accent"),
            ("View Search History", self.view_search_history, "accent"),
            ("Clear All History", self.clear_all_history, "error")
        ]
        
        for i, (text, command, style) in enumerate(history_buttons):
            btn = self.create_button(history_section, text, command, style, 15)
            btn.grid(row=i//2, column=i%2, padx=3, pady=2)

    # Configuration management
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                global current_theme
                current_theme = config.get("default_theme", "modern_dark")
                self.sort_speed.set(config.get("default_speed", 0.1))
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                "default_theme": current_theme,
                "default_speed": self.sort_speed.get(),
                "save_history": True,
                "max_history_entries": 100
            }
            with open(CONFIG_FILE, "w") as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    # Keyboard shortcuts
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        self.root.bind('<Control-g>', lambda e: self.generate_sort_data())
        self.root.bind('<Control-G>', lambda e: self.generate_sort_data())
        
        self.root.bind('<Control-r>', lambda e: self.reset_sort_visualization())
        self.root.bind('<Control-R>', lambda e: self.reset_sort_visualization())
        
        self.root.bind('<Control-t>', lambda e: self.cycle_theme())
        self.root.bind('<Control-T>', lambda e: self.cycle_theme())
        
        self.root.bind('<space>', lambda e: self.toggle_pause() if hasattr(self, 'is_paused') else None)
        
        self.root.bind('<Control-s>', lambda e: self.save_sorted_data())
        self.root.bind('<Control-S>', lambda e: self.save_sorted_data())
        
        self.root.bind('<Control-o>', lambda e: self.load_data_from_file())
        self.root.bind('<Control-O>', lambda e: self.load_data_from_file())
        
        self.root.bind('<Control-h>', lambda e: self.show_keyboard_shortcuts())
        self.root.bind('<Control-H>', lambda e: self.show_keyboard_shortcuts())

    def show_keyboard_shortcuts(self):
        """Display keyboard shortcuts help"""
        shortcuts_window = tk.Toplevel(self.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("400x400")
        theme = themes[current_theme]
        shortcuts_window.configure(bg=theme["bg"])
        
        # Title
        title_label = tk.Label(shortcuts_window, text="KEYBOARD SHORTCUTS", 
                              bg=theme["bg"], fg=theme["accent"], 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Shortcuts text
        shortcuts_frame = tk.Frame(shortcuts_window, bg=theme["bg"])
        shortcuts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        shortcuts = [
            ("Ctrl + G", "Generate random data"),
            ("Ctrl + R", "Reset visualization"),
            ("Ctrl + T", "Cycle theme"),
            ("Space", "Pause/Resume animation"),
            ("Ctrl + S", "Save data to file"),
            ("Ctrl + O", "Open/Load data from file"),
            ("Ctrl + H", "Show this help window")
        ]
        
        for i, (key, description) in enumerate(shortcuts):
            key_label = tk.Label(shortcuts_frame, text=key, bg=theme["bg"], 
                               fg=theme["accent"], font=("Courier", 11, "bold"),
                               width=15, anchor="w")
            key_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            desc_label = tk.Label(shortcuts_frame, text=description, bg=theme["bg"], 
                                fg=theme["fg"], font=("Arial", 10), anchor="w")
            desc_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        # Close button
        close_btn = self.create_button(shortcuts_window, "Close", shortcuts_window.destroy, "accent", 15)
        close_btn.pack(pady=10)

    # Pause/Resume/Step controls
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.sort_status.config(text="⏸ PAUSED - Press Space or Click Resume to continue")
        else:
            self.sort_status.config(text="▶ Resumed")

    def step_forward(self):
        """Execute one step"""
        if self.is_paused:
            self.step_mode = True
            self.is_paused = False

    # GIF Export functionality
    def start_capture(self):
        """Start capturing frames for GIF export"""
        self.capture_frames = True
        self.frames = []
        self.sort_status.config(text="🔴 Recording started... Run an algorithm to capture frames")

    def stop_and_export_gif(self):
        """Stop capturing and export to GIF"""
        if not self.frames:
            messagebox.showwarning("No Frames", "No frames captured. Start recording and run an algorithm first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Convert frames to PIL Images
                pil_frames = []
                width = int(self.sort_fig.get_figwidth() * self.sort_fig.dpi)
                height = int(self.sort_fig.get_figheight() * self.sort_fig.dpi)
                
                for frame_data in self.frames:
                    img = Image.frombytes('RGB', (width, height), frame_data)
                    pil_frames.append(img)
                
                # Save as GIF
                if pil_frames:
                    pil_frames[0].save(filename, save_all=True, append_images=pil_frames[1:],
                                     duration=100, loop=0, optimize=False)
                    
                    messagebox.showinfo("Success", f"GIF exported successfully!\nLocation: {filename}\nFrames: {len(pil_frames)}")
                    self.frames = []
                    self.capture_frames = False
                    self.sort_status.config(text="✓ GIF exported successfully")
                else:
                    messagebox.showwarning("No Frames", "No frames to export")
                    
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export GIF: {str(e)}")

    # Data generation and management methods
    def generate_sort_data(self):
        """Generate random data for sorting visualization"""
        user_input = self.sort_entry.get().strip()
        if user_input:
            try:
                self.data = list(map(int, user_input.split(',')))
                if not self.data:
                    raise ValueError("Empty array")
                if any(x < -1000 or x > 1000 for x in self.data):
                    messagebox.showwarning("Invalid Range", "Values should be between -1000 and 1000")
                    return
            except ValueError as e:
                messagebox.showerror("Invalid Input", "Please enter valid numbers separated by commas.")
                return
        else:
            size = random.randint(10, 30)
            self.data = [random.randint(1, 100) for _ in range(size)]
            self.sort_entry.delete(0, tk.END)
            self.sort_entry.insert(0, ','.join(map(str, self.data)))
        
        self.draw_sort_data(self.data, [bar_color] * len(self.data))
        self.update_array_display(self.data)
        self.sort_status.config(text=f"✓ Generated {len(self.data)} elements")

    def generate_search_data(self):
        """Generate sorted data for search algorithms"""
        user_input = self.search_array_entry.get().strip()
        if user_input:
            try:
                self.search_array = sorted(list(map(int, user_input.split(','))))
                if not self.search_array:
                    raise ValueError("Empty array")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers separated by commas.")
                return
        else:
            size = random.randint(15, 25)
            self.search_array = sorted([random.randint(1, 100) for _ in range(size)])
            self.search_array_entry.delete(0, tk.END)
            self.search_array_entry.insert(0, ','.join(map(str, self.search_array)))
        
        self.draw_search_data(self.search_array, [bar_color] * len(self.search_array))
        self.search_status.config(text=f"✓ Generated sorted array with {len(self.search_array)} elements")

    def draw_sort_data(self, data, colors):
        """Draw sorting visualization"""
        if not data:
            return
            
        self.sort_ax.clear()
        theme = themes[current_theme]
        self.sort_ax.set_facecolor(theme["surface"])
        
        bars = self.sort_ax.bar(range(len(data)), data, color=colors, edgecolor=theme["fg"], linewidth=0.5)
        self.sort_ax.set_title("Sorting Visualization", color=theme["fg"], fontsize=14, fontweight='bold')
        self.sort_ax.set_xlabel("Index", color=theme["fg"])
        self.sort_ax.set_ylabel("Value", color=theme["fg"])
        
        # Add value labels on bars for smaller datasets
        if len(data) <= 20:
            for i, (bar, value) in enumerate(zip(bars, data)):
                height = bar.get_height()
                self.sort_ax.text(bar.get_x() + bar.get_width()/2., height + max(data)*0.01,
                                f'{value}', ha='center', va='bottom', color=theme["fg"], fontsize=8)
        
        self.sort_canvas.draw()
        
        # Capture frame if recording
        if self.capture_frames:
            try:
                buf = self.sort_fig.canvas.tostring_rgb()
                self.frames.append(buf)
            except:
                pass
        
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            pass

    def draw_search_data(self, data, colors, highlight_indices=None):
        """Draw search visualization"""
        if not data:
            return
            
        self.search_ax.clear()
        theme = themes[current_theme]
        self.search_ax.set_facecolor(theme["surface"])
        
        bars = self.search_ax.bar(range(len(data)), data, color=colors, edgecolor=theme["fg"], linewidth=0.5)
        
        # Highlight specific indices
        if highlight_indices:
            for idx in highlight_indices:
                if 0 <= idx < len(data):
                    bars[idx].set_color(theme["highlight"])
                    bars[idx].set_edgecolor(theme["warning"])
                    bars[idx].set_linewidth(2)
        
        self.search_ax.set_title("Search Visualization", color=theme["fg"], fontsize=14, fontweight='bold')
        self.search_ax.set_xlabel("Index", color=theme["fg"])
        self.search_ax.set_ylabel("Value", color=theme["fg"])
        
        # Add index labels
        if len(data) <= 30:
            self.search_ax.set_xticks(range(len(data)))
            self.search_ax.set_xticklabels(range(len(data)))
        
        self.search_canvas.draw()
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            pass

    def update_array_display(self, data):
        """Update the array display below the chart"""
        if not data:
            return
            
        # Clear existing labels
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        
        theme = themes[current_theme]
        
        # Create scrollable frame if data is large
        if len(data) > 20:
            canvas = tk.Canvas(self.array_frame, bg=theme["bg"], height=40, highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.array_frame, orient="horizontal", command=canvas.xview)
            scrollable_frame = tk.Frame(canvas, bg=theme["bg"])
            
            canvas.configure(xscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            canvas.pack(side="top", fill="both", expand=True)
            scrollbar.pack(side="bottom", fill="x")
            
            parent = scrollable_frame
        else:
            parent = self.array_frame
        
        # Display array elements
        for i, val in enumerate(data):
            label = tk.Label(parent, text=str(val), width=4, height=2,
                           bg=theme["entry_bg"], fg=theme["entry_fg"],
                           relief="solid", bd=1, font=("Arial", 10, "bold"))
            label.pack(side="left", padx=3, pady=5)

    # Sorting algorithms with pause/resume support and statistics
    def bubble_sort(self, data, draw_func, speed):
        """Bubble sort with visualization"""
        n = len(data)
        theme = themes[current_theme]
        comparisons = 0
        swaps = 0
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                colors = [theme["accent"] if x == j or x == j+1 else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[j] > data[j + 1]:
                    swaps += 1
                    data[j], data[j + 1] = data[j + 1], data[j]
                    colors = [theme["error"] if x == j or x == j+1 else theme["fg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
        
        draw_func(data, [theme["success"]] * n)
        return comparisons, swaps

    def selection_sort(self, data, draw_func, speed):
        """Selection sort with visualization"""
        n = len(data)
        theme = themes[current_theme]
        comparisons = 0
        swaps = 0
        
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                colors = [theme["success"] if x < i else theme["accent"] if x == j or x == min_idx else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[j] < data[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                swaps += 1
                data[i], data[min_idx] = data[min_idx], data[i]
                colors = [theme["success"] if x <= i else theme["error"] if x == min_idx else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
        
        draw_func(data, [theme["success"]] * n)
        return comparisons, swaps

    def insertion_sort(self, data, draw_func, speed):
        """Insertion sort with visualization"""
        theme = themes[current_theme]
        comparisons = 0
        swaps = 0
        
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            
            colors = [theme["success"] if x < i else theme["accent"] if x == i else theme["fg"] for x in range(len(data))]
            draw_func(data, colors)
            time.sleep(speed)
            
            while j >= 0 and data[j] > key:
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                swaps += 1
                colors = [theme["success"] if x < i else theme["error"] if x == j or x == j+1 else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                data[j + 1] = data[j]
                j -= 1
            
            data[j + 1] = key
        
        draw_func(data, [theme["success"]] * len(data))
        return comparisons, swaps

    def merge_sort(self, data, draw_func, speed):
        """Merge sort with visualization"""
        theme = themes[current_theme]
        comparisons = [0]
        swaps = [0]
        
        def merge_sort_helper(arr, l, r, depth=0):
            if l < r:
                m = (l + r) // 2
                
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                colors = [theme["warning"] if l <= x <= r else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                merge_sort_helper(arr, l, m, depth+1)
                merge_sort_helper(arr, m + 1, r, depth+1)
                merge(arr, l, m, r)
                
                colors = [theme["success"] if l <= x <= r else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
        
        def merge(arr, l, m, r):
            left = arr[l:m + 1]
            right = arr[m + 1:r + 1]
            i = j = 0
            k = l
            
            while i < len(left) and j < len(right):
                comparisons[0] += 1
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                swaps[0] += 1
                k += 1
                
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                colors = [theme["accent"] if l <= x <= r else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed * 0.5)
            
            while i < len(left):
                arr[k] = left[i]
                swaps[0] += 1
                i += 1
                k += 1
            
            while j < len(right):
                arr[k] = right[j]
                swaps[0] += 1
                j += 1
                k += 1
        
        merge_sort_helper(data, 0, len(data) - 1)
        draw_func(data, [theme["success"]] * len(data))
        return comparisons[0], swaps[0]

    def quick_sort(self, data, draw_func, speed):
        """Quick sort with visualization"""
        theme = themes[current_theme]
        comparisons = [0]
        swaps = [0]
        
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return i + 1
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons[0] += 1
                colors = [theme["warning"] if x == high else theme["accent"] if x == j else theme["success"] if low <= x <= i else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps[0] += 1
                    
                    colors = [theme["warning"] if x == high else theme["error"] if x == i or x == j else theme["success"] if low <= x < i else theme["fg"] for x in range(len(data))]
                    draw_func(data, colors)
                    time.sleep(speed)
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps[0] += 1
            return i + 1
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
        
        quick_sort_helper(data, 0, len(data) - 1)
        draw_func(data, [theme["success"]] * len(data))
        return comparisons[0], swaps[0]

    def heap_sort(self, data, draw_func, speed):
        """Heap sort with visualization"""
        theme = themes[current_theme]
        comparisons = [0]
        swaps = [0]
        
        def heapify(arr, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            
            if l < n:
                comparisons[0] += 1
                if arr[i] < arr[l]:
                    largest = l
            
            if r < n:
                comparisons[0] += 1
                if arr[largest] < arr[r]:
                    largest = r
            
            if largest != i:
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                arr[i], arr[largest] = arr[largest], arr[i]
                swaps[0] += 1
                colors = [theme["error"] if x == i or x == largest else theme["accent"] if x < n else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                heapify(arr, n, largest)
        
        n = len(data)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(data, n, i)
        
        # Extract elements one by one
        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            swaps[0] += 1
            
            # Pause check
            while self.is_paused and not self.step_mode:
                time.sleep(0.1)
                try:
                    self.root.update()
                except:
                    return comparisons[0], swaps[0]
            if self.step_mode:
                self.step_mode = False
                self.is_paused = True
            
            colors = [theme["warning"] if x == 0 or x == i else theme["success"] if x > i else theme["fg"] for x in range(len(data))]
            draw_func(data, colors)
            time.sleep(speed)
            heapify(data, i, 0)
        
        draw_func(data, [theme["success"]] * len(data))
        return comparisons[0], swaps[0]

    def radix_sort(self, data, draw_func, speed):
        """Radix sort with visualization"""
        theme = themes[current_theme]
        comparisons = [0]
        swaps = [0]
        
        def counting_sort_for_radix(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            for i in range(n):
                index = arr[i] // exp
                count[index % 10] += 1
                comparisons[0] += 1
            
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            i = n - 1
            while i >= 0:
                index = arr[i] // exp
                output[count[index % 10] - 1] = arr[i]
                count[index % 10] -= 1
                i -= 1
            
            for i in range(n):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                arr[i] = output[i]
                swaps[0] += 1
                colors = [theme["accent"] if x <= i else theme["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed * 0.5)
        
        if not data:
            return 0, 0
            
        max_val = max(data)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort_for_radix(data, exp)
            exp *= 10
        
        draw_func(data, [theme["success"]] * len(data))
        return comparisons[0], swaps[0]

    def shell_sort(self, data, draw_func, speed):
        """Shell sort with visualization"""
        theme = themes[current_theme]
        n = len(data)
        gap = n // 2
        comparisons = 0
        swaps = 0
        
        while gap > 0:
            for i in range(gap, n):
                temp = data[i]
                j = i
                
                while j >= gap and data[j - gap] > temp:
                    # Pause check
                    while self.is_paused and not self.step_mode:
                        time.sleep(0.1)
                        try:
                            self.root.update()
                        except:
                            return comparisons, swaps
                    if self.step_mode:
                        self.step_mode = False
                        self.is_paused = True
                    
                    comparisons += 1
                    swaps += 1
                    colors = [theme["accent"] if x == j or x == j-gap else theme["fg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
                    
                    data[j] = data[j - gap]
                    j -= gap
                
                data[j] = temp
            gap //= 2
        
        draw_func(data, [theme["success"]] * n)
        return comparisons, swaps

    def cocktail_sort(self, data, draw_func, speed):
        """Cocktail sort (bidirectional bubble sort) with visualization"""
        theme = themes[current_theme]
        n = len(data)
        swapped = True
        start = 0
        end = n - 1
        comparisons = 0
        swaps = 0
        
        while swapped:
            swapped = False
            
            # Forward pass
            for i in range(start, end):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                colors = [theme["accent"] if x == i or x == i+1 else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[i] > data[i + 1]:
                    swaps += 1
                    data[i], data[i + 1] = data[i + 1], data[i]
                    swapped = True
                    colors = [theme["error"] if x == i or x == i+1 else theme["fg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
            
            if not swapped:
                break
            
            swapped = False
            end -= 1
            
            # Backward pass
            for i in range(end - 1, start - 1, -1):
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                colors = [theme["accent"] if x == i or x == i+1 else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[i] > data[i + 1]:
                    swaps += 1
                    data[i], data[i + 1] = data[i + 1], data[i]
                    swapped = True
                    colors = [theme["error"] if x == i or x == i+1 else theme["fg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
            
            start += 1
        
        draw_func(data, [theme["success"]] * n)
        return comparisons, swaps

    def comb_sort(self, data, draw_func, speed):
        """Comb sort with visualization"""
        theme = themes[current_theme]
        n = len(data)
        gap = n
        shrink = 1.3
        sorted_flag = False
        comparisons = 0
        swaps = 0
        
        while not sorted_flag:
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted_flag = True
            
            i = 0
            while i + gap < n:
                # Pause check
                while self.is_paused and not self.step_mode:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except:
                        return comparisons, swaps
                if self.step_mode:
                    self.step_mode = False
                    self.is_paused = True
                
                comparisons += 1
                colors = [theme["accent"] if x == i or x == i+gap else theme["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[i] > data[i + gap]:
                    data[i], data[i + gap] = data[i + gap], data[i]
                    swaps += 1
                    sorted_flag = False
                    colors = [theme["error"] if x == i or x == i+gap else theme["fg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
                
                i += 1
        
        draw_func(data, [theme["success"]] * n)
        return comparisons, swaps

    # Search algorithms
    def linear_search(self, arr, target, draw_func, speed):
        """Linear search with visualization"""
        theme = themes[current_theme]
        
        for i in range(len(arr)):
            colors = [theme["accent"] if x == i else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [i])
            time.sleep(speed)
            
            if arr[i] == target:
                colors = [theme["success"] if x == i else theme["fg"] for x in range(len(arr))]
                draw_func(arr, colors, [i])
                self.search_status.config(text=f"✓ Found {target} at index {i}")
                return i
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    def binary_search(self, arr, target, draw_func, speed):
        """Binary search with visualization"""
        theme = themes[current_theme]
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            colors = [theme["warning"] if left <= x <= right else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, mid, right])
            time.sleep(speed)
            
            if arr[mid] == target:
                colors = [theme["success"] if x == mid else theme["fg"] for x in range(len(arr))]
                draw_func(arr, colors, [mid])
                self.search_status.config(text=f"✓ Found {target} at index {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    def jump_search(self, arr, target, draw_func, speed):
        """Jump search with visualization"""
        theme = themes[current_theme]
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Jump through the array
        while arr[min(step, n) - 1] < target:
            colors = [theme["warning"] if prev <= x < min(step, n) else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [min(step, n) - 1])
            time.sleep(speed)
            
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                self.search_status.config(text=f"✗ {target} not found in array")
                return -1
        
        # Linear search in the identified block
        while arr[prev] < target:
            colors = [theme["accent"] if x == prev else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev])
            time.sleep(speed)
            
            prev += 1
            if prev == min(step, n):
                self.search_status.config(text=f"✗ {target} not found in array")
                return -1
        
        if arr[prev] == target:
            colors = [theme["success"] if x == prev else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev])
            self.search_status.config(text=f"✓ Found {target} at index {prev}")
            return prev
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    def interpolation_search(self, arr, target, draw_func, speed):
        """Interpolation search with visualization"""
        theme = themes[current_theme]
        left, right = 0, len(arr) - 1
        
        while left <= right and arr[left] <= target <= arr[right]:
            if left == right:
                if arr[left] == target:
                    colors = [theme["success"] if x == left else theme["fg"] for x in range(len(arr))]
                    draw_func(arr, colors, [left])
                    self.search_status.config(text=f"✓ Found {target} at index {left}")
                    return left
                else:
                    self.search_status.config(text=f"✗ {target} not found in array")
                    return -1
            
            # Calculate position using interpolation formula
            pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))
            
            # Ensure pos is within bounds
            pos = max(left, min(pos, right))
            
            colors = [theme["warning"] if left <= x <= right else theme["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, pos, right])
            time.sleep(speed)
            
            if arr[pos] == target:
                colors = [theme["success"] if x == pos else theme["fg"] for x in range(len(arr))]
                draw_func(arr, colors, [pos])
                self.search_status.config(text=f"✓ Found {target} at index {pos}")
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    def exponential_search(self, arr, target, draw_func, speed):
        """Exponential search with visualization"""
        theme = themes[current_theme]
        n = len(arr)
        
        if arr[0] == target:
            colors = [theme["success"] if x == 0 else theme["fg"] for x in range(n)]
            draw_func(arr, colors, [0])
            self.search_status.config(text=f"✓ Found {target} at index 0")
            return 0
        
        # Find range for binary search
        i = 1
        while i < n and arr[i] <= target:
            colors = [theme["warning"] if x <= i else theme["fg"] for x in range(n)]
            draw_func(arr, colors, [i])
            time.sleep(speed)
            i *= 2
        
        # Binary search in found range
        left = i // 2
        right = min(i, n - 1)
        
        while left <= right:
            mid = (left + right) // 2
            colors = [theme["warning"] if left <= x <= right else theme["fg"] for x in range(n)]
            draw_func(arr, colors, [left, mid, right])
            time.sleep(speed)
            
            if arr[mid] == target:
                colors = [theme["success"] if x == mid else theme["fg"] for x in range(n)]
                draw_func(arr, colors, [mid])
                self.search_status.config(text=f"✓ Found {target} at index {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    def fibonacci_search(self, arr, target, draw_func, speed):
        """Fibonacci search with visualization"""
        theme = themes[current_theme]
        n = len(arr)
        
        # Initialize fibonacci numbers
        fib_m2 = 0  # (m-2)'th Fibonacci
        fib_m1 = 1  # (m-1)'th Fibonacci
        fib_m = fib_m2 + fib_m1  # m'th Fibonacci
        
        while fib_m < n:
            fib_m2 = fib_m1
            fib_m1 = fib_m
            fib_m = fib_m2 + fib_m1
        
        offset = -1
        
        while fib_m > 1:
            i = min(offset + fib_m2, n - 1)
            
            colors = [theme["accent"] if x == i else theme["fg"] for x in range(n)]
            draw_func(arr, colors, [i])
            time.sleep(speed)
            
            if arr[i] < target:
                fib_m = fib_m1
                fib_m1 = fib_m2
                fib_m2 = fib_m - fib_m1
                offset = i
            elif arr[i] > target:
                fib_m = fib_m2
                fib_m1 = fib_m1 - fib_m2
                fib_m2 = fib_m - fib_m1
            else:
                colors = [theme["success"] if x == i else theme["fg"] for x in range(n)]
                draw_func(arr, colors, [i])
                self.search_status.config(text=f"✓ Found {target} at index {i}")
                return i
        
        if fib_m1 and offset + 1 < n and arr[offset + 1] == target:
            colors = [theme["success"] if x == offset+1 else theme["fg"] for x in range(n)]
            draw_func(arr, colors, [offset + 1])
            self.search_status.config(text=f"✓ Found {target} at index {offset + 1}")
            return offset + 1
        
        self.search_status.config(text=f"✗ {target} not found in array")
        return -1

    # Tree operations
    def insert_node(self):
        """Insert a node into the binary search tree"""
        try:
            value_str = self.tree_value_entry.get().strip()
            
            if not value_str:
                messagebox.showwarning("Empty Input", "Please enter a value.")
                return
            
            value = int(value_str)
            
            if value < -1000 or value > 1000:
                messagebox.showwarning("Invalid Range", 
                                      "Please enter a value between -1000 and 1000")
                return
            
            if self.binary_tree is None:
                self.binary_tree = TreeNode(value)
            else:
                self._insert_recursive(self.binary_tree, value)
            
            self.draw_tree()
            self.update_tree_info()
            self.tree_status.config(text=f"✓ Inserted {value}")
            self.tree_value_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _insert_recursive(self, root, value):
        """Recursive helper for inserting nodes"""
        if value < root.value:
            if root.left is None:
                root.left = TreeNode(value)
            else:
                self._insert_recursive(root.left, value)
        else:
            if root.right is None:
                root.right = TreeNode(value)
            else:
                self._insert_recursive(root.right, value)

    def delete_node(self):
        """Delete a node from the binary search tree"""
        try:
            value_str = self.tree_value_entry.get().strip()
            
            if not value_str:
                messagebox.showwarning("Empty Input", "Please enter a value.")
                return
            
            value = int(value_str)
            self.binary_tree = self._delete_recursive(self.binary_tree, value)
            self.draw_tree()
            self.update_tree_info()
            self.tree_status.config(text=f"✓ Deleted {value}")
            self.tree_value_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _delete_recursive(self, root, value):
        """Recursive helper for deleting nodes"""
        if root is None:
            return root
        
        if value < root.value:
            root.left = self._delete_recursive(root.left, value)
        elif value > root.value:
            root.right = self._delete_recursive(root.right, value)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            
            temp = self._find_min(root.right)
            root.value = temp.value
            root.right = self._delete_recursive(root.right, temp.value)
        
        return root

    def _find_min(self, root):
        """Find minimum value node in tree"""
        while root.left is not None:
            root = root.left
        return root

    def search_tree(self):
        """Search for a value in the tree"""
        try:
            value_str = self.tree_value_entry.get().strip()
            
            if not value_str:
                messagebox.showwarning("Empty Input", "Please enter a value.")
                return
            
            value = int(value_str)
            found = self._search_recursive(self.binary_tree, value)
            if found:
                self.tree_status.config(text=f"✓ Found {value} in tree")
            else:
                self.tree_status.config(text=f"✗ {value} not found in tree")
            self.tree_value_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _search_recursive(self, root, value):
        """Recursive helper for searching nodes"""
        if root is None or root.value == value:
            return root is not None
        
        if value < root.value:
            return self._search_recursive(root.left, value)
        return self._search_recursive(root.right, value)

    def clear_tree(self):
        """Clear the entire tree"""
        self.binary_tree = None
        self.draw_tree()
        self.update_tree_info()
        self.tree_status.config(text="✓ Tree cleared")

    def draw_tree(self):
        """Draw the binary tree"""
        self.tree_ax.clear()
        theme = themes[current_theme]
        self.tree_ax.set_facecolor(theme["surface"])
        self.tree_ax.set_aspect('equal')
        self.tree_ax.axis('off')
        
        if self.binary_tree is None:
            self.tree_ax.text(0.5, 0.5, "Empty Tree", ha='center', va='center', 
                            transform=self.tree_ax.transAxes, color=theme["fg"], fontsize=16)
        else:
            positions = {}
            self._calculate_positions(self.binary_tree, 0, 0, 4, positions)
            self._draw_edges(self.binary_tree, positions, theme)
            self._draw_nodes(positions, theme)
        
        self.tree_canvas.draw()

    def _calculate_positions(self, node, x, y, width, positions):
        """Calculate positions for tree nodes"""
        if node is not None:
            positions[node] = (x, y)
            if node.left:
                self._calculate_positions(node.left, x - width, y - 1, width / 2, positions)
            if node.right:
                self._calculate_positions(node.right, x + width, y - 1, width / 2, positions)

    def _draw_edges(self, node, positions, theme):
        """Draw edges between tree nodes"""
        if node is not None:
            x, y = positions[node]
            if node.left:
                left_x, left_y = positions[node.left]
                self.tree_ax.plot([x, left_x], [y, left_y], '-', color=theme["fg"], linewidth=2, markersize=0)
                self._draw_edges(node.left, positions, theme)
            if node.right:
                right_x, right_y = positions[node.right]
                self.tree_ax.plot([x, right_x], [y, right_y], '-', color=theme["fg"], linewidth=2, markersize=0)
                self._draw_edges(node.right, positions, theme)

    def _draw_nodes(self, positions, theme):
        """Draw tree nodes"""
        for node, (x, y) in positions.items():
            circle = Circle((x, y), 0.3, color=theme["accent"], ec=theme["fg"], linewidth=2)
            self.tree_ax.add_patch(circle)
            self.tree_ax.text(x, y, str(node.value), ha='center', va='center', 
                            color='white', fontsize=12, fontweight='bold')

    def traverse_tree(self, traversal_type):
        """Perform tree traversal"""
        if self.binary_tree is None:
            self.tree_status.config(text="⚠ Tree is empty")
            return
        
        result = []
        
        if traversal_type == "inorder":
            self._inorder_traversal(self.binary_tree, result)
        elif traversal_type == "preorder":
            self._preorder_traversal(self.binary_tree, result)
        elif traversal_type == "postorder":
            self._postorder_traversal(self.binary_tree, result)
        elif traversal_type == "level_order":
            self._level_order_traversal(self.binary_tree, result)
        
        self.tree_info_text.delete(1.0, tk.END)
        self.tree_info_text.insert(tk.END, f"{traversal_type.replace('_', ' ').title()}:\n{' → '.join(map(str, result))}")
        self.tree_status.config(text=f"✓ {traversal_type.replace('_', ' ').title()} traversal completed")

    def _inorder_traversal(self, root, result):
        """Inorder traversal: Left -> Root -> Right"""
        if root:
            self._inorder_traversal(root.left, result)
            result.append(root.value)
            self._inorder_traversal(root.right, result)

    def _preorder_traversal(self, root, result):
        """Preorder traversal: Root -> Left -> Right"""
        if root:
            result.append(root.value)
            self._preorder_traversal(root.left, result)
            self._preorder_traversal(root.right, result)

    def _postorder_traversal(self, root, result):
        """Postorder traversal: Left -> Right -> Root"""
        if root:
            self._postorder_traversal(root.left, result)
            self._postorder_traversal(root.right, result)
            result.append(root.value)

    def _level_order_traversal(self, root, result):
        """Level order traversal (BFS)"""
        if root:
            queue = [root]
            while queue:
                node = queue.pop(0)
                result.append(node.value)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

    def update_tree_info(self):
        """Update tree information display"""
        if self.binary_tree is None:
            info = "Tree: Empty\nHeight: 0\nNodes: 0"
        else:
            height = self._get_tree_height(self.binary_tree)
            node_count = self._count_nodes(self.binary_tree)
            info = f"Tree: Binary Search Tree\nHeight: {height}\nNodes: {node_count}"
        
        self.tree_info_text.delete(1.0, tk.END)
        self.tree_info_text.insert(tk.END, info)

    def _get_tree_height(self, root):
        """Get height of tree"""
        if root is None:
            return 0
        return max(self._get_tree_height(root.left), self._get_tree_height(root.right)) + 1

    def _count_nodes(self, root):
        """Count nodes in tree"""
        if root is None:
            return 0
        return self._count_nodes(root.left) + self._count_nodes(root.right) + 1

    # Algorithm execution methods with threading
    def run_sorting_algorithm(self, algorithm, name):
        """Run a sorting algorithm with timing in a separate thread"""
        if not self.data:
            messagebox.showwarning("No Data", "Please generate data first.")
            return
        
        # Reset pause state
        self.is_paused = False
        self.step_mode = False
        
        def sort_thread():
            try:
                self.is_running = True
                data_copy = self.data.copy()
                
                # Update status on main thread
                self.root.after(0, lambda: self.sort_status.config(text=f"⏵ Running {name}..."))
                
                start_time = time.time()
                result = algorithm(data_copy, self.draw_sort_data, self.sort_speed.get())
                end_time = time.time()
                
                execution_times[name] = end_time - start_time
                self.data = data_copy
                
                # Format status with stats if available
                if result and len(result) == 2:
                    comparisons, swaps = result
                    status_text = f"✓ {name} completed in {end_time - start_time:.4f}s | Comparisons: {comparisons} | Swaps: {swaps}"
                else:
                    status_text = f"✓ {name} completed in {end_time - start_time:.4f} seconds"
                
                # Update UI on main thread
                self.root.after(0, lambda: self.update_array_display(self.data))
                self.root.after(0, lambda: self.sort_status.config(text=status_text))
                self.root.after(0, lambda: self.save_to_sort_history(name, self.data.copy(), end_time - start_time))
                
                self.is_running = False
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Algorithm error: {str(e)}"))
                self.is_running = False
        
        # Start thread
        threading.Thread(target=sort_thread, daemon=True).start()

    def run_search_algorithm(self, algorithm, name):
        """Run a search algorithm"""
        if not self.search_array:
            messagebox.showwarning("No Data", "Please generate search data first.")
            return
        
        target_str = self.search_target_entry.get().strip()
        if not target_str:
            messagebox.showwarning("No Target", "Please enter a target value.")
            return
        
        try:
            target = int(target_str)
        except ValueError:
            messagebox.showerror("Invalid Target", "Please enter a valid integer.")
            return
        
        def search_thread():
            try:
                self.search_status.config(text=f"⏵ Running {name}...")
                
                start_time = time.time()
                result = algorithm(self.search_array, target, self.draw_search_data, 0.5)
                end_time = time.time()
                
                # Save to search history
                search_entry = {
                    "algorithm": name,
                    "array": self.search_array.copy(),
                    "target": target,
                    "result": result,
                    "time": end_time - start_time,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                search_history.append(search_entry)
                self.root.after(0, lambda: self.save_search_history())
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Search error: {str(e)}"))
        
        threading.Thread(target=search_thread, daemon=True).start()

    # History and data management
    def save_to_sort_history(self, algorithm, data, execution_time):
        """Save sorting result to history"""
        try:
            entry = {
                "algorithm": algorithm,
                "data": data,
                "time": execution_time,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            sorting_history.append(entry)
            self.save_sort_history()
        except Exception as e:
            print(f"Failed to save sort history: {e}")

    def load_history(self):
        """Load history from files"""
        global sorting_history, search_history
        try:
            with open(HISTORY_FILE, "r") as file:
                sorting_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            sorting_history = []
        
        try:
            with open(SEARCH_HISTORY_FILE, "r") as file:
                search_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            search_history = []

    def save_sort_history(self):
        """Save sorting history to file"""
        try:
            with open(HISTORY_FILE, "w") as file:
                json.dump(sorting_history, file, indent=4)
        except Exception as e:
            print(f"Failed to save sort history: {e}")

    def save_search_history(self):
        """Save search history to file"""
        try:
            with open(SEARCH_HISTORY_FILE, "w") as file:
                json.dump(search_history, file, indent=4)
        except Exception as e:
            print(f"Failed to save search history: {e}")

    def save_sorted_data(self):
        """Save current sorted data"""
        if not self.data:
            messagebox.showwarning("No Data", "No data to save.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Index', 'Value'])
                        for i, value in enumerate(self.data):
                            writer.writerow([i, value])
                else:
                    with open(filename, 'w') as file:
                        json.dump({
                            "data": self.data,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }, file, indent=4)
                
                messagebox.showinfo("Success", f"Data saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def load_data_from_file(self):
        """Load data from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'r') as file:
                        reader = csv.reader(file)
                        next(reader)  # Skip header
                        self.data = [int(row[1]) for row in reader if len(row) > 1]
                else:
                    with open(filename, 'r') as file:
                        data = json.load(file)
                        self.data = data.get('data', [])
                
                if self.data:
                    self.sort_entry.delete(0, tk.END)
                    self.sort_entry.insert(0, ','.join(map(str, self.data)))
                    self.draw_sort_data(self.data, [bar_color] * len(self.data))
                    self.update_array_display(self.data)
                    messagebox.showinfo("Success", f"Data loaded from {filename}")
                else:
                    messagebox.showwarning("Empty File", "No data found in file.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    # Analysis and comparison methods
    def compare_sorting_algorithms(self):
        """Compare sorting algorithm performance"""
        if not execution_times:
            messagebox.showinfo("No Data", "Run some sorting algorithms first to compare performance.")
            return
        
        self.time_ax.clear()
        theme = themes[current_theme]
        self.time_ax.set_facecolor(theme["surface"])
        
        algorithms = list(execution_times.keys())
        times = list(execution_times.values())
        
        bars = self.time_ax.bar(algorithms, times, color=theme["accent"], alpha=0.8, edgecolor=theme["fg"])
        self.time_ax.set_title("Sorting Algorithm Time Comparison", color=theme["fg"], fontsize=14, fontweight='bold')
        self.time_ax.set_ylabel("Execution Time (seconds)", color=theme["fg"])
        self.time_ax.set_xlabel("Algorithm", color=theme["fg"])
        self.time_ax.tick_params(axis='x', rotation=45, colors=theme["fg"])
        
        # Add value labels on bars
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.time_ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{time_val:.4f}s', ha='center', va='bottom', color=theme["fg"], fontsize=9)
        
        # Space complexity chart (theoretical)
        self.space_ax.clear()
        self.space_ax.set_facecolor(theme["surface"])
        
        space_complexity = {
            'Bubble Sort': 1, 'Selection Sort': 1, 'Insertion Sort': 1,
            'Merge Sort': len(self.data) if self.data else 10,
            'Quick Sort': math.log2(len(self.data)) if self.data and len(self.data) > 1 else 3,
            'Heap Sort': 1, 'Radix Sort': len(self.data) if self.data else 10,
            'Shell Sort': 1, 'Cocktail Sort': 1, 'Comb Sort': 1
        }
        
        present_algorithms = [alg for alg in algorithms if alg in space_complexity]
        space_values = [space_complexity[alg] for alg in present_algorithms]
        
        if present_algorithms:
            bars2 = self.space_ax.bar(present_algorithms, space_values, color=theme["warning"], alpha=0.8, edgecolor=theme["fg"])
            self.space_ax.set_title("Space Complexity (Relative)", color=theme["fg"], fontsize=14, fontweight='bold')
            self.space_ax.set_ylabel("Space Usage", color=theme["fg"])
            self.space_ax.set_xlabel("Algorithm", color=theme["fg"])
            self.space_ax.tick_params(axis='x', rotation=45, colors=theme["fg"])
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def compare_search_algorithms(self):
        """Compare search algorithm performance from history"""
        if not search_history:
            messagebox.showinfo("No Data", "Run some search algorithms first to compare performance.")
            return
        
        self.time_ax.clear()
        self.space_ax.clear()
        theme = themes[current_theme]
        self.time_ax.set_facecolor(theme["surface"])
        self.space_ax.set_facecolor(theme["surface"])
        
        # Group search history by algorithm
        algo_times = {}
        for entry in search_history:
            algo = entry['algorithm']
            if algo not in algo_times:
                algo_times[algo] = []
            algo_times[algo].append(entry['time'])
        
        # Calculate average times
        algorithms = list(algo_times.keys())
        avg_times = [sum(times) / len(times) for times in algo_times.values()]
        
        bars = self.time_ax.bar(algorithms, avg_times, color=theme["accent"], alpha=0.8, edgecolor=theme["fg"])
        self.time_ax.set_title("Search Algorithm Time Comparison (Average)", color=theme["fg"], fontsize=14, fontweight='bold')
        self.time_ax.set_ylabel("Average Execution Time (seconds)", color=theme["fg"])
        self.time_ax.set_xlabel("Algorithm", color=theme["fg"])
        self.time_ax.tick_params(axis='x', rotation=45, colors=theme["fg"])
        
        # Add value labels on bars
        for bar, time_val in zip(bars, avg_times):
            height = bar.get_height()
            self.time_ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{time_val:.4f}s', ha='center', va='bottom', color=theme["fg"], fontsize=9)
        
        # Success rate chart
        success_rates = {}
        for algo in algorithms:
            total = len([e for e in search_history if e['algorithm'] == algo])
            successful = len([e for e in search_history if e['algorithm'] == algo and e['result'] != -1])
            success_rates[algo] = (successful / total * 100) if total > 0 else 0
        
        bars2 = self.space_ax.bar(algorithms, list(success_rates.values()), 
                                   color=theme["success"], alpha=0.8, edgecolor=theme["fg"])
        self.space_ax.set_title("Search Success Rate", color=theme["fg"], fontsize=14, fontweight='bold')
        self.space_ax.set_ylabel("Success Rate (%)", color=theme["fg"])
        self.space_ax.set_xlabel("Algorithm", color=theme["fg"])
        self.space_ax.tick_params(axis='x', rotation=45, colors=theme["fg"])
        self.space_ax.set_ylim(0, 110)
        
        # Add value labels
        for bar, rate in zip(bars2, success_rates.values()):
            height = bar.get_height()
            self.space_ax.text(bar.get_x() + bar.get_width()/2., height,
                              f'{rate:.1f}%', ha='center', va='bottom', color=theme["fg"], fontsize=9)
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def show_complexity_analysis(self):
        """Show Big O complexity analysis"""
        complexity_window = tk.Toplevel(self.root)
        complexity_window.title("Big O Complexity Analysis")
        complexity_window.geometry("900x700")
        theme = themes[current_theme]
        complexity_window.configure(bg=theme["bg"])
        
        # Title
        title_label = tk.Label(complexity_window, text="ALGORITHM COMPLEXITY ANALYSIS", 
                              bg=theme["bg"], fg=theme["accent"], 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # Create notebook for different categories
        notebook = ttk.Notebook(complexity_window)
        
        # Sorting algorithms tab
        sort_frame = tk.Frame(notebook, bg=theme["bg"])
        notebook.add(sort_frame, text="Sorting Algorithms")
        
        # Create scrolled text for sorting
        sort_text = scrolledtext.ScrolledText(sort_frame, width=100, height=30, 
                                             bg=theme["entry_bg"], fg=theme["entry_fg"],
                                             font=("Courier", 10), relief=tk.FLAT, padx=10, pady=10)
        sort_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        sorting_complexity = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         SORTING ALGORITHMS COMPLEXITY                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│   Algorithm     │  Best Case   │ Average Case │  Worst Case  │Space Complex.│
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Bubble Sort     │   O(n)       │   O(n²)      │   O(n²)      │   O(1)       │
│ Selection Sort  │   O(n²)      │   O(n²)      │   O(n²)      │   O(1)       │
│ Insertion Sort  │   O(n)       │   O(n²)      │   O(n²)      │   O(1)       │
│ Merge Sort      │   O(n log n) │   O(n log n) │   O(n log n) │   O(n)       │
│ Quick Sort      │   O(n log n) │   O(n log n) │   O(n²)      │   O(log n)   │
│ Heap Sort       │   O(n log n) │   O(n log n) │   O(n log n) │   O(1)       │
│ Radix Sort      │   O(nk)      │   O(nk)      │   O(nk)      │   O(n+k)     │
│ Shell Sort      │   O(n log n) │   O(n^1.5)   │   O(n²)      │   O(1)       │
│ Cocktail Sort   │   O(n)       │   O(n²)      │   O(n²)      │   O(1)       │
│ Comb Sort       │   O(n log n) │   O(n²/2^p)  │   O(n²)      │   O(1)       │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

ALGORITHM CHARACTERISTICS:

1. BUBBLE SORT
   • Simple comparison-based sorting
   • Repeatedly swaps adjacent elements if in wrong order
   • Stable sort (maintains relative order of equal elements)
   • Best for: Small datasets, nearly sorted data
   
2. SELECTION SORT
   • Divides array into sorted and unsorted regions
   • Repeatedly finds minimum from unsorted region
   • Not stable, minimal swaps (O(n) swaps)
   • Best for: Small datasets where swap cost is high
   
3. INSERTION SORT
   • Builds final sorted array one item at a time
   • Efficient for small data sets
   • Adaptive: O(n) when nearly sorted
   • Best for: Small/nearly sorted datasets, online sorting
   
4. MERGE SORT
   • Divide and conquer algorithm
   • Stable, predictable performance
   • Requires extra space for merging
   • Best for: Large datasets, linked lists, external sorting
   
5. QUICK SORT
   • Divide and conquer with partitioning
   • In-place sorting (low space overhead)
   • Unstable, but can be made stable
   • Best for: Large datasets, general-purpose sorting
   
6. HEAP SORT
   • Uses binary heap data structure
   • In-place, not stable
   • Consistent O(n log n) performance
   • Best for: When guaranteed O(n log n) needed with O(1) space
   
7. RADIX SORT
   • Non-comparison based sorting
   • Sorts by processing digits
   • Linear time for fixed-length integers
   • Best for: Integer keys, fixed-length strings
   
8. SHELL SORT
   • Generalization of insertion sort
   • Allows exchange of far items
   • Gap sequence affects performance
   • Best for: Medium-sized arrays
   
9. COCKTAIL SORT
   • Bidirectional bubble sort
   • Slightly better than bubble sort
   • Stable sorting algorithm
   • Best for: Small datasets with some order
   
10. COMB SORT
    • Improved bubble sort with gap
    • Eliminates turtles (small values at end)
    • Simple to implement
    • Best for: Better alternative to bubble sort

CHOOSING THE RIGHT ALGORITHM:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Small datasets (n < 10): Insertion Sort
- Nearly sorted data: Insertion Sort, Bubble Sort
- Large datasets: Merge Sort, Quick Sort, Heap Sort
- Memory constraints: Heap Sort, Quick Sort, Shell Sort
- Stability required: Merge Sort, Insertion Sort, Bubble Sort
- Integer/String keys: Radix Sort
- General purpose: Quick Sort (with good pivot selection)
"""
        
        sort_text.insert(tk.END, sorting_complexity)
        sort_text.config(state=tk.DISABLED)
        
        # Search algorithms tab
        search_frame = tk.Frame(notebook, bg=theme["bg"])
        notebook.add(search_frame, text="Search Algorithms")
        
        search_text = scrolledtext.ScrolledText(search_frame, width=100, height=30,
                                               bg=theme["entry_bg"], fg=theme["entry_fg"],
                                               font=("Courier", 10), relief=tk.FLAT, padx=10, pady=10)
        search_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        search_complexity = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         SEARCH ALGORITHMS COMPLEXITY                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────┬──────────────┬──────────────┬──────────────┬────────────┐
│     Algorithm        │  Best Case   │ Average Case │  Worst Case  │Prerequisites│
├──────────────────────┼──────────────┼──────────────┼──────────────┼────────────┤
│ Linear Search        │   O(1)       │   O(n)       │   O(n)       │   None     │
│ Binary Search        │   O(1)       │   O(log n)   │   O(log n)   │   Sorted   │
│ Jump Search          │   O(1)       │   O(√n)      │   O(√n)      │   Sorted   │
│ Interpolation Search │   O(1)       │   O(log log n│   O(n)       │ Sorted+Uni │
│ Exponential Search   │   O(1)       │   O(log n)   │   O(log n)   │   Sorted   │
│ Fibonacci Search     │   O(1)       │   O(log n)   │   O(log n)   │   Sorted   │
└──────────────────────┴──────────────┴──────────────┴──────────────┴────────────┘

Note: Uni = Uniformly distributed data

ALGORITHM CHARACTERISTICS:

1. LINEAR SEARCH
   • Sequentially checks each element
   • Works on unsorted data
   • Simple to implement
   • Space Complexity: O(1)
   • Best for: Small datasets, unsorted data, single search
   
2. BINARY SEARCH
   • Divide and conquer on sorted array
   • Eliminates half the search space each iteration
   • Most commonly used search algorithm
   • Space Complexity: O(1) iterative, O(log n) recursive
   • Best for: Large sorted datasets, multiple searches
   
3. JUMP SEARCH
   • Jumps ahead by fixed steps, then linear search
   • Better than linear, simpler than binary
   • Optimal jump size: √n
   • Space Complexity: O(1)
   • Best for: When jumping back is costly (tape drives, forward-only)
   
4. INTERPOLATION SEARCH
   • Estimates position based on value
   • Best for uniformly distributed data
   • Can degrade to O(n) for non-uniform data
   • Space Complexity: O(1)
   • Best for: Large uniformly distributed sorted datasets
   
5. EXPONENTIAL SEARCH
   • Finds range then applies binary search
   • Useful for unbounded/infinite arrays
   • Combines with binary search
   • Space Complexity: O(1)
   • Best for: Unbounded searches, when target is near beginning
   
6. FIBONACCI SEARCH
   • Uses Fibonacci numbers to divide array
   • Similar to binary search but uses addition
   • Good for when division is expensive
   • Space Complexity: O(1)
   • Best for: When division/multiplication is costly

PERFORMANCE COMPARISON:
━━━━━━━━━━━━━━━━━━━━━━
For array of size n = 1,000,000:
- Linear Search:     ~500,000 comparisons (average)
- Binary Search:     ~20 comparisons
- Jump Search:       ~1,000 comparisons
- Interpolation:     ~8 comparisons (uniform distribution)
- Exponential:       ~20 comparisons
- Fibonacci:         ~20 comparisons

CHOOSING THE RIGHT ALGORITHM:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Unsorted data: Linear Search (only option)
- Small sorted arrays (n < 100): Linear Search
- Large sorted arrays: Binary Search
- Uniformly distributed data: Interpolation Search
- Unbounded/infinite arrays: Exponential Search
- Division is expensive: Fibonacci Search
- Forward-only access: Jump Search
"""
        
        search_text.insert(tk.END, search_complexity)
        search_text.config(state=tk.DISABLED)
        
        # Tree operations tab
        tree_frame = tk.Frame(notebook, bg=theme["bg"])
        notebook.add(tree_frame, text="Tree Operations")
        
        tree_text = scrolledtext.ScrolledText(tree_frame, width=100, height=30,
                                             bg=theme["entry_bg"], fg=theme["entry_fg"],
                                             font=("Courier", 10), relief=tk.FLAT, padx=10, pady=10)
        tree_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_complexity = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    BINARY SEARCH TREE COMPLEXITY                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────┬──────────────┬──────────────┬──────────────────────────┐
│     Operation        │  Best Case   │ Average Case │     Worst Case           │
├──────────────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Search               │   O(log n)   │   O(log n)   │   O(n)                   │
│ Insert               │   O(log n)   │   O(log n)   │   O(n)                   │
│ Delete               │   O(log n)   │   O(log n)   │   O(n)                   │
│ Inorder Traversal    │   O(n)       │   O(n)       │   O(n)                   │
│ Preorder Traversal   │   O(n)       │   O(n)       │   O(n)                   │
│ Postorder Traversal  │   O(n)       │   O(n)       │   O(n)                   │
│ Level Order          │   O(n)       │   O(n)       │   O(n)                   │
└──────────────────────┴──────────────┴──────────────┴──────────────────────────┘

Space Complexity: O(n) for storing tree, O(h) for recursive operations
where h = height of tree

TREE CHARACTERISTICS:

BINARY SEARCH TREE (BST):
- Left subtree contains nodes with keys less than parent
- Right subtree contains nodes with keys greater than parent
- Both subtrees must also be binary search trees
- Allows efficient search, insert, and delete operations
- Performance depends on tree balance

BALANCED vs UNBALANCED:
━━━━━━━━━━━━━━━━━━━━━━━
Balanced Tree (height = log n):
    4
   / \
  2   6
 / \ / \
1  3 5  7

Unbalanced Tree (height = n):
1
 \
  2
   \
    3
     \
      4
       \
        5

TRAVERSAL METHODS:

1. INORDER (Left → Root → Right)
   • Visits nodes in ascending order
   • Used for: Printing sorted values, BST validation
   • Result for above balanced tree: 1, 2, 3, 4, 5, 6, 7

2. PREORDER (Root → Left → Right)
   • Root visited before children
   • Used for: Tree copying, prefix expression evaluation
   • Result for above balanced tree: 4, 2, 1, 3, 6, 5, 7

3. POSTORDER (Left → Right → Root)
   • Root visited after children
   • Used for: Tree deletion, postfix expression evaluation
   • Result for above balanced tree: 1, 3, 2, 5, 7, 6, 4

4. LEVEL ORDER (Breadth-First)
   • Visits nodes level by level
   • Uses queue data structure
   • Result for above balanced tree: 4, 2, 6, 1, 3, 5, 7

INSERTION ALGORITHM:
━━━━━━━━━━━━━━━━━━━
1. Start at root
2. If value < current node, go left; otherwise go right
3. Repeat until finding empty position
4. Insert new node at empty position

DELETION CASES:
━━━━━━━━━━━━━━━
1. Node with no children: Simply remove
2. Node with one child: Replace with child
3. Node with two children: Replace with inorder successor/predecessor

BST ADVANTAGES:
━━━━━━━━━━━━━━━
- Fast search, insert, delete (O(log n) average)
- Maintains sorted order
- Dynamic size
- Easy to implement
- In-order traversal gives sorted sequence

BST DISADVANTAGES:
━━━━━━━━━━━━━━━━━
- Can become unbalanced → O(n) operations
- No random access like arrays
- Extra memory for pointers
- More complex than linear structures

WHEN TO USE BST:
━━━━━━━━━━━━━━━━
✓ Need to maintain sorted data with frequent insertions/deletions
✓ Need fast search with dynamic data
✓ Implementing associative arrays/maps
✓ Priority queues (with heap variant)
✗ Need guaranteed O(log n) → Use AVL/Red-Black trees instead
✗ Need sequential access → Use arrays/linked lists
"""
        
        tree_text.insert(tk.END, tree_complexity)
        tree_text.config(state=tk.DISABLED)
        
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        close_btn = self.create_button(complexity_window, "Close", complexity_window.destroy, "accent", 15)
        close_btn.pack(pady=10)

    def export_analysis(self):
        """Export analysis results to file"""
        if not execution_times and not search_history:
            messagebox.showwarning("No Data", "No analysis data available to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if filename.endswith('.json'):
                    export_data = {
                        "timestamp": timestamp,
                        "sorting_times": execution_times,
                        "search_history": search_history[-10:] if len(search_history) > 10 else search_history
                    }
                    with open(filename, 'w') as file:
                        json.dump(export_data, file, indent=4)
                else:
                    with open(filename, 'w') as file:
                        file.write("=" * 80 + "\n")
                        file.write("ALGORITHM VISUALIZER - ANALYSIS REPORT\n")
                        file.write(f"Generated: {timestamp}\n")
                        file.write("=" * 80 + "\n\n")
                        
                        if execution_times:
                            file.write("SORTING ALGORITHM PERFORMANCE:\n")
                            file.write("-" * 80 + "\n")
                            for algo, time_val in sorted(execution_times.items(), key=lambda x: x[1]):
                                file.write(f"{algo:.<40} {time_val:.6f} seconds\n")
                            file.write("\n")
                        
                        if search_history:
                            file.write("RECENT SEARCH HISTORY:\n")
                            file.write("-" * 80 + "\n")
                            recent_searches = search_history[-10:] if len(search_history) > 10 else search_history
                            for i, entry in enumerate(recent_searches, 1):
                                file.write(f"\n{i}. {entry['algorithm']}\n")
                                file.write(f"   Target: {entry['target']}\n")
                                file.write(f"   Result: {'Found at index ' + str(entry['result']) if entry['result'] != -1 else 'Not found'}\n")
                                file.write(f"   Time: {entry['time']:.6f} seconds\n")
                                file.write(f"   Date: {entry['timestamp']}\n")
                
                messagebox.showinfo("Success", f"Analysis exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export analysis: {str(e)}")

    def view_sort_history(self):
        """View sorting history"""
        if not sorting_history:
            messagebox.showinfo("No History", "No sorting history available.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Sorting History")
        history_window.geometry("800x600")
        theme = themes[current_theme]
        history_window.configure(bg=theme["bg"])
        
        # Title
        title_label = tk.Label(history_window, text="SORTING HISTORY", 
                              bg=theme["bg"], fg=theme["accent"], 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Create frame for listbox and scrollbar
        list_frame = tk.Frame(history_window, bg=theme["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                 bg=theme["entry_bg"], fg=theme["entry_fg"],
                                 font=("Courier", 10), selectmode=tk.SINGLE)
        history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)
        
        # Populate history
        for i, entry in enumerate(reversed(sorting_history), 1):
            history_list.insert(tk.END, f"{i}. {entry['algorithm']} - {entry['timestamp']} - Time: {entry['time']:.4f}s")
        
        # Detail frame
        detail_frame = tk.LabelFrame(history_window, text="Details", 
                                    bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        detail_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        detail_text = scrolledtext.ScrolledText(detail_frame, height=6, bg=theme["entry_bg"], 
                                               fg=theme["entry_fg"], font=("Courier", 9))
        detail_text.pack(fill=tk.X, padx=5, pady=5)
        
        def show_details(event):
            selection = history_list.curselection()
            if selection:
                idx = len(sorting_history) - 1 - selection[0]
                entry = sorting_history[idx]
                detail_text.delete(1.0, tk.END)
                detail_text.insert(tk.END, f"Algorithm: {entry['algorithm']}\n")
                detail_text.insert(tk.END, f"Timestamp: {entry['timestamp']}\n")
                detail_text.insert(tk.END, f"Execution Time: {entry['time']:.6f} seconds\n")
                detail_text.insert(tk.END, f"Array Size: {len(entry['data'])}\n")
                detail_text.insert(tk.END, f"Sorted Data: {entry['data'][:20]}{'...' if len(entry['data']) > 20 else ''}\n")
        
        history_list.bind('<<ListboxSelect>>', show_details)
        
        # Close button
        close_btn = self.create_button(history_window, "Close", history_window.destroy, "accent", 15)
        close_btn.pack(pady=10)

    def view_search_history(self):
        """View search history"""
        if not search_history:
            messagebox.showinfo("No History", "No search history available.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Search History")
        history_window.geometry("800x600")
        theme = themes[current_theme]
        history_window.configure(bg=theme["bg"])
        
        # Title
        title_label = tk.Label(history_window, text="SEARCH HISTORY", 
                              bg=theme["bg"], fg=theme["accent"], 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Create frame for listbox and scrollbar
        list_frame = tk.Frame(history_window, bg=theme["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                 bg=theme["entry_bg"], fg=theme["entry_fg"],
                                 font=("Courier", 10), selectmode=tk.SINGLE)
        history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)
        
        # Populate history
        for i, entry in enumerate(reversed(search_history), 1):
            result_text = f"Found at {entry['result']}" if entry['result'] != -1 else "Not found"
            history_list.insert(tk.END, f"{i}. {entry['algorithm']} - Target: {entry['target']} - {result_text}")
        
        # Detail frame
        detail_frame = tk.LabelFrame(history_window, text="Details", 
                                    bg=theme["bg"], fg=theme["fg"], font=("Arial", 11, "bold"))
        detail_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        detail_text = scrolledtext.ScrolledText(detail_frame, height=6, bg=theme["entry_bg"], 
                                               fg=theme["entry_fg"], font=("Courier", 9))
        detail_text.pack(fill=tk.X, padx=5, pady=5)
        
        def show_details(event):
            selection = history_list.curselection()
            if selection:
                idx = len(search_history) - 1 - selection[0]
                entry = search_history[idx]
                detail_text.delete(1.0, tk.END)
                detail_text.insert(tk.END, f"Algorithm: {entry['algorithm']}\n")
                detail_text.insert(tk.END, f"Target Value: {entry['target']}\n")
                detail_text.insert(tk.END, f"Result: {'Found at index ' + str(entry['result']) if entry['result'] != -1 else 'Not found'}\n")
                detail_text.insert(tk.END, f"Execution Time: {entry['time']:.6f} seconds\n")
                detail_text.insert(tk.END, f"Timestamp: {entry['timestamp']}\n")
                detail_text.insert(tk.END, f"Array: {entry['array'][:15]}{'...' if len(entry['array']) > 15 else ''}\n")
        
        history_list.bind('<<ListboxSelect>>', show_details)
        
        # Close button
        close_btn = self.create_button(history_window, "Close", history_window.destroy, "accent", 15)
        close_btn.pack(pady=10)

    def clear_all_history(self):
        """Clear all history"""
        result = messagebox.askyesno("Clear History", 
                                    "Are you sure you want to clear all history?\nThis action cannot be undone.")
        if result:
            global sorting_history, search_history, execution_times
            sorting_history.clear()
            search_history.clear()
            execution_times.clear()
            self.save_sort_history()
            self.save_search_history()
            messagebox.showinfo("Success", "All history cleared successfully.")

    def reset_sort_visualization(self):
        """Reset sorting visualization"""
        self.data = []
        self.sort_entry.delete(0, tk.END)
        self.is_paused = False
        self.step_mode = False
        self.capture_frames = False
        self.frames = []
        
        self.sort_ax.clear()
        theme = themes[current_theme]
        self.sort_ax.set_facecolor(theme["surface"])
        self.sort_ax.text(0.5, 0.5, "Generate data to start", ha='center', va='center',
                        transform=self.sort_ax.transAxes, color=theme["fg"], fontsize=14)
        self.sort_canvas.draw()
        
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        self.sort_status.config(text="✓ Visualization reset")

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = themes[current_theme]
        
        # Apply to root window
        self.root.configure(bg=theme["bg"])
        
        # Update notebook style
        self.style.configure('TNotebook', background=theme["bg"])
        self.style.configure('TNotebook.Tab', background=theme["button_bg"], 
                           foreground=theme["fg"])
        self.style.map('TNotebook.Tab', background=[('selected', theme["accent"])])
        
        # Update all frames
        for tab in [self.sorting_tab, self.search_tab, self.tree_tab, self.analysis_tab]:
            tab.configure(bg=theme["bg"])
            self._update_frame_colors(tab, theme)
        
        # Update matplotlib figures
        for fig, ax in [(self.sort_fig, self.sort_ax), 
                       (self.search_fig, self.search_ax),
                       (self.tree_fig, self.tree_ax)]:
            fig.patch.set_facecolor(theme["surface"])
            if isinstance(ax, list):
                for a in ax:
                    a.set_facecolor(theme["surface"])
                    a.tick_params(colors=theme["fg"])
                    for spine in a.spines.values():
                        spine.set_color(theme["fg"])
            else:
                ax.set_facecolor(theme["surface"])
                ax.tick_params(colors=theme["fg"])
                for spine in ax.spines.values():
                    spine.set_color(theme["fg"])
        
        # Update analysis axes
        for ax in [self.time_ax, self.space_ax]:
            ax.set_facecolor(theme["surface"])
            ax.tick_params(colors=theme["fg"])
            for spine in ax.spines.values():
                spine.set_color(theme["fg"])
        
        # Redraw canvases
        self.sort_canvas.draw()
        self.search_canvas.draw()
        self.tree_canvas.draw()
        self.analysis_canvas.draw()
        
        # Update status labels
        for status in [self.sort_status, self.search_status, self.tree_status]:
            status.configure(bg=theme["surface"], fg=theme["fg"])
        
        # Save config
        self.save_config()

    def _update_frame_colors(self, parent, theme):
        """Recursively update colors for all child widgets"""
        for widget in parent.winfo_children():
            widget_class = widget.winfo_class()
            
            try:
                if widget_class in ['Frame', 'LabelFrame']:
                    widget.configure(bg=theme["bg"])
                    if widget_class == 'LabelFrame':
                        widget.configure(fg=theme["fg"])
                    self._update_frame_colors(widget, theme)
                elif widget_class == 'Label':
                    widget.configure(bg=theme["bg"], fg=theme["fg"])
                elif widget_class == 'Button':
                    # Skip buttons as they have specific styling
                    pass
                elif widget_class == 'Entry':
                    widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
                elif widget_class in ['Text', 'Listbox']:
                    widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
                elif widget_class == 'Radiobutton':
                    widget.configure(bg=theme["bg"], fg=theme["fg"], 
                                   selectcolor=theme["accent"], activebackground=theme["bg"])
            except tk.TclError:
                # Some widgets might not support certain configure options
                pass

    def cycle_theme(self):
        """Cycle through available themes"""
        global current_theme
        theme_list = list(themes.keys())
        current_index = theme_list.index(current_theme)
        next_index = (current_index + 1) % len(theme_list)
        current_theme = theme_list[next_index]
        
        self.apply_theme()
        self.sort_status.config(text=f"✓ Theme changed to {current_theme.replace('_', ' ').title()}")

    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Algorithm Visualizer")
        about_window.geometry("500x400")
        theme = themes[current_theme]
        about_window.configure(bg=theme["bg"])
        about_window.resizable(False, False)
        
        # Title
        title_label = tk.Label(about_window, text="Algorithm Visualizer", 
                              bg=theme["bg"], fg=theme["accent"], 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Version
        version_label = tk.Label(about_window, text="Version 2.0", 
                                bg=theme["bg"], fg=theme["fg"], 
                                font=("Arial", 12))
        version_label.pack(pady=5)
        
        # Description
        desc_frame = tk.Frame(about_window, bg=theme["bg"])
        desc_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        description = """
An advanced interactive tool for visualizing
and analyzing sorting, searching, and tree algorithms.

Features:
- 10+ Sorting Algorithms
- 6 Search Algorithms
- Binary Search Tree Operations
- Performance Analysis & Comparison
- Multiple Themes
- Export to GIF
- History Tracking
- Keyboard Shortcuts

© 2024 Algorithm Visualizer
All Rights Reserved
        """
        
        desc_label = tk.Label(desc_frame, text=description, 
                            bg=theme["bg"], fg=theme["fg"], 
                            font=("Arial", 10), justify=tk.LEFT)
        desc_label.pack()
        
        # Close button
        close_btn = self.create_button(about_window, "Close", about_window.destroy, "accent", 15)
        close_btn.pack(pady=20)

# Main execution
def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = AlgorithmVisualizer(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Add menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Load Data", command=app.load_data_from_file, accelerator="Ctrl+O")
    file_menu.add_command(label="Save Data", command=app.save_sorted_data, accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label="Export Analysis", command=app.export_analysis)
    file_menu.add_command(label="Export GIF", command=app.stop_and_export_gif)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Sort History", command=app.view_sort_history)
    view_menu.add_command(label="Search History", command=app.view_search_history)
    view_menu.add_separator()
    view_menu.add_command(label="Cycle Theme", command=app.cycle_theme, accelerator="Ctrl+T")
    
    # Tools menu
    tools_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tools", menu=tools_menu)
    tools_menu.add_command(label="Compare Sorting Algorithms", command=app.compare_sorting_algorithms)
    tools_menu.add_command(label="Compare Search Algorithms", command=app.compare_search_algorithms)
    tools_menu.add_command(label="Big O Analysis", command=app.show_complexity_analysis)
    tools_menu.add_separator()
    tools_menu.add_command(label="Clear All History", command=app.clear_all_history)
    tools_menu.add_command(label="Reset Visualization", command=app.reset_sort_visualization, accelerator="Ctrl+R")
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Keyboard Shortcuts", command=app.show_keyboard_shortcuts, accelerator="Ctrl+H")
    help_menu.add_command(label="About", command=app.show_about)
    
    # Handle window close
    def on_closing():
        if app.is_running:
            result = messagebox.askyesno("Quit", "An algorithm is running. Are you sure you want to quit?")
            if result:
                root.quit()
        else:
            root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()