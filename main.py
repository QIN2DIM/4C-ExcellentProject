from gevent import monkey

monkey.patch_all()
from middleware import app


def sample_():
    # 随机抽取1个作品
    import random

    sample = random.choices(all_id, k=1)

    # 拷贝MTH
    app.run_crawl_to_backup_data(sample)

    # 采集数据
    app.run_crawl_to_capture_data(sample)

    # 快速打开目标网页，留下本地缓存
    app.find_works_by_id(sample)

    # 作品查询
    app.find_works(attrs={'name': '红楼梦'})


if __name__ == '__main__':
    app.get_school_psar('海南大学', save=True)

    all_id = app.get_all_works_id()
