from itertools import combinations

ITEMS = {
    "r": ("rifle", 3, 25),
    "p": ("pistol", 2, 15),
    "a": ("ammo", 2, 15),
    "m": ("medkit", 2, 20),
    "i": ("inhaler", 1, 5),
    "k": ("knife", 1, 15),
    "x": ("axe", 3, 20),
    "t": ("talisman", 1, 25),
    "f": ("flask", 1, 15),
    "d": ("antidot", 1, 10),
    "s": ("supplies", 2, 20),
    "c": ("crossbow", 2, 20),
}


def inventory_score(items, base):
    score = sum(ITEMS[i][2] for i in items)
    penalty = sum(ITEMS[i][2] for i in ITEMS if i not in items)
    return base + score - penalty


def inventory_size(items):
    return sum(ITEMS[i][1] for i in items)


def all_positive_combos(capacity, base):
    valid = []
    keys = list(ITEMS.keys())
    for r in range(1, len(keys) + 1):
        for combo in combinations(keys, r):
            if inventory_size(combo) <= capacity:
                score = inventory_score(combo, base)
                if score > 0:
                    valid.append((combo, score))
    return valid


def best_combo(capacity, base):
    combos = all_positive_combos(capacity, base)
    return max(combos, key=lambda x: x[1], default=None)


def render_inventory(items, rows=3, cols=3):
    grid = [[" "] * cols for _ in range(rows)]
    for item in items:
        size = ITEMS[item][1]
        placed = False
        for r in range(rows):
            for c in range(cols):
                if c + size <= cols and all(grid[r][c + k] == " " for k in range(size)):
                    for k in range(size):
                        grid[r][c + k] = item
                    placed = True
                    break
                if size == 2 and r + 1 < rows and grid[r][c] == " " and grid[r + 1][c] == " ":
                    grid[r][c] = item
                    grid[r + 1][c] = item
                    placed = True
                    break
            if placed:
                break
        if not placed:
            return None
    return [",".join(f"[{x}]" for x in row) for row in grid]


if __name__ == "__main__":
    base_score = 10
    print("=== Вариант 10 ===")
    print("\n--- 9 ячеек (3x3) ---")
    pos_9 = all_positive_combos(9, base_score)
    print(f"Всего положительных комбинаций: {len(pos_9)}")
    best_9 = best_combo(9, base_score)
    if best_9:
        items, score = best_9
        print("Лучший набор:", items)
        print("Очки:", score)
        grid = render_inventory(items)
        if grid:
            for row in grid:
                print(row)
        else:
            print("Набор не помещается в инвентарь 3x3.")

    print("\n--- 7 ячеек (3x3 с 2 пустыми) ---")
    pos_7 = all_positive_combos(7, base_score)
    print(f"Всего положительных комбинаций: {len(pos_7)}")
    best_7 = best_combo(7, base_score)
    if best_7:
        items, score = best_7
        print("Лучший набор:", items)
        print("Очки:", score)
    else:
        print("Для рюкзака из 7 ячеек все варианты дают отрицательный итог.")
