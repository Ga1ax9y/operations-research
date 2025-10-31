def backpack(v, c, B):
    n = len(v)
    OPT = [[0] * (B + 1) for _ in range(n + 1)]
    X = [[0] * (B + 1) for _ in range(n + 1)]

    for k in range(1, n + 1):
        for b in range(B + 1):
            if k == 1:
                if v[0] <= b:
                    OPT[k][b] = c[0]
                    X[k][b] = 1
                else:
                    OPT[k][b] = 0
                    X[k][b] = 0
            else:
                if v[k-1] <= b:
                    not_take = OPT[k-1][b]
                    take = OPT[k-1][b - v[k-1]] + c[k-1]

                    if take > not_take:
                        OPT[k][b] = take
                        X[k][b] = 1
                    else:
                        OPT[k][b] = not_take
                        X[k][b] = 0
                else:
                    OPT[k][b] = OPT[k-1][b]
                    X[k][b] = 0

    print("Восстановление выбранных предметов:")
    selected = []
    current_b = B
    for k in range(n, 0, -1):
        if X[k][current_b] == 1:
            selected.append(k)
            print(f"Выбран предмет {k}", end=", ")
            current_b -= v[k-1]
            print(f"Объем стал {current_b}")
        else:
            print(f"Предмет {k} не выбран")

    selected.reverse()
    print()
    return OPT, X, selected

if __name__ == "__main__":
    v = [1, 2, 3, 3]
    c = [2, 2, 1, 2]
    B = 6

    OPT, X, selected = backpack(v, c, B)

    print("Матрица OPT:")
    for i in range(1, len(OPT)):
        print(OPT[i])

    print("\nМатрица X:")
    for i in range(1, len(X)):
        print(X[i])

    print("\nВыбранные предметы:", selected)

    total_value = 0
    total_volume = 0
    for item in selected:
        total_value += c[item-1]
        total_volume += v[item-1]

    print(f"Суммарная ценность = {total_value}")
    print(f"Суммарный объем = {total_volume}")
    print(f"Вместимость рюкзака = {B}")
