import subprocess
import datetime

# Run 'ps aux' command and capture output
output = subprocess.check_output(['ps', 'aux']).decode().split('\n')

# Initialize variables
users = []
user_processes = {}
total_processes = 0
total_cpu = 0.0
total_mem = 0.0
max_mem_process = ('', 0.0)
max_cpu_process = ('', 0.0)

# Parse output and extract relevant information
for line in output[1:]:
    if not line:
        continue
    fields = line.split()
    user = fields[0]
    if user not in users:
        users.append(user)
        user_processes[user] = 0
    user_processes[user] += 1
    total_processes += 1
    cpu = float(fields[2])
    mem = float(fields[3])
    total_cpu += cpu
    total_mem += mem
    if mem > max_mem_process[1]:
        max_mem_process = (fields[10][:20], mem)
    if cpu > max_cpu_process[1]:
        max_cpu_process = (fields[10][:20], cpu)

# Output results to console
print('System Status Report:')
print(f"System Users: {', '.join(users)}")
print(f"Processes started: {total_processes}")
print('User processes:')
for user, num_processes in user_processes.items():
    print(f"{user}: {num_processes}")
print(f"Total memory used: {total_mem:.1f}%")
print(f"Total CPU used: {total_cpu:.1f}%")
print(f"Uses the most memory: ({max_mem_process[0]}, {max_mem_process[1]:.1f}%)")
print(f"Most CPU uses: ({max_cpu_process[0]}, {max_cpu_process[1]:.1f}%)")

# Save report to file
now = datetime.datetime.now()
filename = now.strftime('%m-%d-%Y-%H:%M-scan.txt')
with open(filename, 'w') as f:
    f.write('System Status Report:\n')
    f.write(f"System Users: {', '.join(users)}\n")
    f.write(f"Processes started: {total_processes}\n")
    f.write('User processes:\n')
    for user, num_processes in user_processes.items():
        f.write(f"{user}: {num_processes}\n")
    f.write(f"Total memory used: {total_mem:.1f}%\n")
    f.write(f"Total CPU used: {total_cpu:.1f}%\n")
    f.write(f"Uses the most memory: ({max_mem_process[0]}, {max_mem_process[1]:.1f}%)\n")
    f.write(f"Most CPU uses: ({max_cpu_process[0]}, {max_cpu_process[1]:.1f}%)\n")
