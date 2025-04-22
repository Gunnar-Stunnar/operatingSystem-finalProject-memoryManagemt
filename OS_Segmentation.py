import collections

def simulate_fifo(page_reference_string, num_frames):
    """
    Simulates the FIFO page replacement algorithm.

    Args:
        page_reference_string (list): Sequence of page numbers requested.
        num_frames (int): Number of available physical memory frames.

    Returns:
        int: Total number of page faults.
    """
    frames = collections.deque(maxlen=num_frames) # Use deque for efficient FIFO queue
    frame_set = set() # For quick checking if page is in frames
    page_faults = 0
    print("\n--- FIFO Simulation ---")
    print(f"Frames: {num_frames}, Reference String: {page_reference_string}")
    print("Step | Page | Frames Status         | Fault?")
    print("-----+------+-----------------------+--------")

    for i, page in enumerate(page_reference_string):
        fault = False
        if page not in frame_set:
            page_faults += 1
            fault = True
            if len(frames) == num_frames:
                # Frames are full, remove the oldest (leftmost in deque)
                evicted_page = frames.popleft()
                frame_set.remove(evicted_page)
            # Add the new page to the end (rightmost in deque)
            frames.append(page)
            frame_set.add(page)

        # Print status for this step
        frame_list = list(frames)
        frame_str = str(frame_list).ljust(21) # Pad for alignment
        fault_str = "Yes" if fault else "No"
        print(f"{i+1:<4} | {page:<4} | {frame_str} | {fault_str}")

    print(f"\nTotal Page Faults (FIFO): {page_faults}")
    return page_faults

#-------------------------------------------------

def simulate_lru(page_reference_string, num_frames):
    """
    Simulates the LRU page replacement algorithm.

    Args:
        page_reference_string (list): Sequence of page numbers requested.
        num_frames (int): Number of available physical memory frames.

    Returns:
        int: Total number of page faults.
    """
    # We use an OrderedDict to maintain access order easily.
    # The rightmost item is the most recently used (MRU).
    # The leftmost item is the least recently used (LRU).
    frames = collections.OrderedDict()
    page_faults = 0
    print("\n--- LRU Simulation ---")
    print(f"Frames: {num_frames}, Reference String: {page_reference_string}")
    print("Step | Page | Frames Status (LRU->MRU) | Fault?")
    print("-----+------+--------------------------+--------")

    for i, page in enumerate(page_reference_string):
        fault = False
        if page not in frames:
            page_faults += 1
            fault = True
            if len(frames) == num_frames:
                # Frames are full, remove the LRU item (first item)
                frames.popitem(last=False) # popitem(last=False) removes the first item (LRU)
            # Add the new page (it becomes the MRU)
            frames[page] = None # Value doesn't matter, only keys and their order
        else:
            # Page hit! Move the accessed page to the end (make it MRU)
            frames.move_to_end(page)

        # Print status for this step
        frame_list = list(frames.keys())
        frame_str = str(frame_list).ljust(26) # Pad for alignment
        fault_str = "Yes" if fault else "No"
        print(f"{i+1:<4} | {page:<4} | {frame_str} | {fault_str}")

    print(f"\nTotal Page Faults (LRU): {page_faults}")
    return page_faults

#-------------------------------------------------

def find_optimal_victim(current_frames, future_references):
    """
    Helper for Optimal: Finds the page in current_frames that will be
    used furthest in the future (or not at all).
    """
    victim = -1
    max_future_distance = -1

    for frame_page in current_frames:
        try:
            # Find the next index where this page appears in the future
            future_index = future_references.index(frame_page)
            if future_index > max_future_distance:
                max_future_distance = future_index
                victim = frame_page
        except ValueError:
            # Page is not referenced again in the future, perfect victim!
            return frame_page

    # If all pages in frames are referenced again, return the one used furthest away
    if victim == -1: # Should only happen if current_frames is empty, which isn't the case here
         # Or if all remaining future refs are in current_frames. Pick the last one.
         if current_frames: return list(current_frames)[0] # Fallback: FIFO-like if needed, but logic above covers most. Or pick last used. max_future_distance page needed.
         else: return -1 # Should not happen

    return victim # The page whose next use is furthest away


