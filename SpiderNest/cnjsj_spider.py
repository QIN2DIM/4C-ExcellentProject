from config import *

# 代理ip
proxy = ""

# 获取数据输出路径
path_ = version_control('new')

# 记录最大任务数量
max_len = 0

# 记录任务实时进度
count = 0

# 任务队列
idQ = Queue()

# 数据表头
title = ['作品编号', '作品名称', '作品分类', '作品简介', '开源代码与组件使用情况说明', '作品安装说明',
         '作品效果图', '设计思路', '设计重点和难点', '指导老师自评', '其他说明', '部署链接1', '部署链接2', '插图']


def load_idQ(works_command: str or list):
    """

    :param works_command:
    :return:
    """
    global max_len

    try:
        # 当指令为字符串时执行语句
        if isinstance(works_command, str):
            # 当无指令为空时，默认采集所有在库id
            if works_command == '':
                data_flow = load_data_from_id_set(mode='spider_key')[1:]
                for data in data_flow:
                    idQ.put_nowait(data)
            # 当指定id时，将该id加入任务队列
            else:
                idQ.put_nowait(works_command)

        # 当指令为列表时执行语句
        elif isinstance(works_command, list):
            # => if works_command == []
            if not works_command:
                data_flow = load_data_from_id_set(mode='spider_key')[1:]
                for data in data_flow:
                    idQ.put_nowait(data)
            # 遍历id队列，添加任务
            else:
                for data in works_command:
                    idQ.put_nowait(data)
    finally:
        # 记录任务队列最大长度，用于修饰调试信息
        max_len = idQ.qsize()


def save_data(flow=None, INIT=False):
    """

    :param flow:
    :param INIT:
    :return:
    """

    if flow is None:
        flow = []
    if INIT:
        with open(path_, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title)
            print(magic_msg('>>> the csv file has been initialed\n>>> {}'.format(path_), 'g'))
    with open(path_, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(flow)


class CnJsjSpider(object):
    """中国大学生计算机设计大赛 作品信息采集"""

    def __init__(self, work_id=''):
        save_data(INIT=True)

        load_idQ(work_id)

    @staticmethod
    def handle_html(key):
        global count
        # 根据作品编号组装URL

        data = {
            'keys': key
        }
        url = demo_url + urlencode(data)
        count += 1
        print(magic_msg('\r>>>【{}/{}】 goto {}'.format(count, max_len, url), 'c'), end='')

        # 代理ip参数组装
        proxies = {
            # proxy = ip:port
            'http': 'http://' + proxy
        }

        try:
            if proxy:
                res = requests.get(url, headers=SPIDER_HEADERS, proxies=proxies)
            else:
                res = requests.get(url, headers=SPIDER_HEADERS)

            # 状态码200，请求正常
            if res.status_code == 200:
                return res.text

            # 状态码302 表示ip封禁;请执行IP更换策略
            elif res.status_code == 302:
                print(magic_msg(text=url, text_color='r'))

        except RequestException:
            print(magic_msg(url, text_color='yellow'))
            return None

    @staticmethod
    def parse_html(html: str) -> dict:
        """

        :param html: response.text
        :return: OUT_FLOW dict
        """

        soup = BeautifulSoup(html, 'html.parser')

        # 解析作品详细信息
        data_flow = [item.find('td').text.strip() for item in soup.find_all('tr', attrs={'bgcolor': '#ffffff'})][3:]

        # 解析作品简介
        flag_flow = [info.text for info in soup.find_all('td', attrs={'colspan': '5'})]

        # 解析图片链接
        img_flow = [home + img['src'] for img in soup.find_all('img')]
        try:
            link_1 = data_flow[8][5:].strip()
            link_2 = data_flow[9][5:].strip()
        except IndexError:
            link_1, link_2 = 'N/A', 'N/A'

        # 组装数据流
        OUT_FLOW = {
            '作品编号'         : home + '/chaxun/?keys=' + flag_flow[0],
            '作品名称'         : flag_flow[1],
            '作品分类'         : flag_flow[-1],
            '作品简介'         : data_flow[0][4:].strip(),
            '开源代码与组件使用情况说明': data_flow[1][13:].strip(),
            '作品安装说明'       : data_flow[2][6:].strip(),
            '作品效果图'        : data_flow[3][5:].strip(),
            '设计思路'         : data_flow[4][4:].strip(),
            '设计重点和难点'      : data_flow[5][7:].strip(),
            '指导老师自评'       : data_flow[6][6:].strip(),
            '其他说明'         : data_flow[7][4:].strip(),
            '部署链接1'        : link_1,
            '部署链接2'        : link_2,
            '插图'           : img_flow
        }
        return OUT_FLOW

    def coroutines_acceleration(self, power: int, ):
        """
        携程加速
        :param power: 协程数
        :return:
        """

        task_list = []

        # 设置有误,则使用限定功率
        if power <= 0:
            power = 3
            print(magic_msg('Warning : Invalid credentials(crawl power)', 'y'))

        # 当协程数大于任务数时，将协程数强制转化为最大任务数，避免闲置协程浪费资源
        elif power > max_len:
            power = max_len
        print(magic_msg('>>> POWER = {}'.format(power), 'g'))
        for x in range(power):
            task = gevent.spawn(self.start_the_crawler)
            task_list.append(task)
        gevent.joinall(task_list)

    def start_the_crawler(self):
        while not idQ.empty():
            key = idQ.get_nowait()
            try:
                # 信息采集与解析
                html: str = self.handle_html(key)
                flow: dict = self.parse_html(html)

                # 留下痕迹
                Println(flow)

                # 保存数据
                save_data(flow=list(flow.values()))

            except Exception as et:
                # 任务出错，记录日志
                with open(log_fp, 'a', encoding='utf-8', ) as f:
                    now_ = str(datetime.now()).strip('.')[0]
                    log_msg = home + '/chaxun/?keys={}\n'.format(key)
                    err_msg = """
                    >>>【{}】
                    ERROR_KEY:{}
                    ERROR_INFO:{}
                    """.format(now_, log_msg, et)
                    f.write(err_msg)


if __name__ == '__main__':
    cjs = CnJsjSpider(work_id='70775')
    cjs.coroutines_acceleration(power=POWER)
