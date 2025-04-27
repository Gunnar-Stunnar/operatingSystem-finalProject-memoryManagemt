import matplotlib.pyplot as plt
import numpy as np

class Segment:
    def __init__(self, name, base, limit, perm, path):
        self.name = name
        self.base = base
        self.limit = limit
        self.perm = perm
        self.path = path

    def print_segment_info(self):
        print(f"Segment {self.name}: Base = {self.base}, Limit = {self.limit}")

    def print_windows_memory_map(self):
        start_addr = f"{self.base:08X}"
        end_addr = f"{self.base + self.limit - 1:08X}"
        size_kb = f"{(self.limit + 1023) // 1024} KB"
        if 'x' in self.perm:
            prot = "ReadExecute"
        elif 'w' in self.perm:
            prot = "ReadWrite"
        elif 'r' in self.perm:
            prot = "ReadOnly"
        else:
            prot = "No Access"

        region_type = "Image" if self.name.lower() == "code" else "Private"
        segment_path = f"{self.path}\\{self.name}"
        print(f"{start_addr}    {end_addr}    {region_type:10}  {prot:12}  {size_kb}   {segment_path}")

class Process:
    def __init__(self, path):
        self.segments = []
        self.path = path

    def add_segment(self, name, size, perm):
        base = 0 if not self.segments else self.segments[-1].base + self.segments[-1].limit
        segment = Segment(name, base, size, perm, self.path)
        self.segments.append(segment)

    def show_segments(self):
        print("Segment Information:")
        for segment in self.segments:
            segment.print_segment_info()

        print("\nMemory Segment Mapping:")
        print("Start       End         Type        Protection   Size     Path")
        for segment in self.segments:
            segment.print_windows_memory_map()

# Setup process
process_path = "C:\\Users\\spand\\OneDrive\\Desktop\\OS_Seg.py"
process = Process(process_path)
process.add_segment("Code", 400, "r-xp")
process.add_segment("Data", 300, "r--p")
process.add_segment("Stack", 200, "rw-p")
process.show_segments()

# Simulated access time in nanoseconds
access_times = {
    'Code': {'Read': 20, 'Write': 9999, 'Execute': 15},
    'Data': {'Read': 25, 'Write': 30, 'Execute': 9999},
    'Stack': {'Read': 22, 'Write': 28, 'Execute': 9999}
}

segments = list(access_times.keys())
read_times = [access_times[seg]['Read'] for seg in segments]
write_times = [access_times[seg]['Write'] for seg in segments]
execute_times = [access_times[seg]['Execute'] for seg in segments]

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(segments))
bar_width = 0.25

# Plot bars
ax.bar([i - bar_width for i in x], read_times, width=bar_width, label='Read')
ax.bar(x, write_times, width=bar_width, label='Write')
ax.bar([i + bar_width for i in x], execute_times, width=bar_width, label='Execute')

# Labeling
ax.set_xlabel('Memory Segment')
ax.set_ylabel('Access Time (ns)')
ax.set_title('Simulated Access Time per Segment and Operation')
ax.set_xticks(x)
ax.set_xticklabels(segments)

# Log scale and visible ticks
ax.set_yscale('log')
ax.set_yticks([10, 100, 1000, 10000])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()
