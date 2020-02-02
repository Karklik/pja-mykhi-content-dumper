# Method for conversion of display size of files to bytes
def to_bytes(value):
    value = value.strip()
    last_character = value[-1:]
    exit_value = 0.0
    if last_character.isnumeric():
        exit_value = float(value)
    elif last_character == 'K':
        exit_value = float(value[:-1]) * 1024
    elif last_character == 'M':
        exit_value = float(value[:-1]) * 1024 * 1024
    elif last_character == 'G':
        exit_value = float(value[:-1]) * 1024 * 1024 * 1024
    return exit_value

# Method for conversion of bytes to human readable form
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + 'bytes'