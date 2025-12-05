# 🎯 Advanced Algorithm Visualizer - Enhanced Edition

<div align="center">

![Algorithm Visualizer Banner](https://img.shields.io/badge/Algorithm-Visualizer-blueviolet?style=for-the-badge)

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.3+-11557c?style=flat-square&logo=plotly&logoColor=white)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**A professionally refactored, modular algorithm visualization application featuring event-driven animations, graph paper backgrounds, and clean architecture for educational and research purposes.**

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

---

![Demo Animation](https://via.placeholder.com/800x400/ffffff/4CAF50?text=Algorithm+Visualizer+with+Graph+Paper+Background)

*Real-time visualization with graph paper background and GREEN highlight animations*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Module Documentation](#-module-documentation)
- [Algorithm Reference](#-algorithm-reference)
- [User Interface](#-user-interface)
- [Visual Design](#-visual-design)
- [Performance Analysis](#-performance-analysis)
- [Configuration](#-configuration)
- [Use Cases](#-use-cases)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

The **Advanced Algorithm Visualizer - Enhanced Edition** is a complete refactoring of the original visualizer, built with clean architecture principles. It separates algorithm logic from UI rendering, uses event-driven animations, and features a professional graph paper background theme.

### 🎓 Why This Version?

- **Clean Architecture**: 6 modular files with clear separation of concerns
- **Event-Driven**: Algorithms emit events; UI plays them back (no UI in core logic)
- **Graph Paper Theme**: Professional 5-unit grid cells for clarity
- **GREEN Highlights**: Consistent color scheme across all animations
- **Improved Tree Layout**: Better spacing with exponential width reduction
- **No Flickering**: Proper layer management with cached backgrounds
- **Extensible**: Easy to add new algorithms without touching UI code

### ✨ What Makes This Different?

<table>
<tr>
<td width="50%">

#### Before (Original)
❌ Mixed UI and algorithm logic  
❌ Grid corruption during animations  
❌ Inconsistent color schemes  
❌ Direct canvas updates (flickering)  
❌ Monolithic code structure  
❌ Tree nodes overlapping  

</td>
<td width="50%">

#### After (Enhanced)
✅ Pure algorithm functions (zero UI)  
✅ Static cached graph paper background  
✅ Unified GREEN highlight theme  
✅ Layered rendering (smooth animations)  
✅ 6 modular files (clean separation)  
✅ Auto-centering tree with proper spacing  

</td>
</tr>
</table>

---

## ✨ Key Features

### 🔄 Algorithm Coverage

<table>
<tr>
<td width="50%">

#### Sorting Algorithms (7)
- ✅ **Bubble Sort** - O(n²)
- ✅ **Selection Sort** - O(n²)
- ✅ **Insertion Sort** - O(n²)
- ✅ **Merge Sort** - O(n log n)
- ✅ **Quick Sort** - O(n log n) avg
- ✅ **Heap Sort** - O(n log n)
- ✅ **Radix Sort** - O(d(n+k))

</td>
<td width="50%">

#### Search Algorithms (4)
- 🔍 **Linear Search** - O(n)
- 🔍 **Binary Search** - O(log n)
- 🔍 **Jump Search** - O(√n)
- 🔍 **Interpolation Search** - O(log log n)

</td>
</tr>
</table>

### 🌳 Tree Operations
- **Insert** - Add nodes with GREEN highlighting
- **Delete** - Remove with proper restructuring
- **Search** - Visual path highlighting
- **Traversals** - Inorder, Preorder, Postorder, Level-order

### 🎮 Interactive Controls

| Feature | Description |
|---------|-------------|
| ⚡ **Adjustable Speed** | Slider from 0.01s to 1.0s per step |
| 🎬 **Event Playback** | Step-by-step animation replay |
| 📊 **Live Statistics** | Real-time comparisons and execution time |
| 🎨 **Graph Paper Background** | Professional 5-unit grid cells |
| 💾 **Data Management** | Import/Export CSV and JSON |
| 📈 **Performance Analysis** | Compare algorithms with charts |
| 📜 **History Tracking** | Auto-saved execution history (JSON) |
| 🎯 **Complexity Info** | Built-in Big O reference guide |

---

## 🚀 Installation

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.7 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Display**: 1280x800 minimum resolution

### Step 1: Install Python

Download and install Python from [python.org](https://www.python.org/downloads/)

**Verify installation:**
```bash
python --version
# Should output: Python 3.7.x or higher
```

### Step 2: Clone Repository
```bash
git clone https://github.com/yourusername/algorithm-visualizer-enhanced.git
cd algorithm-visualizer-enhanced
```

Or download ZIP and extract:
```bash
cd algorithm-visualizer-enhanced
```

### Step 3: Install Dependencies

**Required packages:**
```bash
pip install matplotlib>=3.3.0
pip install numpy>=1.19.0
```

**Create requirements.txt:**
```txt
matplotlib>=3.3.0
numpy>=1.19.0
```

**Install from requirements:**
```bash
pip install -r requirements.txt
```

**Note**: Tkinter comes pre-installed with Python. If missing:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (via Homebrew)
brew install python-tk
```

### Step 4: Launch Application
```bash
python app_main.py
```

**Alternative launch methods:**
```bash
# With info display
python app_main.py --info

# Run tests
python app_main.py --test

# Run tests without GUI
python app_main.py --test --no-gui
```

If the application window opens, installation is successful! ✅

---

## 🎯 Quick Start

### 1. Basic Sorting Visualization
```bash
# Launch the application
python app_main.py

# In the Sorting Tab:
1. Click "GENERATE" to create random data
2. Adjust speed slider (default: 0.1s)
3. Click any sorting algorithm (e.g., "QUICK")
4. Watch GREEN-highlighted animation
5. View statistics in status bar
```

### 2. Custom Data Input
```python
# In the Array input field, enter:
64,34,25,12,22,11,90

# Press Enter or click any algorithm to visualize
```

### 3. Search Operations
```bash
# Switch to Search Tab
1. Click "GENERATE" to create sorted array
2. Enter target value (e.g., 42)
3. Select search algorithm (e.g., "BINARY")
4. Watch step-by-step search with highlights
5. Result shown in status bar
```

### 4. Binary Search Tree
```bash
# Switch to Tree Tab
1. Enter value (e.g., 50)
2. Click "INSERT" - node highlighted in GREEN
3. Add more nodes: 30, 70, 20, 40, 60, 80
4. Click "INORDER" to see sorted traversal
5. Try "SEARCH" with existing value
```

### 5. Performance Comparison
```bash
# Switch to Analysis Tab
1. Run multiple sorting algorithms (from Sorting tab)
2. Click "COMPARE SORT"
3. View bar chart comparison
4. Click "BIG O" for complexity reference
5. Click "EXPORT" to save results (JSON/CSV)
```

---

## 🏗️ Architecture

### Modular Design Philosophy

The application is split into **6 independent modules** for maximum maintainability:

```
algorithm-visualizer-enhanced/
│
├── core_algorithms.py          # Part 1: Pure algorithm implementations
│   ├── AlgorithmCore           # Sorting algorithms
│   ├── SearchCore              # Search algorithms
│   ├── TreeNode                # Tree data structure
│   └── AlgorithmEvent          # Event emission system
│
├── ui_rendering.py             # Part 2: Rendering & visualization layer
│   ├── GraphPaperBackground    # Static 5-unit grid generator
│   ├── LayeredRenderer         # 4-layer drawing system
│   ├── SortingVisualizer       # Sorting display
│   ├── SearchVisualizer        # Search display
│   ├── TreeVisualizer          # Tree display with auto-layout
│   └── AnimationPlayer         # Event playback engine
│
├── tree_history.py             # Part 3: Tree operations & history
│   ├── TreeOperations          # BST insert/delete/search
│   ├── HistoryManager          # JSON history storage
│   ├── DataManager             # CSV/JSON import/export
│   └── ComplexityInfo          # Algorithm complexity database
│
├── main_application.py         # Part 4: GUI framework & layouts
│   ├── AlgorithmVisualizer     # Main window class
│   ├── setup_sorting_tab()     # Sorting UI
│   ├── setup_search_tab()      # Search UI
│   ├── setup_tree_tab()        # Tree UI
│   └── setup_analysis_tab()    # Analysis UI
│
├── algorithm_execution.py      # Part 5: Event handling & execution
│   ├── AlgorithmExecutor       # Runs algorithms with timing
│   ├── TreeEventHandler        # Handles tree operations
│   ├── DataIOHandler           # File operations
│   ├── AnalysisHandler         # Performance comparison
│   └── HistoryViewHandler      # History viewing
│
└── app_main.py                 # Part 6: Entry point & integration
    ├── IntegratedAlgorithmVisualizer  # Complete app
    ├── ApplicationLauncher            # Window setup
    ├── DevTools                       # Testing utilities
    └── main()                         # Entry point
```

### Event-Driven Architecture

```mermaid
graph LR
    A[User Action] --> B[Algorithm Execution]
    B --> C[Event Generation]
    C --> D[Event Queue]
    D --> E[Animation Player]
    E --> F[Layered Renderer]
    F --> G[UI Update]
    G --> H[History Save]
```

### Rendering Pipeline

```
Layer 0: Static Graph Paper Background (cached, drawn once)
    ↓
Layer 1: Grid Lines (5-unit squares, semi-transparent)
    ↓
Layer 2: Bar Chart Elements (with 30% padding)
    ↓
Layer 3: GREEN Highlights (active operations)
    ↓
Layer 4: Text Overlays (messages, labels)
```

### Data Flow

```python
# Algorithm emits events (no UI dependency)
events = AlgorithmCore.bubble_sort(data)

# UI plays back events
player = AnimationPlayer(visualizer)
player.play_events(events, speed=0.1)

# History automatically saved
history_manager.add_entry("Bubble Sort", data, time)
```

---

## 📚 Module Documentation

### Part 1: `core_algorithms.py` (~600 lines)

**Purpose**: Pure algorithm implementations with zero UI dependencies

**Key Classes:**
- `EventType` - Enum for event types (COMPARE, SWAP, SORTED, etc.)
- `AlgorithmEvent` - Data class for algorithm events
- `AlgorithmCore` - Static methods for sorting algorithms
- `SearchCore` - Static methods for search algorithms
- `TreeNode` - Binary tree node structure

**Example Usage:**
```python
from core_algorithms import AlgorithmCore, EventType

# Generate events
data = [64, 34, 25, 12, 22, 11, 90]
events = AlgorithmCore.quick_sort(data)

# Each event contains:
for event in events:
    print(f"Type: {event.event_type}")
    print(f"Indices: {event.indices}")
    print(f"Message: {event.message}")
    print(f"Data: {event.data_snapshot}")
```

**All Algorithms Return:**
```python
List[AlgorithmEvent]  # Sequence of events for playback
```

---

### Part 2: `ui_rendering.py` (~600 lines)

**Purpose**: Rendering engine with graph paper background and layered drawing

**Key Classes:**

#### `GraphPaperBackground`
```python
# Static background generator
GraphPaperBackground.create_background(ax, width=100, height=100)

# Features:
# - 5-unit grid cells (larger for clarity)
# - Semi-transparent lines (alpha=0.4)
# - Cached for performance
```

#### `LayeredRenderer`
```python
renderer = LayeredRenderer(ax)

# Layer 1: Draw bars with padding
renderer.draw_bars(data, colors)  # width=0.7 (30% padding)

# Layer 2: Add highlights
renderer.add_highlights([0, 1, 2], len(data))

# Layer 3: Add text
renderer.add_text_overlay("Sorting...", position='top')
```

#### `SortingVisualizer`
```python
visualizer = SortingVisualizer(fig, ax, canvas)

# Draw current state
visualizer.draw_state(data, event)

# Automatically handles:
# - Background refresh
# - Color selection based on event type
# - Highlight rendering
# - Message display
```

#### `AnimationPlayer`
```python
player = AnimationPlayer(visualizer, update_callback)

# Play events with timing
player.play_events(events, speed=0.1)

# Control playback
player.stop()
player.is_running()  # Check if playing
```

**Color Theme:**
```python
THEME = {
    "bg": "#f8f8f6",           # Off-white background
    "fg": "#000000",           # Black text
    "canvas_bg": "#ffffff",    # Pure white canvas
    "grid": "#c0c0c0",         # Light gray grid
    "highlight": "#4CAF50",    # GREEN (all animations)
    "sorted": "#90EE90",       # Light green (sorted)
    "found": "#2E7D32",        # Dark green (found)
}
```

---

### Part 3: `tree_history.py` (~600 lines)

**Purpose**: Tree operations and history management

**Key Classes:**

#### `TreeOperations`
```python
tree = TreeOperations()

# Insert
success, message = tree.insert(50)

# Delete
success, message = tree.delete(30)

# Search
found, message = tree.search(42)

# Traversals
inorder = tree.inorder_traversal()       # [20, 30, 40, 50, 60, 70, 80]
preorder = tree.preorder_traversal()     # [50, 30, 20, 40, 70, 60, 80]
postorder = tree.postorder_traversal()   # [20, 40, 30, 60, 80, 70, 50]
level_order = tree.level_order_traversal()  # [50, 30, 70, 20, 40, 60, 80]

# Info
info = tree.get_info()
# Returns: {"type": "BST", "height": 3, "nodes": 7, "is_empty": False}
```

#### `HistoryManager`
```python
history = HistoryManager("sorting_history.json")

# Add entry
history.add_entry(
    algorithm="Quick Sort",
    data=[1, 2, 3, 4, 5],
    execution_time=0.0234,
    size=5
)

# Retrieve
all_entries = history.get_all()
recent = history.get_recent(10)
by_algo = history.get_by_algorithm("Quick Sort")

# Statistics
stats = history.get_statistics()
# Returns: {"total_runs": 15, "algorithms": {...}, "avg_time": 0.0123}

# Export
history.export_csv("history.csv")
```

#### `DataManager`
```python
# Save/Load JSON
DataManager.save_to_json(data, "output.json", metadata={"sorted": True})
data, metadata = DataManager.load_from_json("output.json")

# Save/Load CSV
DataManager.save_to_csv(data, "output.csv")
data = DataManager.load_from_csv("output.csv")

# Export analysis
DataManager.export_analysis(
    sorting_history,
    search_history,
    execution_times,
    "analysis.json"
)
```

#### `ComplexityInfo`
```python
# Get algorithm info
info = ComplexityInfo.get_sorting_info("Quick Sort")
# Returns: {
#   "time_best": "O(n log n)",
#   "time_average": "O(n log n)",
#   "time_worst": "O(n²)",
#   "space": "O(log n)",
#   "stable": False,
#   "description": "Fast in-place sorting..."
# }

# Get formatted text
text = ComplexityInfo.format_complexity_text()
print(text)  # Full complexity reference
```

---

### Part 4: `main_application.py` (~600 lines)

**Purpose**: GUI framework with tabs and controls

**Main Class:**
```python
class AlgorithmVisualizer:
    def __init__(self, root):
        # Initialize visualizers
        self.sort_visualizer = SortingVisualizer(...)
        self.search_visualizer = SearchVisualizer(...)
        self.tree_visualizer = TreeVisualizer(...)
        
        # Initialize data
        self.data = []
        self.search_array = []
        self.tree_ops = TreeOperations()
        
        # Initialize history
        self.sorting_history = HistoryManager("sorting_history.json")
        self.search_history = HistoryManager("search_history.json")
        
        # Setup tabs
        self.setup_sorting_tab()
        self.setup_search_tab()
        self.setup_tree_tab()
        self.setup_analysis_tab()
```

**Tab Structure:**

#### Sorting Tab
```
┌─────────────────────────────────────────┐
│  Visualization Area (Graph Paper)       │
│  [Green highlighted bars with padding]  │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  Array Display: [5][2][8][1][9][3][7]  │
└─────────────────────────────────────────┘
┌──────────┬──────────────┬──────────────┐
│ DATA     │ ALGORITHMS   │ CONTROLS     │
│ Array:__ │ [BUBBLE]     │ [SAVE]       │
│ [GEN]    │ [SELECTION]  │ [LOAD]       │
│ Speed:⚡  │ [INSERTION]  │ [RESET]      │
│          │ [MERGE]      │              │
│          │ [QUICK]      │              │
│          │ [HEAP]       │              │
│          │ [RADIX]      │              │
└──────────┴──────────────┴──────────────┘
Status: READY | Message: Ready to sort
```

#### Search Tab
```
┌─────────────────────────────────────────┐
│  Visualization Area (Graph Paper)       │
│  [Green highlighted search progression] │
└─────────────────────────────────────────┘
┌──────────────┬──────────────────────────┐
│ SEARCH SETUP │ SEARCH ALGORITHMS        │
│ Array:____   │ [LINEAR]  [BINARY]       │
│ Target:__    │ [JUMP]    [INTERPOLATION]│
│ [GENERATE]   │                          │
└──────────────┴──────────────────────────┘
Status: READY | Message: Ready to search
```

#### Tree Tab
```
┌─────────────────────────────────────────┐
│      Binary Search Tree Display         │
│          [50]                           │
│         /    \                          │
│      [30]    [70]                       │
│      / \      / \                       │
│   [20][40][60][80]                      │
└─────────────────────────────────────────┘
┌─────────────┬─────────────┬────────────┐
│ OPERATIONS  │ TRAVERSALS  │ TREE INFO  │
│ Value:___   │ [INORDER]   │ Type: BST  │
│ [INSERT]    │ [PREORDER]  │ Height: 3  │
│ [DELETE]    │ [POSTORDER] │ Nodes: 7   │
│ [SEARCH]    │ [LEVEL]     │            │
│ [CLEAR]     │             │            │
└─────────────┴─────────────┴────────────┘
Status: READY
```

#### Analysis Tab
```
┌─────────────────────────────────────────┐
│  Time Comparison    │  Space Info       │
│  [Bar Chart]        │  [Complexity]     │
│                     │                   │
└─────────────────────────────────────────┘
┌──────────────────┬──────────────────────┐
│ ANALYSIS         │ HISTORY              │
│ [COMPARE SORT]   │ [SORT HISTORY]       │
│ [COMPARE SEARCH] │ [SEARCH HISTORY]     │
│ [BIG O]          │ [CLEAR ALL]          │
│ [EXPORT]         │                      │
└──────────────────┴──────────────────────┘
```

---

### Part 5: `algorithm_execution.py` (~600 lines)

**Purpose**: Event handling and algorithm execution

**Key Handlers:**

#### `AlgorithmExecutor`
```python
executor = AlgorithmExecutor(app_reference)

# Run sorting with timing
executor.run_sorting_algorithm(
    name="Quick Sort",
    algorithm_func=AlgorithmCore.quick_sort
)

# Features:
# - Automatic timing
# - Event playback
# - Status updates
# - History saving
```

#### `TreeEventHandler`
```python
handler = TreeEventHandler(app_reference)

# Operations
handler.insert_node()      # With GREEN highlight
handler.delete_node()      # With animation
handler.search_tree()      # With path highlighting
handler.clear_tree()       # With confirmation
handler.traverse_tree("inorder")  # With result display
```

#### `DataIOHandler`
```python
handler = DataIOHandler(app_reference)

# File operations
handler.save_sorted_data()        # CSV or JSON
handler.load_data_from_file()     # With validation
handler.reset_sort_visualization()  # With confirmation
```

#### `AnalysisHandler`
```python
handler = AnalysisHandler(app_reference)

# Performance analysis
handler.compare_sorting_algorithms()   # Bar chart
handler.compare_search_algorithms()    # Avg time chart
handler.show_complexity_analysis()     # Reference window
handler.export_analysis()              # JSON/CSV export
```

#### `HistoryViewHandler`
```python
handler = HistoryViewHandler(app_reference)

# History viewing
handler.view_sort_history()      # Table view
handler.view_search_history()    # Table view
handler.clear_all_history()      # With confirmation
```

---

### Part 6: `app_main.py` (~600 lines)

**Purpose**: Application entry point and integration

**Main Components:**

#### `IntegratedAlgorithmVisualizer`
```python
class IntegratedAlgorithmVisualizer(AlgorithmVisualizer):
    def __init__(self, root):
        super().__init__(root)
        
        # Initialize all handlers
        self.executor = AlgorithmExecutor(self)
        self.tree_handler = TreeEventHandler(self)
        self.data_io_handler = DataIOHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.history_handler = HistoryViewHandler(self)
    
    # Delegate to handlers
    def run_sorting(self, name, func):
        self.executor.run_sorting_algorithm(name, func)
```

#### `ApplicationLauncher`
```python
# Window setup
ApplicationLauncher.configure_window(root)
ApplicationLauncher.setup_window_icon(root)
ApplicationLauncher.setup_close_handler(root, app)
ApplicationLauncher.show_welcome_message(app)
```

#### `DevTools`
```python
# Development utilities
DevTools.print_module_info()  # Show loaded modules
DevTools.run_tests()          # Basic functionality tests
```

#### Entry Point
```python
def main():
    root = tk.Tk()
    app = IntegratedAlgorithmVisualizer(root)
    ApplicationLauncher.configure_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🔄 Algorithm Reference

### Sorting Algorithms - Detailed Analysis

<details>
<summary><b>Bubble Sort</b></summary>

**Description**: Repeatedly compares adjacent elements and swaps if in wrong order

**Complexity**:
- Time: O(n²) average and worst, O(n) best
- Space: O(1)
- Stable: ✅

**Visual Behavior**:
- GREEN highlights comparisons
- Sorted elements remain light green
- Bubbles largest element to end each pass

**Best for**: 
- Educational purposes
- Nearly sorted data
- Small datasets (<10 elements)

**Implementation Pseudocode**:
```
for i = 0 to n-1:
    for j = 0 to n-i-2:
        if arr[j] > arr[j+1]:
            swap(arr[j], arr[j+1])
```

**Optimization**: Add flag to stop if no swaps in a pass

</details>

<details>
<summary><b>Quick Sort</b></summary>

**Description**: Divide-and-conquer using pivot partitioning

**Complexity**:
- Time: O(n log n) average, O(n²) worst
- Space: O(log n) for recursion stack
- Stable: ❌

**Visual Behavior**:
- Shows pivot selection (last element)
- Demonstrates partitioning
- GREEN highlights active comparisons

**Best for**:
- Large datasets
- General-purpose sorting
- In-place sorting requirements

**Pivot Selection Strategies**:
- Last element (implemented)
- First element
- Random element
- Median-of-three

**Worst Case**: Already sorted array with last element pivot

</details>

<details>
<summary><b>Merge Sort</b></summary>

**Description**: Divide array, sort halves, merge back

**Complexity**:
- Time: O(n log n) all cases
- Space: O(n)
- Stable: ✅

**Visual Behavior**:
- Shows divide phase
- Demonstrates merge operations
- GREEN highlights during merge

**Best for**:
- Large datasets
- When stability is required
- External sorting (disk-based)
- Linked lists

**Advantages**:
- Guaranteed O(n log n)
- Predictable performance
- Stable sort

**Disadvantages**:
- Requires O(n) extra space
- Slower for small arrays
- Not in-place

</details>

<details>
<summary><b>Heap Sort</b></summary>

**Description**: Build max heap, extract maximum repeatedly

**Complexity**:
- Time: O(n log n) all cases
- Space: O(1)
- Stable: ❌

**Visual Behavior**:
- Shows heapify operations
- Demonstrates swap to end
- GREEN highlights active nodes

**Best for**:
- When O(1) space is critical
- Guaranteed O(n log n) needed
- Priority queue implementations

**Phases**:
1. Build max heap: O(n)
2. Extract max n times: O(n log n)

</details>

<details>
<summary><b>Radix Sort</b></summary>

**Description**: Non-comparison sort processing digits

**Complexity**:
- Time: O(d(n+k)) where d=digits, k=base
- Space: O(n+k)
- Stable: ✅

**Visual Behavior**:
- Sorts digit by digit (ones, tens, hundreds)
- Shows counting sort for each digit
- GREEN highlights current digit processing

**Best for**:
- Integer arrays
- Fixed-length strings
- When range is not >> n

**Limitations**:
- Only for integers/strings
- Requires extra space
- Performance depends on digit count

</details>

### Search Algorithms - Detailed Analysis

<details>
<summary><b>Binary Search</b></summary>

**Description**: Divide sorted array in half repeatedly

**Complexity**:
- Time: O(log n)
- Space: O(1) iterative
- **Prerequisite**: Sorted array

**Implementation**:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Visual Behavior**:
- GREEN highlights search range
- Shows mid calculation
- Demonstrates range elimination

**When to Use**:
- ✅ Large sorted arrays
- ✅ Multiple searches
- ❌ Unsorted data
- ❌ Frequent insertions

</details>

<details>
<summary><b>Interpolation Search</b></summary>

**Description**: Estimates position using interpolation formula

**Complexity**:
- Time: O(log log n) average, O(n) worst
- Space: O(1)
- **Prerequisite**: Sorted + uniformly distributed

**Formula**:
```python
pos = low + ((target - arr[low]) * (high - low)) / (arr[high] - arr[low])
```

**Best for**: Phone books, dictionaries, uniform distributions

**Visual Behavior**:
- Shows position calculation
- Demonstrates intelligent guessing
- GREEN highlights interpolated position

**Advantages**:
- Faster than binary for uniform data
- O(log log n) is very
