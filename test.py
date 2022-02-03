def create_pole(s):
    # Создаем начальное поле
    matrix = [[chr(96 + j) if i == 0 else (str(i) if j == 0 else "_") for j in range(s + 1)] for i in range(s + 1)]
    matrix[0][0] = ""

    # создаем начальный список свободных ходов
    free_turns = set(i + j for i in map(str, range(1, s + 1)) for j in map(str, range(1, s + 1)))
    return matrix, free_turns


def make_items_for_check(pole):
    column = diagm = diagr = ""
    diags_main = []
    diags_reverse = []
    raws = []
    columns = []
    # формируем списки строк, столбцов
    for i in range(1, len(pole)):
        raw = "".join(pole[i][1:])
        for j in range(1, len(pole)):
            column += pole[j][i]
        columns.append(column)
        raws.append(raw)
        column = ""
    # формируем списки основных и побочных диаганалей
    for step in range(len(pole) - 5):
        for i in range(len(pole) - 5):
            for j in range(1, 6):
                diagr += pole[len(pole) - j - i][j + step]
                diagm += pole[j + i][j + step]
            diags_main.append(diagm)
            diags_reverse.append(diagr)
            diagm = diagr = ""
    return raws, columns, diags_main, diags_reverse


# Отображение игрового поля
def show_game(pole):
    print()
    for raw in pole:
        raw = list(map(lambda x: x.ljust(2), raw))
        print(*raw)


# Ход комьютера
def ii_turn(pole, free_turns, ii_item):
    turn = free_turns.pop()
    print(turn)
    if turn.startswith("10"):
        x = 10
        y = int(turn[2:])
    else:
        x = int(turn[0])
        y = int(turn[1:])
    pole[x][y] = ii_item
    return turn, pole


# Ход игрока
def player_turn(pole, pl_item, free_turns):
    turn = free_turns.pop()
    if turn.startswith("10"):
        x = 10
        y = int(turn[2:])
    else:
        x = int(turn[0])
        y = int(turn[1:])
    pole[x][y] = pl_item
    return turn, pole


# Проверка результата игры
def end_game(pole, turns, pl_item, ii_item):
    flag_end = False
    grats = "\nПоздравляем, Вы победили!!!\n"
    shame = "\nВы проиграли :(\n"
    wtf = "\nНичья...\n"
    gg = ii_item * 5
    bg = pl_item * 5
    # формируем строки, столбцы, диаганали
    raws, columns, diags_main, diags_reverse = make_items_for_check(pole)
    all_items = raws + columns + diags_main + diags_reverse
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


def game(size, pl_item):
    pole, free_turns = [], []
    ii_item = ""
    d = {}
    flag_end = False
    items = ["x", "0"]
    if any([pl_item not in items, size not in range(3, 11)]):
        flag_end = True
        print("игра запущена с неверными параметрами")
    else:
        d = {str(i + 1): chr(97 + i) for i in range(size)}
        items.remove(pl_item)
        ii_item = "".join(items)
        pole, free_turns = create_pole(size)
        print(f"\nвы играете {pl_item.upper()}")

    while not flag_end:
        turn, pole = player_turn(pole, pl_item, free_turns)
        if turn.startswith("10"):
            print(f"\nваш ход: {d['10']}{turn[0]}")
        else:
            print(f"\nваш ход: {d[turn[1:]]}{turn[0]}")
        show_game(pole)
        flag_end = end_game(pole, free_turns, pl_item, ii_item)

        # ход противника
        if not flag_end:
            turn, pole = ii_turn(pole, free_turns, ii_item)
            if turn.startswith("10"):
                print(f"\nход противника: {d['10']}{turn[0]}")
            else:
                print(f"\nход противника: {d[turn[1:]]}{turn[0]}")
            show_game(pole)
            flag_end = end_game(pole, free_turns, pl_item, ii_item)


# опции игры
# pl_item - выбор чем будет играть игрок ["x" или 0]
# size - размер поля от 5 до 10

if __name__ == "__main__":
    game(pl_item="x", size=10)
