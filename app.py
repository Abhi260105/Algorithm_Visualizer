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

# Enhanced color theme with animation colors
THEME = {
    "bg": "#f8f8f6",           # off-white background
    "fg": "#000000",           # pure black text
    "border": "#000000",       # black borders
    "grid": "#d0d0d0",         # light gray for graph grid
    "highlight": "#000000",    # black highlight
    "canvas_bg": "#f8f8f6",    # off-white canvas
    "comparing": "#FFA500",    # orange for comparing
    "swapping": "#FF6B35",     # red-orange for swapping
    "sorted": "#4CAF50",       # green for sorted
    "found": "#2E7D32",        # dark green for found
    "searching": "#FFB74D",    # light orange for searching
    "button_hover": "#e0e0e0", # hover color for buttons
    "button_active": "#333333" # active button color
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
        self.root.title("Algorithm Visualizer - Enhanced")
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
        """Setup custom ttk styles"""
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
        """Setup the sorting algorithms tab with enhanced design"""
        # Main container
        main_frame = tk.Frame(self.sorting_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area with graph paper grid
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
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
        
        tk.Label(input_section, text="Array:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sort_entry = tk.Entry(input_section, width=30, bg=THEME["bg"], fg=THEME["fg"], 
                                 font=("Courier", 9), relief=tk.SOLID, bd=2,
                                 highlightbackground=THEME["border"], highlightthickness=1)
        self.sort_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.create_enhanced_button(input_section, "GENERATE", self.generate_sort_data, 12).grid(
            row=0, column=2, padx=5, pady=5)
        
        tk.Label(input_section, text="Speed:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
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
            self.create_enhanced_button(algo_section, text, command, 10).grid(
                row=row, column=col, padx=3, pady=3)
        
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
            self.create_enhanced_button(control_section, text, command, 8).grid(
                row=i, column=0, padx=5, pady=3)
        
        # Status bar with message area
        status_frame = tk.Frame(main_frame, bg=THEME["bg"])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.sort_status = tk.Label(status_frame, text="READY", bg=THEME["bg"], 
                                  fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                  relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.sort_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Message display area
        self.sort_message = tk.Label(status_frame, text="", bg=THEME["canvas_bg"], 
                                    fg=THEME["comparing"], font=("Courier", 8, "bold"), 
                                    relief=tk.SOLID, bd=2, anchor='w', padx=10, width=30)
        self.sort_message.pack(side=tk.RIGHT, padx=(10, 0))

    def setup_search_tab(self):
        """Setup the search algorithms tab with enhanced design"""
        main_frame = tk.Frame(self.search_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure for search
        self.search_fig, self.search_ax = plt.subplots(figsize=(12, 6))
        self.search_fig.patch.set_facecolor(THEME["canvas_bg"])
        self.search_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.search_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', 
                          linewidth=0.3, alpha=0.5)
        self.search_ax.minorticks_on()
        self.search_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', 
                          linewidth=0.15, alpha=0.3)
        
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
        
        tk.Label(input_section, text="Array:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.search_array_entry = tk.Entry(input_section, width=30, bg=THEME["bg"], 
                                         fg=THEME["fg"], font=("Courier", 9), 
                                         relief=tk.SOLID, bd=2)
        self.search_array_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_section, text="Target:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.search_target_entry = tk.Entry(input_section, width=10, bg=THEME["bg"], 
                                          fg=THEME["fg"], font=("Courier", 9), 
                                          relief=tk.SOLID, bd=2)
        self.search_target_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.create_enhanced_button(input_section, "GENERATE", self.generate_search_data, 12).grid(
            row=0, column=2, padx=5, pady=5)
        
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
            self.create_enhanced_button(search_section, text, command, 14).grid(
                row=i//2, column=i%2, padx=3, pady=3)
        
        # Status with message area
        status_frame = tk.Frame(main_frame, bg=THEME["bg"])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.search_status = tk.Label(status_frame, text="READY", bg=THEME["bg"], 
                                    fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                    relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.search_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Message display area
        self.search_message = tk.Label(status_frame, text="", bg=THEME["canvas_bg"], 
                                      fg=THEME["searching"], font=("Courier", 8, "bold"), 
                                      relief=tk.SOLID, bd=2, anchor='w', padx=10, width=30)
        self.search_message.pack(side=tk.RIGHT, padx=(10, 0))

    def create_enhanced_button(self, parent, text, command, width):
        """Create an enhanced button with hover effects"""
        btn = tk.Button(parent, text=text, command=command, width=width,
                       bg=THEME["bg"], fg=THEME["fg"], 
                       font=("Courier", 9, "bold"),
                       relief=tk.SOLID, bd=2,
                       highlightbackground=THEME["border"],
                       highlightthickness=0,
                       activebackground=THEME["button_active"],
                       activeforeground=THEME["bg"],
                       cursor="hand2")
        
        # Add hover effects
        def on_enter(e):
            btn['background'] = THEME["button_hover"]
        
        def on_leave(e):
            btn['background'] = THEME["bg"]
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

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
        self.sort_message.config(text="Ready to sort")

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
        self.search_message.config(text="Ready to search")

    def draw_sort_data(self, data, colors, message=""):
        """Draw sorting visualization with animated colors"""
        self.sort_ax.clear()
        self.sort_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.sort_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', 
                        linewidth=0.3, alpha=0.5)
        self.sort_ax.minorticks_on()
        self.sort_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', 
                        linewidth=0.15, alpha=0.3)
        
        bars = self.sort_ax.bar(range(len(data)), data, color=colors, 
                               edgecolor=THEME["border"], linewidth=2)
        
        self.sort_ax.set_title("SORTING VISUALIZATION", color=THEME["fg"], 
                             fontsize=12, fontweight='bold', family='Courier')
        self.sort_ax.set_xlabel("INDEX", color=THEME["fg"], family='Courier', fontsize=10)
        self.sort_ax.set_ylabel("VALUE", color=THEME["fg"], family='Courier', fontsize=10)
        
        for spine in self.sort_ax.spines.values():
            spine.set_color(THEME["border"])
            spine.set_linewidth(2)
        
        self.sort_canvas.draw()
        
        # Update message if provided
        if message:
            self.sort_message.config(text=message)
        
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            pass

    def draw_search_data(self, data, colors, highlight_indices=None, message=""):
        """Draw search visualization with animated colors"""
        self.search_ax.clear()
        self.search_ax.set_facecolor(THEME["canvas_bg"])
        
        # Add graph paper grid
        self.search_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', 
                          linewidth=0.3, alpha=0.5)
        self.search_ax.minorticks_on()
        self.search_ax.grid(True, which='minor', color=THEME["grid"], linestyle='-', 
                          linewidth=0.15, alpha=0.3)
        
        bars = self.search_ax.bar(range(len(data)), data, color=colors, 
                                 edgecolor=THEME["border"], linewidth=2)
        
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
        
        # Update message if provided
        if message:
            self.search_message.config(text=message)
        
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
        
        # Display array elements
        for i, val in enumerate(data):
            label = tk.Label(parent, text=str(val), width=4, height=2,
                           bg=THEME["bg"], fg=THEME["fg"],
                           relief="solid", bd=2, font=("Courier", 10, "bold"))
            label.pack(side="left", padx=3, pady=5)
# Sorting algorithms with enhanced animation
    def bubble_sort(self, data, draw_func, speed):
        """Bubble sort with colorful animation"""
        n = len(data)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight comparing elements (orange)
                colors = [THEME["sorted"] if x >= n-i else THEME["comparing"] if x == j or x == j+1 else THEME["bg"] for x in range(n)]
                draw_func(data, colors, f"Comparing: {data[j]} vs {data[j+1]}")
                time.sleep(speed)
                
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    # Highlight swapped elements (red-orange)
                    colors = [THEME["sorted"] if x >= n-i else THEME["swapping"] if x == j or x == j+1 else THEME["bg"] for x in range(n)]
                    draw_func(data, colors, f"Swapped: {data[j+1]} ↔ {data[j]}")
                    time.sleep(speed)
        
        # Show final sorted array (all green)
        draw_func(data, [THEME["sorted"]] * n, "✓ Sorting Complete!")

    def selection_sort(self, data, draw_func, speed):
        """Selection sort with colorful animation"""
        n = len(data)
        
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                colors = [THEME["sorted"] if x < i else THEME["comparing"] if x == j or x == min_idx else THEME["bg"] for x in range(n)]
                draw_func(data, colors, f"Finding min: checking {data[j]}")
                time.sleep(speed)
                
                if data[j] < data[min_idx]:
                    min_idx = j
            
            data[i], data[min_idx] = data[min_idx], data[i]
            colors = [THEME["sorted"] if x <= i else THEME["swapping"] if x == min_idx else THEME["bg"] for x in range(n)]
            draw_func(data, colors, f"Swapped: {data[i]} to position {i}")
            time.sleep(speed)
        
        draw_func(data, [THEME["sorted"]] * n, "✓ Sorting Complete!")

    def insertion_sort(self, data, draw_func, speed):
        """Insertion sort with colorful animation"""
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            
            colors = [THEME["sorted"] if x < i else THEME["comparing"] if x == i else THEME["bg"] for x in range(len(data))]
            draw_func(data, colors, f"Inserting: {key}")
            time.sleep(speed)
            
            while j >= 0 and data[j] > key:
                colors = [THEME["sorted"] if x < i else THEME["swapping"] if x == j or x == j+1 else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Shifting: {data[j]} right")
                time.sleep(speed)
                
                data[j + 1] = data[j]
                j -= 1
            
            data[j + 1] = key
        
        draw_func(data, [THEME["sorted"]] * len(data), "✓ Sorting Complete!")

    def merge_sort(self, data, draw_func, speed):
        """Merge sort with colorful animation"""
        def merge_sort_helper(arr, l, r, depth=0):
            if l < r:
                m = (l + r) // 2
                
                # Highlight the section being divided (orange)
                colors = [THEME["comparing"] if l <= x <= r else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Dividing: [{l}:{r}]")
                time.sleep(speed)
                
                merge_sort_helper(arr, l, m, depth+1)
                merge_sort_helper(arr, m + 1, r, depth+1)
                merge(arr, l, m, r)
                
                # Highlight merged section (green)
                colors = [THEME["sorted"] if l <= x <= r else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Merged: [{l}:{r}]")
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
                
                colors = [THEME["swapping"] if l <= x <= r else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Merging at position {k-1}")
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
        draw_func(data, [THEME["sorted"]] * len(data), "✓ Sorting Complete!")

    def quick_sort(self, data, draw_func, speed):
        """Quick sort with colorful animation"""
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                colors = [THEME["comparing"] if x == high else THEME["searching"] if x == j else THEME["sorted"] if low <= x <= i else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Pivot: {pivot}, checking {arr[j]}")
                time.sleep(speed)
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    colors = [THEME["comparing"] if x == high else THEME["swapping"] if x == i or x == j else THEME["sorted"] if low <= x < i else THEME["bg"] for x in range(len(data))]
                    draw_func(data, colors, f"Swapped: {arr[i]} ↔ {arr[j]}")
                    time.sleep(speed)
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
        
        quick_sort_helper(data, 0, len(data) - 1)
        draw_func(data, [THEME["sorted"]] * len(data), "✓ Sorting Complete!")

    def heap_sort(self, data, draw_func, speed):
        """Heap sort with colorful animation"""
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
                colors = [THEME["swapping"] if x == i or x == largest else THEME["comparing"] if x < n else THEME["bg"] for x in range(len(data))]
                draw_func(data, colors, f"Heapify: swapping {arr[largest]} ↔ {arr[i]}")
                time.sleep(speed)
                heapify(arr, n, largest)
        
        n = len(data)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(data, n, i)
        
        # Extract elements one by one
        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            colors = [THEME["swapping"] if x == 0 or x == i else THEME["sorted"] if x > i else THEME["bg"] for x in range(len(data))]
            draw_func(data, colors, f"Moving {data[i]} to sorted position")
            time.sleep(speed)
            heapify(data, i, 0)
        
        draw_func(data, [THEME["sorted"]] * len(data), "✓ Sorting Complete!")

    def radix_sort(self, data, draw_func, speed):
        """Radix sort with colorful animation"""
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
                colors = [THEME["swapping"] if x <= i else THEME["comparing"] for x in range(len(data))]
                draw_func(data, colors, f"Digit sort: processing position {i}")
                time.sleep(speed * 0.5)
        
        max_val = max(data)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort_for_radix(data, exp)
            exp *= 10
        
        draw_func(data, [THEME["sorted"]] * len(data), "✓ Sorting Complete!")

    # Search algorithms with enhanced animation
    def linear_search(self, arr, target, draw_func, speed):
        """Linear search with colorful animation"""
        for i in range(len(arr)):
            colors = [THEME["searching"] if x == i else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [i], f"Checking index {i}: {arr[i]}")
            time.sleep(speed)
            
            if arr[i] == target:
                colors = [THEME["found"] if x == i else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [i], f"✓ FOUND {target} at index {i}!")
                self.search_status.config(text=f"FOUND {target} AT INDEX {i}")
                return i
        
        colors = [THEME["bg"] for _ in range(len(arr))]
        draw_func(arr, colors, [], f"✗ {target} not found")
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def binary_search(self, arr, target, draw_func, speed):
        """Binary search with colorful animation"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            colors = [THEME["searching"] if left <= x <= right else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, mid, right], f"Searching range [{left}:{right}], mid={mid}")
            time.sleep(speed)
            
            if arr[mid] == target:
                colors = [THEME["found"] if x == mid else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [mid], f"✓ FOUND {target} at index {mid}!")
                self.search_status.config(text=f"FOUND {target} AT INDEX {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
                colors = [THEME["comparing"] if left <= x <= right else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [mid], f"Target > {arr[mid]}, search right")
                time.sleep(speed * 0.7)
            else:
                right = mid - 1
                colors = [THEME["comparing"] if left <= x <= right else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [mid], f"Target < {arr[mid]}, search left")
                time.sleep(speed * 0.7)
        
        colors = [THEME["bg"] for _ in range(len(arr))]
        draw_func(arr, colors, [], f"✗ {target} not found")
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def jump_search(self, arr, target, draw_func, speed):
        """Jump search with colorful animation"""
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Jump through the array
        while arr[min(step, n) - 1] < target:
            colors = [THEME["searching"] if prev <= x < min(step, n) else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [min(step, n) - 1], f"Jumping: block [{prev}:{min(step, n)}]")
            time.sleep(speed)
            
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                colors = [THEME["bg"] for _ in range(len(arr))]
                draw_func(arr, colors, [], f"✗ {target} not found")
                self.search_status.config(text=f"{target} NOT FOUND")
                return -1
        
        # Linear search in the identified block
        while arr[prev] < target:
            colors = [THEME["comparing"] if x == prev else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev], f"Linear search at index {prev}")
            time.sleep(speed)
            
            prev += 1
            if prev == min(step, n):
                colors = [THEME["bg"] for _ in range(len(arr))]
                draw_func(arr, colors, [], f"✗ {target} not found")
                self.search_status.config(text=f"{target} NOT FOUND")
                return -1
        
        if arr[prev] == target:
            colors = [THEME["found"] if x == prev else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [prev], f"✓ FOUND {target} at index {prev}!")
            self.search_status.config(text=f"FOUND {target} AT INDEX {prev}")
            return prev
        
        colors = [THEME["bg"] for _ in range(len(arr))]
        draw_func(arr, colors, [], f"✗ {target} not found")
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    def interpolation_search(self, arr, target, draw_func, speed):
        """Interpolation search with colorful animation"""
        left, right = 0, len(arr) - 1
        
        while left <= right and arr[left] <= target <= arr[right]:
            if left == right:
                if arr[left] == target:
                    colors = [THEME["found"] if x == left else THEME["bg"] for x in range(len(arr))]
                    draw_func(arr, colors, [left], f"✓ FOUND {target} at index {left}!")
                    self.search_status.config(text=f"FOUND {target} AT INDEX {left}")
                    return left
                else:
                    colors = [THEME["bg"] for _ in range(len(arr))]
                    draw_func(arr, colors, [], f"✗ {target} not found")
                    self.search_status.config(text=f"{target} NOT FOUND")
                    return -1
            
            # Calculate position using interpolation formula
            pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))
            
            colors = [THEME["searching"] if left <= x <= right else THEME["bg"] for x in range(len(arr))]
            draw_func(arr, colors, [left, pos, right], f"Interpolating: checking position {pos}")
            time.sleep(speed)
            
            if arr[pos] == target:
                colors = [THEME["found"] if x == pos else THEME["bg"] for x in range(len(arr))]
                draw_func(arr, colors, [pos], f"✓ FOUND {target} at index {pos}!")
                self.search_status.config(text=f"FOUND {target} AT INDEX {pos}")
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        colors = [THEME["bg"] for _ in range(len(arr))]
        draw_func(arr, colors, [], f"✗ {target} not found")
        self.search_status.config(text=f"{target} NOT FOUND")
        return -1

    # Tree operations
    def setup_tree_tab(self):
        """Setup the tree operations tab"""
        main_frame = tk.Frame(self.tree_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
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
        
        tk.Label(tree_ops_section, text="Value:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=0, column=0, padx=5, pady=5)
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
            self.create_enhanced_button(tree_ops_section, text, command, 8).grid(
                row=1, column=i, padx=3, pady=5)
        
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
            self.create_enhanced_button(traversal_section, text, command, 10).grid(
                row=i//2, column=i%2, padx=3, pady=3)
        
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
                        next(reader)
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

    def compare_sorting_algorithms(self):
        """Compare sorting algorithm performance"""
        if not execution_times:
            messagebox.showinfo("No Data", "Run some sorting algorithms first.")
            return
        
        self.time_ax.clear()
        self.time_ax.set_facecolor(THEME["canvas_bg"])
        self.time_ax.grid(True, which='both', color=THEME["grid"], linestyle='-', 
                        linewidth=0.3, alpha=0.5)
        
        algorithms = list(execution_times.keys())
        times = list(execution_times.values())
        
        bars = self.time_ax.bar(algorithms, times, color=THEME["comparing"], 
                               edgecolor=THEME["border"], linewidth=2, alpha=0.7)
        
        self.time_ax.set_title("SORTING ALGORITHM TIME COMPARISON", 
                             color=THEME["fg"], fontweight='bold', family='Courier', fontsize=11)
        self.time_ax.set_ylabel("TIME (SECONDS)", color=THEME["fg"], family='Courier', fontsize=9)
        self.time_ax.tick_params(colors=THEME["fg"], rotation=45, labelsize=8)
        
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.time_ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{time_val:.4f}', ha='center', va='bottom', 
                            color=THEME["fg"], family='Courier', fontsize=8)
        
        self.space_ax.clear()
        self.space_ax.set_facecolor(THEME["canvas_bg"])
        self.space_ax.text(0.5, 0.5, "SPACE COMPLEXITY\nVARIES BY ALGORITHM", 
                          ha='center', va='center', transform=self.space_ax.transAxes,
                          color=THEME["fg"], fontsize=10, family='Courier', fontweight='bold')
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def compare_search_algorithms(self):
        """Compare search algorithm performance"""
        if not search_history:
            messagebox.showinfo("No Data", "Run some search algorithms first.")
            return
        
        algo_times = {}
        for entry in search_history:
            algo = entry['algorithm']
            if algo not in algo_times:
                algo_times[algo] = []
            algo_times[algo].append(entry['time'])
        
        avg_times = {algo: sum(times)/len(times) for algo, times in algo_times.items()}
        
        self.time_ax.clear()
        self.time_ax.set_facecolor(THEME["canvas_bg"])
        
        algorithms = list(avg_times.keys())
        times = list(avg_times.values())
        
        bars = self.time_ax.bar(algorithms, times, color=THEME["searching"], 
                               edgecolor=THEME["border"], linewidth=2, alpha=0.7)
        self.time_ax.set_title("SEARCH ALGORITHM AVG TIME", 
                             color=THEME["fg"], fontweight='bold', family='Courier', fontsize=11)
        
        self.space_ax.clear()
        self.space_ax.set_facecolor(THEME["canvas_bg"])
        self.space_ax.text(0.5, 0.5, "SEARCH ALGORITHMS\nUSE O(1) SPACE", 
                          ha='center', va='center', transform=self.space_ax.transAxes,
                          color=THEME["fg"], fontsize=10, family='Courier', fontweight='bold')
        
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()

    def show_complexity_analysis(self):
        """Show Big O complexity analysis"""
        complexity_window = tk.Toplevel(self.root)
        complexity_window.title("Algorithm Complexity")
        complexity_window.geometry("900x650")
        complexity_window.configure(bg=THEME["bg"])
        
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
    
    See original code for full complexity details...
    """
        
        complexity_text.insert(tk.END, complexity_info)
        complexity_text.config(state=tk.DISABLED)

    def export_analysis(self):
        """Export analysis results"""
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
                
                with open(filename, 'w') as file:
                    json.dump(export_data, file, indent=4)
                
                messagebox.showinfo("Success", f"Analysis exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

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
        """Create history window"""
        history_window = tk.Toplevel(self.root)
        history_window.title(title)
        history_window.geometry("900x500")
        history_window.configure(bg=THEME["bg"])
        
        tree_frame = tk.Frame(history_window, bg=THEME["bg"], relief=tk.SOLID, bd=2)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ("Algorithm", "Time", "Timestamp")
        if data_type == "search":
            columns = ("Algorithm", "Target", "Result", "Time", "Timestamp")
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != "Timestamp" else 150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for entry in history_data:
            if data_type == "sorting":
                values = (entry["algorithm"], f"{entry['time']:.4f}s", entry["timestamp"])
            else:
                result_text = f"Index {entry['result']}" if entry['result'] != -1 else "Not found"
                values = (entry["algorithm"], entry["target"], result_text, 
                         f"{entry['time']:.4f}s", entry["timestamp"])
            tree.insert("", tk.END, values=values)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_all_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            global sorting_history, search_history
            sorting_history = []
            search_history = []
            self.save_sort_history()
            self.save_search_history()
            messagebox.showinfo("Cleared", "All history cleared.")

    def reset_sort_visualization(self):
        """Reset sorting visualization"""
        global execution_times
        execution_times = {}
        self.data = []
        self.sort_entry.delete(0, tk.END)
        
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        
        self.sort_ax.clear()
        self.sort_ax.set_facecolor(THEME["canvas_bg"])
        self.sort_canvas.draw()
        
        self.sort_status.config(text="RESET COMPLETED")
        self.sort_message.config(text="")

def main():
    root = tk.Tk()
    app = AlgorithmVisualizer(root)
    
    try:
        root.iconname("Algorithm Visualizer")
        root.minsize(1200, 800)
    except:
        pass
    
    def on_closing():
        app.save_sort_history()
        app.save_search_history()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()