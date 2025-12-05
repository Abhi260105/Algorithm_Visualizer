"""
Algorithm Execution & Event Handling Module
Handles running algorithms and playing back events
"""

import time
from tkinter import messagebox
from typing import Callable, List
from core_algorithms import AlgorithmEvent
from ui_rendering import AnimationPlayer


class AlgorithmExecutor:
    """Handles algorithm execution with timing and history"""
    
    def __init__(self, app_ref):
        """
        Args:
            app_ref: Reference to main AlgorithmVisualizer instance
        """
        self.app = app_ref
    
    def run_sorting_algorithm(self, name: str, algorithm_func: Callable):
        """
        Run a sorting algorithm with event playback
        
        Args:
            name: Algorithm name
            algorithm_func: Function that returns list of AlgorithmEvent
        """
        if not self.app.data:
            messagebox.showwarning("No Data", "Please generate data first.")
            return
        
        # Update status
        self.app.sort_status.config(text=f"RUNNING {name.upper()}...")
        self.app.sort_message.config(text="Starting...")
        self.app.root.update()
        
        # Generate events
        start_time = time.time()
        events = algorithm_func(self.app.data.copy())
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Update execution times
        self.app.execution_times[name] = execution_time
        
        # Create animation player
        def update_callback(event, index, total):
            self.app.sort_message.config(text=event.message)
            self.app.sort_status.config(
                text=f"{name.upper()} - Step {index+1}/{total}"
            )
            try:
                self.app.root.update_idletasks()
                self.app.root.update()
            except:
                pass
        
        player = AnimationPlayer(
            self.app.sort_visualizer, 
            update_callback
        )
        
        # Play animation
        self.app.current_player = player
        player.play_events(events, self.app.sort_speed.get())
        
        # Update final data
        if events and events[-1].data_snapshot:
            self.app.data = events[-1].data_snapshot.copy()
            self.app.update_array_display(self.app.data)
        
        # Update status
        self.app.sort_status.config(
            text=f"{name.upper()} COMPLETED IN {execution_time:.4f}S"
        )
        self.app.sort_message.config(text="✓ Complete")
        
        # Save to history
        self.app.sorting_history.add_entry(
            algorithm=name,
            data=self.app.data.copy(),
            execution_time=execution_time,
            size=len(self.app.data)
        )
    
    def run_search_algorithm(self, name: str, algorithm_func: Callable):
        """
        Run a search algorithm with event playback
        
        Args:
            name: Algorithm name
            algorithm_func: Function that returns list of AlgorithmEvent
        """
        if not self.app.search_array:
            messagebox.showwarning("No Data", "Please generate search data first.")
            return
        
        target_str = self.app.search_target_entry.get().strip()
        if not target_str:
            messagebox.showwarning("No Target", "Please enter a target value.")
            return
        
        try:
            target = int(target_str)
        except ValueError:
            messagebox.showerror("Invalid Target", "Please enter a valid integer.")
            return
        
        # Update status
        self.app.search_status.config(text=f"RUNNING {name.upper()}...")
        self.app.search_message.config(text="Starting search...")
        self.app.root.update()
        
        # Generate events
        start_time = time.time()
        events = algorithm_func(self.app.search_array, target)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Create animation player
        def update_callback(event, index, total):
            self.app.search_message.config(text=event.message)
            self.app.search_status.config(
                text=f"{name.upper()} - Step {index+1}/{total}"
            )
            try:
                self.app.root.update_idletasks()
                self.app.root.update()
            except:
                pass
        
        player = AnimationPlayer(
            self.app.search_visualizer,
            update_callback
        )
        
        # Play animation
        self.app.current_player = player
        player.play_events(events, 0.5)
        
        # Determine result
        result_index = -1
        if events:
            last_event = events[-1]
            if last_event.indices and last_event.event_type.value == "found":
                result_index = last_event.indices[0]
        
        # Update status
        if result_index != -1:
            self.app.search_status.config(
                text=f"FOUND {target} AT INDEX {result_index} IN {execution_time:.4f}S"
            )
        else:
            self.app.search_status.config(
                text=f"{target} NOT FOUND IN {execution_time:.4f}S"
            )
        
        # Save to history
        self.app.search_history.add_entry(
            algorithm=name,
            data=self.app.search_array.copy(),
            execution_time=execution_time,
            target=target,
            result=result_index,
            size=len(self.app.search_array)
        )


