"""
This script simulates the Least Recently Used (LRU) Cache replacement algorithm.

It allows the user to:
- Input the number of memory frames (cache capacity).
- Enter a sequence of page references.

The program then:
- Applies the LRU page replacement logic.
- Displays the memory state after each page reference.
- Reports the total number of page faults at the end.
"""

# Get input from user
def getInput():
    """
    Get input from the user for the cache size and page reference string.
    - Returns: A tuple containing the cache size and a list of page references.
    """
    
    frameSize = int(input("Enter the number of memory frames: "))
    pageInput = input("Enter the page reference string (space-separated): ")
    pageReferenceString = list(map(int, pageInput.strip().split()))
    return frameSize, pageReferenceString

# Node class for doubly linked list
class Node:
    def __init__(self, page):
        """
        Initialize a Node object with a given page number.
        - page: The page number associated with the node.
        - prev: Previous node in the doubly linked list (initially None).
        - next: Next node in the doubly linked list (initially None).
        """
        self.page = page # Page number
        self.prev = None # Previous node of doubly linked list
        self.next = None # Next node of doubly linked list

# LRU Cache class
class LRUCache:
    def __init__(self, capacity):
        """
        Initialize the LRUCache with a given capacity.
        - capacity: The number of frames the cache can hold.
        """
        
        self.capacity = capacity # No. of memory frames
        self.pageMap = {} # Map (page no. to node)
        self.head = None # Most recently used (MRU) page.
        self.tail = None # Least recently used (LRU) page.
        self.pageFaults = 0 # To count the number of page faults.

   
    def remove(self, node):
        """
        Remove a node from the doubly linked list.
        - node: The node to remove from the list.
        """
        
        if node.prev: 
            node.prev.next = node.next # To adjust the previous node's next pointer.
        else:
            self.head = node.next # If node is head, update the head pointer.

        if node.next:
            node.next.prev = node.prev # To adjust the next node's previous pointer.
        else:
            self.tail = node.prev # If node is tail, update tail pointer.

    
    def addToFront(self, node):
        """
        Add a node to the front (most recently used) of the doubly linked list.
        - node: The node to add to the front of the list.
        """
        
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node # To adjust the old head's previous pointer
        self.head = node # To make the new node the head.

        if self.tail is None:
            self.tail = node # If the list was empty, make this node the tail.

    def getMemoryState(self):
        """
        Return a list representing the current memory state from MRU to LRU.
        - Returns: A list of page numbers in the order from MRU to LRU.
        """
        
        result = []
        current = self.head
        while current:
            result.append(current.page) # To collect page numbers from MRU to LRU.
            current = current.next
        return result

    def accessPage(self, page):
        """
        Simulate accessing a page.
        - If the page is in the cache (hit), move it to the front (MRU).
        - If the page is not in the cache (fault), add it to the front.
          - If the cache is full, remove the least recently used (LRU) page.
        - page: The page number being accessed.
        """
        
        if page in self.pageMap:
            node = self.pageMap[page]
            self.remove(node) # To remove from its current position
            self.addToFront(node) # To move to the front (MRU)
            print(f"Page {page} -> Hit -> Memory: {self.getMemoryState()}")

        else:
            # Page fault
            self.pageFaults += 1
            newNode = Node(page)
            if len(self.pageMap) >= self.capacity:
                # If memory is full, remove the LRU (tail)
                del self.pageMap[self.tail.page] # To remove page from map
                self.remove(self.tail) # To remove the LRU node
            self.addToFront(newNode) # To add the new page to the front
            self.pageMap[page] = newNode # To add the page to the map.
            print(f"Page {page} -> Fault -> Memory: {self.getMemoryState()}")


if __name__ == "__main__":
   
    frameSize, pageReferenceString = getInput() # To get input from the user.

    leastRecentlyUsed = LRUCache(frameSize) # To create an LRU cache with the specified frame size.

    # To simulate accessing each page in the reference string.
    for page in pageReferenceString:
        leastRecentlyUsed.accessPage(page)
    
    # To output the total number of page faults.
    totalFaults = leastRecentlyUsed.pageFaults
    print(f"\nTotal page faults: {totalFaults}")
