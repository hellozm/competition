import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def load_dataset(txt):
    fr = np.loadtxt(txt)
    info = np.array(fr)
    labels = info[:, -1]
    dataset = info[:, :-1]
    return dataset, labels


def train_1(data, target, feature_list=[]):
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.1, random_state=0)
    print(len(x_train), len(x_test))
    model = LogisticRegression(penalty='l1').fit(x_train, y_train)
    print("LR测试集准确率:{}".format(model.score(x_test, y_test)))
    # print(model.predict(x_test))  # 测试集结果
    feature_list = [int(feature) for feature in feature_list]
    print(feature_list)
    reliability = round(model.predict_proba(np.array([feature_list]))[0][1], 3)
    print(reliability)
    # print("该网站可信度为：{}".format(model.predict_proba(np.array([[1, 2, 2, 4, 0, 0, 0, 0]]))[0][1]))  # 前者为0的可能性，后者为1的可能性
    # print(model.predict(np.array([[1, 2, 2, 0, 0, 0, 0, 0],
    #                              [1, 1, 2, 0, 50, 50, 50, 50]])))  # 预测2个数据
    return reliability


def train_2(data, target):
    """
    对数据做标准化处理后再训练
    :param data:
    :param target:
    :return:
    """
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.1, random_state=0)
    print(len(x_train), len(x_test))
    sc = StandardScaler()
    sc.fit(x_train)
    x_train_std = sc.transform(x_train)
    x_test_std = sc.transform(x_test)
    model = LogisticRegression(penalty='l1').fit(x_train_std, y_train)
    print("LR测试集准确率:{}".format(model.score(x_test_std, y_test)))


if __name__ == '__main__':
    data, target = load_dataset('feature_2.txt')
    train_1(data, target)
    # train_2(data, target)
