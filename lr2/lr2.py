def resource_task(P, Q, A):
    B = [[0] * (Q + 1) for _ in range(P)]
    C = [[0] * (Q + 1) for _ in range(P)]

    print("Матрица прибыли A:")
    print("   " + " ".join(f"{j:3d}" for j in range(Q + 1)))
    for i in range(P):
        print(f"{i+1}: " + " ".join(f"{A[i][j]:3d}" for j in range(Q + 1)))
    print()

    print("Заполнение матриц B и C:")
    for p in range(P):
        for q in range(Q + 1):
            if p == 0:
                B[p][q] = A[p][q]
                C[p][q] = q
            else:
                max_profit = -1
                best_i = 0
                for i in range(q + 1):
                    profit = A[p][i] + B[p-1][q-i]
                    if profit > max_profit:
                        max_profit = profit
                        best_i = i
                B[p][q] = max_profit
                C[p][q] = best_i

        print(f"\nПосле агента {p+1}:")
        print("Матрица B:")
        print("   " + " ".join(f"{j:3d}" for j in range(Q + 1)))
        for i in range(p + 1):
            print(f"{i+1}: " + " ".join(f"{B[i][j]:3d}" for j in range(Q + 1)))

        print("\nМатрица C:")
        print("   " + " ".join(f"{j:3d}" for j in range(Q + 1)))
        for i in range(p + 1):
            print(f"{i+1}: " + " ".join(f"{C[i][j]:3d}" for j in range(Q + 1)))

    print("\n" + "="*50)
    print("Обратный ход:")
    print("="*50)

    distribution = [0] * P
    q_remaining = Q
    path = []

    for p in range(P-1, -1, -1):
        optimal_resource = C[p][q_remaining]
        distribution[p] = optimal_resource
        path.append((p, q_remaining, optimal_resource))
        print(f"Агент {p+1}: C[{p+1}][{q_remaining}] = {optimal_resource}")
        q_remaining -= optimal_resource

    print("\n" + "="*50)
    print("Финальные матрицы:")
    print("="*50)

    print("\nМатрица B:")
    print("   " + " ".join(f"{j:3d}" for j in range(Q + 1)))
    for i in range(P):
        print(f"{i+1}: " + " ".join(f"{B[i][j]:3d}" for j in range(Q + 1)))

    print("\nМатрица C:")
    print("   " + " ".join(f"{j:3d}" for j in range(Q + 1)))

    COLOR_RED = '\033[91m'
    COLOR_END = '\033[0m'

    for i in range(P):
        row = ""
        for j in range(Q + 1):
            cell_value = f"{C[i][j]:3d}"
            if any(x[0] == i and x[1] == j for x in path):
                row += f"{COLOR_RED}{cell_value}{COLOR_END} "
            else:
                row += f"{cell_value} "
        print(f"{i+1}: {row}")

    print("\n" + "="*50)
    print("Оптимальное решение:")
    print("="*50)

    solution_parts = [f"x{i+1}={distribution[i]}" for i in range(P)]
    solution_str = "(" + ", ".join(solution_parts) + ")"

    print(f"Максимальная прибыль: {B[P-1][Q]}, распределение: {solution_str}")

    return B[P-1][Q], distribution

if __name__ == "__main__":
    P = 3
    Q = 3
    A = [
        [0, 1, 2, 3],
        [0, 0, 1, 2],
        [0, 2, 2, 3]
    ]

    max_profit, distribution = resource_task(P, Q, A)
