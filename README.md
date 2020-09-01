# C42020-计算机设计大赛_信息挖掘

利用官网接口，以及公开数据，采集作品信息

[TOC]

## Quick Start

进入`main.py`,合理设置`power`控制协程功率 ，运行程序即可采集**第一批**决赛入围作品的数据

### 采集作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/`目录下生成`合成.csv`文件
- 从`config`配置文件中打印变量`title`即可查询信息键

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    id_list = ['75945','68589']
    # app.run_crawl_to_capture_workData(work_id='75945',power=30)
    app.run_crawl_to_capture_workData(['75945', '70773'], 2)
    
```



### 拷贝作品信息

- `app.run_crawl_to_capture_workData(work_id: str or list,power: int=4)`
  - work_id = 作品编号，支持**单个字符串**输入以及**List**多个字符串输入
  - power = 协程功率，`power∈[1,∞)`，脚本内置弹性协程队列，此处可`随意`设置
- 运行后会在`/dataBase/BACKUP/`目录下生成以作品编号命名的`.mhtml`文件，该格式网页文件封装了源所有的文本插图和渲染效果，在断网情况下也不会丢失数据细节，部分作品插图较多，体积占用较大。（注：safari可能会打不开这种格式文件）

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.run_crawl_to_backup_workData('70773',power=1)

```



## API

在从`MiddleWare`中导入`app`，即可调用脚本功能，别忘了调用`config`配置文件设置全局变量~

```python
from MiddleWare import app
from config import *
```



### 作品查询~学校成果

- `app.get_school_psar(school_name: str,save: bool)`
  - school_name = 学校名称。这里不支持模糊匹配，请输入**全称**！
  - save = 保存输出。默认为False；建议为True，运行后会在`/dataBase/PSAR`目录下生成对应学校的分析结果，文件格式为`.json`，信息键仅包括`获奖信息`以及`作品链接`。文件会**自动打开**。

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    app.get_school_psar(school_name='海南大学',save=True)
```

- `/海南大学_分析报告.json`

```json
{
    "海南大学": {
        "成果概要": {
            "一等奖": 1,
            "二等奖": 4,
            "三等奖": 2
        },
        "作品细节": {
            "一等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=70775": "基于时序热词挖掘的COVID-19舆情监测和情感分析系统"
                }
            ],
            "二等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=70983": "多场景智控医疗机器人"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=72687": "海洋牧场-水下多功能工作平台"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=75194": "基于差分萤火虫算法的盲水印系统"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=77243": "HiCollage-基于微信小程序的学生校务管理"
                }
            ],
            "三等奖": [
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=71095": "校代达微信小程序"
                },
                {
                    "http://2020.jsjds.com.cn/chaxun/?keys=71634": "防疫口罩监控系统"
                }
            ]
        }
    }
}
```



### 作品查询~奖级AND赛道

- `app.find_works_by_level(level: str,class_: str)`
  - level = 作品等级。这里需要**规范输入**，只能输入以下选项
    - `一等奖`、`二等奖`、`三等奖`
  - class_ = 作品赛道。这里支持模糊匹配。在`/dataBase/TPTDP/class_name.txt`中有C4-2020所有赛道的全称
- 食用说明：`level`和`class_`都不是必选参数，比如只想知道一等奖的所有作品，只需传入`level`即可，`class_`可不传或传入空字符串。
- ~~**（嗯！别骂了别骂了，Excel也能做到）**~~

```python
from MiddleWare import app
from config import *

if __name__ == '__main__':
    # app.find_works_by_level(level='一等奖', class_='大数据')
    # app.find_works_by_level(level='', class_='人工智能')
    app.find_works_by_level(level='一等奖', class_='')
```



### 作品查询~比赛摘要

- `app.get_summary()`可打印决赛成绩概况~~（后来觉得这个功能太鸡肋了，就没再写这个API，可凑合着看看）~~



### 作品查询~链接直达

- `app.find_works_by_id(key: str, goto: bool)`
  - key = 作品编号，仅支持单个字符串输入
  - goto = 是否打开网页。若为True，则使用默认浏览器打开作品首页
- ~~确实又是个很鸡肋的API~~



### works_id数据加载

- 由于表数据结构比较乱，我已经写好了一个全局load id 的函数，使用方法也很粗暴，调用该函数并传入`spider_key`，即可获取含表头的在库id列表。获取列表后使用切片去除表头候即可获得干净的数据~
- 因为合成BASE文件有点大，故使用`csv.field_size_limit()`捕获数据流。函数源码如下

```python
# config.py
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
            return [i[1] for i in data]
```

- 食用方法

```python
from config import load_data_from_id_set

if __name__ == '__main__':
    id_flow: list = load_data_from_id_set(mode='spider_key')
    print(id_flow)
    print('id池大小：{}'.format(id_flow.__len__()))
```



## 注意事项

- 工程文件中的`/dataBase`目录下存放了脚本核心BASE文件，请勿随意挪动或删除文件，否则会出大问题！
- `config.py`中可以自己调整的参数并不多，请勿随意改动其中数值，否则也会出大问题~



## 文档树

```
中国大学生计算机设计大赛_抓取
 ├── dataBase
 │   ├── BACKUP
 │   ├── CNJSJ_BASE.csv
 │   ├── error_log.txt
 │   ├── id_pool.xlsx
 │   ├── id_set_01.csv
 │   ├── PSAR
 │   └── TPTDP
 ├── MiddleWare
 │   ├── app.py
 │   ├── cmp_data.py
 │   ├── raw_data_load.py
 │   └── __pycache__
 ├── SpiderNest
 │   ├── cnjsj_spider.py
 │   ├── ppy_flow_spider.py
 │   ├── snsProj_spider.py
 │   └── __pycache__
 ├── config.py
 ├── LICENSE
 ├── main.py
 ├── README.md
 └── requirements.txt
```





