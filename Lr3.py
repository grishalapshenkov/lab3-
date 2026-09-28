"""
Лабораторная работа № 3. Вариант 14.
Быстрая сортировка (опорный — последний элемент, разбиение Ломуто) и
нисходящая сортировка слиянием. Доп. задание Г2 — подсчёт сравнений.
"""
import math
from sorts_common import generate_data, measure
from lr2_main import bubble_sort, insertion_sort


# ---------- Быстрая сортировка (Ломуто, опорный — последний) ----------
def quick_sort(arr):
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1)
    return a


def _quick_sort(a, lo, hi):
    while lo < hi:
        p = _partition(a, lo, hi)
        # рекурсия в меньшую часть — глубина стека O(log n)
        if p - lo < hi - p:
            _quick_sort(a, lo, p - 1)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi)
            hi = p - 1


def _partition(a, lo, hi):
    """Разбиение Ломуто, опорный элемент — последний."""
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


# ---------- Сортировка слиянием (нисходящая) ----------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    return _merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # «<=» обеспечивает устойчивость
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- Версии со счётчиком сравнений (Г2) ----------
def quick_sort_counted(arr):
    a = arr.copy()
    cnt = [0]

    def part(lo, hi):
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            cnt[0] += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        return i + 1

    def qs(lo, hi):
        while lo < hi:
            p = part(lo, hi)
            if p - lo < hi - p:
                qs(lo, p - 1)
                lo = p + 1
            else:
                qs(p + 1, hi)
                hi = p - 1

    qs(0, len(a) - 1)
    return a, cnt[0]


def merge_sort_counted(arr):
    cnt = [0]

    def ms(x):
        if len(x) <= 1:
            return x.copy()
        mid = len(x) // 2
        left, right = ms(x[:mid]), ms(x[mid:])
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            cnt[0] += 1
            if left[i] <= right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:]); res.extend(right[j:])
        return res

    return ms(arr), cnt[0]


# ---------- Эксперименты ----------
def run_experiment(algorithms, sizes, kind="random", repeats=7, lo=0, hi=100_000):
    results = {name: [] for name in algorithms}
    print(f"{'n':>8}" + "".join(f"{name:>12}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind=kind, lo=lo, hi=hi)
        row = f"{n:>8}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>12.4f}"
        print(row)
    return results


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Эксперимент 1: размеры из варианта ЛР № 2
    small = [400, 800, 1200, 1600, 2000]
    algs1 = {"Пузырьком": bubble_sort, "Вставками": insertion_sort,
             "Быстрая": quick_sort, "Слиянием": merge_sort}
    res1a = run_experiment(algs1, small, "random", 7, -100, 100)
    res1b = run_experiment(algs1, small, "reversed", 7, -100, 100)

    # Эксперимент 2: O(n log n) на больших размерах (вариант 14)
    large = [50_000, 75_000, 100_000, 125_000]
    res2 = run_experiment({"Быстрая": quick_sort, "Слиянием": merge_sort,
                           "sorted()": sorted}, large, "random", 7, 0, 100_000)

    # Эксперимент 3: влияние структуры данных (n = 3000 из-за опорного «последний»)
    print("\nЭксперимент 3, n = 3000")
    for label, kind, lo, hi in [("R", "random", 0, 100_000), ("S", "sorted", 0, 100_000),
                                ("V", "reversed", 0, 100_000),
                                ("N", "nearly_sorted", 0, 100_000), ("D", "random", 0, 10)]:
        data = generate_data(3000, kind=kind, lo=lo, hi=hi)
        print(f"{label:>3}: быстрая {measure(quick_sort, data, 7):.4f} с, "
              f"слиянием {measure(merge_sort, data, 7):.4f} с")

    # Г2: число сравнений
    print("\nГ2: число сравнений (случайные данные)")
    for n in large:
        data = generate_data(n, "random", 0, 100_000)
        _, cq = quick_sort_counted(data)
        _, cm = merge_sort_counted(data)
        nl = n * math.log2(n)
        print(f"{n:>8} {cq:>10} {cm:>10} {nl:>10.0f} {cq / nl:>6.2f} {cm / nl:>6.2f}")

    # Графики
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for name, t in res1a.items():
        axes[0].plot(small, t, marker="o", label=name)
    axes[0].set_yscale("log")
    axes[0].set_title("Эксперимент 1а (лог. шкала времени)")
    for name, t in res2.items():
        axes[1].plot(large, t, marker="o", label=name)
    axes[1].set_title("Эксперимент 2")
    for ax in axes:
        ax.set_xlabel("Размер массива n")
        ax.set_ylabel("Время, с")
        ax.grid(True)
        ax.legend()
    plt.tight_layout()
    plt.savefig("lr3_plot.png", dpi=150)
    plt.show()
