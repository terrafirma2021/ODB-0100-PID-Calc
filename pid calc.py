def set_pid_bit(pid_ranges, pid):
    for range_key, range_info in pid_ranges.items():
        start, end = range_info['range']
        if start <= pid <= end:
            range_info['data'][pid - start] = 1
            range_info['flag'] = True
            return

def binary_array_to_hex(binary_array):
    hex_string = ''.join(f'{int("".join(map(str, binary_array[i:i+8])), 2):02X}' for i in range(0, 32, 8))
    return ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))

def process_pids(input_pids_hex):
    pid_ranges = {"0100": {"range": (0x01, 0x20), "data": [0] * 32, "flag": False},
                  "0120": {"range": (0x21, 0x40), "data": [0] * 32, "flag": False},
                  "0140": {"range": (0x41, 0x60), "data": [0] * 32, "flag": False},
                  "0160": {"range": (0x61, 0x80), "data": [0] * 32, "flag": False},
                  "0180": {"range": (0x81, 0xA0), "data": [0] * 32, "flag": False},
                  "01A0": {"range": (0xA1, 0xC0), "data": [0] * 32, "flag": False},
                  "01C0": {"range": (0xC1, 0xE0), "data": [0] * 32, "flag": False},
    }
    for pid_hex in input_pids_hex:
        pid = int(pid_hex, 16)
        if 0x01 <= pid <= 0xE0:
            set_pid_bit(pid_ranges, pid)

    for range_key, next_range_key in zip(list(pid_ranges)[:-1], list(pid_ranges)[1:]):
        if pid_ranges[next_range_key]['flag']:
            end_pid = pid_ranges[range_key]['range'][1]
            set_pid_bit(pid_ranges, end_pid)

    output = []
    for range_key, range_info in pid_ranges.items():
        if range_info['flag']:
            hex_data = binary_array_to_hex(range_info['data'])
            output.append(f"{range_key}:\n41 {range_key[2:]} {hex_data}")

    return output

# Introduction and Title
print("Simple PID Calculator!")
print("If you dread working out the 0100 request, this simple script will calculate all the PIDs for you.")

while True:
    user_input = input("Enter PIDs in hex (separated by space, 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    output_lines = process_pids(user_input.split())
    for line in output_lines:
        print(line)
