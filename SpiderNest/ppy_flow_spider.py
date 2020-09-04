from config import *

# 任务队列
works_idQ = Queue()

# 调试数据，当前，最大任务数
count, max_len = 1, 0

# 静默启动,若采集功率过大，则强制使用静默采集
silence = True
if POWER >= 5:
    silence = True

# 图像释放，必须为True，否则附件存储异常
anti = True


class WebCopySpider(object):

    def __init__(self, ):
        self.start()

    @staticmethod
    def set_spiderOption():
        """
        浏览器初始化
        :return:
        """
        options = ChromeOptions()

        # 最高权限运行
        options.add_argument('--no-sandbox')

        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')

        # fake UserAgent
        options.add_argument('user-agent={}'.format(UserAgent().random))

        options.add_argument('Connection:"close"')
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

            # browser = Chrome(
            #     options=options,
            #     desired_capabilities=d_c,
            # )
            return d_c

        if anti is False:
            DC = NonAnti()
            try:
                return Chrome(options=options, desired_capabilities=DC, executable_path=CHROME_CODE_PATH)
            except OSError:
                return Chrome(options=options, desired_capabilities=DC)

        # 未指定ChromeDriver，默认读取环境变量
        if CHROME_CODE_PATH == '':
            return Chrome(options=options)
        else:
            return Chrome(options=options, executable_path=CHROME_CODE_PATH)

    @staticmethod
    def error_log(info: str):
        with open(log_fp, 'a', encoding='utf-8') as f:
            now_ = '\n\n[{}]\n'.format(str(datetime.now()).split('.')[0])
            f.write(now_ + info)

    def get_page(self, target, file_name):

        # 接管Chrome
        api = self.set_spiderOption()

        api.get(target)

        # 等待元素全部加载
        # WebDriverWait(api, 30).until(EC.presence_of_all_elements_located)

        res = api.execute_cdp_cmd('Page.captureSnapshot', {})

        with open(file_name, 'w', newline='') as f:
            html = res.get('data')
            if html:
                f.write(html)
            else:
                error_msg = ' The  MTH message is empty: {}'.format(target)
                self.error_log(error_msg)

        # 垃圾回收
        api.quit()

    def start(self):
        global count
        while not works_idQ.empty():
            # target : url
            target: str = demo_url + 'keys={}'.format(works_idQ.get_nowait())

            # 将《作品编号.mhtml》作为文件名
            file_name = target.split('=')[-1].strip() + '.mhtml'

            # 扫描输出路径，若该文件已留下采集痕迹，则跳过采集，否则启动爬虫程序
            if file_name not in BACKUP_CASHED_FILE:
                # 合并文件输出路径
                file_outPath = os.path.join(BACKUP_OUT_PATH, file_name)
                try:
                    # 采集网页
                    self.get_page(target=target, file_name=file_outPath)

                    # 打印调试信息
                    print(magic_msg('\r>>> 【{}/{}】任务队列:{}'.format(count, max_len, target), 'm'), end='')

                # 将任意错误类型记入日志
                except Exception as et:
                    print('\nERROR from ppy_flow_spider', et, target)
                    error_msg = target + '\n{}'.format(et)
                    self.error_log(error_msg)

                finally:
                    # 更新调试信息
                    count += 1
            else:
                count += 1
                continue


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
            print(magic_msg('>>> 监测到您设置的协程功率较大，请确保网络通通畅，否则采集可能出现异常！', 'r'))

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
    random.shuffle(url)

    sample = [url.pop() for i in range(4)]

    go_bbr_spider(sample, power=15)
