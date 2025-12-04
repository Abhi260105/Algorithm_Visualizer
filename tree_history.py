from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import csv
from core_algorithms import TreeNode


class TreeOperations:
    """Binary Search Tree operations with event tracking"""
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
        
    def insert(self, value: int) -> tuple[bool, str]:
        """
        Insert a value into the BST
        
        Returns:
            (success, message) tuple
        """
        if self.root is None:
            self.root = TreeNode(value)
            return True, f"Inserted {value} as root"
        else:
            success = self._insert_recursive(self.root, value)
            if success:
                return True, f"Inserted {value}"
            else:
                return False, f"Value {value} already exists"
    
    def _insert_recursive(self, node: TreeNode, value: int) -> bool:
        """Recursive insertion helper"""
        if value == node.value:
            return False  # Duplicate
        elif value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                return True
            else:
                return self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
                return True
            else:
                return self._insert_recursive(node.right, value)
    
    def delete(self, value: int) -> tuple[bool, str]:
        """
        Delete a value from the BST
        
        Returns:
            (success, message) tuple
        """
        if self.root is None:
            return False, "Tree is empty"
        
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            return True, f"Deleted {value}"
        else:
            return False, f"Value {value} not found"
    
    def _delete_recursive(self, node: Optional[TreeNode], 
                         value: int) -> tuple[Optional[TreeNode], bool]:
        """
        Recursive deletion helper
        
        Returns:
            (new_root, was_deleted) tuple
        """
        if node is None:
            return None, False
        
        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
            return node, deleted
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
            return node, deleted
        else:
            # Found the node to delete
            
            # Case 1: Leaf node
            if node.left is None and node.right is None:
                return None, True
            
            # Case 2: One child
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            
            # Case 3: Two children
            # Find inorder successor (minimum in right subtree)
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right, _ = self._delete_recursive(node.right, successor.value)
            return node, True
    
    def search(self, value: int) -> tuple[bool, str]:
        """
        Search for a value in the BST
        
        Returns:
            (found, message) tuple
        """
        found = self._search_recursive(self.root, value)
        if found:
            return True, f"✓ Found {value} in tree"
        else:
            return False, f"✗ {value} not found in tree"
    
    def _search_recursive(self, node: Optional[TreeNode], value: int) -> bool:
        """Recursive search helper"""
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find minimum value node in subtree"""
        while node.left is not None:
            node = node.left
        return node
    
    def clear(self):
        """Clear the entire tree"""
        self.root = None
    
    def get_height(self) -> int:
        """Get height of the tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: Optional[TreeNode]) -> int:
        """Recursive height calculation"""
        if node is None:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return max(left_height, right_height) + 1
    
    def count_nodes(self) -> int:
        """Count total nodes in tree"""
        return self._count_recursive(self.root)
    
    def _count_recursive(self, node: Optional[TreeNode]) -> int:
        """Recursive node counting"""
        if node is None:
            return 0
        return 1 + self._count_recursive(node.left) + self._count_recursive(node.right)
    
    def is_empty(self) -> bool:
        """Check if tree is empty"""
        return self.root is None
    
    # Traversal methods
    def inorder_traversal(self) -> List[int]:
        """Inorder traversal (Left-Root-Right)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Recursive inorder helper"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self) -> List[int]:
        """Preorder traversal (Root-Left-Right)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Recursive preorder helper"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self) -> List[int]:
        """Postorder traversal (Left-Right-Root)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Recursive postorder helper"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def level_order_traversal(self) -> List[int]:
        """Level order traversal (BFS)"""
        if self.root is None:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """Get tree information as dictionary"""
        return {
            "type": "Binary Search Tree",
            "height": self.get_height(),
            "nodes": self.count_nodes(),
            "is_empty": self.is_empty()
        }


class HistoryManager:
    """Manages execution history for algorithms"""
    
    def __init__(self, history_file: str):
        self.history_file = history_file
        self.history: List[Dict[str, Any]] = []
        self.load()
    
    def add_entry(self, algorithm: str, data: Any, 
                  execution_time: float, **kwargs):
        """
        Add a history entry
        
        Args:
            algorithm: algorithm name
            data: input/output data
            execution_time: time taken in seconds
            **kwargs: additional metadata
        """
        entry = {
            "algorithm": algorithm,
            "data": data,
            "time": execution_time,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **kwargs
        }
        self.history.append(entry)
        self.save()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all history entries"""
        return self.history.copy()
    
    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get n most recent entries"""
        return self.history[-n:]
    
    def get_by_algorithm(self, algorithm: str) -> List[Dict[str, Any]]:
        """Get entries for specific algorithm"""
        return [entry for entry in self.history 
                if entry.get("algorithm") == algorithm]
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self.save()
    
    def save(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load(self):
        """Load history from file"""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
    
    def export_csv(self, filename: str):
        """Export history to CSV"""
        if not self.history:
            return
        
        # Get all unique keys
        keys = set()
        for entry in self.history:
            keys.update(entry.keys())
        keys = sorted(keys)
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.history)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from history"""
        if not self.history:
            return {
                "total_runs": 0,
                "algorithms": {},
                "avg_time": 0
            }
        
        # Count by algorithm
        algo_counts = {}
        algo_times = {}
        
        for entry in self.history:
            algo = entry.get("algorithm", "Unknown")
            time_val = entry.get("time", 0)
            
            if algo not in algo_counts:
                algo_counts[algo] = 0
                algo_times[algo] = []
            
            algo_counts[algo] += 1
            algo_times[algo].append(time_val)
        
        # Calculate averages
        algo_avg_times = {
            algo: sum(times) / len(times) if times else 0
            for algo, times in algo_times.items()
        }
        
        # Overall average
        all_times = [entry.get("time", 0) for entry in self.history]
        avg_time = sum(all_times) / len(all_times) if all_times else 0
        
        return {
            "total_runs": len(self.history),
            "algorithms": algo_counts,
            "avg_times": algo_avg_times,
            "avg_time": avg_time,
            "total_time": sum(all_times)
        }


