"""
Main Entry Point - Complete Application Integration
Connects all modules and launches the application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Import all modules
from core_algorithms import AlgorithmCore, SearchCore
from ui_rendering import (THEME, SortingVisualizer, SearchVisualizer, 
                          TreeVisualizer, AnimationPlayer)
from tree_history import (TreeOperations, HistoryManager, DataManager, 
                          ComplexityInfo)
from main_application import AlgorithmVisualizer
from algorithm_execution import (AlgorithmExecutor, TreeEventHandler, 
                                DataIOHandler, AnalysisHandler, 
                                HistoryViewHandler)


class IntegratedAlgorithmVisualizer(AlgorithmVisualizer):
    """
    Complete integrated application with all handlers
    Extends AlgorithmVisualizer with execution handlers
    """
    
    def __init__(self, root):
        # Initialize parent
        super().__init__(root)
        
        # Initialize handlers
        self.executor = AlgorithmExecutor(self)
        self.tree_handler = TreeEventHandler(self)
        self.data_io_handler = DataIOHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.history_handler = HistoryViewHandler(self)
    
    # ===== Sorting Tab Methods =====
    
    def run_sorting(self, name, algorithm_func):
        """Run sorting algorithm (delegated to executor)"""
        self.executor.run_sorting_algorithm(name, algorithm_func)
    
    def save_sorted_data(self):
        """Save sorted data (delegated to data IO handler)"""
        self.data_io_handler.save_sorted_data()
    
    def load_data_from_file(self):
        """Load data from file (delegated to data IO handler)"""
        self.data_io_handler.load_data_from_file()
    
    def reset_sort_visualization(self):
        """Reset visualization (delegated to data IO handler)"""
        self.data_io_handler.reset_sort_visualization()
    
    # ===== Search Tab Methods =====
    
    def run_search(self, name, algorithm_func):
        """Run search algorithm (delegated to executor)"""
        self.executor.run_search_algorithm(name, algorithm_func)
    
    # ===== Tree Tab Methods =====
    
    def insert_node(self):
        """Insert node (delegated to tree handler)"""
        self.tree_handler.insert_node()
    
    def delete_node(self):
        """Delete node (delegated to tree handler)"""
        self.tree_handler.delete_node()
    
    def search_tree(self):
        """Search tree (delegated to tree handler)"""
        self.tree_handler.search_tree()
    
    def clear_tree(self):
        """Clear tree (delegated to tree handler)"""
        self.tree_handler.clear_tree()
    
    def traverse_tree(self, traversal_type):
        """Perform tree traversal (delegated to tree handler)"""
        self.tree_handler.traverse_tree(traversal_type)
    
    def update_tree_display(self, highlight_values=None):
        """Update tree visualization"""
        if highlight_values is None:
            highlight_values = []
        
        # Draw tree with highlights
        self.tree_visualizer.draw_tree(self.tree_ops.root, highlight_values)
        
        # Update info display
        info = self.tree_ops.get_info()
        info_text = (
            f"TREE: {info['type']}\n"
            f"HEIGHT: {info['height']}\n"
            f"NODES: {info['nodes']}\n"
            f"STATUS: {'EMPTY' if info['is_empty'] else 'ACTIVE'}"
        )
        
        self.tree_info_text.delete(1.0, 'end')
        self.tree_info_text.insert('end', info_text)
    
    # ===== Analysis Tab Methods =====
    
    def compare_sorting_algorithms(self):
        """Compare sorting algorithms (delegated to analysis handler)"""
        self.analysis_handler.compare_sorting_algorithms()
    
    def compare_search_algorithms(self):
        """Compare search algorithms (delegated to analysis handler)"""
        self.analysis_handler.compare_search_algorithms()
    
    def show_complexity_analysis(self):
        """Show complexity analysis (delegated to analysis handler)"""
        self.analysis_handler.show_complexity_analysis()
    
    def export_analysis(self):
        """Export analysis (delegated to analysis handler)"""
        self.analysis_handler.export_analysis()
    
    # ===== History Methods =====
    
    def view_sort_history(self):
        """View sorting history (delegated to history handler)"""
        self.history_handler.view_sort_history()
    
    def view_search_history(self):
        """View search history (delegated to history handler)"""
        self.history_handler.view_search_history()
    
    def clear_all_history(self):
        """Clear all history (delegated to history handler)"""
        self.history_handler.clear_all_history()


class ApplicationLauncher:
    """Handles application startup and configuration"""
    
    @staticmethod
    def check_dependencies():
        """Check if all required dependencies are available"""
        required_modules = [
            'tkinter',
            'matplotlib',
            'numpy'
        ]
        
        missing = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            print(f"Error: Missing required modules: {', '.join(missing)}")
            print("Please install them using:")
            print(f"pip install {' '.join(missing)}")
            return False
        
        return True
    
    @staticmethod
    def setup_window_icon(root):
        """Setup window icon (if available)"""
        try:
            # Try to set window icon
            root.iconname("Algorithm Visualizer")
        except Exception:
            pass  # Icon not critical
    
    @staticmethod
    def configure_window(root):
        """Configure main window properties"""
        # Set minimum size
        root.minsize(1200, 800)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def setup_close_handler(root, app):
        """Setup proper cleanup on window close"""
        def on_closing():
            # Save history
            try:
                app.sorting_history.save()
                app.search_history.save()
            except Exception as e:
                print(f"Warning: Failed to save history: {e}")
            
            # Destroy window
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
    
    @staticmethod
    def show_welcome_message(app):
        """Show welcome message with instructions"""
        welcome_text = """
