from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import math


class EventType(Enum):
    """Event types for algorithm visualization"""
    COMPARE = "compare"
    SWAP = "swap"
    SET = "set"
    SORTED = "sorted"
    FOUND = "found"
    NOT_FOUND = "not_found"
    HIGHLIGHT = "highlight"
    DIVIDE = "divide"
    MERGE = "merge"
    PIVOT = "pivot"


@dataclass
class AlgorithmEvent:
    """Event emitted during algorithm execution"""
    event_type: EventType
    indices: List[int]
    values: Optional[List[int]] = None
    message: str = ""
    data_snapshot: Optional[List[int]] = None


class TreeNode:
    """Binary tree node"""
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class AlgorithmCore:
    """Core algorithm implementations - pure functions that emit events"""
    
    @staticmethod
    def bubble_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Bubble sort - returns event sequence"""
        events = []
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Compare event
                events.append(AlgorithmEvent(
                    event_type=EventType.COMPARE,
                    indices=[j, j + 1],
                    values=[data_copy[j], data_copy[j + 1]],
                    message=f"Comparing: {data_copy[j]} vs {data_copy[j+1]}",
                    data_snapshot=data_copy.copy()
                ))
                
                if data_copy[j] > data_copy[j + 1]:
                    # Swap
                    data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
                    events.append(AlgorithmEvent(
                        event_type=EventType.SWAP,
                        indices=[j, j + 1],
                        values=[data_copy[j], data_copy[j + 1]],
                        message=f"Swapped: {data_copy[j]} ↔ {data_copy[j+1]}",
                        data_snapshot=data_copy.copy()
                    ))
            
            # Mark sorted
            events.append(AlgorithmEvent(
                event_type=EventType.SORTED,
                indices=list(range(n - i, n)),
                message=f"Position {n-i-1} sorted",
                data_snapshot=data_copy.copy()
            ))
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(n)),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def selection_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Selection sort - returns event sequence"""
        events = []
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            min_idx = i
            
            for j in range(i + 1, n):
                # Compare to find minimum
                events.append(AlgorithmEvent(
                    event_type=EventType.COMPARE,
                    indices=[j, min_idx],
                    values=[data_copy[j], data_copy[min_idx]],
                    message=f"Finding min: checking {data_copy[j]}",
                    data_snapshot=data_copy.copy()
                ))
                
                if data_copy[j] < data_copy[min_idx]:
                    min_idx = j
            
            # Swap with minimum
            data_copy[i], data_copy[min_idx] = data_copy[min_idx], data_copy[i]
            events.append(AlgorithmEvent(
                event_type=EventType.SWAP,
                indices=[i, min_idx],
                values=[data_copy[i], data_copy[min_idx]],
                message=f"Swapped: {data_copy[i]} to position {i}",
                data_snapshot=data_copy.copy()
            ))
            
            # Mark sorted
            events.append(AlgorithmEvent(
                event_type=EventType.SORTED,
                indices=list(range(i + 1)),
                message=f"First {i+1} elements sorted",
                data_snapshot=data_copy.copy()
            ))
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(n)),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def insertion_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Insertion sort - returns event sequence"""
        events = []
        data_copy = data.copy()
        
        for i in range(1, len(data_copy)):
            key = data_copy[i]
            j = i - 1
            
            # Highlight key being inserted
            events.append(AlgorithmEvent(
                event_type=EventType.HIGHLIGHT,
                indices=[i],
                values=[key],
                message=f"Inserting: {key}",
                data_snapshot=data_copy.copy()
            ))
            
            # Shift elements
            while j >= 0 and data_copy[j] > key:
                events.append(AlgorithmEvent(
                    event_type=EventType.COMPARE,
                    indices=[j, j + 1],
                    values=[data_copy[j], key],
                    message=f"Shifting: {data_copy[j]} right",
                    data_snapshot=data_copy.copy()
                ))
                
                data_copy[j + 1] = data_copy[j]
                j -= 1
            
            data_copy[j + 1] = key
            
            # Mark sorted section
            events.append(AlgorithmEvent(
                event_type=EventType.SORTED,
                indices=list(range(i + 1)),
                message=f"First {i+1} elements sorted",
                data_snapshot=data_copy.copy()
            ))
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(len(data_copy))),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def merge_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Merge sort - returns event sequence"""
        events = []
        data_copy = data.copy()
        
        def merge_sort_helper(arr: List[int], l: int, r: int, depth: int = 0):
            if l < r:
                m = (l + r) // 2
                
                # Divide event
                events.append(AlgorithmEvent(
                    event_type=EventType.DIVIDE,
                    indices=list(range(l, r + 1)),
                    message=f"Dividing: [{l}:{r}]",
                    data_snapshot=arr.copy()
                ))
                
                merge_sort_helper(arr, l, m, depth + 1)
                merge_sort_helper(arr, m + 1, r, depth + 1)
                merge(arr, l, m, r)
                
                # Merge complete event
                events.append(AlgorithmEvent(
                    event_type=EventType.MERGE,
                    indices=list(range(l, r + 1)),
                    message=f"Merged: [{l}:{r}]",
                    data_snapshot=arr.copy()
                ))
        
        def merge(arr: List[int], l: int, m: int, r: int):
            left = arr[l:m + 1]
            right = arr[m + 1:r + 1]
            i = j = 0
            k = l
            
            while i < len(left) and j < len(right):
                events.append(AlgorithmEvent(
                    event_type=EventType.COMPARE,
                    indices=[k],
                    values=[left[i], right[j]],
                    message=f"Merging at position {k}",
                    data_snapshot=arr.copy()
                ))
                
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
        
        merge_sort_helper(data_copy, 0, len(data_copy) - 1)
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(len(data_copy))),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def quick_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Quick sort - returns event sequence"""
        events = []
        data_copy = data.copy()
        
        def partition(arr: List[int], low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            
            # Mark pivot
            events.append(AlgorithmEvent(
                event_type=EventType.PIVOT,
                indices=[high],
                values=[pivot],
                message=f"Pivot: {pivot}",
                data_snapshot=arr.copy()
            ))
            
            for j in range(low, high):
                events.append(AlgorithmEvent(
                    event_type=EventType.COMPARE,
                    indices=[j, high],
                    values=[arr[j], pivot],
                    message=f"Pivot: {pivot}, checking {arr[j]}",
                    data_snapshot=arr.copy()
                ))
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    events.append(AlgorithmEvent(
                        event_type=EventType.SWAP,
                        indices=[i, j],
                        values=[arr[i], arr[j]],
                        message=f"Swapped: {arr[i]} ↔ {arr[j]}",
                        data_snapshot=arr.copy()
                    ))
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            events.append(AlgorithmEvent(
                event_type=EventType.SWAP,
                indices=[i + 1, high],
                values=[arr[i + 1], arr[high]],
                message=f"Pivot {pivot} in place",
                data_snapshot=arr.copy()
            ))
            
            return i + 1
        
        def quick_sort_helper(arr: List[int], low: int, high: int):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
        
        quick_sort_helper(data_copy, 0, len(data_copy) - 1)
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(len(data_copy))),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def heap_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Heap sort - returns event sequence"""
        events = []
        data_copy = data.copy()
        
        def heapify(arr: List[int], n: int, i: int):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            
            if l < n and arr[i] < arr[l]:
                largest = l
            
            if r < n and arr[largest] < arr[r]:
                largest = r
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                
                events.append(AlgorithmEvent(
                    event_type=EventType.SWAP,
                    indices=[i, largest],
                    values=[arr[i], arr[largest]],
                    message=f"Heapify: swapping {arr[largest]} ↔ {arr[i]}",
                    data_snapshot=arr.copy()
                ))
                
                heapify(arr, n, largest)
        
        n = len(data_copy)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(data_copy, n, i)
        
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            data_copy[i], data_copy[0] = data_copy[0], data_copy[i]
            
            events.append(AlgorithmEvent(
                event_type=EventType.SWAP,
                indices=[0, i],
                values=[data_copy[0], data_copy[i]],
                message=f"Moving {data_copy[i]} to sorted position",
                data_snapshot=data_copy.copy()
            ))
            
            events.append(AlgorithmEvent(
                event_type=EventType.SORTED,
                indices=list(range(i, n)),
                message=f"Sorted from position {i}",
                data_snapshot=data_copy.copy()
            ))
            
            heapify(data_copy, i, 0)
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(n)),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events

    @staticmethod
    def radix_sort(data: List[int]) -> List[AlgorithmEvent]:
        """Radix sort - returns event sequence"""
        events = []
        data_copy = data.copy()
        
        def counting_sort_for_radix(arr: List[int], exp: int):
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
                events.append(AlgorithmEvent(
                    event_type=EventType.SET,
                    indices=[i],
                    values=[arr[i]],
                    message=f"Digit sort: processing position {i}",
                    data_snapshot=arr.copy()
                ))
        
        max_val = max(data_copy)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort_for_radix(data_copy, exp)
            exp *= 10
        
        # Final sorted event
        events.append(AlgorithmEvent(
            event_type=EventType.SORTED,
            indices=list(range(len(data_copy))),
            message="✓ Sorting Complete!",
            data_snapshot=data_copy.copy()
        ))
        
        return events


