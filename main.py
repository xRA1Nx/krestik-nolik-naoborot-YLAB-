"""
Противник ходит по принципу рандома из множествасвободных ходов
Это реализовано через tuple - free_turns, с помощью pop()
сокращаем рандомно множество и имеем скорость О(1)
____________________________________________________

с помощью модуль test.py можно произвести тестирование, полностью рандомной генерации поля
"""

# создаем поле
from typing import Tuple


def create_pole(s: int) -> Tuple[list, set]:
    # Создаем начальное поле
    matrix = [[chr(96 + j) if i == 0 else (str(i) if j == 0 else "_") for j in range(s + 1)] for i in range(s + 1)]
    matrix[0][0] = ""
    # создаем начальный список свободных ходов
    free_turns = set(i + j for i in map(str, range(1, s + 1)) for j in map(str, range(1, s + 1)))
    return matrix, free_turns


# формируем список из возможных диаганалей, строк, столбцов, для дальнейшей проверки окончания игры
def make_items_for_check(pole: list) -> Tuple[set, set, set, set]:
    column = diagm = diagr = ""
    diags_main = set()  # основная диаганаль
    diags_reverse = set()  # побочная диаганаль
    raws = set()
    columns = set()
    # формируем списки строк, столбцов
    for i in range(1, len(pole)):
        raw = "".join(pole[i][1:])
        for j in range(1, len(pole)):
            column += pole[j][i]
        columns.add(column)
        raws.add(raw)
        column = ""
    # формируем списки основных и побочных диаганалей
    for step in range(len(pole) - 5):  # игнорируем диаганали размером меньше 5
        for i in range(len(pole) - 5):
            for j in range(1, 6):  # формируем диаганаль длиной 5
                diagr += pole[len(pole) - j - i][j + step]
                diagm += pole[j + i][j + step]
            diags_main.add(diagm)
            diags_reverse.add(diagr)
            diagm = diagr = ""
    return raws, columns, diags_main, diags_reverse

# Проверка результата игры
def check_game(pole: list, turns: set, pl_item: str, ii_item: str) -> bool:
    flag_end = False
    grats = "\nПоздравляем, Вы победили!!!\n"
    shame = "\nВы проиграли :(\n"
    wtf = "\nНичья...\n"
    gg = ii_item * 5
    bg = pl_item * 5
    # формируем строки, столбцы, диаганали
    raws, columns, diags_main, diags_reverse = make_items_for_check(pole)
    all_items = raws | columns | diags_main | diags_reverse
    for target in all_items:
        # проверка выигрыша
        if gg in target:
            print(grats)
            flag_end = True
            break
        # проверка проигрыш
        if bg in target:
            print(shame)
            flag_end = True
            break
        # проверка ничья
    if len(turns) == 0 and not flag_end:
        print(wtf)
        flag_end = True
    return flag_end


# Отображение игрового поля
def show_game(pole: list) -> None:
    print()
    for raw in pole:
        raw = list(map(lambda x: x.ljust(2), raw))
        print(*raw)


# Ход комьютера
def ii_turn(pole: list, free_turns: set, ii_item: str, d: dict) -> str:
    turn = free_turns.pop()
    if turn.startswith("10"):
        x = 10
        y = int(turn[2:])
        print(f"\nход противника: {d['10']}{turn[0]}")
    else:
        x = int(turn[0])
        y = int(turn[1:])
        print(f"\nход противника: {d[turn[1:]]}{turn[0]}")
    pole[x][y] = ii_item
    show_game(pole)
    return turn


# Ход игрока
def player_turn(pole: list, pl_item: str) -> str:
    # словарь для преобразования введеного игроком хода в индексы игрового поля
    d_columns = {chr(96 + i): i for i in range(1, len(pole))}
    d = d_columns.copy()
    d_raws = {str(i): i for i in range(1, len(pole))}
    d.update(d_raws)
    turn = ""

    flag = False
    while not flag:
        turn = input("\nваш ход: ").lower()
        # проверка на длину вводимых данных
        if len(turn) < 2 or len(turn) > 3:
            print("\nход введен не корректно. Формат вводимых данных: 'A1'")
            continue
        # если ход начинается с цифры то меняем символы местами, приводим к формату A1
        if turn[0].isdigit():
            turn = turn[-1] + turn[:-1]
        column = turn[0]
        raw = turn[1:]

        # проверка попадает ли введеный ход на поле
        if column in d_columns.keys() and raw in d_raws.keys():
            turn = str(d[turn[1:]]) + str(d[turn[0]])
            # проверка свободно ли место на поле
            if pole[d[raw]][d[column]] != "_":
                print("\nсюда уже ходили")
            else:
                pole[d[raw]][d[column]] = pl_item
                flag = True
        else:
            print("\nход введен не корректно. Формат вводимых данных: 'A1'")
        show_game(pole)
    return turn


def game(size: int, pl_item: str) -> None:
    pole, free_turns = set(), []
    ii_item = ""
    d = {}
    flag_end = False
    items = ["x", "0"]
    if any([pl_item not in items, size not in range(5, 11)]):
        flag_end = True
        print("игра запущена с неверными параметрами")
    else:
        d = {str(i + 1): chr(97 + i) for i in range(size)}
        items.remove(pl_item)
        ii_item = "".join(items)
        pole, free_turns = create_pole(size)
        print(f"\nвы играете {pl_item.upper()}")
    show_game(pole)

    while not flag_end:
        # ход пользователя
        turn = player_turn(pole, pl_item)
        free_turns.remove(turn)
        flag_end = check_game(pole, free_turns, pl_item, ii_item)
        # ход противника
        if not flag_end:
            ii_turn(pole, free_turns, ii_item, d)
            flag_end = check_game(pole, free_turns, pl_item, ii_item)


"""
опции игры:
pl_item - выбор чем будет играть игрок ["x" или 0]
size - размер поля от 5 до 10
"""

if __name__ == "__main__":
    game(pl_item="x", size=10)
