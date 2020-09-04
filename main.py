from MiddleWare import app
from config import *

if __name__ == '__main__':
    # 读取所有id
    all_id = load_data_from_id_set('spider_key')[1:]

    # 拷贝所有MTH
    app.run_crawl_to_backup_workData(all_id, 5)

    # 采集所有数据
    # app.run_crawl_to_capture_workData(all_id, 10)