Welcome to Algorithm Visualizer!

Quick Start:
• SORTING: Generate data, select algorithm, watch visualization
• SEARCH: Generate sorted data, enter target, run search
• TREE: Insert/delete nodes, perform traversals
• ANALYSIS: Compare algorithms, view complexity, export results

Tips:
• Use the speed slider to control animation speed
• All animations use GREEN highlights consistently
• Graph paper background provides clear visual reference
• History is automatically saved between sessions

Enjoy exploring algorithms!
        """
        
        # We'll skip the welcome dialog for now to avoid interruption
        # Uncomment below if you want to show it:
        # messagebox.showinfo("Welcome", welcome_text.strip())
        
        # Just set initial status
        app.sort_status.config(text="READY - Generate data to begin")


def main():
    """Main entry point for the application"""
    
    # Check dependencies
    if not ApplicationLauncher.check_dependencies():
        sys.exit(1)
    
    # Create main window
    root = tk.Tk()
    
    try:
        # Create application
        app = IntegratedAlgorithmVisualizer(root)
        
        # Configure window
        ApplicationLauncher.configure_window(root)
        ApplicationLauncher.setup_window_icon(root)
        ApplicationLauncher.setup_close_handler(root, app)
        
        # Show welcome message
        ApplicationLauncher.show_welcome_message(app)
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror(
            "Application Error",
            f"An error occurred while starting the application:\n\n{str(e)}\n\n"
            "Please check that all dependencies are installed correctly."
        )
        sys.exit(1)


# Development utilities
class DevTools:
    """Development and debugging utilities"""
    
    @staticmethod
    def print_module_info():
        """Print information about loaded modules"""
        print("=" * 60)
        print("Algorithm Visualizer - Module Information")
        print("=" * 60)
        print(f"Core Algorithms: {AlgorithmCore.__module__}")
        print(f"Search Algorithms: {SearchCore.__module__}")
        print(f"UI Rendering: {SortingVisualizer.__module__}")
        print(f"Tree Operations: {TreeOperations.__module__}")
        print(f"History Manager: {HistoryManager.__module__}")
        print(f"Data Manager: {DataManager.__module__}")
        print("=" * 60)
    
    @staticmethod
    def run_tests():
        """Run basic functionality tests"""
        print("\nRunning basic tests...")
        
        # Test sorting algorithms
        print("Testing sorting algorithms...")
        test_data = [64, 34, 25, 12, 22, 11, 90]
        
        for name, func in [
            ("Bubble Sort", AlgorithmCore.bubble_sort),
            ("Quick Sort", AlgorithmCore.quick_sort),
        ]:
            events = func(test_data.copy())
            sorted_data = events[-1].data_snapshot if events else []
            expected = sorted(test_data)
            status = "✓ PASS" if sorted_data == expected else "✗ FAIL"
            print(f"  {name}: {status}")
        
        # Test search algorithms
        print("\nTesting search algorithms...")
        sorted_data = sorted(test_data)
        target = 22
        
        for name, func in [
            ("Linear Search", SearchCore.linear_search),
            ("Binary Search", SearchCore.binary_search),
        ]:
            events = func(sorted_data, target)
            found = any(e.event_type.value == "found" for e in events)
            status = "✓ PASS" if found else "✗ FAIL"
            print(f"  {name}: {status}")
        
        # Test tree operations
        print("\nTesting tree operations...")
        tree = TreeOperations()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            tree.insert(val)
        
        inorder = tree.inorder_traversal()
        expected_inorder = [20, 30, 40, 50, 60, 70, 80]
        status = "✓ PASS" if inorder == expected_inorder else "✗ FAIL"
        print(f"  Tree Operations: {status}")
        
        print("\nAll tests completed!")


# Command line interface
def cli_main():
    """Command line interface for the application"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Algorithm Visualizer - Enhanced Edition"
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run basic functionality tests'
    )
    parser.add_argument(
        '--info',
        action='store_true',
        help='Display module information'
    )
    parser.add_argument(
        '--no-gui',
        action='store_true',
        help='Run without GUI (for testing)'
    )
    
    args = parser.parse_args()
    
    if args.info:
        DevTools.print_module_info()
        return
    
    if args.test:
        DevTools.run_tests()
        if args.no_gui:
            return
    
    # Launch GUI
    main()


if __name__ == "__main__":
    # Check if running from command line with arguments
    if len(sys.argv) > 1:
        cli_main()
    else:
        # Direct launch - start GUI
        main()