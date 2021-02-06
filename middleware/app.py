import csv
import json
import os
import webbrowser
from collections import Counter

from spiders.sns_project import get_985, get_211
from config import println, ROOT_DIR_DATABASE, TITLE, \
    version_control, COMP_DATABASE, magic_msg, load_data_from_id_set

# 摘要报告输出路径
out_flow_path = ''


class SystemPanel(object):
    def __init__(self):
        self.home = 'http://2020.jsjds.com.cn/chaxun?keys={}'

        self.data = self.load_data()
        self.bits = dict(zip(TITLE, list(range(TITLE.__len__()))))

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

    @staticmethod
    def println_summary(docker):
        for x in docker:
            print(x)

        print(magic_msg('>>> summary:{}'.format(docker.__len__()), 'r'))

    def find_works_by_id(self, work_id: str, goto=False) -> dict:
        """
        根据作品编号跳转网页,不传参则弹出panel手动输入
        :param goto: 若为True则根据id打开网页
        :param work_id: 作品编号
        :return:
        """
        for item in self.data:
            if work_id in item[1]:
                docker = dict(zip(TITLE, item))
                with open(ROOT_DIR_DATABASE + '/psar/ASH.json', 'w+', encoding='utf-8') as f:
                    json.dump(docker, f, ensure_ascii=False, indent=4)

                # goto website
                if goto:
                    webbrowser.open(item[0])
                return docker

    def find_works_by_level(self, level: str or bool, work_class: str or bool) -> list or bool:
        """
        根据作品登记筛选数据,不兼容模糊匹配
        :param work_class:
        :param level: 作品奖级,'一等奖','二等奖','三等奖','优秀奖',分别代表一等奖~三等奖以及优秀奖
        :return:
        """
        docker = []

        if level != '' and work_class != '':
            for item in self.data:
                if item[2] == level and work_class in item[3]:
                    docker.append(list(item[:6]))
        elif (level == '' or level is False) and work_class != '':
            for item in self.data:
                if work_class in item[3]:
                    docker.append(list(item[:6]))
        elif level != '' and (work_class == '' or work_class is False):
            for item in self.data:
                if item[2] == level:
                    docker.append(list(item[:6]))
        else:
            return False

        self.println_summary(docker)
        return docker

    def find_works_by_title(self, work_name: str, work_class: str = ''):

        if work_class != '':
            docker = [x[:8] for x in self.data if work_name in x[4] and work_class in x[3]]
        else:
            docker = [x[:8] for x in self.data if work_name in x[4]]

        self.println_summary(docker)
        return docker

    def find_works_by_player(self, player: str, school: str = ''):

        if school != '':
            docker = [x[:8] for x in self.data if player in x[6] and school in x[5]]
        else:
            docker = [x[:8] for x in self.data if player in x[6]]

        self.println_summary(docker)
        return docker

    def find_works_by_tutor(self, tutor: str, school: str = ''):

        if school != '':
            docker = [x[:8] for x in self.data if tutor in x[7] and school in x[5]]
        else:
            docker = [x[:8] for x in self.data if tutor in x[7]]

        self.println_summary(docker)
        return docker

    def find_works(self, key, border=8, **kwargs):

        # 全文模糊匹配
        docker = [x[:border] for x in self.data if key in ''.join(x)]

        # work_id = kwargs.get('attrs').get('work_id')
        work_level = self.level_convert(kwargs.get('attrs').get('level'))
        work_class = kwargs.get('attrs').get('class_')
        work_name = kwargs.get('attrs').get('name')
        school: str = kwargs.get('attrs').get('school')
        player = kwargs.get('attrs').get('player')
        tutor = kwargs.get('attrs').get('tutor')

        if school:
            docker = [x for x in docker if school in x[self.bits['school']]]

        if work_class:
            docker = [x for x in docker if work_class in x[self.bits['work_class']]]

        if work_level:
            docker = [x for x in docker if work_level == x[self.bits['work_level']]]

        if work_name:
            docker = [x for x in docker if work_name in x[self.bits['work_name']]]

        if player:
            docker = [x for x in docker if player in x[self.bits['player']]]

        elif tutor:
            docker = [x for x in docker if tutor in x[self.bits['tutor']]]

        self.println_summary(docker)

        return docker

    @staticmethod
    def level_convert(level: str):
        if level is None:
            return None

        if '1' in level:
            return '一等奖'
        elif '2' in level:
            return '二等奖'
        elif '3' in level:
            return '三等奖'

    def get_psar(self, school_name, save=False):
        global out_flow_path
        score_list = dict(zip(set(self.school_name), [[0, 0, 0]] * set(self.school_name).__len__()))

        if school_name in self.school_name:

            my_level = ['一等奖', '二等奖', '三等奖']
            id_docker_1 = [[], [], []]
            for t in zip(self.school_name, self.work_uuid, self.work_name, self.level_group):
                if school_name == t[0]:
                    if my_level[0] == t[-1]:
                        score_list[t[0]][0] += 1
                        id_docker_1[0].append({t[1]: t[2]})
                    elif my_level[1] == t[-1]:
                        score_list[t[0]][1] += 1
                        id_docker_1[1].append({t[1]: t[2]})
                    elif my_level[2] == t[-1]:
                        score_list[t[0]][2] += 1
                        id_docker_1[2].append({t[1]: t[2]})

            docker = {
                school_name: {
                    '成果概要': dict(zip(my_level, score_list[school_name])),
                    '作品细节': dict(zip(my_level, id_docker_1))
                }
            }

            if save:
                out_flow_path = ROOT_DIR_DATABASE + '/psar/{}_分析报告.json'.format(school_name)
                with open(out_flow_path, 'w+', encoding='utf-8') as f:
                    json.dump(docker, f, ensure_ascii=False, indent=4)

            return docker
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
    return SystemPanel().find_works_by_level(level=level, work_class=class_)


