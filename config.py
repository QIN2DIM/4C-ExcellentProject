import os
import csv
from datetime import datetime

try:
    from gevent import monkey

    monkey.patch_all()
    import gevent
    import requests
    from fake_useragent import UserAgent
    from urllib.parse import urlencode
    from bs4 import BeautifulSoup
    from requests.exceptions import *
    from gevent.queue import Queue
    from retrying import retry
    from selenium.webdriver import Chrome, ChromeOptions
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.support.wait import WebDriverWait
    import selenium.webdriver.support.expected_conditions as EC
except ModuleNotFoundError as e:
    print('\n{}\n>>> 请手动安装清单中的第三方库 \n{}'.format(
        e,
        os.path.dirname(__file__) + '/config.py'
    ))
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent bs4 requests')
    exit(1)


# 文本装饰器
def magic_msg(text: str, text_color, show_style='default', bk_color='default'):
    """
    修饰打印信息
    设置颜色开始 ：\033[显示方式;前景色;背景色m
    https://www.cnblogs.com/easypython/p/9084426.html
    :param text: 要装饰的文本
    :param show_style: 设置显示方式，使用系统默认
    :param text_color: 颜色模式，前景色，可选参数 见 set_text_color()
    :param bk_color: 
    :return:字符串
    """

    def set_show_style():
        """
        设置显示方式
        0                    终端默认设置
        1                    高亮显示
        22　　　　　　　　　　　非高亮显示
        4                    使用下划线
        24　　　　　　　　　　　去下划线
        5                    闪烁
        25　　　　　　　　　　　去闪烁
        7                    反白显示
        27　　　　　　　　　　　非反显
        8                    不可见
        28　　　　　　　　　　　可见
        :return:
        """
        if show_style == 'default':
            return '1'
        else:
            return '1'

    def set_text_color():
        """
        设置字体颜色,也叫前景色
        前景色         背景色              颜色
        ---------------------------------------
        30                40              黑色
        31                41              红色
        32                42              绿色
        33                43              黃色
        34                44              蓝色
        35                45              洋红
        36                46              青色
        37                47              白色
        :return:
        """
        if text_color == 'bk' or text_color == 'black':
            return '30'
        elif text_color == 'r' or text_color == 'red':
            return '31'
        elif text_color == 'g' or text_color == 'green':
            return '32'
        elif text_color == 'y' or text_color == 'yellow':
            return '33'
        elif text_color == 'bl' or text_color == 'blue':
            return '34'
        elif text_color == 'm' or text_color == 'magenta':
            return '35'
        elif text_color == 'c' or text_color == 'cyan ':
            return '36'
        elif text_color == 'w' or text_color == 'white':
            return '37'
        else:
            # 输入有误时默认返回红色
            return '31'

    def set_background_color():
        """
        设置背景色
        :return:
        """
        if bk_color == 'default':
            return '1'
        else:
            return '1'

    # The foreground
    #     设置颜色开始 ：\033[显示方式;前景色;背景色m
    setup_msg = '\033[{};{};{}m'.format(set_show_style(), set_text_color(), set_background_color())
    release_msg = '\033[0m'

    master_msg = setup_msg + text + release_msg

    return master_msg


# 版本控制
def version_control(mode='', BASE_NAME='国赛', INIT=True) -> str:
    """
    获取当前最新版本的输出文件
    :return:
    """

    try:
        # 取出对应BASE_NAME的最新版本文件
        out_dir_version = sorted([i for i in os.listdir(ROOT_DATABASE) if BASE_NAME in i])[-1]
    except IndexError:
        # 当目录未初始化或不存在对应BASE_NAME文件，则初始化文件名，
        # 文件命名严格按照如下范式
        # 赛名_属性_版本号.csv
        if '国赛' in BASE_NAME:
            out_dir_version = '中国大学生计算机设计大赛_国赛_0.csv'
        elif '合成' in BASE_NAME:
            out_dir_version = '中国大学生计算机设计大赛_合成_0.csv'
        else:
            out_dir_version = '中国大学生计算机设计大赛_panic_0.csv'

    # 依据范式，对字符串切片，取出版本号
    ver_num = out_dir_version.split('.csv')[0].split('_')[-1]

    # 执行模式’fn‘; 返回在库的对应 base_name 的最新版本的【csv文件路径】
    if mode == 'fn':
        return '{}/{}'.format(ROOT_DATABASE, out_dir_version)

    # 执行模式’num‘; 返回在库的对应base_name 的csv文件的最新【版本号】
    elif mode == 'num':
        return ver_num

    # 执行模式’new‘;构造并返回对应base_name 的新版本【csv文件路径】
    elif mode == 'new':

        new_file_name = '{}/{}_{}_{}.csv'.format(
            # dataBase路径
            ROOT_DATABASE,
            # base文件名
            base_name,
            # BASE_NAME
            out_dir_version.split('_')[1],
            # 现存版本号 + 1，
            str(int(ver_num) + 1)
        )
        return new_file_name


