from MiddleWare import app
import random


def __text__():
    # 读取所有id
    all_id = app.get_all_works_id()

    # 随机抽取k个id
    sample = random.choices(all_id, k=1)

    # 拷贝MTH
    app.run_crawl_to_backup_workData(sample)

    # 采集数据
    app.run_crawl_to_capture_workData(sample)

    # 快速打开目标网页，留下本地缓存
    app.find_works_by_id(sample)

    # 作品查询
    app.find_works(attrs={'name': '红楼梦'})
