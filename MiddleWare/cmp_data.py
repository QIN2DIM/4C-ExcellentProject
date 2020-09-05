""""合并数据，工程核心文件，请勿挪动或删改"""

import csv
from config import version_control, comp_table_fp, id_fp, title


def load_id_set_01() -> list:
    """固定的id池"""
    with open(id_fp, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = [[i[1], i] for i in reader if i[1] != 'N/A']

    data_flow = sorted(data[1:])
    return data_flow


def load_out_data_set() -> list:
    """抽取最新版本的采集表"""
    fp_name = version_control(mode='fn')
    with open(fp_name, 'r', encoding='utf-8') as f:
        csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(f)
        data = [i for i in reader if i and 'N/A' not in i[0]]
    data_flow = sorted([[i[0].split('=')[-1], i] for i in data[1:]])

    return data_flow


def merge_data() -> list:
    data_1 = load_id_set_01()
    data_2 = load_out_data_set()
    if data_1.__len__() == data_2.__len__():
        return [
            [
                data_2[x][-1][0], data_1[x][-1][1], data_1[x][-1][2],
                data_2[x][-1][2], data_2[x][-1][1],
            ] + data_1[x][-1][4:] + data_2[x][-1][3:] for x in range(data_2.__len__())
        ]
    else:
        temp_set = []
        for item in data_2:
            works_id = item[0]
            for target in data_1:
                if target[0] == works_id:
                    temp_set.append(target)
        temp_set = sorted(temp_set)
        try:
            return [
                [
                    data_2[x][-1][0], temp_set[x][-1][1], temp_set[x][-1][2],
                    data_2[x][-1][2], data_2[x][-1][1],
                ] + temp_set[x][-1][4:] + data_2[x][-1][3:] for x in range(data_2.__len__())
            ]
        except IndexError:
            pass


def outFlow(DATA: list):
    with open(version_control('new', '合成'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(title)
        try:
            for data in DATA:
                writer.writerow(data)
        except TypeError:
            pass


# 合并数据接口
def comp_workData():
    outFlow(merge_data())


