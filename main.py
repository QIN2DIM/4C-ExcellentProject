from MiddleWare import app
from config import *

if __name__ == '__main__':
    # 读取所有id
    all_id = app.get_all_works_id()

    # 拷贝所有MTH
    # app.run_crawl_to_backup_workData(all_id, 12)

    # app.find_works_by_id('69742')

    # 采集所有数据
    app.run_crawl_to_capture_workData(all_id, 32)
