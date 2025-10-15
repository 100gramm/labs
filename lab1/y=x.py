CSI = '\x1b['
RESET = f'{CSI}0m'

def function():
    h = 12
    w = 36
    for y in range(h, -1, -1):
        line_str = ""
        for x in range(w):
            if x == 0 and y == 0:
                line_str += "+"  #точка пересечения осей
            elif y == 0:
                line_str += "-"
            elif x == 0:
                line_str += "|" 
            elif int(x / 3) == y:
                line_str += f'{CSI}48;5;46m {RESET}'  #точка функции
            else:
                line_str += " "
        print(line_str)

if __name__ == "__main__":
    function()