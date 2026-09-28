"""
Лабораторная работа № 2. Вариант 14.
n = 400, 800, 1200, 1600, 2000; тип V (обратно упорядоченные);
диапазон [-100; 100]; повторов k = 7. Доп. задание М6.
Сравнение сортировки пузырьком (с флагом), сортировки вставками (классической)
и сортировки вставками с бинарным поиском позиции вставки.
"""
from sorts_common import generate_data, measure


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr):
    """Классическая сортировка вставками."""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def insertion_sort_binary(arr):
    """М6: сортировка вставками с бинарным поиском позиции вставки (без bisect)."""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        lo, hi = 0, i
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] <= key:
                lo = mid + 1
            else:
                hi = mid
        j = i - 1
        while j >= lo:
            a[j + 1] = a[j]
            j -= 1
        a[lo] = key
    return a


# --- версии со счётчиком сравнений (для доп. задания М6) ---

def insertion_sort_counted(arr):
    a = arr.copy()
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons


def insertion_sort_binary_counted(arr):
    a = arr.copy()
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        lo, hi = 0, i
        while lo < hi:
            mid = (lo + hi) // 2
            comparisons += 1
            if a[mid] <= key:
                lo = mid + 1
            else:
                hi = mid
        j = i - 1
        while j >= lo:
            a[j + 1] = a[j]
            j -= 1
        a[lo] = key
    return a, comparisons


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    SIZES = [400, 800, 1200, 1600, 2000]
    REPEATS = 7
    algorithms = {
        "Пузырьком": bubble_sort,
        "Вставками (классич.)": insertion_sort,
        "Вставками (бинарный поиск)": insertion_sort_binary,
    }
    results = {name: [] for name in algorithms}

    print(f"{'n':>6}" + "".join(f"{name:>28}" for name in algorithms))
    for n in SIZES:
        data = generate_data(n, kind="reversed", lo=-100, hi=100)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            results[name].append(t)
            row += f"{t:>28.5f}"
        print(row)

    for name, times in results.items():
        plt.plot(SIZES, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("Зависимость времени сортировки от n (вариант 14, тип V)")
    plt.grid(True)
    plt.legend()
    plt.savefig("lr2_plot.png", dpi=150)
    plt.show()