def simulate_optimal(page_reference_string, num_frames):
    """
    Simulates the Optimal (OPT/MIN) page replacement algorithm.

    Args:
        page_reference_string (list): Sequence of page numbers requested.
        num_frames (int): Number of available physical memory frames.

    Returns:
        int: Total number of page faults.
    """
    frames = set() # Order doesn't matter intrinsically, just presence
    frame_list_for_print = [] # Maintain a list for printing order if desired
    page_faults = 0
    print("\n--- Optimal Simulation ---")
    print(f"Frames: {num_frames}, Reference String: {page_reference_string}")
    print("Step | Page | Frames Status         | Victim | Fault?")
    print("-----+------+-----------------------+--------+--------")

    for i, page in enumerate(page_reference_string):
        fault = False
        victim_page = "-" # Placeholder for victim
        if page not in frames:
            page_faults += 1
            fault = True
            if len(frames) == num_frames:
                # Frames are full, find the optimal victim to evict
                future_refs = page_reference_string[i+1:]
                victim_page = find_optimal_victim(frames, future_refs)
                frames.remove(victim_page)
                frame_list_for_print.remove(victim_page)

            # Add the new page
            frames.add(page)
            frame_list_for_print.append(page) # Add to list for printing consistency

        # Print status for this step
        frame_str = str(sorted(list(frames))).ljust(21) # Sort for consistent display
        fault_str = "Yes" if fault else "No"
        victim_str = str(victim_page).ljust(6)
        print(f"{i+1:<4} | {page:<4} | {frame_str} | {victim_str} | {fault_str}")

    print(f"\nTotal Page Faults (Optimal): {page_faults}")
    return page_faults

# --- Main Execution ---
if __name__ == "__main__":
    # Example usage:
    # Belady's Anomaly example reference string
    # page_refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    page_refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

    num_frames_3 = 3
    num_frames_4 = 4

    print("="*40)
    print(f" SIMULATING WITH {num_frames_3} FRAMES ")
    print("="*40)
    fifo_faults_3 = simulate_fifo(page_refs, num_frames_3)
    lru_faults_3 = simulate_lru(page_refs, num_frames_3)
    opt_faults_3 = simulate_optimal(page_refs, num_frames_3)

    print("\n" + "="*40)
    print(f" SIMULATING WITH {num_frames_4} FRAMES ")
    print("="*40)
    fifo_faults_4 = simulate_fifo(page_refs, num_frames_4)
    lru_faults_4 = simulate_lru(page_refs, num_frames_4)
    opt_faults_4 = simulate_optimal(page_refs, num_frames_4)

    print("\n" + "="*40)
    print(" SUMMARY OF PAGE FAULTS ")
    print("="*40)
    print(f"Algorithm | {num_frames_3} Frames | {num_frames_4} Frames")
    print(f"----------+----------+----------")
    print(f"FIFO      | {fifo_faults_3:<8} | {fifo_faults_4:<8}")
    print(f"LRU       | {lru_faults_3:<8} | {lru_faults_4:<8}")
    print(f"Optimal   | {opt_faults_3:<8} | {opt_faults_4:<8}")
    print("="*40)

    # Example showing potential Belady's Anomaly for FIFO
    belady_refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    print("\nTesting for Belady's Anomaly with FIFO:")
    print(f"Reference String: {belady_refs}")
    fifo_belady_3 = simulate_fifo(belady_refs, 3)
    fifo_belady_4 = simulate_fifo(belady_refs, 4)
    if fifo_belady_4 > fifo_belady_3:
        print(f"\n*** Belady's Anomaly Detected for FIFO! Faults increased from {fifo_belady_3} (3 frames) to {fifo_belady_4} (4 frames). ***")
    else:
        print(f"\nNo Belady's Anomaly detected for FIFO with this string (Faults: {fifo_belady_3} (3 frames), {fifo_belady_4} (4 frames)).")