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


def evaluate(item_list):
    size = sum(ITEMS[i][1] for i in item_list)
    score = sum(ITEMS[i][2] for i in item_list)
    return size, score


def dp_best(capacity, base_score):
    dp = {0: (base_score, [])}
    for key in ITEMS:
        _, size, score = ITEMS[key]
        new_dp = dict(dp)
        for used, (cur_score, taken) in dp.items():
            new_used = used + size
            if new_used <= capacity:
                new_score = cur_score + score
                if new_used not in new_dp or new_dp[new_used][0] < new_score:
                    new_dp[new_used] = (new_score, taken + [key])
        dp = new_dp
    best_score = None
    best_items = None
    for _, (score, taken) in dp.items():
        if score > 0 and (best_score is None or score > best_score):
            best_score = score
            best_items = taken
    return best_score, best_items


def brute_all_positive(capacity, base_score):
    keys = list(ITEMS.keys())
    valid = []
    for r in range(1, len(keys) + 1):
        for combo in combinations(keys, r):
            size, score = evaluate(combo)
            score += base_score
            if size <= capacity and score > 0:
                valid.append((size, score, combo))
    return valid


best9_score, best9_items = dp_best(9, 10)
print("ЛУЧШИЙ НАБОР ДЛЯ 9 ЯЧЕЕК")
print("Очки:", best9_score)
print("Предметы:", best9_items)

best7_score, best7_items = dp_best(7, 10)
print("\nЛУЧШИЙ НАБОР ДЛЯ 7 ЯЧЕЕК")
print("Очки:", best7_score)
print("Предметы:", best7_items)

all9 = brute_all_positive(9, 10)
print("\nВСЕ ПОЛОЖИТЕЛЬНЫЕ КОМБИНАЦИИ ДЛЯ 9 ЯЧЕЕК")
print("Найдено:", len(all9))