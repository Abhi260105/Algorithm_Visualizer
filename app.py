import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle
from datetime import datetime
import json
import csv
import math
import networkx as nx
from matplotlib.animation import FuncAnimation

# Global variables
data = []
sorting_history = []
search_history = []
tree_data = []
HISTORY_FILE = "sorting_history.json"
SEARCH_HISTORY_FILE = "search_history.json"

# Monochrome theme - strict black and white
THEME = {
    "bg": "#f8f8f6",           # off-white background
    "fg": "#000000",           # pure black text
    "border": "#000000",       # black borders
    "grid": "#d0d0d0",         # light gray for graph grid
    "highlight": "#000000",    # black highlight
    "canvas_bg": "#f8f8f6"     # off-white canvas
}

execution_times = {}

# Tree Node class for binary tree operations
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer - Monochrome")
        self.root.geometry("1400x900")
        self.root.configure(bg=THEME["bg"])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.setup_styles()
        
        # Create tabs
        self.sorting_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        self.tree_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.sorting_tab, text="SORTING")
        self.notebook.add(self.search_tab, text="SEARCH")
        self.notebook.add(self.tree_tab, text="TREE")
        self.notebook.add(self.analysis_tab, text="ANALYSIS")
        
        self.setup_sorting_tab()
        self.setup_search_tab()
        self.setup_tree_tab()
        self.setup_analysis_tab()
        
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Initialize data
        self.data = []
        self.search_array = []
        self.binary_tree = None
        
        self.load_history()

    def setup_styles(self):
        """Setup custom ttk styles - monochrome"""
        self.style = ttk.Style()
        
        # Configure notebook style
        self.style.configure('TNotebook', 
                           background=THEME["bg"],
                           borderwidth=2,
                           relief='flat')
        self.style.configure('TNotebook.Tab', 
                           background=THEME["bg"],
                           foreground=THEME["fg"],
                           padding=[20, 10],
                           borderwidth=1,
                           relief='solid')
        self.style.map('TNotebook.Tab', 
                      background=[('selected', THEME["bg"])],
                      foreground=[('selected', THEME["fg"])])

    def setup_sorting_tab(self):
        """Setup the sorting algorithms tab - monochrome design"""
        # Main container
        main_frame = tk.Frame(self.sorting_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area with graph paper grid
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure for sorting
        self.sort_fig, self.sort_ax = plt.subplots(figsize=(12, 6))
        self.sort_fig.patch.set_facecolor(THEME["canvas_bg"])
        self.sort_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.sort_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.sort_ax.minorticks_on()
        self.sort_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        self.sort_ax.tick_params(colors=THEME["fg"], which='both')
        for spine in self.sort_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.sort_canvas = FigureCanvasTkAgg(self.sort_fig, viz_frame)
        self.sort_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Array display frame
        self.array_frame = tk.Frame(main_frame, bg=THEME["bg"], height=60, relief=tk.SOLID, bd=1)
        self.array_frame.pack(fill=tk.X, padx=20, pady=10)
        self.array_frame.pack_propagate(False)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg=THEME["bg"])
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input section
        input_section = tk.LabelFrame(controls_frame, text="DATA INPUT", 
                                    bg=THEME["bg"], fg=THEME["fg"], 
                                    font=("Courier", 10, "bold"),
                                    relief=tk.SOLID, bd=2)
        input_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(input_section, text="Array:", bg=THEME["bg"], fg=THEME["fg"], font=("Courier", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sort_entry = tk.Entry(input_section, width=30, bg=THEME["bg"], fg=THEME["fg"], 
                                 font=("Courier", 9), relief=tk.SOLID, bd=2,
                                 highlightbackground=THEME["border"], highlightthickness=1)
        self.sort_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.create_rect_button(input_section, "GENERATE", self.generate_sort_data, 12).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(input_section, text="Speed:", bg=THEME["bg"], fg=THEME["fg"], font=("Courier", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sort_speed = tk.DoubleVar(value=0.1)
        self.speed_scale = tk.Scale(input_section, from_=0.01, to=1.0, resolution=0.01, 
                                  orient=tk.HORIZONTAL, variable=self.sort_speed, length=200,
                                  bg=THEME["bg"], fg=THEME["fg"], highlightthickness=0,
                                  troughcolor=THEME["bg"], relief=tk.SOLID, bd=1)
        self.speed_scale.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # Algorithm buttons
        algo_section = tk.LabelFrame(controls_frame, text="ALGORITHMS", 
                                   bg=THEME["bg"], fg=THEME["fg"], 
                                   font=("Courier", 10, "bold"),
                                   relief=tk.SOLID, bd=2)
        algo_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        algorithms = [
            ("BUBBLE", lambda: self.run_sorting_algorithm(self.bubble_sort, "Bubble Sort")),
            ("SELECTION", lambda: self.run_sorting_algorithm(self.selection_sort, "Selection Sort")),
            ("INSERTION", lambda: self.run_sorting_algorithm(self.insertion_sort, "Insertion Sort")),
            ("MERGE", lambda: self.run_sorting_algorithm(self.merge_sort, "Merge Sort")),
            ("QUICK", lambda: self.run_sorting_algorithm(self.quick_sort, "Quick Sort")),
            ("HEAP", lambda: self.run_sorting_algorithm(self.heap_sort, "Heap Sort")),
            ("RADIX", lambda: self.run_sorting_algorithm(self.radix_sort, "Radix Sort"))
        ]
        
        for i, (text, command) in enumerate(algorithms):
            row, col = i // 4, i % 4
            self.create_rect_button(algo_section, text, command, 10).grid(row=row, column=col, padx=3, pady=3)
        
        # Control buttons
        control_section = tk.LabelFrame(controls_frame, text="CONTROLS", 
                                      bg=THEME["bg"], fg=THEME["fg"], 
                                      font=("Courier", 10, "bold"),
                                      relief=tk.SOLID, bd=2)
        control_section.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        control_buttons = [
            ("SAVE", self.save_sorted_data),
            ("LOAD", self.load_data_from_file),
            ("RESET", self.reset_sort_visualization)
        ]
        
        for i, (text, command) in enumerate(control_buttons):
            self.create_rect_button(control_section, text, command, 8).grid(row=i, column=0, padx=5, pady=3)
        
        # Status bar
        self.sort_status = tk.Label(main_frame, text="READY", bg=THEME["bg"], 
                                  fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                  relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.sort_status.pack(fill=tk.X, padx=20, pady=(0, 20))

    def setup_search_tab(self):
        """Setup the search algorithms tab - monochrome design"""
        main_frame = tk.Frame(self.search_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure for search
        self.search_fig, self.search_ax = plt.subplots(figsize=(12, 6))
        self.search_fig.patch.set_facecolor(THEME["canvas_bg"])
        self.search_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.search_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.search_ax.minorticks_on()
        self.search_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        self.search_ax.tick_params(colors=THEME["fg"], which='both')
        for spine in self.search_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.search_canvas = FigureCanvasTkAgg(self.search_fig, viz_frame)
        self.search_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=THEME["bg"])
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input section
        input_section = tk.LabelFrame(controls_frame, text="SEARCH SETUP", 
                                    bg=THEME["bg"], fg=THEME["fg"], 
                                    font=("Courier", 10, "bold"),
                                    relief=tk.SOLID, bd=2)
        input_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(input_section, text="Array:", bg=THEME["bg"], fg=THEME["fg"], font=("Courier", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.search_array_entry = tk.Entry(input_section, width=30, bg=THEME["bg"], 
                                         fg=THEME["fg"], font=("Courier", 9), 
                                         relief=tk.SOLID, bd=2)
        self.search_array_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_section, text="Target:", bg=THEME["bg"], fg=THEME["fg"], font=("Courier", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.search_target_entry = tk.Entry(input_section, width=10, bg=THEME["bg"], 
                                          fg=THEME["fg"], font=("Courier", 9), 
                                          relief=tk.SOLID, bd=2)
        self.search_target_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.create_rect_button(input_section, "GENERATE", self.generate_search_data, 12).grid(row=0, column=2, padx=5, pady=5)
        
        # Search algorithms
        search_section = tk.LabelFrame(controls_frame, text="SEARCH ALGORITHMS", 
                                     bg=THEME["bg"], fg=THEME["fg"], 
                                     font=("Courier", 10, "bold"),
                                     relief=tk.SOLID, bd=2)
        search_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        search_algorithms = [
            ("LINEAR", lambda: self.run_search_algorithm(self.linear_search, "Linear Search")),
            ("BINARY", lambda: self.run_search_algorithm(self.binary_search, "Binary Search")),
            ("JUMP", lambda: self.run_search_algorithm(self.jump_search, "Jump Search")),
            ("INTERPOLATION", lambda: self.run_search_algorithm(self.interpolation_search, "Interpolation Search"))
        ]
        
        for i, (text, command) in enumerate(search_algorithms):
            self.create_rect_button(search_section, text, command, 14).grid(row=i//2, column=i%2, padx=3, pady=3)
        
        # Status
        self.search_status = tk.Label(main_frame, text="READY", bg=THEME["bg"], 
                                    fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                    relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.search_status.pack(fill=tk.X, padx=20, pady=(0, 20))

    def create_rect_button(self, parent, text, command, width):
        """Create a perfect rectangular monochrome button"""
        btn = tk.Button(parent, text=text, command=command, width=width,
                       bg=THEME["bg"], fg=THEME["fg"], 
                       font=("Courier", 9, "bold"),
                       relief=tk.SOLID, bd=2,
                       highlightbackground=THEME["border"],
                       highlightthickness=0,
                       activebackground=THEME["fg"],
                       activeforeground=THEME["bg"],
                       cursor="hand2")
        return btn