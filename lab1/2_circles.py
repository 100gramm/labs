import math
CSI = '\x1b['
RESET = f'{CSI}0m'

def circles(width=40, height=15, radius=5):
    center_y = height // 2
    center_x1 = width // 2 - radius
    center_x2 = width // 2 + radius
    for y in range(height):
        line_str = ""
        for x in range(width):
            dist1 = math.sqrt((x - center_x1)**2 + (y - center_y)**2)
            dist2 = math.sqrt((x - center_x2)**2 + (y - center_y)**2)
            if abs(dist1 - radius) < 0.8 or abs(dist2 - radius) < 0.8:
                line_str += f'{CSI}48;5;0m {RESET}'#контур
            elif dist1 < radius or dist2 < radius:
                line_str += f'{CSI}48;5;15m {RESET}'#внутри кругов
            else:
                line_str += " "
        print(line_str)

if __name__ == "__main__":
    circles()