class TreeEventHandler:
    """Handles tree operations with visualization updates"""
    
    def __init__(self, app_ref):
        """
        Args:
            app_ref: Reference to main AlgorithmVisualizer instance
        """
        self.app = app_ref
    
    def insert_node(self):
        """Insert a node into the tree"""
        try:
            value = int(self.app.tree_value_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
            return
        
        success, message = self.app.tree_ops.insert(value)
        
        if success:
            # Highlight the inserted node
            self.app.update_tree_display(highlight_values=[value])
            self.app.tree_status.config(text=message.upper())
            self.app.tree_value_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Insert Failed", message)
            self.app.tree_status.config(text=message.upper())
    
    def delete_node(self):
        """Delete a node from the tree"""
        try:
            value = int(self.app.tree_value_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
            return
        
        success, message = self.app.tree_ops.delete(value)
        
        if success:
            self.app.update_tree_display()
            self.app.tree_status.config(text=message.upper())
            self.app.tree_value_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Delete Failed", message)
            self.app.tree_status.config(text=message.upper())
    
    def search_tree(self):
        """Search for a value in the tree"""
        try:
            value = int(self.app.tree_value_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
            return
        
        found, message = self.app.tree_ops.search(value)
        
        if found:
            # Highlight the found node
            self.app.update_tree_display(highlight_values=[value])
        else:
            self.app.update_tree_display()
        
        self.app.tree_status.config(text=message.upper())
        self.app.tree_value_entry.delete(0, 'end')
    
    def clear_tree(self):
        """Clear the entire tree"""
        if self.app.tree_ops.is_empty():
            messagebox.showinfo("Already Empty", "Tree is already empty.")
            return
        
        confirm = messagebox.askyesno("Confirm Clear", 
                                     "Are you sure you want to clear the tree?")
        if confirm:
            self.app.tree_ops.clear()
            self.app.update_tree_display()
            self.app.tree_status.config(text="TREE CLEARED")
    
    def traverse_tree(self, traversal_type: str):
        """Perform tree traversal"""
        if self.app.tree_ops.is_empty():
            messagebox.showinfo("Empty Tree", "Tree is empty.")
            self.app.tree_status.config(text="TREE IS EMPTY")
            return
        
        # Get traversal result
        if traversal_type == "inorder":
            result = self.app.tree_ops.inorder_traversal()
            name = "INORDER"
        elif traversal_type == "preorder":
            result = self.app.tree_ops.preorder_traversal()
            name = "PREORDER"
        elif traversal_type == "postorder":
            result = self.app.tree_ops.postorder_traversal()
            name = "POSTORDER"
        elif traversal_type == "level_order":
            result = self.app.tree_ops.level_order_traversal()
            name = "LEVEL ORDER"
        else:
            return
        
        # Update info display
        self.app.tree_info_text.delete(1.0, 'end')
        self.app.tree_info_text.insert(
            'end',
            f"{name}: {' → '.join(map(str, result))}"
        )
        
        self.app.tree_status.config(text=f"{name} COMPLETED")
        
        # Highlight all nodes in traversal order (animate if possible)
        self.app.update_tree_display()


class DataIOHandler:
    """Handles data import/export operations"""
    
    def __init__(self, app_ref):
        """
        Args:
            app_ref: Reference to main AlgorithmVisualizer instance
        """
        self.app = app_ref
    
    def save_sorted_data(self):
        """Save current sorted data to file"""
        if not self.app.data:
            messagebox.showwarning("No Data", "No data to save.")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), 
                      ("JSON files", "*.json"), 
                      ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            from tree_history import DataManager
            
            if filename.endswith('.csv'):
                DataManager.save_to_csv(self.app.data, filename)
            else:
                DataManager.save_to_json(
                    self.app.data, 
                    filename,
                    metadata={
                        "size": len(self.app.data),
                        "sorted": True
                    }
                )
            
            messagebox.showinfo("Success", f"Data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_data_from_file(self):
        """Load data from file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), 
                      ("JSON files", "*.json"), 
                      ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            from tree_history import DataManager
            
            if filename.endswith('.csv'):
                self.app.data = DataManager.load_from_csv(filename)
            else:
                self.app.data, metadata = DataManager.load_from_json(filename)
            
            # Update UI
            self.app.sort_entry.delete(0, 'end')
            self.app.sort_entry.insert(0, ','.join(map(str, self.app.data)))
            self.app.sort_visualizer.draw_state(self.app.data)
            self.app.update_array_display(self.app.data)
            
            messagebox.showinfo("Success", 
                              f"Loaded {len(self.app.data)} elements from {filename}")
            self.app.sort_status.config(
                text=f"LOADED {len(self.app.data)} ELEMENTS"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def reset_sort_visualization(self):
        """Reset sorting visualization"""
        confirm = messagebox.askyesno("Confirm Reset", 
                                     "Clear all data and reset visualization?")
        if not confirm:
            return
        
        # Clear data
        self.app.data = []
        self.app.execution_times = {}
        self.app.sort_entry.delete(0, 'end')
        
        # Clear array display
        for widget in self.app.array_frame.winfo_children():
            widget.destroy()
        
        # Reset visualization
        self.app.sort_visualizer.draw_state([])
        
        # Update status
        self.app.sort_status.config(text="RESET COMPLETED")
        self.app.sort_message.config(text="")


class AnalysisHandler:
    """Handles performance analysis operations"""
    
    def __init__(self, app_ref):
        """
        Args:
            app_ref: Reference to main AlgorithmVisualizer instance
        """
        self.app = app_ref
    
    def compare_sorting_algorithms(self):
        """Compare sorting algorithm performance"""
        if not self.app.execution_times:
            messagebox.showinfo("No Data", 
                              "Run some sorting algorithms first to compare.")
            return
        
        from ui_rendering import THEME, GraphPaperBackground
        
        # Clear axes
        self.app.time_ax.clear()
        self.app.space_ax.clear()
        
        # Apply graph paper background
        GraphPaperBackground.apply_to_axis(self.app.time_ax)
        GraphPaperBackground.apply_to_axis(self.app.space_ax)
        
        # Time comparison
        algorithms = list(self.app.execution_times.keys())
        times = list(self.app.execution_times.values())
        
        bars = self.app.time_ax.bar(
            algorithms, times,
            color=THEME["highlight"],
            edgecolor=THEME["border"],
            linewidth=2,
            alpha=0.7
        )
        
        self.app.time_ax.set_title(
            "SORTING ALGORITHM TIME COMPARISON",
            color=THEME["fg"],
            fontweight='bold',
            family='Courier',
            fontsize=11
        )
        self.app.time_ax.set_ylabel(
            "TIME (SECONDS)",
            color=THEME["fg"],
            family='Courier',
            fontsize=9
        )
        self.app.time_ax.tick_params(
            colors=THEME["fg"],
            rotation=45,
            labelsize=8
        )
        
        # Add value labels on bars
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.app.time_ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{time_val:.4f}',
                ha='center',
                va='bottom',
                color=THEME["fg"],
                family='Courier',
                fontsize=8
            )
        
        # Space complexity info
        self.app.space_ax.text(
            0.5, 0.5,
            "SPACE COMPLEXITY\nVARIES BY ALGORITHM\n\n"
            "See BIG O for details",
            ha='center',
            va='center',
            transform=self.app.space_ax.transAxes,
            color=THEME["fg"],
            fontsize=10,
            family='Courier',
            fontweight='bold'
        )
        
        self.app.analysis_fig.tight_layout()
        self.app.analysis_canvas.draw()
    
    def compare_search_algorithms(self):
        """Compare search algorithm performance"""
        search_history = self.app.search_history.get_all()
        
        if not search_history:
            messagebox.showinfo("No Data", 
                              "Run some search algorithms first to compare.")
            return
        
        from ui_rendering import THEME, GraphPaperBackground
        
        # Calculate average times per algorithm
        algo_times = {}
        for entry in search_history:
            algo = entry['algorithm']
            if algo not in algo_times:
                algo_times[algo] = []
            algo_times[algo].append(entry['execution_time'])
        
        avg_times = {
            algo: sum(times) / len(times)
            for algo, times in algo_times.items()
        }
        
        # Clear axes
        self.app.time_ax.clear()
        self.app.space_ax.clear()
        
        # Apply graph paper background
        GraphPaperBackground.apply_to_axis(self.app.time_ax)
        GraphPaperBackground.apply_to_axis(self.app.space_ax)
        
        # Time comparison
        algorithms = list(avg_times.keys())
        times = list(avg_times.values())
        
        bars = self.app.time_ax.bar(
            algorithms, times,
            color=THEME["searching"],
            edgecolor=THEME["border"],
            linewidth=2,
            alpha=0.7
        )
        
        self.app.time_ax.set_title(
            "SEARCH ALGORITHM AVG TIME",
            color=THEME["fg"],
            fontweight='bold',
            family='Courier',
            fontsize=11
        )
        self.app.time_ax.set_ylabel(
            "AVG TIME (SECONDS)",
            color=THEME["fg"],
            family='Courier',
            fontsize=9
        )
        self.app.time_ax.tick_params(
            colors=THEME["fg"],
            rotation=45,
            labelsize=8
        )
        
        # Add value labels
        for bar, time_val in zip(bars, times):
            height = bar.get_height()
            self.app.time_ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{time_val:.6f}',
                ha='center',
                va='bottom',
                color=THEME["fg"],
                family='Courier',
                fontsize=8
            )
        
        # Space complexity
        self.app.space_ax.text(
            0.5, 0.5,
            "SEARCH ALGORITHMS\nUSE O(1) SPACE\n\n"
            "(No extra space needed)",
            ha='center',
            va='center',
            transform=self.app.space_ax.transAxes,
            color=THEME["fg"],
            fontsize=10,
            family='Courier',
            fontweight='bold'
        )
        
        self.app.analysis_fig.tight_layout()
        self.app.analysis_canvas.draw()
    
    def show_complexity_analysis(self):
        """Show Big O complexity analysis window"""
        import tkinter as tk
        from tkinter import scrolledtext
        from tree_history import ComplexityInfo
        
        complexity_window = tk.Toplevel(self.app.root)
        complexity_window.title("Algorithm Complexity Analysis")
        complexity_window.geometry("900x650")
        complexity_window.configure(bg=THEME["bg"])
        
        text_frame = tk.Frame(
            complexity_window,
            bg=THEME["bg"],
            relief=tk.SOLID,
            bd=2
        )
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        complexity_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            bg=THEME["bg"],
            fg=THEME["fg"],
            font=("Courier", 10),
            relief=tk.SOLID,
            bd=1
        )
        complexity_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert complexity information
        complexity_text.insert('end', ComplexityInfo.format_complexity_text())
        complexity_text.config(state=tk.DISABLED)
    
    def export_analysis(self):
        """Export analysis results to file"""
        from tkinter import filedialog
        from tree_history import DataManager
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), 
                      ("CSV files", "*.csv")]
        )
        
        if not filename:
            return
        
        try:
            DataManager.export_analysis(
                self.app.sorting_history,
                self.app.search_history,
                self.app.execution_times,
                filename
            )
            
            messagebox.showinfo("Success", 
                              f"Analysis exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Failed to export analysis: {str(e)}")


class HistoryViewHandler:
    """Handles history viewing operations"""
    
    def __init__(self, app_ref):
        """
        Args:
            app_ref: Reference to main AlgorithmVisualizer instance
        """
        self.app = app_ref
    
    def view_sort_history(self):
        """View sorting history"""
        history = self.app.sorting_history.get_all()
        
        if not history:
            messagebox.showinfo("No History", "No sorting history available.")
            return
        
        self._create_history_window("SORTING HISTORY", history, "sorting")
    
    def view_search_history(self):
        """View search history"""
        history = self.app.search_history.get_all()
        
        if not history:
            messagebox.showinfo("No History", "No search history available.")
            return
        
        self._create_history_window("SEARCH HISTORY", history, "search")
    
    def _create_history_window(self, title, history_data, data_type):
        """Create history viewing window"""
        import tkinter as tk
        from tkinter import ttk
        
        history_window = tk.Toplevel(self.app.root)
        history_window.title(title)
        history_window.geometry("900x500")
        history_window.configure(bg=THEME["bg"])
        
        tree_frame = tk.Frame(
            history_window,
            bg=THEME["bg"],
            relief=tk.SOLID,
            bd=2
        )
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Define columns based on data type
        if data_type == "search":
            columns = ("Algorithm", "Target", "Result", "Time", "Timestamp")
        else:
            columns = ("Algorithm", "Size", "Time", "Timestamp")
        
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            tree.heading(col, text=col)
            width = 150 if col == "Timestamp" else 120
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate tree
        for entry in history_data:
            if data_type == "sorting":
                values = (
                    entry["algorithm"],
                    entry.get("size", "N/A"),
                    f"{entry['execution_time']:.4f}s",
                    entry["timestamp"]
                )
            else:
                result_text = (f"Index {entry['result']}" 
                             if entry['result'] != -1 
                             else "Not found")
                values = (
                    entry["algorithm"],
                    entry["target"],
                    result_text,
                    f"{entry['execution_time']:.4f}s",
                    entry["timestamp"]
                )
            
            tree.insert("", tk.END, values=values)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def clear_all_history(self):
        """Clear all history"""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear all history?\n"
            "This action cannot be undone."
        )
        
        if confirm:
            self.app.sorting_history.clear()
            self.app.search_history.clear()
            messagebox.showinfo("Cleared", "All history has been cleared.")