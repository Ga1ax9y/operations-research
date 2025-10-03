import numpy as np
from simplex import simplex_solve, Simplex

class GomoryResult:
    def __init__(self, status, plan=None, cut=None, cut_vars=None, cut_rhs=None, message=None):
        self.status = status
        self.plan = plan
        self.cut = cut
        self.cut_vars = cut_vars
        self.cut_rhs = cut_rhs
        self.message = message

def gomory_generation(c, A, b):
    # Шаг 1
    result = simplex_solve(c, A, b)

    # Шаг 2: Проверка на несовместность или неограниченность
    if result.code != 0:
        return GomoryResult(
            status="error",
            message="Задача несовместна или целевая функция не ограничена сверху на множестве допустимых планов"
        )

    x_opt = result.result
    B = result.B_set

    # Шаг 3: Проверка целочисленности
    fractional_indices = []
    for i, val in enumerate(x_opt):
        if not np.isclose(val, round(val), atol=1e-8):
            if i in B:
                fractional_indices.append(i)

    if len(fractional_indices) == 0:
        return GomoryResult(
            status="optimal",
            plan=x_opt,
            message="Найден оптимальный целочисленный план"
        )

    # Шаг 4-5: Выбираем первую дробную базисную компоненту
    i_frac = fractional_indices[0]
    k = B.index(i_frac)

    # Шаг 6: Разбиваем переменные на базисные и небазисные
    all_vars = set(range(len(c)))
    B_set = set(B)
    N = sorted(list(all_vars - B_set))

    A_B = A[:, B]
    A_N = A[:, N]

    # Шаг 8: Находим A_B^{-1}
    try:
        A_B_inv = np.linalg.inv(A_B)
    except np.linalg.LinAlgError:
        return GomoryResult(
            status="error",
            message="Вырожденная базисная матрица при построении отсечения"
        )

    # Шаг 9: Q = A_B^{-1} @ A_N
    Q = A_B_inv @ A_N

    # Шаг 10: Берём k-ую строку матрицы Q
    l_row = Q[k, :]

    # Шаг 11: Строим отсекающее ограничение: sum_p {l_p} * (x_N)_p - s = {x_i}
    # где {α} = α - floor(α) — дробная часть
    cut_coeffs = []
    cut_vars_list = []

    for p, coeff in enumerate(l_row):
        frac_part = coeff - np.floor(coeff)
        if not np.isclose(frac_part, 0, atol=1e-8):
            cut_coeffs.append(frac_part)
            cut_vars_list.append(N[p])

    x_i_val = x_opt[i_frac]
    cut_rhs = x_i_val - np.floor(x_i_val)

    return GomoryResult(
        status="cut_generated",
        cut=cut_coeffs,
        cut_vars=cut_vars_list,
        cut_rhs=cut_rhs,
        message=f"Отсекающее ограничение Гомори"
    )

if __name__ == "__main__":
    c = np.array([0, 1, 0, 0])
    A = np.array([
        [3, 2, 1, 0],
        [-3, 2, 0, 1],
    ])
    b = np.array([6, 0])

    result = gomory_generation(c, A, b)

    if result.status == "optimal":
        print("Оптимальный целочисленный план:", result.plan)
    elif result.status == "cut_generated":
        print("Отсекающее отсечение Гомори:")
        print("   Переменные:", result.cut_vars)
        print("   Коэффициенты:", result.cut)
        print("   Правая часть: {x_i} =", result.cut_rhs)
        print("   Ограничение: ", end="")
        terms = [f"{coeff:.4f}*x_{var}" for coeff, var in zip(result.cut, result.cut_vars)]
        print(" + ".join(terms) + " - s = " + f"{result.cut_rhs:.4f}")

        full_coeffs = [0.0] * (len(c) + 1)
        for var_idx, coeff in zip(result.cut_vars, result.cut):
            full_coeffs[var_idx] = coeff
        full_coeffs[-1] = -1.0
        output_list = full_coeffs + [result.cut_rhs]
        print("   Результат в виде списка:", [round(x, 4) for x in output_list])
    else:
        print("Ошибка:", result.message)