class DataManager:
    """Manages data import/export operations"""
    
    @staticmethod
    def save_to_json(data: List[int], filename: str, metadata: Dict = None):
        """
        Save data to JSON file
        
        Args:
            data: data array
            filename: output filename
            metadata: optional metadata dictionary
        """
        output = {
            "data": data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if metadata:
            output.update(metadata)
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=4)
    
    @staticmethod
    def load_from_json(filename: str) -> tuple[List[int], Dict]:
        """
        Load data from JSON file
        
        Returns:
            (data, metadata) tuple
        """
        with open(filename, 'r') as f:
            content = json.load(f)
        
        data = content.get('data', [])
        metadata = {k: v for k, v in content.items() if k != 'data'}
        
        return data, metadata
    
    @staticmethod
    def save_to_csv(data: List[int], filename: str):
        """Save data to CSV file"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Value'])
            for i, value in enumerate(data):
                writer.writerow([i, value])
    
    @staticmethod
    def load_from_csv(filename: str) -> List[int]:
        """Load data from CSV file"""
        data = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    data.append(int(row[1]))
        return data
    
    @staticmethod
    def export_analysis(sorting_history: HistoryManager,
                       search_history: HistoryManager,
                       execution_times: Dict[str, float],
                       filename: str):
        """
        Export complete analysis to file
        
        Args:
            sorting_history: sorting history manager
            search_history: search history manager
            execution_times: current execution times
            filename: output filename
        """
        export_data = {
            "sorting_performance": execution_times,
            "sorting_history": sorting_history.get_all(),
            "search_history": search_history.get_all(),
            "sorting_statistics": sorting_history.get_statistics(),
            "search_statistics": search_history.get_statistics(),
            "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if filename.endswith('.json'):
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=4)
        elif filename.endswith('.csv'):
            # Export as CSV with basic info
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Sorting performance
                writer.writerow(['SORTING PERFORMANCE'])
                writer.writerow(['Algorithm', 'Time (s)'])
                for algo, time_val in execution_times.items():
                    writer.writerow([algo, f"{time_val:.4f}"])
                
                writer.writerow([])  # Blank line
                
                # Statistics
                writer.writerow(['STATISTICS'])
                sort_stats = sorting_history.get_statistics()
                writer.writerow(['Total Sorting Runs', sort_stats['total_runs']])
                writer.writerow(['Avg Sorting Time', f"{sort_stats['avg_time']:.4f}s"])
                
                search_stats = search_history.get_statistics()
                writer.writerow(['Total Search Runs', search_stats['total_runs']])
                writer.writerow(['Avg Search Time', f"{search_stats['avg_time']:.4f}s"])


class ComplexityInfo:
    """Algorithm complexity information database"""
    
    SORTING_COMPLEXITY = {
        "Bubble Sort": {
            "time_best": "O(n)",
            "time_average": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "description": "Simple comparison sort, good for small or nearly sorted data"
        },
        "Selection Sort": {
            "time_best": "O(n²)",
            "time_average": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "stable": False,
            "description": "Finds minimum element in each iteration"
        },
        "Insertion Sort": {
            "time_best": "O(n)",
            "time_average": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "description": "Efficient for small or nearly sorted data"
        },
        "Merge Sort": {
            "time_best": "O(n log n)",
            "time_average": "O(n log n)",
            "time_worst": "O(n log n)",
            "space": "O(n)",
            "stable": True,
            "description": "Divide and conquer algorithm, guaranteed O(n log n)"
        },
        "Quick Sort": {
            "time_best": "O(n log n)",
            "time_average": "O(n log n)",
            "time_worst": "O(n²)",
            "space": "O(log n)",
            "stable": False,
            "description": "Fast in-place sorting, average case O(n log n)"
        },
        "Heap Sort": {
            "time_best": "O(n log n)",
            "time_average": "O(n log n)",
            "time_worst": "O(n log n)",
            "space": "O(1)",
            "stable": False,
            "description": "Guaranteed O(n log n), uses heap data structure"
        },
        "Radix Sort": {
            "time_best": "O(d(n+k))",
            "time_average": "O(d(n+k))",
            "time_worst": "O(d(n+k))",
            "space": "O(n+k)",
            "stable": True,
            "description": "Non-comparison sort, sorts by individual digits"
        }
    }
    
    SEARCH_COMPLEXITY = {
        "Linear Search": {
            "time_best": "O(1)",
            "time_average": "O(n)",
            "time_worst": "O(n)",
            "space": "O(1)",
            "description": "Sequential search through array"
        },
        "Binary Search": {
            "time_best": "O(1)",
            "time_average": "O(log n)",
            "time_worst": "O(log n)",
            "space": "O(1)",
            "description": "Efficient search on sorted arrays"
        },
        "Jump Search": {
            "time_best": "O(1)",
            "time_average": "O(√n)",
            "time_worst": "O(√n)",
            "space": "O(1)",
            "description": "Jump ahead by fixed steps, then linear search"
        },
        "Interpolation Search": {
            "time_best": "O(1)",
            "time_average": "O(log log n)",
            "time_worst": "O(n)",
            "space": "O(1)",
            "description": "Uses interpolation formula for uniformly distributed data"
        }
    }
    
    @staticmethod
    def get_sorting_info(algorithm: str) -> Dict[str, Any]:
        """Get complexity info for sorting algorithm"""
        return ComplexityInfo.SORTING_COMPLEXITY.get(algorithm, {})
    
    @staticmethod
    def get_search_info(algorithm: str) -> Dict[str, Any]:
        """Get complexity info for search algorithm"""
        return ComplexityInfo.SEARCH_COMPLEXITY.get(algorithm, {})
    
    @staticmethod
    def format_complexity_text() -> str:
        """Format all complexity information as text"""
        lines = []
        lines.append("╔" + "═" * 68 + "╗")
        lines.append("║" + " " * 20 + "ALGORITHM COMPLEXITY ANALYSIS" + " " * 19 + "║")
        lines.append("╚" + "═" * 68 + "╝")
        lines.append("")
        
        # Sorting algorithms
        lines.append("SORTING ALGORITHMS:")
        lines.append("─" * 70)
        for i, (name, info) in enumerate(ComplexityInfo.SORTING_COMPLEXITY.items(), 1):
            lines.append(f"\n{i}. {name.upper()}")
            lines.append(f"   Time: Best={info['time_best']}, "
                        f"Average={info['time_average']}, "
                        f"Worst={info['time_worst']}")
            lines.append(f"   Space: {info['space']}")
            lines.append(f"   Stable: {'Yes' if info['stable'] else 'No'}")
            lines.append(f"   {info['description']}")
        
        lines.append("\n" + "─" * 70)
        lines.append("\nSEARCH ALGORITHMS:")
        lines.append("─" * 70)
        for i, (name, info) in enumerate(ComplexityInfo.SEARCH_COMPLEXITY.items(), 1):
            lines.append(f"\n{i}. {name.upper()}")
            lines.append(f"   Time: Best={info['time_best']}, "
                        f"Average={info['time_average']}, "
                        f"Worst={info['time_worst']}")
            lines.append(f"   Space: {info['space']}")
            lines.append(f"   {info['description']}")
        
        return "\n".join(lines)