CSI = '\x1b['
RESET = f'{CSI}0m'

def draw(size=15):
    red = 196
    white = 15
    thickness = 5
    center = size // 2
    for i in range(size):
        line_str = ""
        for col in range(size):
            if abs(i - center) < thickness // 2 or abs(col - center) < thickness // 2:
                line_str += f'{CSI}48;5;{white}m {RESET}'
            else:
                line_str += f'{CSI}48;5;{red}m {RESET}'
        print(line_str)

if __name__ == "__main__":
    draw()