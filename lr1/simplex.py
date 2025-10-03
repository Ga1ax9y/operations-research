import numpy as np

def find_inverse(A_inv, column, index):
    n = A_inv.shape[0]
    l = A_inv.dot(column)
    l_index = l[index]

    if abs(l_index) < 1e-10:
        return None

    l[index] = -1
    l_new = (-1 / l_index) * l

    A_result_inv = np.zeros((n, n))
    for i in range(n):
        for k in range(n):
            if i == index:
                A_result_inv[i, k] = l_new[i] * A_inv[i, k]
            else:
                A_result_inv[i, k] = A_inv[i, k] + l_new[i] * A_inv[index, k]

    return A_result_inv

class Simplex:
    def __init__(self, code, error_message=None, result=None, B_set=None):
        self.code = code
        self.error_message = error_message
        self.result = result
        self.B_set = B_set

def simplex_solve(c, A, b):
    m, n = A.shape
    b = b.astype(float)
    A = A.astype(float)


    for i in range(m):
        if b[i] < 0:
            b[i] *= -1
            A[i, :] *= -1

    c_wave = np.zeros(n + m)
    c_wave[n:] = -1

    A_wave = np.hstack((A, np.eye(m)))
    x_wave = np.zeros(n + m)
    x_wave[n:] = b

    B_wave = list(range(n, n + m))

    result_phase1 = _simplex_internal(c_wave, A_wave, x_wave, B_wave)

    if result_phase1.code != 0:
        return Simplex(result_phase1.code, "Первая фаза не удалась: " + (result_phase1.error_message or ""))

    artificial_vars = result_phase1.result[n:]
    if not np.allclose(artificial_vars, 0, atol=1e-8):
        return Simplex(3, "Задача несовместна — нет допустимых планов")

    x_original = result_phase1.result[:n]
    B_original = list(result_phase1.B_set)

    while True:
        artificial_in_B = [j for j in B_original if j >= n]
        if not artificial_in_B:
            break

        j_k = max(artificial_in_B)
        k = B_original.index(j_k)
        i_row = j_k - n

        A_B = A_wave[:, B_original]
        try:
            A_B_inv = np.linalg.inv(A_B)
        except np.linalg.LinAlgError:
            return Simplex(2, "Вырожденная матрица при удалении искусственной переменной")

        non_basis = [j for j in range(n) if j not in B_original]
        found = False
        for j in non_basis:
            A_j = A_wave[:, j]
            l_j = A_B_inv @ A_j
            if abs(l_j[k]) > 1e-8:
                B_original[k] = j
                found = True
                break

        if not found:
            A = np.delete(A, i_row, axis=0)
            b = np.delete(b, i_row)
            A_wave = np.delete(A_wave, i_row, axis=0)
            B_original.remove(j_k)
            m -= 1
            if m == 0:
                break

    if any(j >= n for j in B_original):
        return Simplex(5, "Не удалось исключить все искусственные переменные из базиса")


    return _simplex_internal(c, A, x_original, B_original)


def _simplex_internal(c, A, x_init, B_init):
    m, n = A.shape
    x = x_init.copy()
    B = B_init.copy()

    A_B_inv_prev = None

    iteration = 0
    while True:
        iteration += 1
        # Шаг 1: Обратная базисная матрица
        if A_B_inv_prev is None:
            A_B = A[:, B]
            try:
                A_B_inv = np.linalg.inv(A_B)
                A_B_inv_prev = A_B_inv
            except np.linalg.LinAlgError:
                return Simplex(2, "Базисная матрица вырождена")
        else:
            try:
                A_B = A[:, B]
                A_B_inv = np.linalg.inv(A_B)
                A_B_inv_prev = A_B_inv
            except np.linalg.LinAlgError:
                return Simplex(2, "Не удалось вычислить обратную базисную матрицу")

        # Шаг 2-3: Потенциалы
        c_B = c[B]
        u = c_B @ A_B_inv

        # Шаг 4: Оценки
        delta = u @ A - c

        # Шаг 5: Проверка оптимальности
        if np.all(delta >= -1e-8):
            return Simplex(0, None, x, B)

        # Шаг 6: Вводим в базис первую с отрицательной оценкой
        j_0_candidates = np.where(delta < -1e-8)[0]
        if len(j_0_candidates) == 0:
            return Simplex(0, None, x, B)  # на всякий случай
        j_0 = j_0_candidates[0]

        # Шаг 7: Направляющий вектор
        z = A_B_inv @ A[:, j_0]

        # Шаг 8-9: Вычисление тета
        theta = np.full(m, np.inf)
        for i in range(m):
            if z[i] > 1e-8:
                theta[i] = x[B[i]] / z[i]

        theta_0 = np.min(theta)

        # Шаг 10: Проверка неограниченности
        if theta_0 == np.inf:
            return Simplex(1, None, "Целевая функция не ограничена сверху")

        # Шаг 11: Выводим переменную из базиса
        k = np.argmin(theta)
        j_star = B[k]

        # Шаг 12-13: Обновляем базис и план
        B[k] = j_0
        x_new = x.copy()
        x_new[j_0] = theta_0
        for i in range(m):
            if i != k:
                x_new[B[i]] = x[B[i]] - theta_0 * z[i]
        x_new[j_star] = 0
        x = x_new

        A_B_inv_prev = find_inverse(A_B_inv_prev, A[:, j_star], k)
        if A_B_inv_prev is None:
            return Simplex(2, "Не удалось обновить обратную матрицу — возможно, вырожденный базис")


if __name__ == "__main__":
    print("🧪 Тест 1: Совместная задача")
    c = np.array([0, 1, 0, 0])
    A = np.array([
        [3, 2, 1, 0],
        [-3, 2, 0, 1],
    ])
    b = np.array([6, 0])

    result = simplex_solve(c, A, b)

    if result.code == 0:
        print("✅ Оптимальный план:", result.result)
        print("📌 Базис:", result.B_set)
    else:
        print("❌ Ошибка:", result.error_message)

    print("\n" + "="*50 + "\n")

    print("🧪 Тест 2: Несовместная система")
    c = np.array([1, 0, 0])
    A = np.array([[1, 1, 1], [2, 2, 2]])
    b = np.array([0, -13])

    result2 = simplex_solve(c, A, b)

    if result2.code == 0:
        print("✅ Оптимальный план:", result2.result)
        print("📌 Базис:", result2.B_set)
    else:
        print("❌ Ошибка:", result2.error_message)