def find_works_by_id(key, goto=True):
    try:
        if isinstance(key, str):
            msg = SystemPanel().find_works_by_id(work_id=key, goto=goto)
            msg.items()
            return msg
        elif isinstance(key, list):
            assert key.__len__() <= 5, 'assert 请控制自启网页数量小于预设值'
            for id_ in key:
                SystemPanel().find_works_by_id(work_id=id_, goto=goto)

    except AttributeError:
        print('>>> 作品编号不存在!')
        exit(1)


def find_works_by_title(work_name: str, class_: str = '') -> list:
    return SystemPanel().find_works_by_title(work_name=work_name, work_class=class_)


def find_works_by_player(player_name: str, school_name: str = '') -> list:
    return SystemPanel().find_works_by_player(player=player_name, school=school_name)


def find_works_by_tutor(tutor: str, school_name: str = '') -> list:
    pass


def find_works(any_key: str = '', work_id: str = '', attrs=None) -> list:
    """
    支持任意关键字的全文匹配
    :param work_id: 全局唯一的作品编号
    :param any_key: 任意关键字
    :param attrs: 传入字典。{'关键字':"匹配的字符串"}，如 {‘school’:'北京大学'}
    关键字有这些: level（奖级），class_（类别），name（作品名），school（高校），player（成员），tutor（指导老师）
    当传入奖级时，使用str(1),str(2),str(3) 分别表示一二三等奖，其余关键字均支持模糊匹配
    :return:
    """
    if attrs is None:
        attrs = {}

    return SystemPanel().find_works(key=any_key, attrs=attrs)


def get_summary():
    return SystemPanel().get_summary()


def get_school_psar(school_name, save=False):
    if save is True:
        SystemPanel().get_psar(school_name=school_name, save=save)
        os.startfile(out_flow_path)
    else:
        print(SystemPanel().get_psar(school_name=school_name, save=save))


def get_all_class_name():
    with open(ROOT_DIR_DATABASE + '/tpd/class_name.txt', 'r', encoding='utf-8') as f:
        return [i.strip() for i in f.readlines()]


def run_crawl_to_capture_data(work_id='', power: int = 30, ):
    """
    调度爬虫采集数据的接口，当work_id ='‘ 时,采集全部在库id数据
    :param power: int ∈[1, ∞) 弹性协程功率
    :param work_id: list[str,str....] or str ,作品编号，支持列表输入
    :return:
    """
    from spiders.cnjsj import CnJsjSpider
    from middleware.cmp_data import comp_workData

    try:
        # 启动采集程序
        cjs = CnJsjSpider(work_id=work_id)
        cjs.coroutines_acceleration(power=power)

        # 合并数据表
        comp_workData()

        # 打印预抓取信息
        if isinstance(work_id, str):
            println()
        elif isinstance(work_id, list):
            println()

    finally:
        # 垃圾释放
        os.remove(version_control('fn'))


def run_crawl_to_backup_data(work_id, power: int = 4):
    from spiders.ppy_flow import go_bbr_spider
    go_bbr_spider(work_target=work_id, power=power)


def get_all_works_id() -> list:
    """
    获取所有在库作品编号，无表头
    :return:
    """
    return load_data_from_id_set('spider_key')[1:]
