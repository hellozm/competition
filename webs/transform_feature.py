

def transfor():
    """
    将每行以逗号分隔的数据转换成空格分隔的数据
    :return:
    """
    with open('feature.txt', encoding='utf-8') as f:
        for line in f:
            if line and len(line.split(',')) == 9:
                ch = ' '.join(line.split(','))
                with open('feature_2.txt', 'a+', encoding='utf-8') as file:
                    file.write(ch)


def count():
    number_0 = 0
    number_1 = 0
    with open('feature_2.txt', encoding='utf-8') as f:
        for fe in f:
            if fe.strip()[-1] == '0':
                number_0 += 1
            else:
                number_1 += 1
    print(number_0, number_1)


if __name__ == '__main__':
    # transfor()
    count()
