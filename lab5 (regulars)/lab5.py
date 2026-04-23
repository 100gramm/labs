import re
import csv


def task1():
    print("\n=== ЗАДАНИЕ 1 ===")
    with open("task1-en.txt", "r", encoding="utf-8") as f:
        text = f.read()

    words_with_dot = re.findall(r"\b([A-Za-zА-Яа-яЁё]+)\.", text)
    fractional_numbers = re.findall(r"\b\d+\.\d+\b", text)

    print("\nСлова, после которых стоит точка:")
    print(words_with_dot)
    print("\nДробные числа:")
    print(fractional_numbers)


def task2():
    print("\n=== ЗАДАНИЕ 2 ===")
    with open("task2.html", "r", encoding="utf-8") as f:
        html = f.read()

    px_values = re.findall(r"\b\d+px\b", html)

    print("\nЗначения в пикселях:")
    print(px_values)


def task3():
    print("\n=== ЗАДАНИЕ 3 ===")
    with open("task3.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    ids = re.findall(r"(?:^|\s)(\d{1,3})(?:\s|$)", text)
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text
    )
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    sites = re.findall(r"https?://[^\s]+", text)
    surnames = re.findall(
        r"\b(?!https?://)(?!\d{4}-\d{2}-\d{2})[A-Z][a-zA-Z]+\b", text
    )

    n = min(len(ids), len(surnames), len(emails), len(dates), len(sites))

    table = []
    for i in range(n):
        table.append([ids[i], surnames[i], emails[i], dates[i], sites[i]])

    with open("result_task3.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["ID", "Surname", "Email", "Date", "Site"])
        writer.writerows(table)

    print(f"CSV сохранён как result_task3.csv, найдено пользователей: {len(table)}")


def task_add():
    print("\n=== ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ===")
    with open("task_add.txt", "r", encoding="utf-8") as f:
        t = f.read()

    dates = re.findall(r"\s(\d{1,4}[./-]\d{1,2}[./-]\d{1,4})", t)
    emails = re.findall(r"\s([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2})", t)
    sites = re.findall(r"\s(https?://[A-Za-z0-9.-]+(?:\.[A-Za-z]{2,3}))", t)

    print("\nДаты:", dates)
    print("Email:", emails)
    print("Сайты:", sites)


if __name__ == "__main__":
    task1()
    task2()
    task3()
    task_add()