# 载入id_fp数据集
def load_data_from_id_set(mode) -> list:
    """
    data_set = title
    :param mode: 截取模式,
                spider_key : 联采
                str:works_id : 该作品编号对应的数据
                list:works_id :
    :return:返回表头+数据，使用切片[1:]截出数据集
    """

    # 当爬虫程序使用此函数时，并传入‘spider_key’口令，函数执行特殊命令，返回含表头的作品编号 List[str,str...]
    # 返回的列表里包含了所有在库的works_id,既当爬虫爬虫程序传入该口令时，将采取所有作品信息
    with open(id_fp, 'r', encoding='utf-8') as f:
        csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(f)
        data = [i for i in reader]
        if mode == 'spider_key':
            return [i[1] for i in data if i[1] != 'N/A']


def INIT_USER_AGENT():
    import tempfile
    if 'fake_useragent_0.1.11.json' not in os.listdir(tempfile.gettempdir()):
        os.system('copy {} {}'.format(
            ROOT_DATABASE + '/fake_useragent_0.1.11.json',
            tempfile.gettempdir() + '/fake_useragent_0.1.11.json'
        ))


INIT_USER_AGENT()
print(magic_msg('>>> 欢迎使用|=< C4-2020中国大学生计算机设计大赛_数据采集爬虫(C4DmSpider) >=|', 'r'))
print(magic_msg('>>> 该脚本使用协程调度采集任务，请合理配置采集参数!', 'm'))
print(magic_msg('>>> 用餐愉快~', 'g'))
print(magic_msg(''.center(100, '#'), 'w'))
"""############################################################"""

# 赛区官网
home = 'http://2020.jsjds.com.cn'

# 调试网址
# demo_url = 'http://2020.jsjds.com.cn/chaxun?keys=75191'
demo_url = 'http://2020.jsjds.com.cn/chaxun?'

# 数据库根目录
ROOT_DATABASE = os.path.dirname(__file__) + '/dataBase'

# 错误日志路径，记录采集异常并捕获链接
log_fp = ROOT_DATABASE + '/error_log.txt'

# id源表文件位置
id_fp = ROOT_DATABASE + '/id_set_01.csv'

# 输出文件版本控制
base_name = '中国大学生计算机设计大赛'

# 采集输出路径
out_path = version_control('fn')

title = "uuid,work_id,work_level,work_class,work_name,school,player,tutor," \
        "作品简介,开源代码与组件使用情况说明,作品安装说明," \
        "作品效果图,设计思路,设计重点和难点,指导老师自评," \
        "其他说明,部署链接1,部署链接2,插图".split(',')

# 合成表输出路径
# comp_table_fp = ROOT_DATABASE + '/{}合成_0.csv'.format(base_name)
comp_table_fp = version_control('fn', BASE_NAME='合成')

# 脚本核心组件，请勿挪动删除
COMP_DATABASE = ROOT_DATABASE + '/CNJSJ_BASE.csv'

# 爬虫控件
"""############################################################################################"""
SPIDER_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.135 Safari/537.36 '
}
# 采集功率
POWER = 16

# 作品编号，可为list，也可str，当不指定时置为''，此时会开启盲采
USER_KEY = ''

# 缓冲件，用于打印预览信息的容器
VIEWER = {}

# chromedriver.exe path ,若驱动没配置系统环境变量，请在此赋值绝对路径
CHROME_CODE_PATH = os.path.dirname(__file__) + '/MiddleWare/chromedriver.exe'

# MTH离线网页文件的存储文件夹路径，默认./dataBase/BACKUP，若更改，请使用绝对路径
BACKUP_OUT_PATH = os.path.join(ROOT_DATABASE, 'BACKUP')
BACKUP_CASHED_FILE = [i for i in os.listdir(BACKUP_OUT_PATH) if '.mhtml' in i]


def Println(entity=None):
    """

    :param entity: 预览实体
    :return:
    """
    global VIEWER

    # 不传参直接调用则打印实体
    if entity is None:
        entity = {}
        print('\n')
        for i in VIEWER.items():
            print(i)
        print(magic_msg('>>> summary:{}个采集结果 '.format(VIEWER.keys().__len__()), 'c'))

    # 传参调用则填充实体
    elif isinstance(entity, dict) and entity:
        VIEWER.update(
            {entity['作品编号'].split('=')[-1]: entity}
        )
