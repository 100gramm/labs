CSI = '\x1b['
RESET = f'{CSI}0m'
RED = 196
WHITE = 15


def draw(size=15):
    thickness = 5
    center = size // 2
    for i in range(size):
        line_str = ""
        for col in range(size):
            if abs(i - center) < thickness // 2 or abs(col - center) < thickness // 2:
                line_str += f'{CSI}48;5;{WHITE}m {RESET}'
            else:
                line_str += f'{CSI}48;5;{RED}m {RESET}'
        print(line_str)


if __name__ == "__main__":
    draw()