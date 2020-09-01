# C4AI-计算机设计大赛_作品查询爬虫

利用官网接口，以及公开数据，采集作品信息

## Quick Start

进入`main.py`,合理设置`power`控制协程功率 ，运行程序即可采集**”第一批“**决赛入围作品的数据

```python
from SpiderNest.cnjsj_spider import CnJsjSpider
from config import POWER

if __name__ == '__main__':

    cjs = CnJsjSpider()
    cjs.coroutines_acceleration(power=POWER)
    # power 采集功率,power:int ∈[1, ∞）
```

## API

- 进入`MiddleWare`中间件，运行`app.py`，执行功能。
  - 即可调用NLP模型，分析参赛作品信息。
  - 根据`学校`、`作品编号`、`作品名称`、`赛道名称`等任意信息查找、筛选、打印数据。

## 文档树

```
中国大学生计算机设计大赛_抓取
 ├── __pycache__
 │   └── config.cpython-38.pyc
 ├── dataBase
 │   ├── error_log.txt
 │   ├── id_pool.xlsx
 │   ├── id_set_01.csv
 │   └── 中国大学生计算机设计大赛——国赛决赛入围作品信息_0.csv
 ├── MiddleWare
 │   ├── load_data_demo.py
 │   └── __pycache__
 ├── SpiderNest
 │   ├── cnjsj_spider.py
 │   └── __pycache__
 ├── main.py
 ├── config.py
 ├── requirements.txt
 └── 说明文档.md
```





