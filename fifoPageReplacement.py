"""
This script simulates the FIFO (First-In-First-Out) Page Replacement Algorithm.

It allows the user to:
- Input the number of memory frames.
- Enter a sequence of page references.

The program then:
- Applies the FIFO page replacement logic.
- Displays the memory status after each page reference.
- Reports the total number of page faults at the end.
"""

def getInput():

    """
    - Takes user input for the number of memory frames and the page reference string.
    
    Returns:
    -------
        - frameSize (int): The number of memory frames.
        - pages (list): A list of integers representing the page reference string.
    """
    
    frameSize = int(input("Please enter the number of memory frames: ")) # User to enter the no. of memory frames.
    pageInput = input("Please enter the page reference string (space-separated): ") # User to enter the page reference string.


    # To convert the input string into a list of integers.
    # - strip() removes any leading and trailing whitespaces.
    # - split() splits by spaces
        
    pages = list(map(int, pageInput.strip().split()))

    return frameSize, pages


def fifoPageReplacement (pages, frameSize):

    """
    Simulates the FIFO (First-In-First-Out) Page Replacement algorithm.

    Parameters:
    ----------
        pages (list): A list of integers representing the page reference string.
        frameSize (int): The number of memory frames available.

    The function:
    - Prints whether each page reference results in a hit or a fault.
    - Displays the current state of memory after each operation.
    - Shows the total number of page faults at the end.
    
    """
    
    memory = [] # List to simulate memory frames (act like a queue).
    pageFaultsCounter = 0 # Counter the total page faults.

    for page in pages:

        # To check if the page is already in memory (Hit).
        if page not in memory:
            
            pageFaultsCounter += 1 # To increase the page fault no in case if page is not in the memory.

            # As per the FIFO algorithm, if memory is full, remove the oldest page.
            if len(memory) >= frameSize:
            
                memory.pop(0) # To remove the oldest (first) page.
            
            memory.append(page) # To add the new page in the memory.

            print(f"Page {page} -> Fault -> memory: {memory}") # To show status after this operation.

        else:
            print(f"Page {page} -> Hit -> memory: {memory}") # Page Hit (already in the memory).

    print(f"\nTotal Page Faults: {pageFaultsCounter}")


if __name__ == "__main__":
    frameSize, pages = getInput() # To get input from user.
    
    fifoPageReplacement(pages, frameSize); # To execute FIFO page replacement with input.
