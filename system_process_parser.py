import subprocess
import datetime


def get_system_status():
    # Run 'ps aux' command and capture output
    output = subprocess.check_output(['ps', 'aux']).decode().split('\n')

    # Initialize variables_
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

    # Return system status report as a dictionary
    report = {
        'System Users': ', '.join(users),
        'Processes started': total_processes,
        'User processes': user_processes,
        'Total memory used': f'{total_mem:.1f}%',
        'Total CPU used': f'{total_cpu:.1f}%',
        'Uses the most memory': (max_mem_process[0], f'{max_mem_process[1]:.1f}%'),
        'Most CPU uses': (max_cpu_process[0], f'{max_cpu_process[1]:.1f}%')
    }
    return report


def save_report(report):
    # Save report to file
    now = datetime.datetime.now()
    filename = now.strftime('%m-%d-%Y-%H:%M-scan.txt')
    with open(filename, 'w') as f:
        f.write('System Status Report:\n')
        for key, value in report.items():
            if key == 'User processes':
                f.write('User processes:\n')
                for user, num_processes in value.items():
                    f.write(f"{user}: {num_processes}\n")
            else:
                f.write(f"{key}: {value}\n")


if __name__ == '__main__':
    # Get system status report
    report = get_system_status()

    # Output results to console
    print('System Status Report:')
    for key, value in report.items():
        if key == 'User processes':
            print('User processes:')
            for user, num_processes in value.items():
                print(f"{user}: {num_processes}")
        else:
            print(f"{key}: {value}")

    # Save report to file
    save_report(report)
