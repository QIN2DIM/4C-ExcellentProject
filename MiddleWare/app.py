import os
import csv
import webbrowser
import json
from config import comp_table_fp, Println, ROOT_DATABASE, title, POWER, version_control, COMP_DATABASE, magic_msg
from SpiderNest.snsProj_spider import get_985, get_211
from collections import *

# 摘要报告输出路径
out_flow_path = ''


class GUI_PANEL(object):
    def __init__(self):
        self.home = 'http://2020.jsjds.com.cn/chaxun?keys={}'

        self.data = self.load_data()

        self.sns_211 = get_211()
        self.sns_985 = get_985()

        self.school_name = list([i[5] for i in self.data])
        self.level_group = list([i[2] for i in self.data])
        self.work_name = list([i[4] for i in self.data])
        self.work_uuid = list([i[0] for i in self.data])

        self.temp_list_211 = dict(zip(self.sns_211, [0] * self.sns_211.__len__()))
        self.temp_list_985 = dict(zip(self.sns_985, [0] * self.sns_985.__len__()))

        for x in self.school_name:
            if x in list(self.temp_list_211.keys()):
                self.temp_list_211[x] += 1
            if x in list(self.temp_list_985.keys()):
                self.temp_list_985[x] += 1

    @staticmethod
    def load_data():
        with open(COMP_DATABASE, 'r', encoding='utf-8') as f:
            csv.field_size_limit(500 * 1024 * 1024)
            reader = csv.reader(f)
            return [i for i in reader][1:]

    def find_works_by_id(self, key: str, goto=False) -> dict:
        """
        根据作品编号跳转网页,不传参则弹出panel手动输入
        :param goto: 若为True则根据id打开网页
        :param key: 作品编号
        :return:
        """
        for item in self.data:
            if key == item[1]:
                DOCKER = dict(zip(title, item))
                with open(ROOT_DATABASE + '/PSAR/ASH.json', 'w+', encoding='utf-8') as f:
                    json.dump(DOCKER, f, ensure_ascii=False, indent=4)

                # goto website
                if goto:
                    webbrowser.open(item[0])
                return DOCKER

    def find_works_by_level(self, level: str or bool, class_: str or bool) -> list or bool:
        """
        根据作品登记筛选数据,不兼容模糊匹配
        :param class_:
        :param level: 作品奖级,'一等奖','二等奖','三等奖','优秀奖',分别代表一等奖~三等奖以及优秀奖
        :return:
        """
        DOCKER = []

        if level != '' and class_ != '':
            for item in self.data:
                if item[2] == level and class_ in item[3]:
                    DOCKER.append(list(item[:6]))
        elif (level == '' or level is False) and class_ != '':
            for item in self.data:
                if class_ in item[3]:
                    DOCKER.append(list(item[:6]))
        elif level != '' and (class_ == '' or class_ is False):
            for item in self.data:
                if item[2] == level:
                    DOCKER.append(list(item[:6]))
        else:
            return False

        for x in DOCKER:
            print(x)

        print(magic_msg('>>> summary:{}'.format(DOCKER.__len__()), 'r'))
        # print(magic_msg('>>> {}'.format(list(Counter([i[-1] for i in DOCKER]).items())), 'm'))
        return DOCKER

    def get_PSAR(self, school_name, save=False):
        global out_flow_path
        score_list = dict(zip(set(self.school_name), [[0, 0, 0]] * set(self.school_name).__len__()))

        if school_name in self.school_name:

            myLevel = ['一等奖', '二等奖', '三等奖']
            id_docker_1 = [[], [], []]
            for t in zip(self.school_name, self.work_uuid, self.work_name, self.level_group):
                if school_name == t[0]:
                    if myLevel[0] == t[-1]:
                        score_list[t[0]][0] += 1
                        id_docker_1[0].append({t[1]: t[2]})
                    elif myLevel[1] == t[-1]:
                        score_list[t[0]][1] += 1
                        id_docker_1[1].append({t[1]: t[2]})
                    elif myLevel[2] == t[-1]:
                        score_list[t[0]][2] += 1
                        id_docker_1[2].append({t[1]: t[2]})

            DOCKER = {
                school_name: {
                    '成果概要': dict(zip(myLevel, score_list[school_name])),
                    '作品细节': dict(zip(myLevel, id_docker_1))
                }
            }

            if save:
                out_flow_path = ROOT_DATABASE + '/PSAR/{}_分析报告.json'.format(school_name)
                with open(out_flow_path, 'w+', encoding='utf-8') as f:
                    json.dump(DOCKER, f, ensure_ascii=False, indent=4)

            return DOCKER
        else:
            return '>>> 该模块不兼容模糊匹配,请输入学校全称！'

    def get_summary(self, ):

        print('>>> 共{}所高校入围决赛,总计{}件作品入围决赛'.format(
            set(self.school_name).__len__(),
            self.school_name.__len__()
        ))
        print('>>> 其中有【{}/{}】所211工程院校,共有{}件作品入围决赛'.format(
            [i for i, x in self.temp_list_211.items() if x != 0].__len__(),
            self.sns_211.__len__(),
            sum(list(self.temp_list_211.values())),
        ))
        print('>>> 其中有【{}/{}】所985工程院校,共有{}件作品入围决赛'.format(
            [i for i, x in self.temp_list_985.items() if x != 0].__len__(),
            self.sns_985.__len__(),
            sum(list(self.temp_list_985.values())),
        ))

        print('[211]{}...'.format(list(self.temp_list_211.items())[:5]))
        print('[985]{}...'.format(list(self.temp_list_985.items())[:5]))
        print('[ALL]{}...'.format(sorted(
            tuple(Counter(self.school_name).items())[:5],
            key=lambda m: (m[-1], m[0]), reverse=True
        )))


def find_works_by_level(level: str = '', class_: str = ''):
    return GUI_PANEL().find_works_by_level(level=level, class_=class_)


def find_works_by_id(key, goto=True):
    try:
        msg = GUI_PANEL().find_works_by_id(key=key, goto=goto)
        msg.items()
        return msg
    except AttributeError:
        print('>>> 作品编号不存在!')
        exit(1)


def get_summary():
    return GUI_PANEL().get_summary()


def get_school_psar(school_name, save=False):
    if save is True:
        GUI_PANEL().get_PSAR(school_name=school_name, save=save)
        os.startfile(out_flow_path)
    else:
        print(GUI_PANEL().get_PSAR(school_name=school_name, save=save))


def get_all_class_name():
    with open(ROOT_DATABASE + '/TPTDP/class_name.txt', 'r', encoding='utf-8') as f:
        return [i.strip() for i in f.readlines()]


def run_crawl_to_capture_workData(work_id='', power: int = 30, ):
    """
    调度爬虫采集数据的接口，当work_id ='‘ 时,采集全部在库id数据
    :param power: int ∈[1, ∞) 弹性协程功率
    :param work_id: list[str,str....] or str ,作品编号，支持列表输入
    :return:
    """
    from SpiderNest.cnjsj_spider import CnJsjSpider
    from MiddleWare.cmp_data import comp_workData

    try:
        # 启动采集程序
        cjs = CnJsjSpider(work_id=work_id)
        cjs.coroutines_acceleration(power=power)

        # 合并数据表
        comp_workData()

        # 打印预抓取信息
        if work_id != '':
            Println()
    finally:
        # 垃圾释放
        os.remove(version_control('fn'))


def run_crawl_to_backup_workData(work_id, power: int = 4):
    from SpiderNest.ppy_flow_spider import go_bbr_spider
    go_bbr_spider(work_target=work_id, power=power)
