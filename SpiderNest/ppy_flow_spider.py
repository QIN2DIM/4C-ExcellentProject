from gevent import monkey

monkey.patch_all()

import gevent
from gevent.queue import Queue
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import demo_url, ROOT_DATABASE, magic_msg, load_data_from_id_set, log_fp

# 任务队列
works_idQ = Queue()
# 输出路径
OUT_PATH = ROOT_DATABASE + '/BACKUP/'

# 调试数据，当前，最大任务数
count, max_len = 1, 0


class WebCopySpider(object):

    def __init__(self, ):
        self.api = self.set_spiderOption(silence=True, anti=True)
        self.start()

    @staticmethod
    def set_spiderOption(silence: bool, anti: bool):
        """浏览器初始化"""
        options = ChromeOptions()

        # 最高权限运行
        options.add_argument('--no-sandbox')

        # 隐身模式
        options.add_argument('-incognito')

        # 无缓存加载
        options.add_argument('--disk-cache-')

        # 静默启动
        if silence is True:
            options.add_argument('--headless')

        """自定义选项"""

        # 无反爬虫机制：高性能启动，禁止图片加载及js动画渲染，加快selenium页面切换效率
        def NonAnti():
            chrome_prefs = {"profile.default_content_settings"        : {"images": 2, 'javascript': 2},
                            "profile.managed_default_content_settings": {"images": 2}}
            options.experimental_options['prefs'] = chrome_prefs
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            d_c = DesiredCapabilities.CHROME
            d_c['pageLoadStrategy'] = 'none'

            browser = Chrome(
                options=options,
                desired_capabilities=d_c,
            )
            return browser

        if anti is False:
            return NonAnti()
        else:
            # 有反爬虫/默认：一般模式启动
            return Chrome(options=options)

    def get_page(self, target, file_name):
        self.api.get(target)
        res = self.api.execute_cdp_cmd('Page.captureSnapshot', {})

        with open(file_name, 'w', newline='') as f:
            html = res.get('data')
            if html:
                f.write(html)

    def __kill__(self):
        self.api.quit()

    def start(self):
        global count
        while not works_idQ.empty():
            target: str = demo_url + 'keys={}'.format(works_idQ.get_nowait())
            file_name = OUT_PATH + target.split('=')[-1].strip() + '.mhtml'
            try:
                self.get_page(target=target, file_name=file_name)
                print(magic_msg('\r>>> 【{}/{}】任务队列:{}'.format(count, max_len, target), 'm'), end='')
            except Exception as e:
                print('\n', e, target)
                with open(log_fp, 'a', encoding='utf-8') as f:
                    f.writelines([target, ])

                # self.api.close()
            finally:
                count += 1
                self.__kill__()


def go_bbr_spider(work_target, power: int):
    """

    :param power:
    :param work_target:access link
    :return:
    """
    global max_len, count
    # 规整范式
    if isinstance(work_target, str):
        work_target = [work_target, ]

    # 功能实现
    if isinstance(work_target, list):

        # 任务创建
        for works_id in work_target:
            works_idQ.put_nowait(works_id)
        max_len = works_idQ.qsize()

        # 功率限制
        if power > work_target.__len__():
            power = work_target.__len__()

        # 开启协程任务
        task_list = []
        for x in range(power):
            task = gevent.spawn(WebCopySpider)
            task_list.append(task)
        gevent.joinall(task_list)

    # 传参有误
    else:
        print('>>> Input Error!')


if __name__ == '__main__':
    import random

    # 测试拷贝4个作品
    url = [key for key in load_data_from_id_set('spider_key')[1:]]

    go_bbr_spider([random.choice(url) for i in range(4)], 2)
