"""
Main Application Module - GUI Integration
Connects all modules and provides the main interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", message="findfont:")

# Import core modules
from core_algorithms import AlgorithmCore, SearchCore, EventType
from ui_rendering import (THEME, SortingVisualizer, SearchVisualizer, 
                          TreeVisualizer, AnimationPlayer)
from tree_history import (TreeOperations, HistoryManager, DataManager, 
                          ComplexityInfo)


class AlgorithmVisualizer:
    """Main application class integrating all components"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer - Enhanced")
        self.root.geometry("1400x900")
        self.root.configure(bg=THEME["bg"])
        
        # Initialize data structures
        self.data = []
        self.search_array = []
        self.tree_ops = TreeOperations()
        
        # Initialize history managers
        self.sorting_history = HistoryManager("sorting_history.json")
        self.search_history = HistoryManager("search_history.json")
        self.execution_times = {}
        
        # Animation control
        self.current_player = None
        
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
        
        # Setup all tabs
        self.setup_sorting_tab()
        self.setup_search_tab()
        self.setup_tree_tab()
        self.setup_analysis_tab()
        
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
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
        """Setup the sorting algorithms tab"""
        main_frame = tk.Frame(self.sorting_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure with graph paper background
        self.sort_fig, self.sort_ax = plt.subplots(figsize=(12, 6))
        self.sort_canvas = FigureCanvasTkAgg(self.sort_fig, viz_frame)
        self.sort_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize sorting visualizer
        self.sort_visualizer = SortingVisualizer(
            self.sort_fig, self.sort_ax, self.sort_canvas
        )
        
        # Array display frame
        self.array_frame = tk.Frame(main_frame, bg=THEME["bg"], height=60, 
                                   relief=tk.SOLID, bd=1)
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
        self.sort_entry = tk.Entry(input_section, width=30, bg=THEME["bg"], 
                                 fg=THEME["fg"], font=("Courier", 9), 
                                 relief=tk.SOLID, bd=2)
        self.sort_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.create_button(input_section, "GENERATE", 
                          self.generate_sort_data, 12).grid(
            row=0, column=2, padx=5, pady=5)
        
        tk.Label(input_section, text="Speed:", bg=THEME["bg"], fg=THEME["fg"], 
                font=("Courier", 9)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sort_speed = tk.DoubleVar(value=0.1)
        self.speed_scale = tk.Scale(input_section, from_=0.01, to=1.0, 
                                  resolution=0.01, orient=tk.HORIZONTAL, 
                                  variable=self.sort_speed, length=200,
                                  bg=THEME["bg"], fg=THEME["fg"])
        self.speed_scale.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # Algorithm buttons
        algo_section = tk.LabelFrame(controls_frame, text="ALGORITHMS", 
                                   bg=THEME["bg"], fg=THEME["fg"], 
                                   font=("Courier", 10, "bold"),
                                   relief=tk.SOLID, bd=2)
        algo_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        algorithms = [
            ("BUBBLE", lambda: self.run_sorting("Bubble Sort", AlgorithmCore.bubble_sort)),
            ("SELECTION", lambda: self.run_sorting("Selection Sort", AlgorithmCore.selection_sort)),
            ("INSERTION", lambda: self.run_sorting("Insertion Sort", AlgorithmCore.insertion_sort)),
            ("MERGE", lambda: self.run_sorting("Merge Sort", AlgorithmCore.merge_sort)),
            ("QUICK", lambda: self.run_sorting("Quick Sort", AlgorithmCore.quick_sort)),
            ("HEAP", lambda: self.run_sorting("Heap Sort", AlgorithmCore.heap_sort)),
            ("RADIX", lambda: self.run_sorting("Radix Sort", AlgorithmCore.radix_sort))
        ]
        
        for i, (text, command) in enumerate(algorithms):
            row, col = i // 4, i % 4
            self.create_button(algo_section, text, command, 10).grid(
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
            self.create_button(control_section, text, command, 8).grid(
                row=i, column=0, padx=5, pady=3)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg=THEME["bg"])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.sort_status = tk.Label(status_frame, text="READY", bg=THEME["bg"], 
                                  fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                  relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.sort_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.sort_message = tk.Label(status_frame, text="", bg=THEME["canvas_bg"], 
                                    fg=THEME["highlight"], font=("Courier", 8, "bold"), 
                                    relief=tk.SOLID, bd=2, anchor='w', padx=10, width=30)
        self.sort_message.pack(side=tk.RIGHT, padx=(10, 0))
    
    def setup_search_tab(self):
        """Setup the search algorithms tab"""
        main_frame = tk.Frame(self.search_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure
        self.search_fig, self.search_ax = plt.subplots(figsize=(12, 6))
        self.search_canvas = FigureCanvasTkAgg(self.search_fig, viz_frame)
        self.search_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize search visualizer
        self.search_visualizer = SearchVisualizer(
            self.search_fig, self.search_ax, self.search_canvas
        )
        
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
        
        self.create_button(input_section, "GENERATE", 
                          self.generate_search_data, 12).grid(
            row=0, column=2, padx=5, pady=5)
        
        # Search algorithms
        search_section = tk.LabelFrame(controls_frame, text="SEARCH ALGORITHMS", 
                                     bg=THEME["bg"], fg=THEME["fg"], 
                                     font=("Courier", 10, "bold"),
                                     relief=tk.SOLID, bd=2)
        search_section.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        search_algorithms = [
            ("LINEAR", lambda: self.run_search("Linear Search", SearchCore.linear_search)),
            ("BINARY", lambda: self.run_search("Binary Search", SearchCore.binary_search)),
            ("JUMP", lambda: self.run_search("Jump Search", SearchCore.jump_search)),
            ("INTERPOLATION", lambda: self.run_search("Interpolation Search", 
                                                     SearchCore.interpolation_search))
        ]
        
        for i, (text, command) in enumerate(search_algorithms):
            self.create_button(search_section, text, command, 14).grid(
                row=i//2, column=i%2, padx=3, pady=3)
        
        # Status
        status_frame = tk.Frame(main_frame, bg=THEME["bg"])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.search_status = tk.Label(status_frame, text="READY", bg=THEME["bg"], 
                                    fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                    relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.search_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_message = tk.Label(status_frame, text="", bg=THEME["canvas_bg"], 
                                      fg=THEME["searching"], font=("Courier", 8, "bold"), 
                                      relief=tk.SOLID, bd=2, anchor='w', padx=10, width=30)
        self.search_message.pack(side=tk.RIGHT, padx=(10, 0))
    
    def setup_tree_tab(self):
        """Setup the tree operations tab"""
        main_frame = tk.Frame(self.tree_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization area
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        # Create matplotlib figure
        self.tree_fig, self.tree_ax = plt.subplots(figsize=(12, 8))
        self.tree_canvas = FigureCanvasTkAgg(self.tree_fig, viz_frame)
        self.tree_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize tree visualizer
        self.tree_visualizer = TreeVisualizer(
            self.tree_fig, self.tree_ax, self.tree_canvas
        )
        
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
            self.create_button(tree_ops_section, text, command, 8).grid(
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
            self.create_button(traversal_section, text, command, 10).grid(
                row=i//2, column=i%2, padx=3, pady=3)
        
        # Tree info
        info_section = tk.LabelFrame(controls_frame, text="TREE INFO", 
                                   bg=THEME["bg"], fg=THEME["fg"], 
                                   font=("Courier", 10, "bold"),
                                   relief=tk.SOLID, bd=2)
        info_section.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        self.tree_info_text = tk.Text(info_section, width=30, height=4, 
                                    bg=THEME["bg"], fg=THEME["fg"], 
                                    font=("Courier", 8), relief=tk.SOLID, bd=1)
        self.tree_info_text.pack(padx=5, pady=5)
        
        # Status
        self.tree_status = tk.Label(main_frame, text="READY", bg=THEME["bg"], 
                                  fg=THEME["fg"], font=("Courier", 9, "bold"), 
                                  relief=tk.SOLID, bd=2, anchor='w', padx=10)
        self.tree_status.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Initial draw
        self.update_tree_display()
    
    def setup_analysis_tab(self):
        """Setup the performance analysis tab"""
        main_frame = tk.Frame(self.analysis_tab, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Analysis visualization
        viz_frame = tk.Frame(main_frame, bg=THEME["bg"], relief=tk.SOLID, bd=2, 
                           highlightbackground=THEME["border"], highlightthickness=2)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        self.analysis_fig, (self.time_ax, self.space_ax) = plt.subplots(
            1, 2, figsize=(14, 6)
        )
        self.analysis_fig.patch.set_facecolor(THEME["canvas_bg"])
        
        from ui_rendering import GraphPaperBackground
        for ax in [self.time_ax, self.space_ax]:
            GraphPaperBackground.apply_to_axis(ax)
        
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
            self.create_button(analysis_section, text, command, 14).grid(
                row=i//2, column=i%2, padx=3, pady=3)
        
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
            self.create_button(history_section, text, command, 14).grid(
                row=i//2, column=i%2, padx=3, pady=3)
    
    def create_button(self, parent, text, command, width):
        """Create a styled button with hover effects"""
        btn = tk.Button(parent, text=text, command=command, width=width,
                       bg=THEME["bg"], fg=THEME["fg"], 
                       font=("Courier", 9, "bold"),
                       relief=tk.SOLID, bd=2,
                       activebackground=THEME["button_active"],
                       activeforeground=THEME["bg"],
                       cursor="hand2")
        
        def on_enter(e):
            btn['background'] = THEME["button_hover"]
        
        def on_leave(e):
            btn['background'] = THEME["bg"]
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    # Data generation methods
    def generate_sort_data(self):
        """Generate random data for sorting"""
        user_input = self.sort_entry.get().strip()
        if user_input:
            try:
                self.data = list(map(int, user_input.split(',')))
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   "Please enter numbers separated by commas.")
                return
        else:
            size = random.randint(10, 30)
            self.data = [random.randint(1, 100) for _ in range(size)]
            self.sort_entry.delete(0, tk.END)
            self.sort_entry.insert(0, ','.join(map(str, self.data)))
        
        self.sort_visualizer.draw_state(self.data)
        self.update_array_display(self.data)
        self.sort_status.config(text=f"GENERATED {len(self.data)} ELEMENTS")
        self.sort_message.config(text="Ready to sort")
    
    def generate_search_data(self):
        """Generate sorted data for search"""
        user_input = self.search_array_entry.get().strip()
        if user_input:
            try:
                self.search_array = sorted(list(map(int, user_input.split(','))))
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   "Please enter numbers separated by commas.")
                return
        else:
            size = random.randint(15, 25)
            self.search_array = sorted([random.randint(1, 100) for _ in range(size)])
            self.search_array_entry.delete(0, tk.END)
            self.search_array_entry.insert(0, ','.join(map(str, self.search_array)))
        
        self.search_visualizer.draw_state(self.search_array)
        self.search_status.config(text=f"GENERATED {len(self.search_array)} SORTED ELEMENTS")
        self.search_message.config(text="Ready to search")
    
    def update_array_display(self, data):
        """Update the array display below the chart"""
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        
        if len(data) > 20:
            canvas = tk.Canvas(self.array_frame, bg=THEME["bg"], 
                             height=50, highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.array_frame, orient="horizontal", 
                                    command=canvas.xview)
            scrollable_frame = tk.Frame(canvas, bg=THEME["bg"])
            
            canvas.configure(xscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', 
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            canvas.pack(side="top", fill="both", expand=True)
            scrollbar.pack(side="bottom", fill="x")
            
            parent = scrollable_frame
        else:
            parent = self.array_frame
        
        for i, val in enumerate(data):
            label = tk.Label(parent, text=str(val), width=4, height=2,
                           bg=THEME["bg"], fg=THEME["fg"],
                           relief="solid", bd=2, font=("Courier", 10, "bold"))
            label.pack(side="left", padx=3, pady=5)