class SearchCore:
    """Core search algorithm implementations"""
    
    @staticmethod
    def linear_search(arr: List[int], target: int) -> List[AlgorithmEvent]:
        """Linear search - returns event sequence"""
        events = []
        
        for i in range(len(arr)):
            events.append(AlgorithmEvent(
                event_type=EventType.COMPARE,
                indices=[i],
                values=[arr[i]],
                message=f"Checking index {i}: {arr[i]}",
                data_snapshot=arr.copy()
            ))
            
            if arr[i] == target:
                events.append(AlgorithmEvent(
                    event_type=EventType.FOUND,
                    indices=[i],
                    values=[target],
                    message=f"✓ FOUND {target} at index {i}!",
                    data_snapshot=arr.copy()
                ))
                return events
        
        events.append(AlgorithmEvent(
            event_type=EventType.NOT_FOUND,
            indices=[],
            values=[target],
            message=f"✗ {target} not found",
            data_snapshot=arr.copy()
        ))
        
        return events

    @staticmethod
    def binary_search(arr: List[int], target: int) -> List[AlgorithmEvent]:
        """Binary search - returns event sequence"""
        events = []
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            events.append(AlgorithmEvent(
                event_type=EventType.COMPARE,
                indices=[left, mid, right],
                values=[arr[left], arr[mid], arr[right]],
                message=f"Searching range [{left}:{right}], mid={mid}",
                data_snapshot=arr.copy()
            ))
            
            if arr[mid] == target:
                events.append(AlgorithmEvent(
                    event_type=EventType.FOUND,
                    indices=[mid],
                    values=[target],
                    message=f"✓ FOUND {target} at index {mid}!",
                    data_snapshot=arr.copy()
                ))
                return events
            elif arr[mid] < target:
                events.append(AlgorithmEvent(
                    event_type=EventType.HIGHLIGHT,
                    indices=[mid],
                    message=f"Target > {arr[mid]}, search right",
                    data_snapshot=arr.copy()
                ))
                left = mid + 1
            else:
                events.append(AlgorithmEvent(
                    event_type=EventType.HIGHLIGHT,
                    indices=[mid],
                    message=f"Target < {arr[mid]}, search left",
                    data_snapshot=arr.copy()
                ))
                right = mid - 1
        
        events.append(AlgorithmEvent(
            event_type=EventType.NOT_FOUND,
            indices=[],
            values=[target],
            message=f"✗ {target} not found",
            data_snapshot=arr.copy()
        ))
        
        return events

    @staticmethod
    def jump_search(arr: List[int], target: int) -> List[AlgorithmEvent]:
        """Jump search - returns event sequence"""
        events = []
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Jump through array
        while arr[min(step, n) - 1] < target:
            events.append(AlgorithmEvent(
                event_type=EventType.HIGHLIGHT,
                indices=list(range(prev, min(step, n))),
                message=f"Jumping: block [{prev}:{min(step, n)}]",
                data_snapshot=arr.copy()
            ))
            
            prev = step
            step += int(math.sqrt(n))
            
            if prev >= n:
                events.append(AlgorithmEvent(
                    event_type=EventType.NOT_FOUND,
                    indices=[],
                    values=[target],
                    message=f"✗ {target} not found",
                    data_snapshot=arr.copy()
                ))
                return events
        
        # Linear search in block
        while arr[prev] < target:
            events.append(AlgorithmEvent(
                event_type=EventType.COMPARE,
                indices=[prev],
                values=[arr[prev]],
                message=f"Linear search at index {prev}",
                data_snapshot=arr.copy()
            ))
            
            prev += 1
            
            if prev == min(step, n):
                events.append(AlgorithmEvent(
                    event_type=EventType.NOT_FOUND,
                    indices=[],
                    values=[target],
                    message=f"✗ {target} not found",
                    data_snapshot=arr.copy()
                ))
                return events
        
        if arr[prev] == target:
            events.append(AlgorithmEvent(
                event_type=EventType.FOUND,
                indices=[prev],
                values=[target],
                message=f"✓ FOUND {target} at index {prev}!",
                data_snapshot=arr.copy()
            ))
            return events
        
        events.append(AlgorithmEvent(
            event_type=EventType.NOT_FOUND,
            indices=[],
            values=[target],
            message=f"✗ {target} not found",
            data_snapshot=arr.copy()
        ))
        
        return events

    @staticmethod
    def interpolation_search(arr: List[int], target: int) -> List[AlgorithmEvent]:
        """Interpolation search - returns event sequence"""
        events = []
        left, right = 0, len(arr) - 1
        
        while left <= right and arr[left] <= target <= arr[right]:
            if left == right:
                if arr[left] == target:
                    events.append(AlgorithmEvent(
                        event_type=EventType.FOUND,
                        indices=[left],
                        values=[target],
                        message=f"✓ FOUND {target} at index {left}!",
                        data_snapshot=arr.copy()
                    ))
                else:
                    events.append(AlgorithmEvent(
                        event_type=EventType.NOT_FOUND,
                        indices=[],
                        values=[target],
                        message=f"✗ {target} not found",
                        data_snapshot=arr.copy()
                    ))
                return events
            
            # Calculate position using interpolation
            pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))
            
            events.append(AlgorithmEvent(
                event_type=EventType.COMPARE,
                indices=[left, pos, right],
                values=[arr[left], arr[pos], arr[right]],
                message=f"Interpolating: checking position {pos}",
                data_snapshot=arr.copy()
            ))
            
            if arr[pos] == target:
                events.append(AlgorithmEvent(
                    event_type=EventType.FOUND,
                    indices=[pos],
                    values=[target],
                    message=f"✓ FOUND {target} at index {pos}!",
                    data_snapshot=arr.copy()
                ))
                return events
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        events.append(AlgorithmEvent(
            event_type=EventType.NOT_FOUND,
            indices=[],
            values=[target],
            message=f"✗ {target} not found",
            data_snapshot=arr.copy()
        ))
        
        return events