def __pos_available(x, y, x_limit, y_limit):
    return x >= 0 and x < x_limit and y >= 0 and y < y_limit


def __cal_adjacent_life_num_multi(field, i, j):
    num1 = num2 = num3 = num4 = num = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            # 自己不算在周围的点里
            if x == i and y == j:
                continue
                # 当前点为0
            if field[i][j] == 0:
                # 检查周围的点是否合法
                if __pos_available(x, y, len(field), len(field[0])):
                    # 是否有生命
                    if field[x][y] == 1:
                        num1 += 1
                    elif field[x][y] == 2:
                        num2 += 1
                    elif field[x][y] == 3:
                        num3 += 1
                    elif field[x][y] == 4:
                        num4 += 1
            # 当前点非0
            else:
                # 检查周围的点是否合法
                if __pos_available(x, y, len(field), len(field[0])):
                    # 是否有相同生命
                    if field[x][y] == field[i][j]:
                        num += 1
    # 当前点非0
    if field[i][j] != 0:
        return (num, field[i][j])
    # 当前点为0
    else:
        # 最大值Mmax和最大值Mmax的索引值
        max = num1
        index = 1
        sum = 0
        if num2 > max:
            max = num2
            index = 2
        if num3 > max:
            max = num3
            index = 3
        if num4 > max:
            max = num4
            index = 4
        # 求是否最大值Mmax为唯一的
        if max == num1:
            sum += 1;
        if max == num2:
            sum += 1;
        if max == num3:
            sum += 1;
        if max == num4:
            sum += 1;
        # 最大值Mmax唯一
        if sum == 1:
            return (max, index)
        # 最大值Mmax非唯一
        else:
            return (max, 0)


def two_gamer_strategy(field):
    new_field = [[0 for i in field[0]] for i in field]
    for i in range(len(field)):
        for j in range(len(field[0])):
            num, index = __cal_adjacent_life_num_multi(field, i, j)
            if num == 2:
                new_field[i][j] = field[i][j]  # 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变
            elif num == 3:  # 如果一个细胞周围有3个细胞为生（一个细胞周围共有8个细胞）
                if field[i][j] != 0:  # 原来状态非0
                    new_field[i][j] = field[i][j]
                else:
                    if num >= 2 and num <= 3:
                        new_field[i][j] = index  # 如果2≤Mmax≤3且Mmax唯一，产生Mmax所对应的i。
                    else:
                        new_field[i][j] = 0  # 其他状态为死
            else:
                new_field[i][j] = 0  # 其他状态为死
    return new_field


def three_gamer_strategy(field):
    new_field = [[0 for i in field[0]] for i in field]
    for i in range(len(field)):
        for j in range(len(field[0])):
            num, index = __cal_adjacent_life_num_multi(field, i, j)
            if num == 2:
                new_field[i][j] = field[i][j]  # 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变
            elif num == 3 or num == 4 or num == 5:  # 如果一个细胞周围有3，4，5个细胞为生（一个细胞周围共有8个细胞）
                if field[i][j] != 0 and num == 3:  # 原来状态非0且周边有三个相同的细胞体
                    new_field[i][j] = field[i][j]
                elif field[i][j] != 0 and num != 3:
                    new_field[i][j] = 0  # 其他状态为死
                else:
                    if num >= 2 and num <= 3:
                        new_field[i][j] = index  # 如果2≤Mmax≤3且Mmax唯一，产生Mmax所对应的i。
                    else:
                        new_field[i][j] = 0  # 其他状态为死
            else:
                new_field[i][j] = 0  # 其他状态为死
    return new_field


def four_gamer_strategy(field):
    new_field = [[0 for i in field[0]] for i in field]
    for i in range(len(field)):
        for j in range(len(field[0])):
            num, index = __cal_adjacent_life_num_multi(field, i, j)
            if num == 2 or num == 3 or num == 4 or num == 5:  # 如果一个细胞周围有3，4，5个细胞为生（一个细胞周围共有8个细胞）
                if field[i][j] != 0 and num <= 3:  # 原来状态非0且周边有三个或两个相同的细胞体
                    new_field[i][j] = field[i][j]
                elif field[i][j] != 0 and num > 3:
                    new_field[i][j] = 0  # 其他状态为死
                else:
                    if num >= 2 and num <= 3:
                        new_field[i][j] = index  # 如果2≤Mmax≤3且Mmax唯一，产生Mmax所对应的i。
                    else:
                        new_field[i][j] = 0  # 其他状态为死
            else:
                new_field[i][j] = 0  # 其他状态为死
    return new_field


if __name__ == '__main__':
    field = \
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in two_gamer_strategy(field):
        print(i)
    for i in three_gamer_strategy(field):
        print(i)
    for i in four_gamer_strategy(field):
        print(i)
