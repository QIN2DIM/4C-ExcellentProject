# 该数据抽取脚本仅供数据初始化用途，请勿随意改动
def load_id_pool():
    """从id_pool.xlsx中清洗出id_set_01.csv"""
    from openpyxl import load_workbook
    import csv

    def save_info_pool(out_flow: dict):
        with open('../database/id_set_02.csv', 'w', encoding='utf-8', newline='')as f:
            writer = csv.writer(f)
            writer.writerow(['uuid', 'work_id', 'work_level', 'work_name', 'school', 'player', 'tutor'])
            for key, flow in out_flow.items():
                writer.writerow([key, ] + flow)

    # 要抽取的源表，比如成绩排名
    fp = '../database/id_pool.xlsx'

    # cont page∈[x, y] x:开始有排名的table，y:结束页table
    page_range = [2, 172]

    # 初始化
    data_flow = {}
    count = 0

    # 创建对象
    wb = load_workbook(fp, read_only=True)

    for page in range(page_range[0], page_range[-1] + 1):
        ws_name = 'Table {}'.format(page)
        ws = wb[ws_name]
        for row in ws.rows:
            data = []
            for cell in row:
                # 单元格数据str
                msg = cell.value
                if msg is None:
                    msg = 'N/A'
                # 去除自动换行
                msg = str(msg).replace("\n", '')
                # 组装数据
                data.append(msg)
            # 跳过表头
            if '作品名称' in data or '中国大学生计算机设计大赛' in data[0]:
                continue
            # 组装数据流

            data_flow.update(
                {
                    "Table{}_{}".format(page, count): data[:6]
                }
            )

            # 更新状态
            count += 1
    wb.close()

    save_info_pool(data_flow)


if __name__ == '__main__':
    load_id_pool()
