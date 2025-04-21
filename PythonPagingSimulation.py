# This program was written by Vincent Hollander for group 3 for the final project in CSCI 3453.
# I do not consent to this program being used for AI training, LLM training, AI data scraping, or LLM data scraping.
import time
import numpy as np

# Creating the different tables as global arrays. I have them empty so I can load specific, meaningful values using createPageTables().
pageTable = np.empty(5) # A page table the size of 5 means that the process has been split into 5 different pages, this is because the size of the process is about the size of 5 frames.
mainMemory = np.full(30, 0) #The virtual and main memory both are the same size. Their size is independent of the process. I am going to fill them at first with 0s to represent nothing in the table.
virtualMemory = np.full(30, 0)

# Function to populate the tables.
def createPageTables():
    mainMemory[mainMemory] = 0
    virtualMemory[virtualMemory] = 0

    # The page table gives the frame number that the part of the process is stored in.
    pageTable[0] = 5
    pageTable[1] = 6
    pageTable[2] = 7
    pageTable[3] = 31 # Notably, part 3 of the process is not stored in main memory, so it is set to a value outside of the main memory frames to represent it as "indeterminate".
    pageTable[4] = 25

    # The actual main memory address of the part of the process is found by combining the frame number and the offset (in this case we are just adding them together).
    mainMemory[6] = 1
    mainMemory[7] = 2
    mainMemory[8] = 3
    mainMemory[26] = 5

    # While virtual memory mimics the size of main memory, it notably does not have to store processes in the same manner as it does not use the page table to access it.
    virtualMemory[4] = 4

# This is the function that simulates using a Page Table to find process data.
def usePageTable(pageNum, offset):
    actualPageNum = pageNum - 1
    frameNum = pageTable[actualPageNum] # The MMU uses the page number to access the page table and find the listed frame number.
    if(frameNum != 31): # This would be the MMU checking that the listed value is a valid frame number and not indeterminate.
        memAddress = np.int64(frameNum + offset) # If the frame number is valid, then combine that with the offset to get the memory address of where the data is in main memory.
    else: # This simulates the Page Table having "indeterminate" as a value in the table, which is a page fault.
        return 0 

    if(mainMemory[memAddress] != 0): # The MMU now retreives the data from the memory address, assuming that the offset is valid and main memory has not been altered.
        print("The Page Table found: ", mainMemory[memAddress]) # This simulates the MMU successfully retrieving the data. Notice it is mostly instant.
        return 1
    else:
        return 2 # This would symbolize a significant issue in the paging process happened somewhere.

# This is the function that simulates a page fault.
def pageFault(pageNum):
    print("OS Trap Triggered: Invalid Memory Access!") # The MMU causes a trap to the kernel.
    time.sleep(0.5) # This represents the OS accessing the virtual memory (which takes longer than accessing main memory).
    processData = virtualMemory[pageNum] # When the OS finds the correct page, it goes to load it into main memory for easier access next time.
    for i in mainMemory: 
        if i == 0: # The OS must find an open frame in main memory to place the data.
            i = processData # The OS loads the process data into the open frame.
            pageTable[pageNum-1] = i-1 # Then it replaces the indeterminate with the frame number.
            virtualMemory[pageNum] = 0 # The data is then cleared out of virtual memory as it now exists in main memory.
            break # It only needs to do this once, we do not want to fill up main memory with the same thing over and over.
    print("Page fault has been resolved")

if __name__ == '__main__':
    progOn = True # This is set up to let the program loop so the users can test mutliple times in one run.
    print("This is a program to simulate paging as a form of memory management! This is to simulate the time it takes for a page table to perform under standard circumstances.")
    while progOn:
        # Initializing variables to count the time for the whole simulation and individual functions.
        timeTotal = 0
        pageTableTime = 0
        pageFaultTime = 0

        # Re-initializing the page tables so that the page fault triggers if selected multiple times in one session.
        createPageTables()

        # Getting user input to select which process section we want to test
        print("You are playing the role of the CPU, please select a number between 1-5 to signify the request of a process' data. To exit press 0.")
        num = int(input())

        # Handling the user input
        if num > 0 and num < 6: # This is the correct case.
            t1Start = time.perf_counter() # Starting timer.
            result1 = usePageTable(num, 1) # Calling pageTable function.
            t1Stop = time.perf_counter() # Stopping timer.
            timeTotal += t1Stop - t1Start # Adding this to total time.
            pageTableTime += t1Stop - t1Start # Calculating the time of this page table access.
        elif num == 0: # This allows the user to exit gracefully.
            print("Simulation over!")
            progOn = False
            break
        else: # This is error handling for incorrect input.
            print("Invalid option, please select a number between 1 and 5.")
            continue

        # This is the return value of the page table if a page fault is triggered.
        if result1 == 0:
            t2Start = time.perf_counter() # Starting page fault handling timer.
            pageFault(num) # Calling the pageFault function.
            t2Stop = time.perf_counter() # Stopping timer.
            timeTotal += t2Stop - t2Start # Adding to total time.
            pageFaultTime += t2Stop - t2Start # Calculating the time of page fault handling.
            t3Start = time.perf_counter() # Starting the page table timer.
            usePageTable(num,1) # Calling page table now that the memory value is fixed.
            t3Stop = time.perf_counter() # Stopping timer.
            pageFaultTime += t3Stop - t3Start # Adding this to the time it takes for the page fault to be handled.
            timeTotal += t3Stop - t3Start # Adding to total time.

        # The output of the timers
        print("The total time of paging procedures is: ", timeTotal)
        print("The time taken when accessing the page table is: ", pageTableTime)
        if num == 4:
            print("The time taken to handle the page fault is: ", pageFaultTime)
