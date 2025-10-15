CSI = '\x1b['
RESET = f'{CSI}0m'


def file_read(file):
    numbers = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                numbers.append(float(line))
    return numbers


def categorize(numbers):
    num_in = sum(1 for n in numbers if -3 <= n <= 3)
    num_out = len(numbers) - num_in
    return num_in, num_out


def draw_percent(num_in, num_out):
    total = num_in + num_out
    categories = [ ("От -3 до 3", num_in, 46),("Остальные", num_out, 196)]
    max_bar_length = 40
    print("Диаграмма процентного соотношения:\n")
    for condition, count, color in categories:
        percent = (count / total) * 100
        bar_length = int((count / total) * max_bar_length)
        bar = f'{CSI}48;5;{color}m{" " * bar_length}{RESET}'
        print(f"{condition:<15} | {bar} {percent:5.1f}% ({count}/{total})")


if __name__ == "__main__":
    file = "sequence.txt"
    numbers = file_read(file)
    in_range, out_range = categorize(numbers)
    draw_percent(in_range, out_range)