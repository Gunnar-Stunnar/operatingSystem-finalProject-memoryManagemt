# This program implements the Optimal Page Replacement algorithm simulation.
# The Optimal algorithm is a theoretical page replacement algorithm that replaces the page
# that will not be used for the longest period of time in the future.
# This is used as a benchmark to compare against other page replacement algorithms.

import array

def optimalPage(pg, pn, fn):
    """
    Function to simulate the Optimal Page Replacement algorithm.
    
    Parameters:
    pg (array): Array of page references
    pn (int): Number of pages in the reference string
    fn (int): Number of frames available in memory
    
    The function tracks page hits and misses while maintaining the optimal page replacement strategy.
    """
    # Initialize frames array with -1 to represent empty frames
    fr = array.array('i', [-1] * fn)

    # Initialize hit counter
    hit = 0
    
    # Process each page reference in sequence
    for i in range(pn):
        # Check if current page is already in a frame (HIT)
        found = False
        for j in range(fn):
            if fr[j] == pg[i]:
                hit += 1
                found = True
                break

        if found:
            continue

        # If page not found, we have a MISS
        # First try to find an empty frame
        emptyFrame = False
        for j in range(fn):
            if fr[j] == -1:
                fr[j] = pg[i]
                emptyFrame = True
                break

        if emptyFrame:
            continue

        # If no empty frame, find the optimal page to replace
        # by looking ahead in the reference string
        farthest = -1
        replaceIndex = -1
        for j in range(fn):
            k = i + 1
            while(k < pn):
                if fr[j] == pg[k]:
                    if k > farthest:
                        farthest = k
                        replaceIndex = j
                    break
                k += 1
            if k == pn:
                replaceIndex = j
                break
        fr[replaceIndex] = pg[i]

    # Print results
    print("No. of hits =", hit)
    print("No. of misses =", pn - hit)

if __name__ == "__main__":
    # Test case: A sequence of page references
    pg = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5]
    pn = len(pg)  # Number of pages in reference string
    fn = 4        # Number of frames available
    
    # Run the simulation
    optimalPage(pg, pn, fn)
