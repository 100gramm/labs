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

TOTAL_ALL = sum(item[2] for item in ITEMS.values())


def inventory_score(selected, base_score):
    selected_set = set(selected)
    missing_set = set(ITEMS.keys()) - selected_set
    positive = sum(ITEMS[i][2] for i in selected_set)
    negative = sum(ITEMS[i][2] for i in missing_set)
    return base_score + positive - negative


def inventory_size(selected):
    return sum(ITEMS[i][1] for i in selected)


def all_positive_combinations(capacity, base_score):
    valid = []
    keys = list(ITEMS.keys())
    for r in range(1, len(keys) + 1):
        for combo in combinations(keys, r):
            if inventory_size(combo) <= capacity:
                score = inventory_score(combo, base_score)
                if score > 0:
                    valid.append((combo, score))
    return valid


def best_combination(capacity, base_score):
    all_valid = all_positive_combinations(capacity, base_score)
    if not all_valid:
        return None
    return max(all_valid, key=lambda x: x[1])


def render_inventory(items, rows, cols):
    flat_items = []
    for item in items:
        flat_items.extend([item] * ITEMS[item][1])
    grid = []
    for r in range(rows):
        row_items = flat_items[r*cols:(r+1)*cols]
        row_str = ",".join(f"[{i}]" for i in row_items)
        grid.append(row_str)
    return grid


if __name__ == "__main__":
    BASE_SCORE = 10
    CAPACITY_9 = 9
    CAPACITY_7 = 7

    best_9 = best_combination(CAPACITY_9, BASE_SCORE)
    if best_9:
        items, score = best_9
        print("Лучший набор для 9 ячеек:")
        print("Очки:", score)
        print("Предметы:", items)
        grid = render_inventory(list(items), 3, 3)
        for row in grid:
            print(row)

    best_7 = best_combination(CAPACITY_7, BASE_SCORE)
    if best_7:
        items, score = best_7
        print("\nЛучший набор для 7 ячеек:")
        print("Очки:", score)
        print("Предметы:", items)
        grid = render_inventory(list(items), 2, 4)
        for row in grid:
            print(row)
    else:
        print("\nДля рюкзака из 7 ячеек все варианты дают отрицательный итог.")
