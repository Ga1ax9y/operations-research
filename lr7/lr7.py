from collections import deque
import math
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from lr6.lr6 import find_max

RED = "\033[91m"
RESET = "\033[0m"


def hungary(C):
    n = len(C)
    V1 = [f"u{i+1}" for i in range(n)]
    V2 = [f"v{i+1}" for i in range(n)]

    alpha = [0]*n
    beta = [min(C[i][j] for i in range(n)) for j in range(n)]

    iteration = 1

    while True:
        J_eq = []
        for i in range(n):
            for j in range(n):
                if abs((alpha[i] + beta[j]) - C[i][j]) < 1e-9:
                    J_eq.append((i, j))

        transitions = [(f"u{i+1}", f"v{j+1}") for i, j in J_eq]
        print(J_eq)
        M, G_star = find_max(V1, V2, transitions)
        #print(V1, V2, transitions, sep="\n")
        print(f"\nИтерация {iteration}")
        print("Паросочетание M:", M)

        if len(M) == n:
            chosen = []
            for u, v in M:
                    i = int(u[1:]) - 1
                    j = int(v[1:]) - 1
                    chosen.append((i, j))
            chosen_dict = {}
            for i, j in chosen:
                chosen_dict[i] = j

            final_pairs = []
            for i in range(n):
                if i in chosen_dict:
                    final_pairs.append((i, chosen_dict[i]))
                else:
                    final_pairs.append((i, None))

            print("Матрица C:\n")
            max_width = max(len(str(x)) for row in C for x in row) + 1
            for i in range(n):
                row_str = ""
                for j in range(n):
                    val = C[i][j]
                    if final_pairs[i][1] == j:
                        cell = f"{RED}{str(val).rjust(max_width)}{RESET}"
                    else:
                        cell = str(val).rjust(max_width)
                    row_str += cell
                print(row_str)

            total = 0
            chosen_positions = []
            for i, j in final_pairs:
                if j is not None:
                    total += C[i][j]
                    chosen_positions.append((i, j))

            print(f"\nСумма выбранных элементов = {total}")
            return chosen_positions

        reachable = set()
        queue = deque(["s"])
        reachable.add("s")

        while queue:
            u = queue.popleft()
            for v in G_star.get(u, []):
                if v not in reachable:
                    reachable.add(v)
                    queue.append(v)

        I_star = []
        J_star = []

        for i, u in enumerate(V1):
            if u in reachable:
                I_star.append(i)

        for j, v in enumerate(V2):
            if v in reachable:
                J_star.append(j)

        print("I* =", [i+1 for i in I_star])
        print("J* =", [j+1 for j in J_star])

        alpha2 = [1 if i in I_star else -1 for i in range(n)]
        beta2 = [-1 if j in J_star else 1 for j in range(n)]

        tetta = math.inf
        for i in I_star:
            for j in range(n):
                if j not in J_star:
                    tetta = min(tetta, (C[i][j] - alpha[i] - beta[j]) / 2)

        print("θ =", tetta)

        for i in range(n):
            alpha[i] += tetta * alpha2[i]
        for j in range(n):
            beta[j] += tetta * beta2[j]

        iteration += 1


if __name__ == "__main__":
    C = [
        [7, 2, 1, 9, 4],
        [9, 6, 9, 5, 5],
        [3, 8, 3, 1, 8],
        [7, 9, 4, 2, 2],
        [8, 4, 7, 4, 8]
    ]

    result = hungary(C)
    print("\nРезультат:", result)
