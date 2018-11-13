

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


if __name__ == '__main__':
    transfor()
