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
    def setup_tree_tab(self):
        """Setup the tree operations tab - monochrome design"""
        main_frame = tk.Frame(self.tree_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure for tree
        self.tree_fig, self.tree_ax = plt.subplots(figsize=(12, 8))
        self.tree_fig.patch.set_facecolor(THEME["canvas_bg"])
        self.tree_ax.set_facecolor(THEME["canvas_bg"])
        self.tree_ax.set_aspect('equal')
        self.tree_ax.axis('off')
        
        self.tree_canvas = FigureCanvasTkAgg(self.tree_fig, viz_frame)
        self.tree_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=THEME["bg"])
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Tree operations
        tree_ops_section = tk.LabelFrame(controls_frame, text="TREE OPERATIONS", 
                                       bg=THEME["bg"], fg=THEME["fg"], 
                                       font=("Courier", 10, "bold"),
                                       relief=tk.SOLID, bd=2)
        tree_ops_section.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        tk.Label(tree_ops_section, text="Value:", bg=THEME["bg"], fg=THEME["fg"], font=("Courier", 9)).grid(row=0, column=0, padx=5, pady=5)
        self.tree_value_entry = tk.Entry(tree_ops_section, width=15, bg=THEME["bg"], 
                                       fg=THEME["fg"], font=("Courier", 9), 
                                       relief=tk.SOLID, bd=2)
        self.tree_value_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tree_buttons = [
            ("INSERT", self.insert_node),
            ("DELETE", self.delete_node),
            ("SEARCH", self.search_tree),
            ("CLEAR", self.clear_tree)
        ]
        
        for i, (text, command) in enumerate(tree_buttons):
            self.create_rect_button(tree_ops_section, text, command, 8).grid(row=1, column=i, padx=3, pady=5)
        
        # Traversal operations
        traversal_section = tk.LabelFrame(controls_frame, text="TRAVERSALS", 
                                        bg=THEME["bg"], fg=THEME["fg"], 
                                        font=("Courier", 10, "bold"),
                                        relief=tk.SOLID, bd=2)
        traversal_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        traversal_buttons = [
            ("INORDER", lambda: self.traverse_tree("inorder")),
            ("PREORDER", lambda: self.traverse_tree("preorder")),
            ("POSTORDER", lambda: self.traverse_tree("postorder")),
            ("LEVEL", lambda: self.traverse_tree("level_order"))
        ]
        
        for i, (text, command) in enumerate(traversal_buttons):
            self.create_rect_button(traversal_section, text, command, 10).grid(row=i//2, column=i%2, padx=3, pady=3)
        
        # Tree info
        info_section = tk.LabelFrame(controls_frame, text="TREE INFO", 
                                   bg=THEME["bg"], fg=THEME["fg"], 
                                   font=("Courier", 10, "bold"),
                                   relief=tk.SOLID, bd=2)
        info_section.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        self.tree_info_text = tk.Text(info_section, width=30, height=4, bg=THEME["bg"], 
                                    fg=THEME["fg"], font=("Courier", 8), 
                                    relief=tk.SOLID, bd=1)
        self.tree_info_text.pack(padx=5, pady=5)
        
        # Status
        self.tree_status = tk.Label(main_frame, text="READY", bg=THEME["bg"], 
                                  fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                  relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.tree_status.pack(fill=tk.X, padx=20, pady=(0, 20))

    def setup_analysis_tab(self):
        """Setup the performance analysis tab - monochrome design"""
        main_frame = tk.Frame(self.analysis_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Analysis visualization
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        self.analysis_fig, (self.time_ax, self.space_ax) = plt.subplots(1, 2, figsize=(14, 6))
        self.analysis_fig.patch.set_facecolor(THEME["canvas_bg"])
        
        for ax in [self.time_ax, self.space_ax]:
            ax.set_facecolor(THEME["canvas_bg"])
            ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
            ax.minorticks_on()
            ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
            ax.tick_params(colors=THEME["fg"], which='both')
            for spine in ax.spines.values():
                spine.set_color(THEME["border"])
                spine.set_linewidth(2)
        
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, viz_frame)
        self.analysis_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls_frame = tk.Frame(main_frame, bg=THEME["bg"])
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Analysis buttons
        analysis_section = tk.LabelFrame(controls_frame, text="PERFORMANCE ANALYSIS", 
                                       bg=THEME["bg"], fg=THEME["fg"], 
                                       font=("Courier", 10, "bold"),
                                       relief=tk.SOLID, bd=2)
        analysis_section.pack(side=tk.LEFT, padx=(0, 10))
        
        analysis_buttons = [
            ("COMPARE SORT", self.compare_sorting_algorithms),
            ("COMPARE SEARCH", self.compare_search_algorithms),
            ("BIG O", self.show_complexity_analysis),
            ("EXPORT", self.export_analysis)
        ]
        
        for i, (text, command) in enumerate(analysis_buttons):
            self.create_rect_button(analysis_section, text, command, 14).grid(row=i//2, column=i%2, padx=3, pady=3)
        
        # History section
        history_section = tk.LabelFrame(controls_frame, text="HISTORY", 
                                      bg=THEME["bg"], fg=THEME["fg"], 
                                      font=("Courier", 10, "bold"),
                                      relief=tk.SOLID, bd=2)
        history_section.pack(side=tk.RIGHT, padx=(10, 0))
        
        history_buttons = [
            ("SORT HISTORY", self.view_sort_history),
            ("SEARCH HISTORY", self.view_search_history),
            ("CLEAR ALL", self.clear_all_history)
        ]
        
        for i, (text, command) in enumerate(history_buttons):
            self.create_rect_button(history_section, text, command, 14).grid(row=i//2, column=i%2, padx=3, pady=3)

    # Data generation and management methods
    def generate_sort_data(self):
        """Generate random data for sorting visualization"""
        user_input = self.sort_entry.get().strip()
        if user_input:
            try:
                self.data = list(map(int, user_input.split(',')))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter numbers separated by commas.")
                return
        else:
            size = random.randint(10, 30)
            self.data = [random.randint(1, 100) for _ in range(size)]
            self.sort_entry.delete(0, tk.END)
            self.sort_entry.insert(0, ','.join(map(str, self.data)))
        
        self.draw_sort_data(self.data, [THEME["fg"]] * len(self.data))
        self.update_array_display(self.data)
        self.sort_status.config(text=f"GENERATED {len(self.data)} ELEMENTS")

    def generate_search_data(self):
        """Generate sorted data for search algorithms"""
        user_input = self.search_array_entry.get().strip()
        if user_input:
            try:
                self.search_array = sorted(list(map(int, user_input.split(','))))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter numbers separated by commas.")
                return
        else:
            size = random.randint(15, 25)
            self.search_array = sorted([random.randint(1, 100) for _ in range(size)])
            self.search_array_entry.delete(0, tk.END)
            self.search_array_entry.insert(0, ','.join(map(str, self.search_array)))
        
        self.draw_search_data(self.search_array, [THEME["fg"]] * len(self.search_array))
        self.search_status.config(text=f"GENERATED {len(self.search_array)} SORTED ELEMENTS")

    def draw_sort_data(self, data, colors):
        """Draw sorting visualization - monochrome bars"""
        self.sort_ax.clear()
        self.sort_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.sort_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.sort_ax.minorticks_on()
        self.sort_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        bars = self.sort_ax.bar(range(len(data)), data, color=THEME["bg"], 
                               edgecolor=THEME["border"], linewidth=2)
        
        # Fill highlighted bars
        for i, (bar, color) in enumerate(zip(bars, colors)):
            if color == THEME["fg"]:
                bar.set_facecolor(THEME["fg"])
        
        self.sort_ax.set_title("SORTING VISUALIZATION", color=THEME["fg"], 
                             fontsize=12, fontweight='bold', family='Courier')
        self.sort_ax.set_xlabel("INDEX", color=THEME["fg"], family='Courier', fontsize=10)
        self.sort_ax.set_ylabel("VALUE", color=THEME["fg"], family='Courier', fontsize=10)
        
        for spine in self.sort_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.sort_canvas.draw()
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            pass

    def draw_search_data(self, data, colors, highlight_indices=None):
        """Draw search visualization - monochrome bars"""
        self.search_ax.clear()
        self.search_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.search_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.search_ax.minorticks_on()
        self.search_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        bars = self.search_ax.bar(range(len(data)), data, color=THEME["bg"], 
                                 edgecolor=THEME["border"], linewidth=2)
        
        # Highlight specific indices with solid black fill
        if highlight_indices:
            for idx in highlight_indices:
                if 0 <= idx < len(data):
                    bars[idx].set_facecolor(THEME["fg"])
                    bars[idx].set_edgecolor(THEME["border"])
                    bars[idx].set_linewidth(3)
        
        self.search_ax.set_title("SEARCH VISUALIZATION", color=THEME["fg"], 
                               fontsize=12, fontweight='bold', family='Courier')
        self.search_ax.set_xlabel("INDEX", color=THEME["fg"], family='Courier', fontsize=10)
        self.search_ax.set_ylabel("VALUE", color=THEME["fg"], family='Courier', fontsize=10)
        
        # Add index labels
        self.search_ax.set_xticks(range(len(data)))
        self.search_ax.set_xticklabels(range(len(data)), family='Courier')
        
        for spine in self.search_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.search_canvas.draw()
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
           pass

    def update_array_display(self, data):
        """Update the array display below the chart"""
        # Clear existing labels
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame if data is large
        if len(data) > 20:
            canvas = tk.Canvas(self.array_frame, bg=THEME["bg"], height=50, highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.array_frame, orient="horizontal", command=canvas.xview)
            scrollable_frame = tk.Frame(canvas, bg=THEME["bg"])
            
            canvas.configure(xscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            canvas.pack(side="top", fill="both", expand=True)
            scrollbar.pack(side="bottom", fill="x")
            
            parent = scrollable_frame
        else:
            parent = self.array_frame
        
        # Display array elements in monochrome boxes
        for i, val in enumerate(data):
            label = tk.Label(parent, text=str(val), width=4, height=2,
                           bg=THEME["bg"], fg=THEME["fg"],
                           relief="solid", bd=2, font=("Courier", 10, "bold"))
            label.pack(side="left", padx=3, pady=5)

    # Sorting algorithms with enhanced visualization
    def bubble_sort(self, data, draw_func, speed):
        """Bubble sort with monochrome visualization"""
        n = len(data)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight comparing elements (outline only)
                colors = [THEME["bg"] if x == j or x == j+1 else THEME["fg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    # Highlight swapped elements (solid black)
                    colors = [THEME["fg"] if x == j or x == j+1 else THEME["bg"] for x in range(n)]
                    draw_func(data, colors)
                    time.sleep(speed)
        
        # Show final sorted array (all black)
        draw_func(data, [THEME["fg"]] * n)

    def selection_sort(self, data, draw_func, speed):
        """Selection sort with monochrome visualization"""
        n = len(data)
        
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                colors = [THEME["fg"] if x < i else THEME["bg"] if x == j or x == min_idx else THEME["bg"] for x in range(n)]
                draw_func(data, colors)
                time.sleep(speed)
                
                if data[j] < data[min_idx]:
                    min_idx = j
            
            data[i], data[min_idx] = data[min_idx], data[i]
            colors = [THEME["fg"] if x <= i else THEME["bg"] if x == min_idx else THEME["bg"] for x in range(n)]
            draw_func(data, colors)
            time.sleep(speed)
        
        draw_func(data, [THEME["fg"]] * n)

    def insertion_sort(self, data, draw_func, speed):
        """Insertion sort with monochrome visualization"""
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            
            colors = [THEME["fg"] if x < i else THEME["bg"] if x == i else THEME["bg"] for x in range(len(data))]
            draw_func(data, colors)
            time.sleep(speed)
            
            while j >= 0 and data[j] > key:
                colors = [THEME["fg"] if x < i else THEME["bg"] if x == j or x == j+1 else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                data[j + 1] = data[j]
                j -= 1
            
            data[j + 1] = key
        
        draw_func(data, [THEME["fg"]] * len(data))
def merge_sort(self, data, draw_func, speed):
        """Merge sort with monochrome visualization"""
        def merge_sort_helper(arr, l, r, depth=0):
            if l < r:
                m = (l + r) // 2
                
                # Highlight the section being divided
                colors = [THEME["bg"] if l <= x <= r else THEME["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                merge_sort_helper(arr, l, m, depth+1)
                merge_sort_helper(arr, m + 1, r, depth+1)
                merge(arr, l, m, r)
                
                # Highlight merged section
                colors = [THEME["fg"] if l <= x <= r else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
        
        def merge(arr, l, m, r):
            left = arr[l:m + 1]
            right = arr[m + 1:r + 1]
            i = j = 0
            k = l
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
                
                colors = [THEME["bg"] if l <= x <= r else THEME["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed * 0.5)
            
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
        
        merge_sort_helper(data, 0, len(data) - 1)
        draw_func(data, [THEME["fg"]] * len(data))

    def quick_sort(self, data, draw_func, speed):
        """Quick sort with monochrome visualization"""
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                colors = [THEME["bg"] if x == high else THEME["bg"] if x == j else THEME["fg"] if low <= x <= i else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed)
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    colors = [THEME["bg"] if x == high else THEME["fg"] if x == i or x == j else THEME["fg"] if low <= x < i else THEME["bg"] for x in range(len(data))]
                    draw_func(data, colors)
                    time.sleep(speed)
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
        
        quick_sort_helper(data, 0, len(data) - 1)
        draw_func(data, [THEME["fg"]] * len(data))

    def heap_sort(self, data, draw_func, speed):
        """Heap sort with monochrome visualization"""
        def heapify(arr, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            
            if l < n and arr[i] < arr[l]:
                largest = l
            
            if r < n and arr[largest] < arr[r]:
                largest = r
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                colors = [THEME["fg"] if x == i or x == largest else THEME["bg"] if x < n else THEME["bg"] for x in range(len(data))]
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
            colors = [THEME["bg"] if x == 0 or x == i else THEME["fg"] if x > i else THEME["bg"] for x in range(len(data))]
            draw_func(data, colors)
            time.sleep(speed)
            heapify(data, i, 0)
        
        draw_func(data, [THEME["fg"]] * len(data))

    def radix_sort(self, data, draw_func, speed):
        """Radix sort with monochrome visualization"""
        def counting_sort_for_radix(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            for i in range(n):
                index = arr[i] // exp
                count[index % 10] += 1
            
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            i = n - 1
            while i >= 0:
                index = arr[i] // exp
                output[count[index % 10] - 1] = arr[i]
                count[index % 10] -= 1
                i -= 1
            
            for i in range(n):
                arr[i] = output[i]
                colors = [THEME["bg"] if x <= i else THEME["fg"] for x in range(len(data))]
                draw_func(data, colors)
                time.sleep(speed * 0.5)
        
        max_val = max(data)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort_for_radix(data, exp)
            exp *= 10
        
        draw_func(data, [THEME["fg"]] * len(data))

    # Search algorithms
    def linear_search(self, arr, target, draw_func, speed):
        """Linear search with monochrome visualization"""
        for i in range(len(arr)):
            colors = [THEME["bg"] if x == i else THEME["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [i])
            time.sleep(speed)
            
            if arr[i] == target:
                colors = [THEME["fg"] if x == i else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [i])
                self.search_status.config(text=f"FOUND {target} AT INDEX {i}")
                return i
        
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def binary_search(self, arr, target, draw_func, speed):
        """Binary search with monochrome visualization"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            colors = [THEME["bg"] if left <= x <= right else THEME["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, mid, right])
            time.sleep(speed)
            
            if arr[mid] == target:
                colors = [THEME["fg"] if x == mid else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [mid])
                self.search_status.config(text=f"FOUND {target} AT INDEX {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def jump_search(self, arr, target, draw_func, speed):
        """Jump search with monochrome visualization"""
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Jump through the array
        while arr[min(step, n) - 1] < target:
            colors = [THEME["bg"] if prev <= x < min(step, n) else THEME["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [min(step, n) - 1])
            time.sleep(speed)
            
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                self.search_status.config(text=f"{target} NOT FOUND")
                return -1
        
        # Linear search in the identified block
        while arr[prev] < target:
            colors = [THEME["bg"] if x == prev else THEME["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev])
            time.sleep(speed)
            
            prev += 1
            if prev == min(step, n):
                self.search_status.config(text=f"{target} NOT FOUND")
                return -1
        
        if arr[prev] == target:
            colors = [THEME["fg"] if x == prev else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev])
            self.search_status.config(text=f"FOUND {target} AT INDEX {prev}")
            return prev
        
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def interpolation_search(self, arr, target, draw_func, speed):
        """Interpolation search with monochrome visualization"""
        left, right = 0, len(arr) - 1
        
        while left <= right and arr[left] <= target <= arr[right]:
            if left == right:
                if arr[left] == target:
                    colors = [THEME["fg"] if x == left else THEME["bg"] for x in range(len(arr))]
                    draw_func(arr, colors, [left])
                    self.search_status.config(text=f"FOUND {target} AT INDEX {left}")
                    return left
                else:
                    self.search_status.config(text=f"{target} NOT FOUND")
                    return -1
            
            # Calculate position using interpolation formula
            pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))
            
            colors = [THEME["bg"] if left <= x <= right else THEME["fg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, pos, right])
            time.sleep(speed)
            
            if arr[pos] == target:
                colors = [THEME["fg"] if x == pos else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [pos])
                self.search_status.config(text=f"FOUND {target} AT INDEX {pos}")
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    # Tree operations
    def insert_node(self):
        """Insert a node into the binary search tree"""
        try:
            value = int(self.tree_value_entry.get())
            if self.binary_tree is None:
                self.binary_tree = TreeNode(value)
            else:
                self._insert_recursive(self.binary_tree, value)
            
            self.draw_tree()
            self.update_tree_info()
            self.tree_status.config(text=f"INSERTED {value}")
            self.tree_value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

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
            value = int(self.tree_value_entry.get())
            self.binary_tree = self._delete_recursive(self.binary_tree, value)
            self.draw_tree()
            self.update_tree_info()
            self.tree_status.config(text=f"DELETED {value}")
            self.tree_value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

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
            value = int(self.tree_value_entry.get())
            found = self._search_recursive(self.binary_tree, value)
            if found:
                self.tree_status.config(text=f"FOUND {value} IN TREE")
            else:
                self.tree_status.config(text=f"{value} NOT FOUND IN TREE")
            self.tree_value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

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
        self.tree_status.config(text="TREE CLEARED")

    def draw_tree(self):
        """Draw the binary tree - monochrome style"""
        self.tree_ax.clear()
        self.tree_ax.set_facecolor(THEME["canvas_bg"])
        self.tree_ax.set_aspect('equal')
        self.tree_ax.axis('off')
        
        if self.binary_tree is None:
            self.tree_ax.text(0.5, 0.5, "EMPTY TREE", ha='center', va='center', 
                            transform=self.tree_ax.transAxes, color=THEME["fg"], 
                            fontsize=14, family='Courier', fontweight='bold')
        else:
            positions = {}
            self._calculate_positions(self.binary_tree, 0, 0, 4, positions)
            self._draw_edges(self.binary_tree, positions)
            self._draw_nodes(positions)
        
        self.tree_canvas.draw()

    def _calculate_positions(self, node, x, y, width, positions):
        """Calculate positions for tree nodes"""
        if node is not None:
            positions[node] = (x, y)
            if node.left:
                self._calculate_positions(node.left, x - width, y - 1, width / 2, positions)
            if node.right:
                self._calculate_positions(node.right, x + width, y - 1, width / 2, positions)

    def _draw_edges(self, node, positions):
        """Draw edges between tree nodes - black lines"""
        if node is not None:
            x, y = positions[node]
            if node.left:
                left_x, left_y = positions[node.left]
                self.tree_ax.plot([x, left_x], [y, left_y], '-', color=THEME["border"], linewidth=2, markersize=0)
                self._draw_edges(node.left, positions)
            if node.right:
                right_x, right_y = positions[node.right]
                self.tree_ax.plot([x, right_x], [y, right_y], '-', color=THEME["border"], linewidth=2, markersize=0)
                self._draw_edges(node.right, positions)

    def _draw_nodes(self, positions):
        """Draw tree nodes - rectangular boxes"""
        for node, (x, y) in positions.items():
            # Draw rectangle instead of circle
            rect = Rectangle((x - 0.25, y - 0.15), 0.5, 0.3, 
                           facecolor=THEME["bg"], 
                           edgecolor=THEME["border"], 
                           linewidth=2)
            self.tree_ax.add_patch(rect)
            self.tree_ax.text(x, y, str(node.value), ha='center', va='center', 
                            color=THEME["fg"], fontsize=11, fontweight='bold', family='Courier')
def traverse_tree(self, traversal_type):
        """Perform tree traversal"""
        if self.binary_tree is None:
            self.tree_status.config(text="TREE IS EMPTY")
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
        self.tree_info_text.insert(tk.END, f"{traversal_type.upper()}: {' -> '.join(map(str, result))}")
        self.tree_status.config(text=f"{traversal_type.upper()} COMPLETED")

    def _inorder_traversal(self, root, result):
        if root:
            self._inorder_traversal(root.left, result)
            result.append(root.value)
            self._inorder_traversal(root.right, result)

    def _preorder_traversal(self, root, result):
        if root:
            result.append(root.value)
            self._preorder_traversal(root.left, result)
            self._preorder_traversal(root.right, result)

    def _postorder_traversal(self, root, result):
        if root:
            self._postorder_traversal(root.left, result)
            self._postorder_traversal(root.right, result)
            result.append(root.value)

    def _level_order_traversal(self, root, result):
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
            info = "TREE: EMPTY\nHEIGHT: 0\nNODES: 0"
        else:
            height = self._get_tree_height(self.binary_tree)
            node_count = self._count_nodes(self.binary_tree)
            info = f"TREE: BINARY SEARCH TREE\nHEIGHT: {height}\nNODES: {node_count}"
        
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

    # Algorithm execution methods
    def run_sorting_algorithm(self, algorithm, name):
        """Run a sorting algorithm with timing"""
        if not self.data:
            messagebox.showwarning("No Data", "Please generate data first.")
            return
        
        self.sort_status.config(text=f"RUNNING {name.upper()}...")
        self.root.update()
        
        data_copy = self.data.copy()
        start_time = time.time()
        algorithm(data_copy, self.draw_sort_data, self.sort_speed.get())
        end_time = time.time()
        
        execution_times[name] = end_time - start_time
        self.data = data_copy
        self.update_array_display(self.data)
        self.sort_status.config(text=f"{name.upper()} COMPLETED IN {end_time - start_time:.4f}S")
        
        # Save to history
        self.save_to_sort_history(name, self.data.copy(), end_time - start_time)

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
        
        self.search_status.config(text=f"RUNNING {name.upper()}...")
        self.root.update()
        
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
        self.save_search_history()

    # History and data management
    def save_to_sort_history(self, algorithm, data, execution_time):
        """Save sorting result to history"""
        entry = {
            "algorithm": algorithm,
            "data": data,
            "time": execution_time,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        sorting_history.append(entry)
        self.save_sort_history()

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
        with open(HISTORY_FILE, "w") as file:
            json.dump(sorting_history, file, indent=4)

    def save_search_history(self):
        """Save search history to file"""
        with open(SEARCH_HISTORY_FILE, "w") as file:
            json.dump(search_history, file, indent=4)

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
                        self.data = [int(row[1]) for row in reader]
                else:
                    with open(filename, 'r') as file:
                        data = json.load(file)
                        self.data = data.get('data', [])
                
                self.sort_entry.delete(0, tk.END)
                self.sort_entry.insert(0, ','.join(map(str, self.data)))
                self.draw_sort_data(self.data, [THEME["fg"]] * len(self.data))
                self.update_array_display(self.data)
                messagebox.showinfo("Success", f"Data loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    # Analysis and comparison methods
    def compare_sorting_algorithms(self):
        """Compare sorting algorithm performance - monochrome charts"""
        if not execution_times:
            messagebox.showinfo("No Data", "Run some sorting algorithms first.")
            return
        
        self.time_ax.clear()
        self.time_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.time_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.time_ax.minorticks_on()
        self.time_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        algorithms = list(execution_times.keys())
        times = list(execution_times.values())
        
        bars = self.time_ax.bar(algorithms, times, color=THEME["bg"], 
                               edgecolor=THEME["border"], linewidth=2)
        
        self.time_ax.set_title("SORTING ALGORITHM TIME COMPARISON", 
                             color=THEME["fg"], fontweight='bold', family='Courier', fontsize=11)
        self.time_ax.set_ylabel("TIME (SECONDS)", color=THEME["fg"], family='Courier', fontsize=9)
        self.time_ax.tick_params(colors=THEME["fg"], rotation=45, labelsize=8)
        
        # Add value labels on bars
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.time_ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{time_val:.4f}', ha='center', va='bottom', 
                            color=THEME["fg"], family='Courier', fontsize=8)
        
        for spine in self.time_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        # Space complexity chart (theoretical)
        self.space_ax.clear()
        self.space_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.space_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.space_ax.minorticks_on()
        self.space_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        space_complexity = {
            'Bubble Sort': 1, 'Selection Sort': 1, 'Insertion Sort': 1,
            'Merge Sort': len(self.data) if self.data else 10,
            'Quick Sort': math.log2(len(self.data)) if self.data else 3,
            'Heap Sort': 1, 'Radix Sort': len(self.data) if self.data else 10
        }
        
        present_algorithms = [alg for alg in algorithms if alg in space_complexity]
        space_values = [space_complexity[alg] for alg in present_algorithms]
        
        bars2 = self.space_ax.bar(present_algorithms, space_values, color=THEME["bg"], 
                                 edgecolor=THEME["border"], linewidth=2)
        self.space_ax.set_title("SPACE COMPLEXITY (RELATIVE)", 
                              color=THEME["fg"], fontweight='bold', family='Courier', fontsize=11)
        self.space_ax.set_ylabel("SPACE USAGE", color=THEME["fg"], family='Courier', fontsize=9)
        self.space_ax.tick_params(colors=THEME["fg"], rotation=45, labelsize=8)
        
        for spine in self.space_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def compare_search_algorithms(self):
        """Compare search algorithm performance - monochrome charts"""
        if not search_history:
            messagebox.showinfo("No Data", "Run some search algorithms first.")
            return
        
        # Group by algorithm
        algo_times = {}
        for entry in search_history:
            algo = entry['algorithm']
            if algo not in algo_times:
                algo_times[algo] = []
            algo_times[algo].append(entry['time'])
        
        # Calculate averages
        avg_times = {algo: sum(times)/len(times) for algo, times in algo_times.items()}
        
        self.time_ax.clear()
        self.time_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.time_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', linewidth=0.3, alpha=0.5)
        self.time_ax.minorticks_on()
        self.time_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', linewidth=0.15, alpha=0.3)
        
        algorithms = list(avg_times.keys())
        times = list(avg_times.values())
        
        bars = self.time_ax.bar(algorithms, times, color=THEME["bg"], 
                               edgecolor=THEME["border"], linewidth=2)
        self.time_ax.set_title("SEARCH ALGORITHM AVG TIME COMPARISON", 
                             color=THEME["fg"], fontweight='bold', family='Courier', fontsize=11)
        self.time_ax.set_ylabel("AVG TIME (SECONDS)", color=THEME["fg"], family='Courier', fontsize=9)
        self.time_ax.tick_params(colors=THEME["fg"], rotation=45, labelsize=8)
        
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.time_ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{time_val:.4f}', ha='center', va='bottom', 
                            color=THEME["fg"], family='Courier', fontsize=8)
        
        for spine in self.time_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        # Clear second chart
        self.space_ax.clear()
        self.space_ax.set_facecolor(THEME["canvas_bg"])
        self.space_ax.text(0.5, 0.5, "SEARCH ALGORITHMS\nGENERALLY USE O(1) SPACE", 
                          ha='center', va='center', transform=self.space_ax.transAxes,
                          color=THEME["fg"], fontsize=10, family='Courier', fontweight='bold')
        
        for spine in self.space_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def show_complexity_analysis(self):
        """Show Big O complexity analysis"""
        complexity_window = tk.Toplevel(self.root)
        complexity_window.title("Algorithm Complexity Analysis")
        complexity_window.geometry("900x650")
        complexity_window.configure(bg=THEME["bg"])
        
        # Create text widget for complexity information
        text_frame = tk.Frame(complexity_window, bg=THEME["bg"], relief=tk.SOLID, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        complexity_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                  bg=THEME["bg"], fg=THEME["fg"],
                                                  font=("Courier", 10), relief=tk.SOLID, bd=1)
        complexity_text.pack(fill=tk.BOTH, expand=True)
        
        complexity_info = """
╔══════════════════════════════════════════════════════════════════╗
║            ALGORITHM COMPLEXITY ANALYSIS                         ║
╚══════════════════════════════════════════════════════════════════╝

SORTING ALGORITHMS:
──────────────────────────────────────────────────────────────────

BUBBLE SORT:
  Time: O(n²) worst/average, O(n) best
  Space: O(1)
  Stable: Yes

SELECTION SORT:
  Time: O(n²) all cases
  Space: O(1)
  Stable: No

INSERTION SORT:
  Time: O(n²) worst/average, O(n) best
  Space: O(1)
  Stable: Yes

MERGE SORT:
  Time: O(n log n) all cases
  Space: O(n)
  Stable: Yes

QUICK SORT:
  Time: O(n²) worst, O(n log n) average/best
  Space: O(log n) average
  Stable: No

HEAP SORT:
  Time: O(n log n) all cases
  Space: O(1)
  Stable: No

RADIX SORT:
  Time: O(d×(n+k))
  Space: O(n+k)
  Stable: Yes

SEARCH ALGORITHMS:
──────────────────────────────────────────────────────────────────

LINEAR SEARCH:
  Time: O(n)
  Space: O(1)
  Works on: Any array

BINARY SEARCH:
  Time: O(log n)
  Space: O(1) iterative
  Works on: Sorted arrays only

JUMP SEARCH:
  Time: O(√n)
  Space: O(1)
  Works on: Sorted arrays

INTERPOLATION SEARCH:
  Time: O(log log n) best, O(n) worst
  Space: O(1)
  Works on: Uniformly distributed sorted arrays

TREE OPERATIONS:
──────────────────────────────────────────────────────────────────

BINARY SEARCH TREE:
  Search: O(log n) average, O(n) worst
  Insert: O(log n) average, O(n) worst
  Delete: O(log n) average, O(n) worst
  Space: O(n)

TRAVERSALS:
  All: O(n) time, O(h) space (h = height)
  - Inorder: Left → Root → Right
  - Preorder: Root → Left → Right  
  - Postorder: Left → Right → Root
  - Level Order: Breadth-first
"""
        
        complexity_text.insert(tk.END, complexity_info)
        complexity_text.config(state=tk.DISABLED)

    def export_analysis(self):
        """Export analysis results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")]
        )
        
        if filename:
            try:
                export_data = {
                    "sorting_performance": execution_times,
                    "sorting_history": sorting_history,
                    "search_history": search_history,
                    "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if filename.endswith('.csv'):
                    with open(filename, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Type", "Algorithm", "Time", "Timestamp"])
                        
                        for algo, time in execution_times.items():
                            writer.writerow(["Sorting", algo, time, ""])
                        
                        for entry in search_history:
                            writer.writerow(["Search", entry["algorithm"], entry["time"], entry["timestamp"]])
                else:
                    with open(filename, 'w') as file:
                        json.dump(export_data, file, indent=4)
                
                messagebox.showinfo("Success", f"Analysis exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export analysis: {str(e)}")

    def view_sort_history(self):
        """View sorting history"""
        if not sorting_history:
            messagebox.showinfo("No History", "No sorting history available.")
            return
        
        self._create_history_window("SORTING HISTORY", sorting_history, "sorting")

    def view_search_history(self):
        """View search history"""
        if not search_history:
            messagebox.showinfo("No History", "No search history available.")
            return
        
        self._create_history_window("SEARCH HISTORY", search_history, "search")

    def _create_history_window(self, title, history_data, data_type):
        """Create a history viewing window - monochrome"""
        history_window = tk.Toplevel(self.root)
        history_window.title(title)
        history_window.geometry("900x500")
        history_window.configure(bg=THEME["bg"])
        
        # Create treeview for history
        tree_frame = tk.Frame(history_window, bg=THEME["bg"], relief=tk.SOLID, bd=2)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ("Algorithm", "Time", "Timestamp")
        if data_type == "search":
            columns = ("Algorithm", "Target", "Result", "Time", "Timestamp")
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != "Timestamp" else 150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for i, entry in enumerate(history_data):
            if data_type == "sorting":
                values = (entry["algorithm"], f"{entry['time']:.4f}s", entry["timestamp"])
            else:
                result_text = f"Index {entry['result']}" if entry['result'] != -1 else "Not found"
                values = (entry["algorithm"], entry["target"], result_text, 
                         f"{entry['time']:.4f}s", entry["timestamp"])
            
            tree.insert("", tk.END, values=values)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        btn_frame = tk.Frame(history_window, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.create_rect_button(btn_frame, "DELETE", 
                 lambda: self._delete_selected_history(tree, history_data, data_type), 15).pack(side=tk.LEFT, padx=5)
        
        self.create_rect_button(btn_frame, "CLEAR ALL", 
                 lambda: self._clear_history(history_window, data_type), 15).pack(side=tk.LEFT, padx=5)
        
        self.create_rect_button(btn_frame, "CLOSE", history_window.destroy, 10).pack(side=tk.RIGHT, padx=5)

    def _delete_selected_history(self, tree, history_data, data_type):
        """Delete selected history entry"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Delete selected entry?"):
            for item in selected:
                index = tree.index(item)
                history_data.pop(index)
                tree.delete(item)
            
            if data_type == "sorting":
                self.save_sort_history()
            else:
                self.save_search_history()

    def _clear_history(self, window, data_type):
        """Clear all history"""
        if messagebox.askyesno("Confirm Clear", "Clear all history?"):
            if data_type == "sorting":
                global sorting_history
                sorting_history = []
                self.save_sort_history()
            else:
                global search_history
                search_history = []
                self.save_search_history()
            
            window.destroy()
            messagebox.showinfo("Cleared", "History cleared successfully.")

    def clear_all_history(self):
        """Clear all history files"""
        if messagebox.askyesno("Confirm Clear All", "Clear all history data?"):
            global sorting_history, search_history
            sorting_history = []
            search_history = []
            self.save_sort_history()
            self.save_search_history()
            messagebox.showinfo("Cleared", "All history cleared.")

    def reset_sort_visualization(self):
        """Reset the sorting visualization"""
        global execution_times
        execution_times = {}
        self.data = []
        self.sort_entry.delete(0, tk.END)
        
        # Clear array display
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        
        # Clear chart
        self.sort_ax.clear()
        self.sort_ax.set_facecolor(THEME["canvas_bg"])
        self.sort_canvas.draw()
        
        self.sort_status.config(text="RESET COMPLETED")

# Main execution
def main():
    root = tk.Tk()
    app = AlgorithmVisualizer(root)
    
    # Set window properties
    try:
        root.iconname("Algorithm Visualizer")
        root.minsize(1200, 800)
    except:
        pass
    
    # Handle window closing
    def on_closing():
        app.save_sort_history()
        app.save_search_history()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()