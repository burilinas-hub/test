# a: int = 3167940560363555651584
# b: int = 3
# result = a * b
# print(int(result))

# Запрашиваем число у пользователя
decimal_number = int(input("Введите число в десятичной системе: "))
# Переводим число из dec в hex
hex_number = hex(decimal_number)
print(f"Число {decimal_number} в шестнадцатеричной системе: {hex_number}")
print(id(decimal_number))

# Запрашиваем у пользователя ввод hex-числа
hex_number = input("Введите число в шестнадцатеричной системе: ")
# Переводим из hex в decimal с помощью функции int
decimal_number = int(hex_number, 16)
print(f"Число {hex_number} в десятичной системе: {decimal_number}")
print(id(hex_number))
