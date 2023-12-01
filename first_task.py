def sequence(n):
    result = ""
    sum_result = 0
    # Если , число n не учитывается в последовательности, то for i in range(1, n + 1):
    for i in range(1, n + 1):
        result += str(i) * i
        sum_result += i * i
    return result, sum_result


def main():
    n = int(input("Введите количество элементов (n): "))
    result_sequence = sequence(n)
    print(f"Первые {n} элементов последовательности: {result_sequence[0]}")
    print(f"Сумма первых {n} элементов последовательности: {result_sequence[1]}")


if __name__ == "__main__":
    main()
