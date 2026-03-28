import os

# ─────────────────────────────────────────
# TASK 1: Process Class & Input Handling
# ─────────────────────────────────────────

class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid       # Process ID
        self.at  = at        # Arrival Time
        self.bt  = bt        # Burst Time
        self.ct  = 0         # Completion Time
        self.tat = 0         # Turnaround Time
        self.wt  = 0         # Waiting Time

def get_input():
    """Accept process details from the user."""
    processes = []
    n = int(input("Enter number of processes (4-5): "))
    print()
    for i in range(n):
        pid = int(input(f"  Process {i+1} — PID       : "))
        at  = int(input(f"  Process {i+1} — Arrival Time : "))
        bt  = int(input(f"  Process {i+1} — Burst Time   : "))
        processes.append(Process(pid, at, bt))
        print()
    return processes

def display_table(processes, title="Process Table"):
    """Display process details in a formatted table."""
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")
    print(f"  {'PID':<8}{'AT':<10}{'BT':<10}{'CT':<10}{'TAT':<10}{'WT'}")
    print(f"{'─'*55}")
    for p in processes:
        print(f"  {p.pid:<8}{p.at:<10}{p.bt:<10}{p.ct:<10}{p.tat:<10}{p.wt}")
    print(f"{'─'*55}\n")

# ─────────────────────────────────────────
# TASK 2: FCFS Scheduling
# ─────────────────────────────────────────

def fcfs(processes):
    """First Come First Serve — Non-Preemptive."""
    import copy
    procs = copy.deepcopy(processes)

    # Sort by Arrival Time
    procs.sort(key=lambda p: p.at)

    current_time = 0
    gantt = []   # stores (pid, start, end)

    for p in procs:
        # Handle CPU idle (no process has arrived yet)
        if current_time < p.at:
            gantt.append(("IDLE", current_time, p.at))
            current_time = p.at

        start = current_time
        current_time += p.bt          # process runs to completion
        p.ct  = current_time
        p.tat = p.ct - p.at
        p.wt  = p.tat - p.bt
        gantt.append((p.pid, start, p.ct))

    return procs, gantt

# ─────────────────────────────────────────
# TASK 3: SJF Scheduling (Non-Preemptive)
# ─────────────────────────────────────────

def sjf(processes):
    """Shortest Job First — Non-Preemptive."""
    import copy
    procs     = copy.deepcopy(processes)
    completed = []
    gantt     = []
    done      = [False] * len(procs)
    current_time = 0
    n = len(procs)

    for _ in range(n):
        # Build ready queue: arrived AND not done
        ready = [
            p for i, p in enumerate(procs)
            if not done[i] and p.at <= current_time
        ]

        # If no process available, jump to earliest arrival
        if not ready:
            next_arrival = min(p.at for i, p in enumerate(procs) if not done[i])
            gantt.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            ready = [p for i, p in enumerate(procs) if not done[i] and p.at <= current_time]

        # Pick shortest burst time
        shortest = min(ready, key=lambda p: p.bt)

        start = current_time
        current_time += shortest.bt
        shortest.ct  = current_time
        shortest.tat = shortest.ct - shortest.at
        shortest.wt  = shortest.tat - shortest.bt

        gantt.append((shortest.pid, start, shortest.ct))

        # Mark as done
        for i, p in enumerate(procs):
            if p.pid == shortest.pid and not done[i]:
                done[i] = True
                break

        completed.append(shortest)

    return completed, gantt

# ─────────────────────────────────────────
# TASK 4: Gantt Chart (Text-based)
# ─────────────────────────────────────────

def draw_gantt(gantt, title="Gantt Chart"):
    """Draw a simple text-based Gantt chart."""
    print(f"\n  📊 {title}")
    print("  ", end="")

    # Top bar
    for (pid, start, end) in gantt:
        label = f" P{pid} " if pid != "IDLE" else " IDLE"
        width = max(len(label), (end - start) * 2)
        print(f"|{label.center(width)}", end="")
    print("|")

    # Time labels
    print("  ", end="")
    for (pid, start, end) in gantt:
        label = f" P{pid} " if pid != "IDLE" else " IDLE"
        width = max(len(label), (end - start) * 2)
        print(f"{str(start):<{width+1}}", end="")
    # Print last end time
    print(gantt[-1][2])
    print()

# ─────────────────────────────────────────
# TASK 5: Performance Analysis
# ─────────────────────────────────────────

def performance(processes, label):
    """Calculate and display average WT and TAT."""
    avg_tat = sum(p.tat for p in processes) / len(processes)
    avg_wt  = sum(p.wt  for p in processes) / len(processes)
    print(f"  [{label}]")
    print(f"    Average Turnaround Time : {avg_tat:.2f}")
    print(f"    Average Waiting Time    : {avg_wt:.2f}")
    return avg_tat, avg_wt

def compare(fcfs_tat, fcfs_wt, sjf_tat, sjf_wt):
    """Compare FCFS vs SJF and recommend."""
    print(f"\n{'─'*55}")
    print("  📊 COMPARISON: FCFS vs SJF")
    print(f"{'─'*55}")
    print(f"  {'Metric':<30}{'FCFS':<12}{'SJF'}")
    print(f"{'─'*55}")
    print(f"  {'Avg Turnaround Time':<30}{fcfs_tat:<12.2f}{sjf_tat:.2f}")
    print(f"  {'Avg Waiting Time':<30}{fcfs_wt:<12.2f}{sjf_wt:.2f}")
    print(f"{'─'*55}")

    print("\n  🔍 Analysis:")
    if sjf_wt < fcfs_wt:
        print("  ✅ SJF is BETTER — it has lower average waiting time.")
        print("     SJF minimizes WT by always picking the shortest job,")
        print("     reducing the time longer processes wait in the queue.")
    else:
        print("  ✅ FCFS performed equally well or better for this input.")
    print(f"{'─'*55}\n")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    os.system('clear')  # clears terminal on Linux
    print("=" * 55)
    print("   OS Lab Assignment 1 — CPU Scheduling")
    print("   FCFS & SJF (Non-Preemptive)")
    print("=" * 55)

    # Task 1 — Input
    processes = get_input()
    display_table(processes, "INPUT: Process Table")

    # Task 2 — FCFS
    print("\n" + "="*55)
    print("  TASK 2: FCFS Scheduling")
    print("="*55)
    fcfs_result, fcfs_gantt = fcfs(processes)
    display_table(fcfs_result, "FCFS Results")

    # Task 4 — FCFS Gantt
    draw_gantt(fcfs_gantt, "FCFS Gantt Chart")

    # Task 3 — SJF
    print("="*55)
    print("  TASK 3: SJF Scheduling (Non-Preemptive)")
    print("="*55)
    sjf_result, sjf_gantt = sjf(processes)
    display_table(sjf_result, "SJF Results")

    # Task 4 — SJF Gantt
    draw_gantt(sjf_gantt, "SJF Gantt Chart")

    # Task 5 — Performance
    print("="*55)
    print("  TASK 5: Performance Analysis")
    print("="*55)
    fcfs_tat, fcfs_wt = performance(fcfs_result, "FCFS")
    print()
    sjf_tat,  sjf_wt  = performance(sjf_result,  "SJF")
    compare(fcfs_tat, fcfs_wt, sjf_tat, sjf_wt)

if __name__ == "__main__":
    main()