# This program was written by Vincent Hollander for group 3 for the final project in CSCI 3453.
# I do not consent to this program being used for AI training, LLM training, AI data scraping, or LLM data scraping.
import time
import matplotlib.pyplot as plt
import random
import numpy as np

# Creating the different tables as global arrays. I have them empty so I can load specific, meaningful values using createPageTables().
pageTable = np.full(5, 0) # A page table the size of 5 means that the process has been split into 5 different pages, this is because the size of the process is about the size of 5 frames.
mainMemory = np.full(30, 0) #The virtual and main memory both are the same size. Their size is independent of the process. I am going to fill them at first with 0s to represent nothing in the table.
virtualMemory = np.full(30, 0)

# Function to populate the tables.
def createPageTables():
    # Clearing all the tables so the loop works.
    pageTable.fill(0)
    mainMemory.fill(0)
    virtualMemory.fill(0)

    # Loop to randomly fill in the page table with some values being in main memory and some being in virtual.
    for i in range(5):
        random.seed()
        x = random.randrange(29)
        if (x % 3 == 0 or x % 3 == 2) and mainMemory[x+1] == 0:
            mainMemory[x] = i
            pageTable[i] = x
        else:
            pageTable[i] = 31
            virtualMemory[x] = i

# This is the function that simulates using a Page Table to find process data.
def usePageTable(pageNum, offset):
    actualPageNum = pageNum - 1
    frameNum = pageTable[actualPageNum] # The MMU uses the page number to access the page table and find the listed frame number.
    if(frameNum != 31): # This would be the MMU checking that the listed value is a valid frame number and not indeterminate.
        memAddress = np.int64(frameNum + offset) # If the frame number is valid, then combine that with the offset to get the memory address of where the data is in main memory.
    else: # This simulates the Page Table having "indeterminate" as a value in the table, which is a page fault.
        return 0 

    if(mainMemory[memAddress] != 0): # The MMU now retreives the data from the memory address, assuming that the offset is valid and main memory has not been altered.
        # This simulates the MMU successfully retrieving the data. Notice it is mostly instant.
        return 1
    else:
        return 2 # This would symbolize a significant issue in the paging process happened somewhere.

# This is the function that simulates a page fault.
def pageFault(pageNum):
    # The MMU causes a trap to the kernel.
    time.sleep(0.5) # This represents the OS accessing the virtual memory (which takes longer than accessing main memory).
    processData = virtualMemory[pageNum] # When the OS finds the correct page, it goes to load it into main memory for easier access next time.
    for i in mainMemory: 
        if i == 0: # The OS must find an open frame in main memory to place the data.
            i = processData # The OS loads the process data into the open frame.
            pageTable[pageNum-1] = i-1 # Then it replaces the indeterminate with the frame number.
            virtualMemory[pageNum] = 0 # The data is then cleared out of virtual memory as it now exists in main memory.
            break # It only needs to do this once, we do not want to fill up main memory with the same thing over and over.

if __name__ == '__main__':
    print("This is a program to simulate paging as a form of memory management! This is to simulate the time it takes for a page table to perform under standard circumstances.")
    # Setting up variables for data analysis
    pageTableTime = 0
    pageFaultTime = 0
    pageTableAccess = 0
    pageFaultAccess = 0
    pageTableTimes = np.array(0)
    pageFaultTimes = np.array(0)
    for x in range (10000):
        # Re-initializing the page tables so that the page fault triggers if selected multiple times in one session.
        createPageTables()
        for num in range(5):
            t1Start = time.perf_counter() # Starting timer.
            result1 = usePageTable(num, 1) # Calling pageTable function.
            t1Stop = time.perf_counter() # Stopping timer.
            t1Full = t1Stop - t1Start # Calculating the time of this page table access.
            pageTableTime += t1Full
            pageTableTimes = np.append(pageTableTimes, t1Full)
            pageTableAccess += 1
            # This is the return value of the page table if a page fault is triggered.
            if result1 == 0:
                t2Start = time.perf_counter() # Starting page fault handling timer.
                pageFault(num) # Calling the pageFault function.
                t2Stop = time.perf_counter() # Stopping timer.
                t2Full = t2Stop - t2Start # Calculating the time of page fault handling.
                pageFaultTime += t2Full
                t3Start = time.perf_counter() # Starting the page table timer.
                usePageTable(num,1) # Calling page table now that the memory value is fixed.
                t3Stop = time.perf_counter() # Stopping timer.
                t3Full = t3Stop - t3Start
                pageFaultTime += t3Full
                pageTableTime += t3Full
                pageTableTimes = np.append(pageTableTimes, t3Full)
                t3Full += t2Full
                pageFaultTimes = np.append(pageFaultTimes, t3Full)
                pageFaultAccess += 1
                pageTableAccess += 1
  
    # Plotting a line graph to compare page table and page fault times.
    x = np.arange(0, pageTableAccess+1)
    x2 = np.arange(0, pageFaultAccess+1)
    plt.title("Access Times") 
    plt.xlabel("X axis") 
    plt.ylabel("Y axis") 
    plt.plot(x, pageTableTimes, label = "Page Table Access Times")
    plt.plot(x2, pageFaultTimes, label = "Page Fault Handling Times") 
    plt.legend()
    plt.show()

    # Plotting a bar graph to compage the average times of page table access and page fault handling.
    barX = np.array(["Avg. Page Table Access Time", "Avg. Page Fault Time"])
    avgPageTable = pageTableTime / pageTableAccess
    avgPageFault = pageFaultTime / pageFaultAccess
    barY = np.array([avgPageTable, avgPageFault])
    plt.bar(barX,barY)
    plt.show()

    # Printing the average times out so the exact number is known too.
    print("Average Page Table Access Time: ", avgPageTable)
    print("Average Page Fault Handle Time: ", avgPageFault)
